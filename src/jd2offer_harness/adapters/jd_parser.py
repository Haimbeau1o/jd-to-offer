from __future__ import annotations

from pathlib import Path

from jd2offer_harness.domain.jd import TargetJD


def parse_jd(path: Path) -> TargetJD:
    text = path.read_text(encoding="utf-8")
    return TargetJD.from_markdown(text)

