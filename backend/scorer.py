import json
import anthropic


def _parse_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)

_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are GTM Bank's readiness scoring engine for Fiserv. "
            "Score GTM plans 0–100 across four dimensions based on historical memory patterns. "
            "Be critical, specific, and grounded in the evidence provided. "
            "Return valid JSON only — no markdown, no explanation."
        ),
        "cache_control": {"type": "ephemeral"},
    }
]


def score_plan(
    plan_text: str,
    segment: str,
    product: str,
    memories: list[dict],
) -> dict:
    successes = [m for m in memories if m["outcome_type"] == "success"]
    failures  = [m for m in memories if m["outcome_type"] == "failure"]

    ctx = ""
    if successes:
        ctx += "\nSUCCESS PATTERNS FROM MEMORY:\n"
        for m in successes:
            ctx += f"  • {m['title']}: {'; '.join(m['lessons'][:2])}\n"
    if failures:
        ctx += "\nFAILURE PATTERNS FROM MEMORY:\n"
        for m in failures:
            ctx += f"  • {m['title']}: {'; '.join(m['lessons'][:2])}\n"
    if not ctx:
        ctx = "\n(No relevant historical memories found — score conservatively.)\n"

    prompt = f"""Score this GTM plan.

PLAN:
{plan_text}

Segment: {segment or 'Not specified'}
Product: {product or 'Not specified'}

Historical Memory Evidence:
{ctx}

Return JSON with exactly these keys:
{{
  "overall_score": <0-100 integer, weighted average of dimensions>,
  "verdict": "GO" | "PROCEED WITH CAUTION" | "NO-GO",
  "dimensions": {{
    "segment_fit":          {{"score": <0-100>, "rationale": "<1-2 sentences>"}},
    "pricing_risk":         {{"score": <0-100>, "rationale": "<1-2 sentences>"}},
    "competitive_exposure": {{"score": <0-100>, "rationale": "<1-2 sentences>"}},
    "execution_complexity": {{"score": <0-100>, "rationale": "<1-2 sentences>"}}
  }},
  "red_flags": ["<specific risk rooted in memory evidence>", "..."],
  "strengths":  ["<specific strength rooted in memory evidence>", "..."],
  "critical_question": "<The single most important thing to validate before launch>",
  "analogous_memories": ["<title of most relevant memory>", "..."]
}}

Scoring guide:
  GO (verdict) → overall ≥ 75, no blocking red flags
  PROCEED WITH CAUTION → overall 50–74, or has 1-2 addressable risks
  NO-GO → overall < 50, or mirrors a known failure pattern closely

JSON:"""

    response = anthropic.Anthropic().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return _parse_json(response.content[0].text)
