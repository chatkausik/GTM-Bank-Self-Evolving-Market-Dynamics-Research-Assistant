import json
import anthropic


def _parse_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)


def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()

_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are GTM Bank, a self-evolving Go-To-Market research assistant for Fiserv — "
            "a global fintech and payments company. You have access to a ReasoningBank of past "
            "GTM decisions spanning successes and failures across merchant segments. "
            "Surface the most actionable strategic insights for new GTM decisions. "
            "Be specific, opinionated, and grounded in the provided memory context. "
            "Always respond with valid JSON only — no markdown fences, no explanation."
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
    return f"\n{'='*60}\n{outcome} MEMORIES{'='*60}" + "".join(lines)


def research(query: str, memories: list[dict], merchant_segment: str | None = None) -> dict:
    successes = [m for m in memories if m["outcome_type"] == "success"]
    failures = [m for m in memories if m["outcome_type"] == "failure"]

    context = ""
    if successes:
        context += _format_memories(successes, "SUCCESS")
    if failures:
        context += _format_memories(failures, "FAILURE")

    segment_ctx = f" targeting the {merchant_segment} segment" if merchant_segment else ""

    prompt = f"""GTM Research Query: {query}{segment_ctx}

Retrieved ReasoningBank Context:
{context}

Based on these memories, return a comprehensive GTM research response as JSON with exactly these keys:
{{
  "positioning_strategy": "2-3 sentence recommended positioning strategy",
  "confidence": "high | medium | low",
  "key_success_factors": ["factor 1", "factor 2", "factor 3"],
  "risk_factors": ["risk 1", "risk 2", "risk 3"],
  "guardrails": ["specific guardrail from past failures 1", "guardrail 2", "guardrail 3"],
  "competitor_intelligence": "What Stripe, Adyen, Square have done and where we have an edge",
  "analogous_wins": [
    {{"title": "...", "segment": "...", "why_it_worked": "..."}}
  ],
  "analogous_failures": [
    {{"title": "...", "segment": "...", "why_it_failed": "..."}}
  ],
  "recommended_next_steps": ["step 1", "step 2", "step 3"],
  "summary": "One crisp paragraph executive summary"
}}

JSON:"""

    response = _client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(response.content[0].text)


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
