from __future__ import annotations

import re
from pathlib import Path

import typer

from jd_offer.parser import parse_jd_markdown
from jd_offer.project_templates import (
    build_interview_assets,
    build_jd_decomposition,
    build_knowledge_system,
    build_project_blueprint,
    build_resource_pack,
    load_resource_registry,
    select_project_template,
    select_resources,
)
from jd_offer.renderer import render_case_bundle
from jd_offer.research import load_resource_overrides, merge_resources, scaffold_research_template
from jd_offer.taxonomy import map_jd_to_competencies

app = typer.Typer(help="Generate knowledge and project bundles from a JD.")


@app.callback()
def main_callback() -> None:
    """CLI root."""


DEFAULT_TAXONOMY_PATH = Path("configs/competency_taxonomy.yaml")
DEFAULT_PROJECT_TEMPLATES_PATH = Path("configs/project_templates.yaml")
DEFAULT_RESOURCE_REGISTRY_PATH = Path("configs/resource_registry.yaml")


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return normalized.strip("-") or "case"


@app.command()
def generate(
    input: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to JD markdown file."),
    company: str = typer.Option(..., help="Target company."),
    role: str = typer.Option(..., help="Target role slug."),
    outdir: Path = typer.Option(..., file_okay=False, dir_okay=True, help="Output directory."),
    taxonomy: Path = typer.Option(DEFAULT_TAXONOMY_PATH, exists=True, file_okay=True, dir_okay=False, help="Competency taxonomy YAML."),
    resources: Path = typer.Option(DEFAULT_RESOURCE_REGISTRY_PATH, exists=True, file_okay=True, dir_okay=False, help="Resource registry YAML."),
    templates: Path = typer.Option(DEFAULT_PROJECT_TEMPLATES_PATH, exists=True, file_okay=True, dir_okay=False, help="Project templates YAML."),
    resource_overrides: Path | None = typer.Option(None, exists=True, file_okay=True, dir_okay=False, help="Optional per-case research overrides YAML."),
) -> None:
    jd = parse_jd_markdown(input)
    competency_map = map_jd_to_competencies(jd, taxonomy)
    project_template = select_project_template(competency_map, templates)

    base_resources = load_resource_registry(resources)
    if resource_overrides is not None:
        override_resources = load_resource_overrides(resource_overrides)
        merged_resources = merge_resources(base_resources, override_resources)
    else:
        merged_resources = base_resources
    resource_entries = select_resources(competency_map, merged_resources)

    payload = {
        "jd_decomposition": build_jd_decomposition(jd, competency_map),
        "knowledge_system": build_knowledge_system(competency_map),
        "resource_pack": build_resource_pack(competency_map, resource_entries),
        "project_blueprint": build_project_blueprint(jd, competency_map, project_template, company, role),
        "interview_assets": build_interview_assets(jd, competency_map, project_template),
    }
    case_slug = slugify(f"{company}-{role}")
    render_case_bundle(
        case_slug=case_slug,
        outdir=outdir,
        payload=payload,
        source_jd=str(input),
        company=company,
        role=role,
        competencies=competency_map.top_names,
        extra={
            "project_template": project_template.id,
            "resource_overrides": str(resource_overrides) if resource_overrides else None,
        },
    )
    typer.echo(f"Generated case bundle at {outdir}")


@app.command("scaffold-research")
def scaffold_research(
    input: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, help="Path to JD markdown file."),
    outpath: Path = typer.Option(..., file_okay=True, dir_okay=False, help="Path to write the research override template."),
    taxonomy: Path = typer.Option(DEFAULT_TAXONOMY_PATH, exists=True, file_okay=True, dir_okay=False, help="Competency taxonomy YAML."),
) -> None:
    jd = parse_jd_markdown(input)
    competency_map = map_jd_to_competencies(jd, taxonomy)
    scaffold_research_template(jd, competency_map, outpath)
    typer.echo(f"Wrote research template to {outpath}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
