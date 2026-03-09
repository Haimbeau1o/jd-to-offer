from __future__ import annotations

from pathlib import Path
import json

from pydantic import BaseModel, Field

from driverops_agent_lab.agent import DriverOpsAgent


class EvalCase(BaseModel):
    case_id: str
    query: str
    expected_intent: str
    expected_tools: list[str] = Field(default_factory=list)
    city: str = "beijing"
    driver_id: str = "driver-001"


class EvalCaseResult(BaseModel):
    case_id: str
    query: str
    expected_intent: str
    predicted_intent: str
    intent_correct: bool
    expected_tools: list[str]
    used_tools: list[str]
    tool_coverage: float


class EvalReport(BaseModel):
    total_cases: int
    intent_accuracy: float
    tool_coverage: float
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
            )
        )

    total = len(results)
    intent_accuracy = sum(1 for item in results if item.intent_correct) / total if total else 0.0
    tool_coverage = sum(item.tool_coverage for item in results) / total if total else 0.0
    return EvalReport(total_cases=total, intent_accuracy=intent_accuracy, tool_coverage=tool_coverage, cases=results)


def write_eval_report(report: EvalReport, outpath: Path) -> Path:
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return outpath
