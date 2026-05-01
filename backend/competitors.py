import json
import anthropic

TRACKED_COMPETITORS = ["Stripe", "Adyen", "Square", "FIS", "Clover", "Plaid", "Wise"]

_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are GTM Bank's competitive intelligence analyst for Fiserv. "
            "Synthesize competitor profiles from historical GTM memory evidence. "
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

    if not relevant:
        return []

    context = ""
    for comp, mems in relevant.items():
        context += f"\n\n=== {comp} (mentioned in {len(mems)} memories) ===\n"
        for m in mems:
            context += f"  [{m['outcome_type'].upper()}] {m['title']}\n"
            if m.get("competitor_context"):
                context += f"  Intel: {m['competitor_context']}\n"
            context += f"  Lessons: {'; '.join(m.get('lessons', [])[:2])}\n"

    prompt = f"""Synthesize competitive intelligence profiles for each competitor below,
based on Fiserv's historical GTM memories.

{context}

Return a JSON array — one object per competitor, only for competitors listed above:
[{{
  "name": "<competitor name>",
  "data_points": <number of memories mentioning them>,
  "threat_level": "high" | "medium" | "low",
  "where_we_win": ["<specific scenario where Fiserv beats them>", "..."],
  "where_we_lose": ["<specific scenario where they beat Fiserv>", "..."],
  "their_strengths": ["<key strength>", "..."],
  "their_weaknesses": ["<exploitable weakness>", "..."],
  "counter_strategy": "<2-3 sentence recommended counter-positioning against this competitor>"
}}]

JSON array:"""

    response = anthropic.Anthropic().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        system=_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        raw = raw.rsplit("```", 1)[0].strip()
    return json.loads(raw)
