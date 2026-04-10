from pathlib import Path
import json

from typer.testing import CliRunner

from commentops_agent_lab.cli import app


runner = CliRunner()


def test_commentops_evaluate_command(tmp_path: Path) -> None:
    outpath = tmp_path / "commentops_eval.json"

    result = runner.invoke(app, ["evaluate", "--outpath", str(outpath)])

    assert result.exit_code == 0
    assert outpath.exists()

    payload = json.loads(outpath.read_text(encoding="utf-8"))
    assert "total_cases" in payload
    assert "action_accuracy" in payload
    assert "policy_grounding_rate" in payload
    assert "escalation_precision" in payload
    assert "auto_pass_rate" in payload
    assert "auto_reject_rate" in payload
    assert "human_review_rate" in payload
    assert "queue_routing_accuracy" in payload
    assert payload["cases"]
    assert "predicted_action" in payload["cases"][0]
    assert "predicted_queue" in payload["cases"][0]


def test_commentops_export_sft_command(tmp_path: Path) -> None:
    outpath = tmp_path / "commentops_sft.jsonl"

    result = runner.invoke(app, ["export-sft", "--outpath", str(outpath)])

    assert result.exit_code == 0
    assert outpath.exists()

    lines = [json.loads(line) for line in outpath.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert lines
    first = lines[0]
    assert "messages" in first
    assert "decision" in first
    assert "metadata" in first
    assert "queue_routing" in first
    assert "similar_cases" in first


def test_commentops_export_failure_review_command(tmp_path: Path) -> None:
    outpath = tmp_path / "commentops_failure_review.json"

    result = runner.invoke(app, ["export-failure-review", "--outpath", str(outpath)])

    assert result.exit_code == 0
    assert outpath.exists()

    payload = json.loads(outpath.read_text(encoding="utf-8"))
    assert "summary" in payload
    assert "items" in payload
    assert "taxonomy_counts" in payload["summary"]
