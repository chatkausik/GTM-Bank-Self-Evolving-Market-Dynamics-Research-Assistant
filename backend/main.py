import asyncio
import json as json_mod
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional

from .models import ConsolidateRequest, IngestRequest, QueryRequest
from .reasoning_bank import ReasoningBank
from .memory_extractor import extract_memories, consolidate_outcome
from .gtm_assistant import research, follow_up, challenge_strategy
from .scorer import score_plan
from .analytics import compute_analytics
from .competitors import synthesize_competitor_hub, synthesize_competitor_timeline
from .seed_data import SEED_MEMORIES
from .fiserv_history import FISERV_HISTORY

load_dotenv()

BASE_DIR      = Path(__file__).parent.parent
CHROMA_DIR    = str(BASE_DIR / "chroma_db")
FRONTEND_DIR  = BASE_DIR / "frontend"

bank = ReasoningBank(persist_directory=CHROMA_DIR)

_competitors_cache: list[dict] | None = None
_timeline_cache: dict | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    if bank.get_stats()["total"] == 0:
        for memory in SEED_MEMORIES:
            bank.add_memory(memory)
        print(f"Seeded {len(SEED_MEMORIES)} memories into ReasoningBank.")
    yield


app = FastAPI(
    title="GTM Product Analyzer Agent — Self-Evolving Market Dynamics Research Assistant",
    version="3.0.0",
    lifespan=lifespan,
)


# ── Frontend ──────────────────────────────────────────────────────────

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")


# ── Health / Stats ────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "bank": bank.get_stats()}

@app.get("/api/stats")
async def get_stats():
    return bank.get_stats()

@app.get("/api/memories")
async def get_memories():
    return bank.get_all_memories()

@app.delete("/api/memories/{memory_id}")
async def delete_memory(memory_id: str):
    if not bank.delete_memory(memory_id):
        raise HTTPException(404, f"Memory {memory_id} not found.")
    global _competitors_cache
    _competitors_cache = None
    await loadStats_refresh()
    return {"message": f"Deleted {memory_id}"}

async def loadStats_refresh():
    pass  # stats refresh happens on next client poll


# ── Research (standard + streaming) ──────────────────────────────────

@app.post("/api/query")
async def query_gtm(req: QueryRequest):
    if bank.get_stats()["total"] == 0:
        raise HTTPException(400, "ReasoningBank is empty. Seed or ingest data first.")
    memories = bank.retrieve_balanced(req.query, n_per_side=max(3, req.n_results // 2))
    try:
        result = research(req.query, memories, req.merchant_segment)
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")
    result["memories_used"] = memories
    return result


@app.post("/api/query/stream")
async def query_gtm_stream(req: QueryRequest):
    """Server-Sent Events endpoint — streams progress updates then the final result."""
    if bank.get_stats()["total"] == 0:
        raise HTTPException(400, "ReasoningBank is empty.")

    async def generate():
        try:
            yield f"data: {json_mod.dumps({'type': 'status', 'message': 'Searching ReasoningBank for analogous wins and failures…', 'pct': 15})}\n\n"

            n_per_side = max(3, req.n_results // 2)
            memories = bank.retrieve_balanced(req.query, n_per_side=n_per_side)

            yield f"data: {json_mod.dumps({'type': 'status', 'message': f'Retrieved {len(memories)} relevant memories. Launching live web competitor research…', 'pct': 35})}\n\n"
            yield f"data: {json_mod.dumps({'type': 'status', 'message': '🌐 Searching Stripe, Adyen, Square web intel + synthesising competitive PRD…', 'pct': 60})}\n\n"

            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, research, req.query, memories, req.merchant_segment
            )
            result["memories_used"] = memories

            yield f"data: {json_mod.dumps({'type': 'result', 'data': result})}\n\n"
        except Exception as e:
            yield f"data: {json_mod.dumps({'type': 'error', 'message': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Devil's Advocate — Challenge Mode ────────────────────────────────

class ChallengeRequest(BaseModel):
    strategy: str
    query: str

@app.post("/api/challenge")
async def challenge_endpoint(req: ChallengeRequest):
    if not req.strategy.strip():
        raise HTTPException(400, "strategy must not be empty.")
    memories = bank.retrieve_balanced(req.query, n_per_side=3)
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, challenge_strategy, req.strategy, req.query, memories
        )
    except Exception as e:
        raise HTTPException(500, f"Challenge error: {e}")
    return result


# ── Ingest & Consolidate ──────────────────────────────────────────────

@app.post("/api/ingest")
async def ingest_document(req: IngestRequest):
    if not req.raw_text.strip():
        raise HTTPException(400, "raw_text must not be empty.")
    try:
        memories = extract_memories(req.raw_text, req.source_type)
    except Exception as e:
        raise HTTPException(500, f"Extraction error: {e}")
    for m in memories:
        bank.add_memory(m)
    global _competitors_cache
    _competitors_cache = None
    return {
        "message": f"Stored {len(memories)} memories.",
        "memory_ids": [m.id for m in memories],
        "memories": [m.model_dump() for m in memories],
    }


@app.post("/api/consolidate")
async def consolidate(req: ConsolidateRequest):
    related = bank.retrieve_similar(
        f"{req.decision_description} {req.merchant_segment} {req.product_category}",
        n_results=5,
    )
    try:
        new_memories = consolidate_outcome(
            decision=req.decision_description,
            outcome=req.outcome,
            outcome_type=req.outcome_type,
            merchant_segment=req.merchant_segment,
            product_category=req.product_category,
            related_memories=related,
        )
    except Exception as e:
        raise HTTPException(500, f"Consolidation error: {e}")
    for m in new_memories:
        bank.add_memory(m)
    global _competitors_cache
    _competitors_cache = None
    return {
        "message": f"Consolidated {len(new_memories)} new memories.",
        "memory_ids": [m.id for m in new_memories],
        "memories": [m.model_dump() for m in new_memories],
    }


# ── Seed & History ────────────────────────────────────────────────────

@app.post("/api/seed")
async def reseed():
    added = 0
    for m in SEED_MEMORIES:
        if not bank.memory_exists(m.id):
            bank.add_memory(m)
            added += 1
    return {"message": f"Added {added} seed memories.", "total": bank.get_stats()["total"]}


@app.post("/api/load_fiserv_history")
async def load_fiserv_history():
    """Load 13 real Fiserv product history memories (2015–2025) into the ReasoningBank."""
    added = 0
    for m in FISERV_HISTORY:
        if not bank.memory_exists(m.id):
            bank.add_memory(m)
            added += 1
    global _competitors_cache
    _competitors_cache = None
    stats = bank.get_stats()
    return {
        "message": f"Loaded {added} Fiserv product history memories.",
        "new": added,
        "total": stats["total"],
    }


# ── GTM Readiness Score ───────────────────────────────────────────────

class ScoreRequest(BaseModel):
    plan_text: str
    merchant_segment: Optional[str] = None
    product_category: Optional[str] = None

@app.post("/api/score")
async def score_gtm_plan(req: ScoreRequest):
    if not req.plan_text.strip():
        raise HTTPException(400, "plan_text must not be empty.")
    query = f"{req.plan_text} {req.merchant_segment or ''} {req.product_category or ''}"
    memories = bank.retrieve_balanced(query, n_per_side=4)
    try:
        result = score_plan(
            req.plan_text,
            req.merchant_segment or "",
            req.product_category or "",
            memories,
        )
    except Exception as e:
        raise HTTPException(500, f"Scoring error: {e}")
    result["memories_used"] = memories
    return result


# ── Conversational Follow-up ──────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    original_query: str
    memories_used: list[dict]
    history: list[dict] = []

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(400, "message must not be empty.")
    try:
        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(
            None, follow_up, req.message, req.original_query, req.memories_used, req.history
        )
    except Exception as e:
        raise HTTPException(500, f"Chat error: {e}")
    return {"reply": reply}


# ── Analytics ─────────────────────────────────────────────────────────

@app.get("/api/analytics")
async def get_analytics():
    memories = bank.get_all_memories()
    return compute_analytics(memories)


# ── Competitor Intelligence Hub ───────────────────────────────────────

@app.get("/api/competitors")
async def get_competitors(refresh: bool = False):
    global _competitors_cache
    if _competitors_cache is not None and not refresh:
        return {"competitors": _competitors_cache, "cached": True}
    memories = bank.get_all_memories()
    try:
        loop = asyncio.get_event_loop()
        profiles = await loop.run_in_executor(None, synthesize_competitor_hub, memories)
    except Exception as e:
        raise HTTPException(500, f"Competitor synthesis error: {e}")
    _competitors_cache = profiles
    return {"competitors": profiles, "cached": False}


@app.get("/api/competitor-timeline")
async def get_competitor_timeline(refresh: bool = False):
    """Real-time quarterly product timeline for top 5 Fiserv competitors + Fiserv recommendations."""
    global _timeline_cache
    if _timeline_cache is not None and not refresh:
        return {**_timeline_cache, "cached": True}
    memories = bank.get_all_memories()
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, synthesize_competitor_timeline, memories)
    except Exception as e:
        raise HTTPException(500, f"Timeline synthesis error: {e}")
    _timeline_cache = result
    return {**result, "cached": False}
