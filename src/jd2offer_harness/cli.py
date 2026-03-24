from __future__ import annotations

from pathlib import Path

import typer

from jd2offer_harness.harness.artifacts import initialize_case_workspace
from jd2offer_harness.harness.runner import HarnessRunner

app = typer.Typer(help="Initialize and manage resume + JD harness cases.")


@app.callback()
def main_callback() -> None:
    """CLI root."""


@app.command("init-case")
def init_case(
    resume: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to resume markdown."),
    jd: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to target JD markdown."),
    outdir: Path = typer.Option(..., file_okay=False, dir_okay=True, help="Path to case workspace directory."),
    company: str = typer.Option("", help="Target company."),
    role: str = typer.Option("", help="Target role slug."),
) -> None:
    workspace = initialize_case_workspace(
        resume_path=resume,
        jd_path=jd,
        outdir=outdir,
        company=company,
        role=role,
    )
    typer.echo(f"Initialized harness case at {workspace.root}")


@app.command("run-stage")
def run_stage(
    workspace: Path = typer.Option(..., exists=True, file_okay=False, dir_okay=True, help="Path to case workspace."),
    stage: str = typer.Option(..., help="Stage slug to execute."),
) -> None:
    result = HarnessRunner(workspace).run_stage(stage)
    typer.echo(f"Completed stage {result.slug} with status {result.status}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
