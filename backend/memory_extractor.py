import uuid
from datetime import datetime
from .models import Memory
from .utils import parse_json, anthropic_client

_SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are a GTM memory extraction specialist for a fintech/payments company (Fiserv). "
            "Extract structured memories from raw text such as post-mortems, win/loss notes, and launch retrospectives. "
            "Always respond with valid JSON only — no markdown fences, no explanation."
        ),
        "cache_control": {"type": "ephemeral"},
    }
]


def extract_memories(raw_text: str, source_type: str = "post_mortem") -> list[Memory]:
    prompt = f"""Extract 1–3 structured GTM memories from this {source_type}.

Raw text:
{raw_text}

Return a JSON array. Each object must have exactly these keys:
- title: concise (max 10 words)
- description: one-sentence summary
- content: 2–4 sentences of detailed context
- outcome_type: "success" or "failure"
- merchant_segment: e.g. "mid-market retail", "enterprise SaaS", "SMB restaurants"
- product_category: e.g. "real-time payments", "embedded finance", "fraud prevention"
- lessons: array of 2–4 actionable lessons
- competitor_context: competitor intelligence string or null

JSON array:"""

    response = anthropic_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    data = parse_json(raw)

    memories = []
    for item in data:
        memories.append(Memory(
            id=str(uuid.uuid4()),
            title=item["title"],
            description=item["description"],
            content=item["content"],
            outcome_type=item["outcome_type"],
            merchant_segment=item["merchant_segment"],
            pdlc_phase="launch",
            product_category=item["product_category"],
            lessons=item["lessons"],
            competitor_context=item.get("competitor_context"),
            timestamp=datetime.now().isoformat(),
            source=source_type,
        ))
    return memories


def consolidate_outcome(
    decision: str,
    outcome: str,
    outcome_type: str,
    merchant_segment: str,
    product_category: str,
    related_memories: list[dict],
) -> list[Memory]:
    context_lines = "\n".join(
        f"- {m['title']}: {m['description']}" for m in related_memories[:5]
    )

    prompt = f"""A new GTM outcome has been logged:

Decision: {decision}
Merchant Segment: {merchant_segment}
Product Category: {product_category}
Outcome: {outcome}
Result: {outcome_type.upper()}

Related memories already in the bank:
{context_lines}

Synthesize 1–2 new consolidated memories to add to the ReasoningBank.
These should encode new lessons not already covered above.

Return a JSON array with the same schema as above (title, description, content, outcome_type, merchant_segment, product_category, lessons, competitor_context).

JSON array:"""

    response = anthropic_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    data = parse_json(raw)

    memories = []
    for item in data:
        memories.append(Memory(
            id=str(uuid.uuid4()),
            title=item["title"],
            description=item["description"],
            content=item["content"],
            outcome_type=item["outcome_type"],
            merchant_segment=merchant_segment,
            pdlc_phase="launch",
            product_category=product_category,
            lessons=item["lessons"],
            competitor_context=item.get("competitor_context"),
            timestamp=datetime.now().isoformat(),
            source="consolidation",
        ))
    return memories
