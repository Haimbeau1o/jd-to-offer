from pathlib import Path

from typer.testing import CliRunner

from driverops_agent_lab.cli import app


runner = CliRunner()


def test_driverops_evaluate_command(tmp_path: Path) -> None:
    outpath = tmp_path / "eval.json"
    result = runner.invoke(app, ["evaluate", "--outpath", str(outpath)])
    assert result.exit_code == 0
    assert outpath.exists()
    text = outpath.read_text(encoding="utf-8")
    assert '"intent_accuracy"' in text
    assert '"tool_coverage"' in text


def test_driverops_export_training_data(tmp_path: Path) -> None:
    outpath = tmp_path / "training.jsonl"
    result = runner.invoke(app, ["export-training-data", "--outpath", str(outpath)])
    assert result.exit_code == 0
    assert outpath.exists()
    text = outpath.read_text(encoding="utf-8")
    assert '"messages"' in text
    assert '"metadata"' in text
