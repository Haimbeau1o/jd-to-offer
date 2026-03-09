from pathlib import Path

from jd_offer.parser import parse_jd_markdown


JD_PATH = Path("examples/didi_2026_agent_jd.md")


def test_parse_jd_sections() -> None:
    result = parse_jd_markdown(JD_PATH)
    assert result.title == "滴滴26届春招-算法工程师（供需策略）"
    assert len(result.responsibilities) >= 5
    assert len(result.requirements) >= 6
    assert len(result.bonus_items) >= 3
