from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from driverops_agent_lab.agent import DriverOpsAgent
from driverops_agent_lab.schemas import AgentResponse


class EvalCase(BaseModel):
    case_id: str
    query: str
    expected_intent: str
    expected_tools: list[str] = Field(default_factory=list)
    city: str = "beijing"
    driver_id: str = "driver-001"


class StepEvalResult(BaseModel):
    step_id: int
    tool_name: str
    status: str
    success: bool
    evidence_count: int
    summary: str


class EvalCaseResult(BaseModel):
    case_id: str
    query: str
    expected_intent: str
    predicted_intent: str
    intent_correct: bool
    expected_tools: list[str]
    used_tools: list[str]
    tool_coverage: float
    plan_validity: float
    step_execution_success_rate: float
    evidence_coverage: float
    stop_reason: str
    step_results: list[StepEvalResult] = Field(default_factory=list)


class EvalReport(BaseModel):
    total_cases: int
    intent_accuracy: float
    tool_coverage: float
    plan_validity: float
    step_execution_success_rate: float
    evidence_coverage: float
    fallback_rate: float
    cases: list[EvalCaseResult] = Field(default_factory=list)


def default_eval_cases() -> list[EvalCase]:
    return [
        EvalCase(
            case_id="income-001",
            query="帮我解释下我今天收入为什么下降了",
            expected_intent="income_explanation",
            expected_tools=["get_driver_profile", "get_trip_stats", "recommend_strategy"],
        ),
        EvalCase(
            case_id="campaign-001",
            query="今天有什么活动适合我",
            expected_intent="campaign_lookup",
            expected_tools=["get_driver_profile", "get_campaigns", "recommend_strategy"],
        ),
        EvalCase(
            case_id="hotspot-001",
            query="帮我看看热区建议",
            expected_intent="hotspot_recommendation",
            expected_tools=["get_driver_profile", "get_trip_stats", "recommend_strategy"],
        ),
        EvalCase(
            case_id="policy-001",
            query="完单率规则会影响活动资格吗",
            expected_intent="policy_qa",
            expected_tools=["get_driver_profile", "search_policy_kb", "recommend_strategy"],
        ),
    ]


def run_evaluation(agent: DriverOpsAgent | None = None, cases: list[EvalCase] | None = None) -> EvalReport:
    eval_agent = agent or DriverOpsAgent()
    eval_cases = cases or default_eval_cases()
    results: list[EvalCaseResult] = []

    for case in eval_cases:
        response = eval_agent.run(driver_id=case.driver_id, city=case.city, query=case.query)
        used_tools = [item.tool_name for item in response.tool_trace]
        matched = sum(1 for tool in case.expected_tools if tool in used_tools)
        coverage = matched / len(case.expected_tools) if case.expected_tools else 1.0
        step_results = _build_step_results(response)
        results.append(
            EvalCaseResult(
                case_id=case.case_id,
                query=case.query,
                expected_intent=case.expected_intent,
                predicted_intent=response.intent,
                intent_correct=response.intent == case.expected_intent,
                expected_tools=case.expected_tools,
                used_tools=used_tools,
                tool_coverage=coverage,
                plan_validity=_compute_plan_validity(case, response),
                step_execution_success_rate=_compute_step_execution_success_rate(step_results),
                evidence_coverage=_compute_evidence_coverage(response),
                stop_reason=response.stop_reason,
                step_results=step_results,
            )
        )

    total = len(results)
    intent_accuracy = sum(1 for item in results if item.intent_correct) / total if total else 0.0
    tool_coverage = sum(item.tool_coverage for item in results) / total if total else 0.0
    plan_validity = sum(item.plan_validity for item in results) / total if total else 0.0
    step_execution_success_rate = sum(item.step_execution_success_rate for item in results) / total if total else 0.0
    evidence_coverage = sum(item.evidence_coverage for item in results) / total if total else 0.0
    fallback_rate = sum(1 for item in results if item.stop_reason == "fallback_due_to_missing_data") / total if total else 0.0
    return EvalReport(
        total_cases=total,
        intent_accuracy=intent_accuracy,
        tool_coverage=tool_coverage,
        plan_validity=plan_validity,
        step_execution_success_rate=step_execution_success_rate,
        evidence_coverage=evidence_coverage,
        fallback_rate=fallback_rate,
        cases=results,
    )



def _build_step_results(response: AgentResponse) -> list[StepEvalResult]:
    observations_by_step = {item.step_id: item for item in response.observations}
    step_results: list[StepEvalResult] = []
    for step in response.plan:
        observation = observations_by_step.get(step.step_id)
        step_results.append(
            StepEvalResult(
                step_id=step.step_id,
                tool_name=step.tool_name,
                status=step.status,
                success=observation.success if observation is not None else False,
                evidence_count=len(observation.evidence) if observation is not None else 0,
                summary=observation.summary if observation is not None else "",
            )
        )
    return step_results



def _compute_plan_validity(case: EvalCase, response: AgentResponse) -> float:
    if not response.plan:
        return 0.0

    plan_tools = [step.tool_name for step in response.plan]
    step_ids = [step.step_id for step in response.plan]
    checks = [
        1.0 if step_ids == list(range(1, len(step_ids) + 1)) else 0.0,
        1.0 if response.intent == case.expected_intent else 0.0,
        1.0 if all(tool in plan_tools for tool in case.expected_tools) else 0.0,
    ]
    return sum(checks) / len(checks)



def _compute_step_execution_success_rate(step_results: list[StepEvalResult]) -> float:
    if not step_results:
        return 0.0
    succeeded = sum(1 for item in step_results if item.success)
    return succeeded / len(step_results)



def _compute_evidence_coverage(response: AgentResponse) -> float:
    if not response.plan:
        return 0.0

    observations_by_step = {item.step_id: item for item in response.observations}
    covered_steps = 0
    for step in response.plan:
        observation = observations_by_step.get(step.step_id)
        if observation and (observation.summary or observation.evidence):
            covered_steps += 1
    return covered_steps / len(response.plan)



def write_eval_report(report: EvalReport, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return outpath
