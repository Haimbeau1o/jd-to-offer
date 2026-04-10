from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from pydantic import BaseModel, Field

from commentops_agent_lab.agent import CommentOpsAgent
from commentops_agent_lab.data import load_sample_review_cases
from commentops_agent_lab.eval import EvalCaseResult, run_evaluation
from commentops_agent_lab.schemas import ReviewCase


class SFTSample(BaseModel):
    messages: list[dict[str, str]] = Field(default_factory=list)
    decision: dict[str, Any] = Field(default_factory=dict)
    queue_routing: dict[str, Any] = Field(default_factory=dict)
    risk_signals: list[dict[str, Any]] = Field(default_factory=list)
    similar_cases: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PreferenceSample(BaseModel):
    prompt: str
    chosen: str
    rejected: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class FailureReviewItem(BaseModel):
    case_id: str
    predicted_action: str
    predicted_queue: str
    taxonomy: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class FailureReviewReport(BaseModel):
    summary: dict[str, Any] = Field(default_factory=dict)
    items: list[FailureReviewItem] = Field(default_factory=list)


def build_sft_samples(agent: CommentOpsAgent | None = None, cases: list[ReviewCase] | None = None) -> list[SFTSample]:
    sample_agent = agent or CommentOpsAgent()
    sample_cases = cases or load_sample_review_cases()
    records: list[SFTSample] = []

    for case in sample_cases:
        response = sample_agent.run(
            case_id=case.case_id,
            comment_text=case.comment_text,
            thread_context=case.thread_context,
            user_id=case.user_id,
            reporter_count=case.reporter_count,
            prior_violation_count=case.prior_violation_count,
            prior_appeal_overturns=case.prior_appeal_overturns,
            author_tenure_days=case.author_tenure_days,
            policy_version=case.policy_version,
        )
        records.append(
            SFTSample(
                messages=[
                    {
                        "role": "system",
                        "content": "你是评论审核 Agent，必须给出 policy-grounded 的 pass/reject/escalate 决策。",
                    },
                    {"role": "user", "content": case.comment_text},
                    {"role": "assistant", "content": response.decision.rationale},
                ],
                decision=response.decision.model_dump(),
                queue_routing=response.queue_routing.model_dump(),
                risk_signals=[item.model_dump() for item in response.risk_signals],
                similar_cases=[item.model_dump() for item in response.similar_cases],
                metadata={
                    "case_id": case.case_id,
                    "expected_action": case.expected_action,
                    "expected_category": case.expected_category,
                    "expected_queue": case.expected_queue,
                    "business_tags": [
                        response.business_impact.automation_mode,
                        response.queue_routing.queue_name,
                        response.business_impact.risk_level,
                    ],
                    "stop_reason": response.stop_reason,
                    "training_tags": ["comment_moderation", "policy_grounding", response.decision.action],
                },
            )
        )
    return records


def build_preference_samples(cases: list[ReviewCase] | None = None) -> list[PreferenceSample]:
    sample_cases = cases or load_sample_review_cases()
    records: list[PreferenceSample] = []
    for case in sample_cases:
        chosen = _preferred_response(case)
        rejected = _rejected_response(case)
        records.append(
            PreferenceSample(
                prompt=f"审核评论：{case.comment_text}",
                chosen=chosen,
                rejected=rejected,
                metadata={
                    "case_id": case.case_id,
                    "expected_action": case.expected_action,
                    "expected_category": case.expected_category,
                    "expected_queue": case.expected_queue,
                },
            )
        )
    return records


def export_sft_samples(outpath: Path, samples: list[SFTSample] | None = None) -> Path:
    records = samples or build_sft_samples()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open("w", encoding="utf-8") as handle:
        for sample in records:
            handle.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
    return outpath


def export_preference_samples(outpath: Path, samples: list[PreferenceSample] | None = None) -> Path:
    records = samples or build_preference_samples()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open("w", encoding="utf-8") as handle:
        for sample in records:
            handle.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
    return outpath


def build_failure_review(agent: CommentOpsAgent | None = None, cases: list[ReviewCase] | None = None) -> FailureReviewReport:
    report = run_evaluation(agent=agent or CommentOpsAgent(), cases=cases or load_sample_review_cases())
    items: list[FailureReviewItem] = []
    taxonomy_counts: dict[str, int] = {
        "queue_mismatch": 0,
        "manual_review_pressure": 0,
        "shadow_audit_candidate": 0,
        "appeal_sensitive": 0,
    }

    for case in report.cases:
        taxonomy = _classify_failure_taxonomy(case)
        if not taxonomy:
            continue
        for key in taxonomy:
            taxonomy_counts[key] += 1
        items.append(
            FailureReviewItem(
                case_id=case.case_id,
                predicted_action=case.predicted_action,
                predicted_queue=case.predicted_queue,
                taxonomy=taxonomy,
                notes=_build_failure_notes(case, taxonomy),
            )
        )

    return FailureReviewReport(
        summary={
            "total_cases": report.total_cases,
            "items_with_flags": len(items),
            "taxonomy_counts": taxonomy_counts,
            "queue_routing_accuracy": report.queue_routing_accuracy,
            "human_review_rate": report.human_review_rate,
        },
        items=items,
    )


def export_failure_review(outpath: Path, report: FailureReviewReport | None = None) -> Path:
    review = report or build_failure_review()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(review.model_dump_json(indent=2), encoding="utf-8")
    return outpath


def _preferred_response(case: ReviewCase) -> str:
    if case.expected_action == "reject":
        return "命中明确违规条款，给出拒绝结论并记录证据片段。"
    if case.expected_action == "escalate":
        return "语义依赖上下文，升级人工审核并附上命中条款与不确定性说明。"
    return "未命中高风险条款，保守放行并保留抽样复查建议。"


def _rejected_response(case: ReviewCase) -> str:
    if case.expected_action == "reject":
        return "语义有点激烈，但先升级人工，不给明确条款依据。"
    if case.expected_action == "escalate":
        return "虽然上下文不足，也直接拒绝处理。"
    return "虽然没有明显违规，也直接拒绝。"


def _classify_failure_taxonomy(case: EvalCaseResult) -> list[str]:
    taxonomy: list[str] = []
    if not case.queue_correct:
        taxonomy.append("queue_mismatch")
    if case.predicted_action == "escalate":
        taxonomy.append("manual_review_pressure")
    if case.predicted_queue == "shadow_audit_queue":
        taxonomy.append("shadow_audit_candidate")
    if case.predicted_queue in {"shadow_audit_queue", "context_review_queue"}:
        taxonomy.append("appeal_sensitive")

    unique_taxonomy: list[str] = []
    for key in taxonomy:
        if key not in unique_taxonomy:
            unique_taxonomy.append(key)
    return unique_taxonomy


def _build_failure_notes(case: EvalCaseResult, taxonomy: list[str]) -> list[str]:
    notes: list[str] = []
    if "queue_mismatch" in taxonomy:
        notes.append("路由策略和期望队列不一致，说明阈值或队列映射需要校准。")
    if "manual_review_pressure" in taxonomy:
        notes.append("该 case 进入人工复核，会直接影响 reviewer 吞吐和 SLA。")
    if "shadow_audit_candidate" in taxonomy:
        notes.append("该 case 体现了 guarded auto-pass 边界，适合回灌抽样复查策略。")
    if "appeal_sensitive" in taxonomy:
        notes.append("该 case 更适合进入 preference / appeal 数据池，用于后续策略优化。")
    return notes
