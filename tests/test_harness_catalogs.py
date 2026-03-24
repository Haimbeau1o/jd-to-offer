from pathlib import Path

import yaml


def test_project_archetype_catalog_exists() -> None:
    payload = yaml.safe_load(Path("configs/project_archetypes.yaml").read_text(encoding="utf-8"))
    assert payload["archetypes"]
    assert any(item["id"] == "vertical_agent_system" for item in payload["archetypes"])


def test_evaluation_rubric_catalog_exists() -> None:
    payload = yaml.safe_load(Path("configs/evaluation_rubrics.yaml").read_text(encoding="utf-8"))
    assert payload["rubrics"]
    assert any(item["name"] == "resume_grounding_score" for item in payload["rubrics"])
