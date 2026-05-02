import anthropic
from .utils import parse_json

TRACKED_COMPETITORS = ["Stripe", "Adyen", "Square", "FIS", "Clover", "Plaid", "Wise"]
TOP_5_COMPETITORS   = ["FIS", "Jack Henry", "Stripe", "Adyen", "Square"]

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

Return a JSON array — one object per competitor:
[{{
  "name": "<competitor name>",
  "data_points": <number of memories>,
  "threat_level": "high" | "medium" | "low",
  "latest_moves": "<2024-2025 product launches or strategic shifts from web research>",
  "where_we_win": ["<specific scenario>", "..."],
  "where_we_lose": ["<specific scenario>", "..."],
  "their_strengths": ["<key strength>", "..."],
  "their_weaknesses": ["<exploitable weakness>", "..."],
  "counter_strategy": "<2-3 sentence recommended counter-positioning>"
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


# ── Quarterly Competitor Timeline ─────────────────────────────────────────


def synthesize_competitor_timeline(memories: list[dict]) -> dict:
    """
    Fetch quarter-by-quarter product release timelines for the top 5 Fiserv competitors
    via live web search, then generate one enhanced Fiserv recommendation per competitor.
    Covers Q1 2024 → Q2 2025 (released) + Q3–Q4 2025 (upcoming).
    """
    mem_ctx = "\n".join(
        f"  [{m['outcome_type'].upper()}] {m.get('title','')}: "
        f"{'; '.join((m.get('lessons') or [])[:1])}"
        for m in memories[:10]
    )

    prompt = f"""Search the web comprehensively for quarterly product launches, major feature releases,
acquisitions, and strategic announcements from these top 5 Fiserv competitors:

1. FIS (Fidelity National Information Services) — core banking + issuer processing
2. Jack Henry & Associates — community and regional bank technology
3. Stripe — developer-first payments infrastructure
4. Adyen — unified global commerce platform
5. Square (Block) — SMB payments and seller ecosystem

For EACH competitor, find:
- Q1 2024 through Q2 2025: all confirmed / released products, features, partnerships
- Q3 2025 and Q4 2025: announced or rumored upcoming releases

Then generate exactly ONE specific, actionable recommendation for Fiserv per competitor —
a concrete enhanced product or feature Fiserv should build or accelerate to counter them.

Use this Fiserv memory context to ground the recommendations:
{mem_ctx}

Return a JSON object with EXACTLY this structure (no markdown, no extra text):
{{
  "as_of": "Q2 2025",
  "competitors": [
    {{
      "name": "FIS",
      "primary_arena": "<1 sentence: where they most directly compete with Fiserv>",
      "threat_level": "high" | "medium" | "low",
      "color": "#1d4ed8",
      "timeline": [
        {{
          "quarter": "Q1 2024",
          "status": "released",
          "releases": [
            {{
              "name": "<product / feature name>",
              "category": "<core banking | fraud | payments | BaaS | lending | digital banking | open banking | POS>",
              "summary": "<1 crisp sentence>",
              "impact": "high" | "medium" | "low"
            }}
          ]
        }},
        {{
          "quarter": "Q3 2025",
          "status": "upcoming",
          "releases": [
            {{
              "name": "<product name>",
              "category": "<category>",
              "summary": "<1 sentence>",
              "impact": "high" | "medium" | "low",
              "confidence": "confirmed" | "likely" | "rumored"
            }}
          ]
        }}
      ],
      "fiserv_recommendation": {{
        "enhanced_product": "<specific Fiserv product name — make it compelling>",
        "action": "<what Fiserv should build or launch — 1-2 sentences>",
        "urgency": "immediate" | "this_quarter" | "this_year",
        "rationale": "<why this specific counter-move wins — 1-2 sentences>"
      }}
    }}
  ]
}}

Rules:
- Include timeline entries ONLY for quarters with at least one real release or confirmed announcement
- Cover at minimum Q1-Q4 2024 and Q1-Q2 2025 as released quarters
- Cover Q3-Q4 2025 as upcoming where relevant
- Use these exact colors per competitor: FIS=#1d4ed8, Jack Henry=#059669, Stripe=#7c3aed, Adyen=#0e7490, Square=#374151
- All 5 competitors must be present in the output

JSON:"""

    response = anthropic.Anthropic().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        system=_SYSTEM,
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
        messages=[{"role": "user", "content": prompt}],
    )
    raw = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
    result = parse_json(raw)
    result["web_intel_used"] = any(
        getattr(b, "type", "") in ("server_tool_use", "web_search_tool_result")
        for b in response.content
    )
    return result
