import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from .models import ConsolidateRequest, IngestRequest, QueryRequest
from .reasoning_bank import ReasoningBank
from .memory_extractor import extract_memories, consolidate_outcome
from .gtm_assistant import research, follow_up
from .scorer import score_plan
from .analytics import compute_analytics
from .competitors import synthesize_competitor_hub
from .seed_data import SEED_MEMORIES

load_dotenv()

BASE_DIR   = Path(__file__).parent.parent
CHROMA_DIR = str(BASE_DIR / "chroma_db")
FRONTEND_DIR = BASE_DIR / "frontend"

bank = ReasoningBank(persist_directory=CHROMA_DIR)

# Simple in-process cache for expensive competitor synthesis
_competitors_cache: list[dict] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    if bank.get_stats()["total"] == 0:
        for memory in SEED_MEMORIES:
            bank.add_memory(memory)
        print(f"Seeded {len(SEED_MEMORIES)} memories into ReasoningBank.")
    yield


app = FastAPI(
    title="GTM Bank — Self-Evolving Market Dynamics Research Assistant",
    version="2.0.0",
    lifespan=lifespan,
)


# ── Frontend ─────────────────────────────────────────────────────────

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")


# ── Core endpoints ────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "bank": bank.get_stats()}

@app.get("/api/stats")
async def get_stats():
    return bank.get_stats()

@app.get("/api/memories")
async def get_memories():
    return bank.get_all_memories()


@app.post("/api/query")
async def query_gtm(req: QueryRequest):
    if bank.get_stats()["total"] == 0:
        raise HTTPException(400, "ReasoningBank is empty. Seed or ingest data first.")
    memories = bank.retrieve_similar(req.query, n_results=req.n_results)
    try:
        result = research(req.query, memories, req.merchant_segment)
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")
    result["memories_used"] = memories
    return result


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
    _competitors_cache = None          # invalidate competitor cache
    return {"message": f"Stored {len(memories)} memories.", "memory_ids": [m.id for m in memories], "memories": [m.model_dump() for m in memories]}


@app.post("/api/consolidate")
async def consolidate(req: ConsolidateRequest):
    related = bank.retrieve_similar(
        f"{req.decision_description} {req.merchant_segment} {req.product_category}", n_results=5
    )
    try:
        new_memories = consolidate_outcome(
            decision=req.decision_description, outcome=req.outcome,
            outcome_type=req.outcome_type, merchant_segment=req.merchant_segment,
            product_category=req.product_category, related_memories=related,
        )
    except Exception as e:
        raise HTTPException(500, f"Consolidation error: {e}")
    for m in new_memories:
        bank.add_memory(m)
    global _competitors_cache
    _competitors_cache = None
    return {"message": f"Consolidated {len(new_memories)} new memories.", "memory_ids": [m.id for m in new_memories], "memories": [m.model_dump() for m in new_memories]}


@app.post("/api/seed")
async def reseed():
    count = sum(1 for m in SEED_MEMORIES if not bank.memory_exists(m.id) and bank.add_memory(m) is not None or not bank.memory_exists(m.id))
    # simpler re-seed
    added = 0
    for m in SEED_MEMORIES:
        if not bank.memory_exists(m.id):
            bank.add_memory(m)
            added += 1
    return {"message": f"Added {added} seed memories.", "total": bank.get_stats()["total"]}


# ── GTM Readiness Score ──────────────────────────────────────────────

class ScoreRequest(BaseModel):
    plan_text: str
    merchant_segment: Optional[str] = None
    product_category: Optional[str] = None

@app.post("/api/score")
async def score_gtm_plan(req: ScoreRequest):
    if not req.plan_text.strip():
        raise HTTPException(400, "plan_text must not be empty.")
    query = f"{req.plan_text} {req.merchant_segment or ''} {req.product_category or ''}"
    memories = bank.retrieve_similar(query, n_results=8)
    try:
        result = score_plan(req.plan_text, req.merchant_segment or "", req.product_category or "", memories)
    except Exception as e:
        raise HTTPException(500, f"Scoring error: {e}")
    result["memories_used"] = memories
    return result


# ── Conversational Follow-up ─────────────────────────────────────────

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
        reply = follow_up(req.message, req.original_query, req.memories_used, req.history)
    except Exception as e:
        raise HTTPException(500, f"Chat error: {e}")
    return {"reply": reply}


# ── Analytics ────────────────────────────────────────────────────────

@app.get("/api/analytics")
async def get_analytics():
    memories = bank.get_all_memories()
    return compute_analytics(memories)


# ── Competitor Intelligence Hub ──────────────────────────────────────

@app.get("/api/competitors")
async def get_competitors(refresh: bool = False):
    global _competitors_cache
    if _competitors_cache is not None and not refresh:
        return {"competitors": _competitors_cache, "cached": True}
    memories = bank.get_all_memories()
    try:
        profiles = synthesize_competitor_hub(memories)
    except Exception as e:
        raise HTTPException(500, f"Competitor synthesis error: {e}")
    _competitors_cache = profiles
    return {"competitors": profiles, "cached": False}
