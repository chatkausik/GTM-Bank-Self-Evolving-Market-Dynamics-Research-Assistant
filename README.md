# GTM Bank — Self-Evolving Market Dynamics Research Assistant

> A Fiserv-focused AI research assistant that learns from both wins and failures to surface smarter Go-To-Market strategy.

Built on the [ReasoningBank architecture](https://arxiv.org/abs/2509.25140) (Ouyang et al., Google Cloud AI / UIUC / Yale) — an LLM-powered memory system that distills past GTM decisions into reusable reasoning strategies.

---

## What It Does

| Feature | Description |
|---|---|
| **Research** | Ask any GTM question; retrieves analogous wins + failures from the memory bank and returns a full strategic brief |
| **GTM Score** | Paste a launch plan and get a 0–100 readiness score across segment fit, pricing risk, competitive exposure, and execution complexity |
| **Analytics** | Visual dashboard of win/failure rates by product category and merchant segment |
| **Competitors** | AI-synthesized competitive intelligence profiles for Stripe, Adyen, Square, and more — grounded in memory evidence |
| **Conversational Follow-up** | Chat with the research results to drill deeper without losing context |
| **Export Brief** | Download or copy your research output as a clean Markdown brief |

---

## Architecture

```
Frontend (vanilla HTML/CSS/JS)
        ↕ REST API
Backend (FastAPI + Uvicorn)
   ├── ReasoningBank  →  ChromaDB (vector store, cosine similarity)
   ├── Memory Extractor  →  Claude claude-sonnet-4-6 (extraction + consolidation)
   ├── GTM Assistant  →  Claude claude-sonnet-4-6 (research + follow-up)
   ├── Scorer  →  Claude claude-sonnet-4-6 (0–100 readiness score)
   └── Competitor Hub  →  Claude claude-sonnet-4-6 (competitive synthesis)
```

Memories are structured as `success | failure` pairs with lessons, segment tags, and competitor context — enabling contrastive retrieval that surfaces both what worked and what didn't.

---

## Quick Start

**Prerequisites:** Python 3.11+, an Anthropic API key.

```bash
git clone https://github.com/chatkausik/GTM-Bank-Self-Evolving-Market-Dynamics-Research-Assistant.git
cd GTM-Bank-Self-Evolving-Market-Dynamics-Research-Assistant

cp .env.example .env
# Add your key: ANTHROPIC_API_KEY=sk-ant-...

chmod +x run.sh && ./run.sh
```

Open `http://localhost:8000` in your browser.

The bank auto-seeds with 12 realistic Fiserv GTM memories (6 wins, 6 failures) on first run.

---

## Project Structure

```
backend/
  main.py            # FastAPI app + all API endpoints
  reasoning_bank.py  # ChromaDB wrapper (add, retrieve, stats)
  memory_extractor.py # Claude-powered extraction + consolidation
  gtm_assistant.py   # Research query + conversational follow-up
  scorer.py          # GTM Readiness Score engine
  competitors.py     # Competitor Intelligence Hub
  analytics.py       # Win/failure stats computation
  models.py          # Pydantic schemas
  seed_data.py       # 12 seed memories
frontend/
  index.html         # Single-page UI (no framework)
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check + memory bank stats |
| `GET` | `/api/memories` | All memories in the bank |
| `POST` | `/api/query` | GTM research query |
| `POST` | `/api/ingest` | Ingest raw text (post-mortems, win/loss notes) |
| `POST` | `/api/consolidate` | Log an outcome and consolidate new memories |
| `POST` | `/api/score` | Score a GTM plan (0–100) |
| `POST` | `/api/chat` | Conversational follow-up |
| `GET` | `/api/analytics` | Analytics data |
| `GET` | `/api/competitors` | Competitor intelligence profiles |

---

## Academic Foundation

This project implements the **ReasoningBank** paradigm from:

> *"ReasoningBank: A Self-Evolving Memory System for LLM Reasoning"*
> Ouyang et al. — Google Cloud AI Research, UIUC, Yale (2025)
> [arxiv.org/abs/2509.25140](https://arxiv.org/abs/2509.25140)

Key concepts applied: structured experience extraction, contrastive success/failure signals, closed-loop outcome consolidation, and semantic similarity retrieval.

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn, ChromaDB, sentence-transformers
- **AI:** Anthropic Claude claude-sonnet-4-6 with prompt caching
- **Frontend:** Vanilla JS/CSS, no framework, no build step
- **Storage:** Local ChromaDB (persistent vector store)
