from pathlib import Path

from jd2offer_harness.harness.registry import default_stage_registry


def test_stage_registry_exposes_project_design_contract() -> None:
    registry = default_stage_registry()

    spec = registry.get("project-design")
    assert spec.slug == "project-design"
    assert spec.output_artifact == "project_spec.yaml"
    assert spec.dependencies == ["gap-mapping"]
    assert spec.prompt_path.exists()
    assert spec.prompt_path == Path("prompts/project_design.md")


def test_stage_registry_exposes_gap_mapping_contract() -> None:
    registry = default_stage_registry()

    spec = registry.get("gap-mapping")
    assert spec.output_artifact == "gap_analysis.yaml"
    assert spec.dependencies == ["intake"]
    assert spec.prompt_path.exists()

