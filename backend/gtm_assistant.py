from .utils import parse_json, anthropic_client


_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are GTM Bank, a self-evolving Go-To-Market research assistant for Fiserv — "
            "a global fintech and payments company. You have access to a ReasoningBank of past "
            "GTM decisions and can search the web for live competitor intelligence. "
            "Surface the most actionable strategic insights for new GTM decisions. "
            "Be specific, opinionated, and grounded in evidence. "
            "When you finish researching, output ONLY valid JSON — no markdown fences, no explanation."
        ),
        "cache_control": {"type": "ephemeral"},
    }
]


def _format_memories(memories: list[dict], outcome: str) -> str:
    lines = []
    for m in memories:
        lines.append(f"\n[{m['merchant_segment'].upper()} | {m['product_category']}]")
        lines.append(f"  Title: {m['title']}")
        lines.append(f"  What happened: {m['content']}")
        lines.append(f"  Lessons: {'; '.join(m['lessons'])}")
        if m.get("competitor_context"):
            lines.append(f"  Competitor Intel: {m['competitor_context']}")
        lines.append(f"  Relevance: {m.get('relevance_score', 'N/A')}")
    return f"\n{'='*60}\n{outcome} MEMORIES\n{'='*60}" + "".join(lines)


def research(query: str, memories: list[dict], merchant_segment: str | None = None) -> dict:
    """Single Claude call: web-searches competitors live, then synthesises research + PRD."""
    successes = [m for m in memories if m["outcome_type"] == "success"]
    failures  = [m for m in memories if m["outcome_type"] == "failure"]

    context = ""
    if successes:
        context += _format_memories(successes, "SUCCESS")
    if failures:
        context += _format_memories(failures, "FAILURE")

    segment_ctx = f" targeting the {merchant_segment} segment" if merchant_segment else ""

    prompt = f"""GTM Research Query: {query}{segment_ctx}

STEP 1 — Search the web for current (2024-2025) product features, pricing, and positioning
from Stripe, Adyen, Square, PayPal, Clover, and Worldpay specifically around: {query}.
Find their key features, pricing models, recent launches, target customers, and weaknesses.

STEP 2 — Combine those web findings with the ReasoningBank memories below to produce your response.

Retrieved ReasoningBank Context:
{context}

STEP 3 — Return a single JSON object with EXACTLY these keys (no markdown, no extra text):
{{
  "positioning_strategy": "2-3 sentence recommended positioning strategy grounded in evidence",
  "confidence": "high | medium | low",
  "key_success_factors": ["factor 1", "factor 2", "factor 3"],
  "risk_factors": ["risk 1", "risk 2", "risk 3"],
  "guardrails": ["guardrail from past failures 1", "guardrail 2", "guardrail 3"],
  "competitor_intelligence": "What Stripe, Adyen, Square etc. are doing based on web research, and exactly where Fiserv has an exploitable edge",
  "analogous_wins": [{{"title": "...", "segment": "...", "why_it_worked": "..."}}],
  "analogous_failures": [{{"title": "...", "segment": "...", "why_it_failed": "..."}}],
  "recommended_next_steps": ["step 1", "step 2", "step 3"],
  "summary": "One crisp paragraph executive summary",
  "competitive_prd": {{
    "product_name": "A specific, compelling Fiserv product name for this opportunity",
    "tagline": "One punchy sentence — the elevator pitch",
    "vision": "2-3 sentence product vision: who it is for, what it does, why it matters",
    "target_icp": "Specific ideal customer profile — segment, size, pain point, buying trigger",
    "market_opportunity": "The gap in the market, size of the prize, and why now is the right moment",
    "key_features": [
      {{
        "name": "Feature name",
        "description": "What it does and how it works",
        "beats": "Which specific competitor this outperforms and exactly how"
      }}
    ],
    "differentiators": ["Concrete differentiator vs Stripe/Adyen/Square 1", "differentiator 2", "differentiator 3"],
    "pricing_strategy": "Specific pricing model with numbers/tiers and rationale for why it wins on value",
    "go_to_market_motion": "Channel strategy, sales motion, and first 90-day launch plan",
    "success_metrics": ["Metric + specific target 1", "Metric + target 2", "Metric + target 3"],
    "mvp_scope": ["Core capability 1 for launch", "Core capability 2", "Core capability 3"],
    "phase_2": ["Enhancement 1 for v2", "Enhancement 2"],
    "why_now": "Market timing argument — competitor gap, regulatory window, customer readiness signal"
  }}
}}"""

    resp = anthropic_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        system=_SYSTEM,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        messages=[{"role": "user", "content": prompt}],
    )

    raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
    web_used = any(
        getattr(b, "type", "") in ("server_tool_use", "web_search_tool_result")
        for b in resp.content
    )
    result = parse_json(raw)
    result["web_intel_used"] = web_used
    return result


# ── Conversational follow-up ──────────────────────────────────────────────

_CHAT_SYSTEM = (
    "You are GTM Bank, a Go-To-Market research assistant for Fiserv. "
    "Answer follow-up questions concisely and specifically, drawing from the memory context provided. "
    "Never repeat the full research output — respond conversationally in 2-5 sentences unless a longer answer is clearly needed. "
    "Do NOT use JSON. Respond in plain prose."
)


def follow_up(
    message: str,
    original_query: str,
    memories: list[dict],
    history: list[dict],
) -> str:
    mem_lines = "\n".join(
        f"  [{m['outcome_type'].upper()}] {m['title']}: {m.get('content','')[:200]}"
        for m in memories
    )
    context_primer = (
        f"Original GTM research query: {original_query}\n\n"
        f"Memories already retrieved and used:\n{mem_lines}"
    )

    messages = [
        {"role": "user",      "content": context_primer},
        {"role": "assistant", "content": "Understood — I have the research context loaded. What would you like to explore further?"},
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = anthropic_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=_CHAT_SYSTEM,
        messages=messages,
    )
    return response.content[0].text.strip()


# ── Devil's Advocate — Challenge Mode ────────────────────────────────────

_CHALLENGE_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are a senior Fiserv board member playing devil's advocate. "
            "Your job is to stress-test proposed GTM strategies ruthlessly — "
            "surface blind spots, failure conditions, and unconventional risks that optimistic "
            "strategists miss. Be specific, evidence-grounded, and brutally honest. "
            "Return valid JSON only — no markdown fences, no explanation."
        ),
        "cache_control": {"type": "ephemeral"},
    }
]


def challenge_strategy(strategy: str, query: str, memories: list[dict]) -> dict:
    """Devil's advocate: surface blind spots and failure conditions for a proposed GTM strategy."""
    failures = [m for m in memories if m["outcome_type"] == "failure"]

    failure_ctx = ""
    if failures:
        failure_ctx = "\n\nAnalogous failures from ReasoningBank:\n"
        for m in failures:
            failure_ctx += f"  [{m['merchant_segment']} | {m['product_category']}]\n"
            failure_ctx += f"  {m['title']}: {'; '.join(m['lessons'][:2])}\n"

    prompt = f"""Stress-test this Fiserv GTM strategy as a ruthless devil's advocate.

Original Query: {query}

Proposed Strategy:
{strategy}
{failure_ctx}

Return a JSON object with EXACTLY these keys (no markdown, no extra text):
{{
  "worst_case_scenario": "The single most catastrophic but realistic failure mode for this strategy",
  "critical_blind_spots": ["blind spot 1", "blind spot 2", "blind spot 3"],
  "failure_conditions": ["Specific condition that would trigger failure 1", "condition 2", "condition 3"],
  "underestimated_risks": ["Risk the strategy understates 1", "risk 2"],
  "competitor_counter_moves": ["How Stripe would likely respond", "How Adyen would respond", "How the market would adapt"],
  "alternative_hypothesis": "A stronger alternative GTM framing that might work better",
  "pressure_test_questions": ["Hard question a board member would ask 1", "question 2", "question 3"],
  "confidence_gaps": ["Critical unknown that must be validated before launch 1", "unknown 2"],
  "devils_verdict": "PROCEED" | "RECONSIDER" | "ABANDON",
  "devils_rationale": "2-3 sentence verdict with the single most important reason"
}}

JSON:"""

    response = anthropic_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=_CHALLENGE_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return parse_json(response.content[0].text)
