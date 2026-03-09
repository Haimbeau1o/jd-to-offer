from pathlib import Path

from typer.testing import CliRunner

from jd_offer.cli import app


runner = CliRunner()


def test_generate_didi_case(tmp_path: Path) -> None:
    outdir = tmp_path / "didi-case"
    result = runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/didi_2026_agent_jd.md",
            "--company",
            "didi",
            "--role",
            "agent-algorithm",
            "--outdir",
            str(outdir),
        ],
    )
    assert result.exit_code == 0
    assert (outdir / "01_jd_decomposition.md").exists()
    assert (outdir / "02_knowledge_system.md").exists()
    assert (outdir / "03_resource_pack.md").exists()
    assert (outdir / "04_project_blueprint.md").exists()
    assert (outdir / "05_interview_assets.md").exists()
