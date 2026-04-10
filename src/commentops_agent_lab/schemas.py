from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PolicyClause(BaseModel):
    clause_id: str
    category: str
    title: str
    severity: str
    decision: str
    description: str
    queue_hint: str | None = None
    keywords: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    reviewer_guidance: list[str] = Field(default_factory=list)


class ReviewCase(BaseModel):
    case_id: str
    user_id: str
    comment_text: str
    thread_context: list[str] = Field(default_factory=list)
    reporter_count: int = 0
    prior_violation_count: int = 0
    prior_appeal_overturns: int = 0
    author_tenure_days: int = 365
    policy_version: str = "comment-policy-v1"
    review_outcome_note: str | None = None
    expected_action: str | None = None
    expected_category: str | None = None
    expected_queue: str | None = None


class EvidenceSpan(BaseModel):
    text: str
    label: str


class PolicyHit(BaseModel):
    clause_id: str
    title: str
    category: str
    severity: str
    decision: str
    matched_keywords: list[str] = Field(default_factory=list)
    reviewer_guidance: list[str] = Field(default_factory=list)


class RiskSignal(BaseModel):
    signal: str
    level: str
    value: str
    note: str


class SimilarCase(BaseModel):
    case_id: str
    comment_text: str
    final_action: str
    category: str
    queue_name: str
    summary: str


class QueueRouting(BaseModel):
    queue_name: str
    priority: str
    rationale: str
    sla_minutes: int


class BusinessImpact(BaseModel):
    automation_mode: str
    reviewer_load: str
    risk_level: str
    notes: list[str] = Field(default_factory=list)


class ToolTrace(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    result_summary: str


class ReviewDecision(BaseModel):
    action: str
    primary_category: str
    confidence: float
    policy_clause_ids: list[str] = Field(default_factory=list)
    evidence_spans: list[EvidenceSpan] = Field(default_factory=list)
    rationale: str
    escalation_reason: str | None = None


class ReviewResponse(BaseModel):
    case_id: str
    user_id: str
    comment_text: str
    thread_context: list[str] = Field(default_factory=list)
    matched_policies: list[PolicyHit] = Field(default_factory=list)
    risk_signals: list[RiskSignal] = Field(default_factory=list)
    similar_cases: list[SimilarCase] = Field(default_factory=list)
    queue_routing: QueueRouting
    business_impact: BusinessImpact
    recommended_actions: list[str] = Field(default_factory=list)
    decision: ReviewDecision
    review_notes: list[str] = Field(default_factory=list)
    tool_trace: list[ToolTrace] = Field(default_factory=list)
    stop_reason: str = "completed_auto_pass"
