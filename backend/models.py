from pydantic import BaseModel
from typing import Optional, Literal


class Memory(BaseModel):
    id: str
    title: str
    description: str
    content: str
    outcome_type: Literal["success", "failure"]
    merchant_segment: str
    pdlc_phase: str = "launch"
    product_category: str
    lessons: list[str]
    competitor_context: Optional[str] = None
    timestamp: str
    source: str = "manual"


class IngestRequest(BaseModel):
    raw_text: str
    source_type: str = "post_mortem"


class QueryRequest(BaseModel):
    query: str
    merchant_segment: Optional[str] = None
    n_results: int = 6


class ConsolidateRequest(BaseModel):
    decision_description: str
    outcome: str
    outcome_type: Literal["success", "failure"]
    merchant_segment: str
    product_category: str


class QueryResponse(BaseModel):
    positioning_strategy: str
    confidence: str
    key_success_factors: list[str]
    risk_factors: list[str]
    guardrails: list[str]
    competitor_intelligence: str
    analogous_wins: list[dict]
    analogous_failures: list[dict]
    recommended_next_steps: list[str]
    summary: str
    memories_used: list[dict]
