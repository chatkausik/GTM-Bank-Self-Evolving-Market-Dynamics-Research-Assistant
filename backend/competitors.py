import anthropic
from .utils import parse_json

TRACKED_COMPETITORS = ["Stripe", "Adyen", "Square", "FIS", "Clover", "Plaid", "Wise"]

_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are GTM Bank's competitive intelligence analyst for Fiserv. "
            "Search the web for the latest competitor moves (2024-2025), then synthesize profiles "
            "combining live web findings with historical GTM memory evidence. "
            "Be specific and evidence-grounded. Return valid JSON only."
        ),
        "cache_control": {"type": "ephemeral"},
    }
]


def _find_competitor_memories(memories: list[dict]) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {c: [] for c in TRACKED_COMPETITORS}
    for m in memories:
        combined = (
            (m.get("content") or "") + " " +
            (m.get("competitor_context") or "") + " " +
            (m.get("title") or "") + " " +
            " ".join(m.get("lessons") or [])
        ).lower()
        for comp in TRACKED_COMPETITORS:
            if comp.lower() in combined:
                result[comp].append(m)
    return result


def synthesize_competitor_hub(memories: list[dict]) -> list[dict]:
    comp_memories = _find_competitor_memories(memories)
    relevant = {c: mems for c, mems in comp_memories.items() if mems}

    context = ""
    # Always include at least the top 4 competitors even without memory mentions
    all_comps = list(relevant.keys()) or TRACKED_COMPETITORS[:4]
    for comp in all_comps:
        mems = relevant.get(comp, [])
        context += f"\n\n=== {comp} (mentioned in {len(mems)} Fiserv GTM memories) ===\n"
        for m in mems:
            context += f"  [{m['outcome_type'].upper()}] {m['title']}\n"
            if m.get("competitor_context"):
                context += f"  Intel: {m['competitor_context']}\n"
            context += f"  Lessons: {'; '.join(m.get('lessons', [])[:2])}\n"

    prompt = f"""Search the web for the latest (2024-2025) product launches, pricing changes, enterprise wins,
and strategic moves from Stripe, Adyen, Square, FIS, Clover, Plaid, and Wise.
Then synthesize competitive intelligence profiles for each competitor, combining live web findings
with Fiserv's historical GTM evidence below.

Historical Memory Evidence:
{context}

Return a JSON array — one object per competitor, for all competitors mentioned above:
[{{
  "name": "<competitor name>",
  "data_points": <number of Fiserv GTM memories mentioning them>,
  "threat_level": "high" | "medium" | "low",
  "latest_moves": "<2024-2025 product launches, pricing changes, or strategic shifts from web research>",
  "where_we_win": ["<specific scenario where Fiserv beats them>", "..."],
  "where_we_lose": ["<specific scenario where they beat Fiserv>", "..."],
  "their_strengths": ["<key strength>", "..."],
  "their_weaknesses": ["<exploitable weakness Fiserv should target>", "..."],
  "counter_strategy": "<2-3 sentence recommended counter-positioning against this competitor>"
}}]

JSON array:"""

    response = anthropic.Anthropic().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=5000,
        system=_SYSTEM,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
        messages=[{"role": "user", "content": prompt}],
    )
    raw = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
    return parse_json(raw)
