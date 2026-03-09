from pathlib import Path

from jd_offer.parser import parse_jd_markdown
from jd_offer.taxonomy import map_jd_to_competencies


JD_PATH = Path("examples/didi_2026_agent_jd.md")
TAXONOMY_PATH = Path("configs/competency_taxonomy.yaml")


def test_map_jd_to_competencies() -> None:
    jd = parse_jd_markdown(JD_PATH)
    result = map_jd_to_competencies(jd, TAXONOMY_PATH)
    tags = {item.name for item in result.items}
    assert "agent_system_design" in tags
    assert "post_training_alignment" in tags
    assert "rl_and_reward_design" in tags
    assert "ride_hailing_supply_demand" in tags
