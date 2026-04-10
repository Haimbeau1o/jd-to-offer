from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from commentops_agent_lab.agent import CommentOpsAgent
from commentops_agent_lab.data import load_sample_review_cases
from commentops_agent_lab.schemas import ReviewCase


class EvalCaseResult(BaseModel):
    case_id: str
    expected_action: str
    predicted_action: str
    expected_category: str | None = None
    predicted_category: str
    expected_queue: str | None = None
    predicted_queue: str
    action_correct: bool
    queue_correct: bool
    policy_grounded: bool
    escalated: bool
    confidence: float
    used_tools: list[str] = Field(default_factory=list)


class EvalReport(BaseModel):
    total_cases: int
    action_accuracy: float
    policy_grounding_rate: float
    escalation_precision: float
    auto_pass_rate: float
    auto_reject_rate: float
    human_review_rate: float
    queue_routing_accuracy: float
    average_confidence: float
    cases: list[EvalCaseResult] = Field(default_factory=list)


def run_evaluation(agent: CommentOpsAgent | None = None, cases: list[ReviewCase] | None = None) -> EvalReport:
    eval_agent = agent or CommentOpsAgent()
    eval_cases = cases or load_sample_review_cases()
    results: list[EvalCaseResult] = []

    for case in eval_cases:
        response = eval_agent.run(
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
        results.append(
            EvalCaseResult(
                case_id=case.case_id,
                expected_action=case.expected_action or "",
                predicted_action=response.decision.action,
                expected_category=case.expected_category,
                predicted_category=response.decision.primary_category,
                expected_queue=case.expected_queue,
                predicted_queue=response.queue_routing.queue_name,
                action_correct=response.decision.action == case.expected_action,
                queue_correct=response.queue_routing.queue_name == case.expected_queue,
                policy_grounded=bool(response.decision.policy_clause_ids),
                escalated=response.decision.action == "escalate",
                confidence=response.decision.confidence,
                used_tools=[item.tool_name for item in response.tool_trace],
            )
        )

    total = len(results)
    escalated_results = [item for item in results if item.escalated]
    escalation_precision = (
        sum(1 for item in escalated_results if item.expected_action == "escalate") / len(escalated_results)
        if escalated_results
        else 1.0
    )
    auto_pass_rate = sum(1 for item in results if item.predicted_action == "pass") / total if total else 0.0
    auto_reject_rate = sum(1 for item in results if item.predicted_action == "reject") / total if total else 0.0
    human_review_rate = sum(1 for item in results if item.predicted_action == "escalate") / total if total else 0.0
    queue_routing_accuracy = sum(1 for item in results if item.queue_correct) / total if total else 0.0
    return EvalReport(
        total_cases=total,
        action_accuracy=sum(1 for item in results if item.action_correct) / total if total else 0.0,
        policy_grounding_rate=sum(1 for item in results if item.policy_grounded) / total if total else 0.0,
        escalation_precision=escalation_precision,
        auto_pass_rate=auto_pass_rate,
        auto_reject_rate=auto_reject_rate,
        human_review_rate=human_review_rate,
        queue_routing_accuracy=queue_routing_accuracy,
        average_confidence=sum(item.confidence for item in results) / total if total else 0.0,
        cases=results,
    )


def write_eval_report(report: EvalReport, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return outpath
