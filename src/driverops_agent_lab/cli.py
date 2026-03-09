from __future__ import annotations

from pathlib import Path

import typer
import uvicorn

from driverops_agent_lab.app import app as fastapi_app
from driverops_agent_lab.eval import run_evaluation, write_eval_report
from driverops_agent_lab.training_data import export_training_samples

cli = typer.Typer(help="DriverOps Agent Lab commands.")


@cli.command("serve")
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind."),
    port: int = typer.Option(8001, help="Port to bind."),
) -> None:
    uvicorn.run(fastapi_app, host=host, port=port, reload=False)


@cli.command("evaluate")
def evaluate(
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Where to write the evaluation JSON report."),
) -> None:
    report = run_evaluation()
    write_eval_report(report, outpath)
    typer.echo(f"Wrote evaluation report to {outpath}")


@cli.command("export-training-data")
def export_training_data(
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Where to write the JSONL training samples."),
) -> None:
    export_training_samples(outpath)
    typer.echo(f"Wrote training data to {outpath}")


def main() -> None:
    cli()


app = cli


if __name__ == "__main__":
    main()
