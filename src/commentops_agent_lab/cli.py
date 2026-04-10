from __future__ import annotations

from pathlib import Path

import typer
import uvicorn

from commentops_agent_lab.app import app as fastapi_app
from commentops_agent_lab.eval import run_evaluation, write_eval_report
from commentops_agent_lab.training_data import export_failure_review, export_preference_samples, export_sft_samples


cli = typer.Typer(help="CommentOps Agent Lab commands.")


@cli.command("serve")
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind."),
    port: int = typer.Option(8002, help="Port to bind."),
) -> None:
    uvicorn.run(fastapi_app, host=host, port=port, reload=False)


@cli.command("evaluate")
def evaluate(
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Where to write the evaluation JSON report."),
) -> None:
    report = run_evaluation()
    write_eval_report(report, outpath)
    typer.echo(f"Wrote evaluation report to {outpath}")


@cli.command("export-sft")
def export_sft(
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Where to write the SFT JSONL samples."),
) -> None:
    export_sft_samples(outpath)
    typer.echo(f"Wrote SFT samples to {outpath}")


@cli.command("export-preferences")
def export_preferences(
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Where to write the preference JSONL samples."),
) -> None:
    export_preference_samples(outpath)
    typer.echo(f"Wrote preference samples to {outpath}")


@cli.command("export-failure-review")
def export_failure_review_command(
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Where to write the failure review JSON report."),
) -> None:
    export_failure_review(outpath)
    typer.echo(f"Wrote failure review to {outpath}")


def main() -> None:
    cli()


app = cli


if __name__ == "__main__":
    main()
