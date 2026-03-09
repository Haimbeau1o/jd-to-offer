from pathlib import Path

from jd_offer.parser import parse_jd_markdown
from jd_offer.project_templates import load_resource_registry, select_resources
from jd_offer.research import load_resource_overrides, merge_resources, scaffold_research_template
from jd_offer.taxonomy import map_jd_to_competencies


JD_PATH = Path("examples/didi_2026_agent_jd.md")
BASE_RESOURCES = Path("configs/resource_registry.yaml")
OVERRIDES = Path("examples/didi_2026_verified_resources.yaml")
TAXONOMY = Path("configs/competency_taxonomy.yaml")


def test_merge_resource_overrides_adds_latest_resources() -> None:
    base = load_resource_registry(BASE_RESOURCES)
    overrides = load_resource_overrides(OVERRIDES)
    merged = merge_resources(base, overrides)
    ids = {item.id for item in merged}
    assert "autogen-agentchat-dev" in ids
    assert "trl-docs" in ids


def test_select_resources_uses_overrides() -> None:
    jd = parse_jd_markdown(JD_PATH)
    competencies = map_jd_to_competencies(jd, TAXONOMY)
    base = load_resource_registry(BASE_RESOURCES)
    overrides = load_resource_overrides(OVERRIDES)
    merged = merge_resources(base, overrides)
    selected = select_resources(competencies, merged)
    titles = {item.title for item in selected}
    assert "AgentChat — AutoGen" in titles


def test_scaffold_research_template(tmp_path: Path) -> None:
    jd = parse_jd_markdown(JD_PATH)
    competencies = map_jd_to_competencies(jd, TAXONOMY)
    out = tmp_path / "research.yaml"
    scaffold_research_template(jd, competencies, out)
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "top_competencies" in text
    assert "resources:" in text
