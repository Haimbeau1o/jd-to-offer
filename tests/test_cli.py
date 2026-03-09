from typer.testing import CliRunner

from jd_offer.cli import app


runner = CliRunner()


def test_cli_shows_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.stdout
