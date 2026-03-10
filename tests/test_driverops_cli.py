from pathlib import Path
import json

from typer.testing import CliRunner

from driverops_agent_lab.agent import DriverOpsAgent
from driverops_agent_lab.cli import app
from driverops_agent_lab.eval import EvalCase, run_evaluation


runner = CliRunner()


def test_driverops_evaluate_command(tmp_path: Path) -> None:
    outpath = tmp_path / "eval.json"
    result = runner.invoke(app, ["evaluate", "--outpath", str(outpath)])
    assert result.exit_code == 0
    assert outpath.exists()
    payload = json.loads(outpath.read_text(encoding="utf-8"))
    assert "intent_accuracy" in payload
    assert "tool_coverage" in payload
    assert "plan_validity" in payload
    assert "step_execution_success_rate" in payload
    assert "evidence_coverage" in payload
    assert "fallback_rate" in payload
    assert payload["cases"]
    assert "stop_reason" in payload["cases"][0]
    assert "step_results" in payload["cases"][0]


def test_driverops_evaluation_tracks_fallback_and_step_results() -> None:
    agent = DriverOpsAgent()

    def broken_stats(_: str):
        raise RuntimeError("trip stats unavailable")

    agent.tools.get_trip_stats = broken_stats
    report = run_evaluation(
        agent=agent,
        cases=[
            EvalCase(
                case_id="income-fallback-001",
                query="帮我解释下我今天收入为什么下降了",
                expected_intent="income_explanation",
                expected_tools=["get_driver_profile", "get_trip_stats", "recommend_strategy"],
            )
        ],
    )

    assert report.total_cases == 1
    assert report.fallback_rate == 1.0
    assert report.step_execution_success_rate < 1.0
    assert report.evidence_coverage > 0.0
    assert report.cases[0].stop_reason == "fallback_due_to_missing_data"
    assert report.cases[0].step_results
    assert any(not item.success for item in report.cases[0].step_results)


def test_driverops_export_training_data(tmp_path: Path) -> None:
    outpath = tmp_path / "training.jsonl"
    result = runner.invoke(app, ["export-training-data", "--outpath", str(outpath)])
    assert result.exit_code == 0
    assert outpath.exists()
    text = outpath.read_text(encoding="utf-8")
    assert '"messages"' in text
    assert '"metadata"' in text
