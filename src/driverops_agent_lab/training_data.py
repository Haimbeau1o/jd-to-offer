from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from pydantic import BaseModel, Field

from driverops_agent_lab.agent import DriverOpsAgent
from driverops_agent_lab.eval import EvalCaseResult, default_eval_cases, run_evaluation


class GroundedAnswerPayload(BaseModel):
    answer_summary: str
    evidence_items: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    risk_notes: list[str] = Field(default_factory=list)


class TrainingSample(BaseModel):
    messages: list[dict[str, str]] = Field(default_factory=list)
    plan: list[dict[str, Any]] = Field(default_factory=list)
    observations: list[dict[str, Any]] = Field(default_factory=list)
    grounded_answer: GroundedAnswerPayload
    stop_reason: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class FailureReviewItem(BaseModel):
    case_id: str
    query: str
    expected_intent: str
    predicted_intent: str
    stop_reason: str
    taxonomy: list[str] = Field(default_factory=list)
    metrics: dict[str, float] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)


class FailureReviewReport(BaseModel):
    summary: dict[str, Any] = Field(default_factory=dict)
    failures: list[FailureReviewItem] = Field(default_factory=list)


TAXONOMY_KEYS = [
    "planning_error",
    "missing_evidence",
    "wrong_tool_choice",
    "weak_recommendation",
    "fallback_triggered",
]


def build_training_samples() -> list[TrainingSample]:
    cases = default_eval_cases()
    evaluation_agent = DriverOpsAgent()
    evaluation_report = run_evaluation(agent=evaluation_agent, cases=cases)
    failure_tags_by_case = {
        case_result.case_id: _classify_failure_taxonomy(case_result) for case_result in evaluation_report.cases
    }

    generation_agent = DriverOpsAgent()
    samples: list[TrainingSample] = []
    for case in cases:
        response = generation_agent.run(driver_id=case.driver_id, city=case.city, query=case.query)
        samples.append(
            TrainingSample(
                messages=[
                    {"role": "system", "content": _system_prompt_for_intent(case.expected_intent)},
                    {"role": "user", "content": case.query},
                    {"role": "assistant", "content": response.answer_summary},
                ],
                plan=[step.model_dump() for step in response.plan],
                observations=[item.model_dump() for item in response.observations],
                grounded_answer=GroundedAnswerPayload(
                    answer_summary=response.answer_summary,
                    evidence_items=response.evidence_items,
                    recommendations=response.recommendations,
                    risk_notes=response.risk_notes,
                ),
                stop_reason=response.stop_reason,
                metadata={
                    "case_id": case.case_id,
                    "driver_id": case.driver_id,
                    "city": case.city,
                    "expected_intent": case.expected_intent,
                    "predicted_intent": response.intent,
                    "training_tags": _training_tags_for_case(response.intent),
                    "failure_tags": failure_tags_by_case.get(case.case_id, []),
                },
            )
        )
    return samples



def build_failure_review() -> FailureReviewReport:
    baseline_report = run_evaluation(agent=DriverOpsAgent(), cases=default_eval_cases())
    fallback_report = run_evaluation(agent=_build_fallback_agent(), cases=[_fallback_eval_case()])
    all_case_results = [*baseline_report.cases, *fallback_report.cases]

    failures: list[FailureReviewItem] = []
    taxonomy_counts = {key: 0 for key in TAXONOMY_KEYS}
    for case_result in all_case_results:
        taxonomy = _classify_failure_taxonomy(case_result)
        if not taxonomy:
            continue
        for key in taxonomy:
            taxonomy_counts[key] += 1
        failures.append(
            FailureReviewItem(
                case_id=case_result.case_id,
                query=case_result.query,
                expected_intent=case_result.expected_intent,
                predicted_intent=case_result.predicted_intent,
                stop_reason=case_result.stop_reason,
                taxonomy=taxonomy,
                metrics={
                    "plan_validity": case_result.plan_validity,
                    "tool_coverage": case_result.tool_coverage,
                    "step_execution_success_rate": case_result.step_execution_success_rate,
                    "evidence_coverage": case_result.evidence_coverage,
                },
                notes=_build_failure_notes(case_result, taxonomy),
            )
        )

    return FailureReviewReport(
        summary={
            "total_cases": len(all_case_results),
            "failed_cases": len(failures),
            "taxonomy_counts": taxonomy_counts,
        },
        failures=failures,
    )



def export_training_samples(outpath: Path, samples: list[TrainingSample] | None = None) -> Path:
    records = samples or build_training_samples()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with outpath.open("w", encoding="utf-8") as handle:
        for sample in records:
            handle.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
    return outpath



def export_failure_review(outpath: Path, report: FailureReviewReport | None = None) -> Path:
    review_report = report or build_failure_review()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(review_report.model_dump_json(indent=2), encoding="utf-8")
    return outpath



def _system_prompt_for_intent(intent: str) -> str:
    prompts = {
        "income_explanation": "你是司机经营助手，优先用结构化工具、长期记忆和经营事实回答收入问题。",
        "campaign_lookup": "你是司机经营助手，优先结合司机画像、活动匹配和历史偏好做推荐。",
        "hotspot_recommendation": "你是司机经营助手，优先结合热区统计和近期策略记忆给出行动建议。",
        "policy_qa": "你是司机经营助手，回答规则问题时必须给出规则依据与后续动作。",
    }
    return prompts.get(intent, "你是司机经营助手，优先基于工具结果和执行轨迹回答问题。")



def _training_tags_for_case(intent: str) -> list[str]:
    common_tags = ["react", "tool_use", "grounded_answer"]
    intent_tags = {
        "income_explanation": ["income_analysis", "memory"],
        "campaign_lookup": ["campaign_recommendation", "memory"],
        "hotspot_recommendation": ["hotspot_strategy", "memory"],
        "policy_qa": ["policy_grounding"],
    }
    return [*common_tags, *intent_tags.get(intent, ["general_support"])]



def _build_fallback_agent() -> DriverOpsAgent:
    agent = DriverOpsAgent()

    def broken_stats(_: str):
        raise RuntimeError("trip stats unavailable")

    agent.tools.get_trip_stats = broken_stats
    return agent



def _fallback_eval_case():
    from driverops_agent_lab.eval import EvalCase

    return EvalCase(
        case_id="income-fallback-001",
        query="帮我解释下我今天收入为什么下降了",
        expected_intent="income_explanation",
        expected_tools=["get_driver_profile", "get_trip_stats", "recommend_strategy"],
    )



def _classify_failure_taxonomy(case_result: EvalCaseResult) -> list[str]:
    taxonomy: list[str] = []

    if not case_result.intent_correct or case_result.plan_validity < 1.0:
        taxonomy.append("planning_error")
    if case_result.tool_coverage < 1.0:
        taxonomy.append("wrong_tool_choice")
    if case_result.stop_reason in {"completed_with_partial_evidence", "fallback_due_to_missing_data"}:
        taxonomy.append("missing_evidence")
    if case_result.stop_reason == "fallback_due_to_missing_data":
        taxonomy.append("fallback_triggered")
    recommendation_steps = [item for item in case_result.step_results if item.tool_name == "recommend_strategy"]
    if recommendation_steps and recommendation_steps[-1].evidence_count < 2:
        taxonomy.append("weak_recommendation")

    unique_taxonomy: list[str] = []
    for key in taxonomy:
        if key not in unique_taxonomy:
            unique_taxonomy.append(key)
    return unique_taxonomy



def _build_failure_notes(case_result: EvalCaseResult, taxonomy: list[str]) -> list[str]:
    notes: list[str] = []
    if "planning_error" in taxonomy:
        notes.append("当前案例的 intent 或计划步骤与预期存在偏差，需要检查 planner 的规则或 prompt。")
    if "wrong_tool_choice" in taxonomy:
        notes.append("工具覆盖不足，说明 planner 可能选择了错误工具或遗漏了关键步骤。")
    if "missing_evidence" in taxonomy:
        notes.append("证据覆盖不完整，回答需要补足 observation 或增加保守提示。")
    if "weak_recommendation" in taxonomy:
        notes.append("recommend_strategy 输出偏弱，可补充更具体的行动建议或奖励信息。")
    if "fallback_triggered" in taxonomy:
        notes.append("触发了 fallback，建议将该路径单独沉淀为失败样例和奖励惩罚数据。")
    return notes
