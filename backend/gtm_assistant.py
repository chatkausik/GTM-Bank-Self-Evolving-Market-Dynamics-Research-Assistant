import json
import anthropic


def _parse_json(text: str):
    text = text.strip()
    # Strip markdown fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    # If Claude wrote prose before the JSON, find the first { … last }
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


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

    # web_search_20250305 is a server-executed tool — Anthropic handles the search
    # within the same API call. The response arrives with stop_reason="end_turn"
    # and content blocks of types: server_tool_use, web_search_tool_result, text.
    resp = _client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        system=_SYSTEM,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        messages=[{"role": "user", "content": prompt}],
    )

    # Collect only text blocks; skip server_tool_use / web_search_tool_result
    raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
    web_used = any(
        getattr(b, "type", "") in ("server_tool_use", "web_search_tool_result")
        for b in resp.content
    )
    result = _parse_json(raw)
    result["web_intel_used"] = web_used
    return result


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

    response = _client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        system=_CHAT_SYSTEM,
        messages=messages,
    )
    return response.content[0].text.strip()
