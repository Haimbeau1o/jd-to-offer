from __future__ import annotations

import re
from pathlib import Path

from jd_offer.schemas import JDDocument


SECTION_MAP = {
    "岗位职责": "responsibilities",
    "任职要求": "requirements",
    "加分项": "bonus_items",
}

LIST_PATTERN = re.compile(r"^\s*\d+[\.、\)]\s*(.+?)\s*$")
HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$")
TITLE_PATTERN = re.compile(r"^#\s+(.+?)\s*$")


def parse_jd_markdown(path: Path) -> JDDocument:
    text = path.read_text(encoding="utf-8")
    title = ""
    buckets: dict[str, list[str]] = {value: [] for value in SECTION_MAP.values()}
    current_section: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        title_match = TITLE_PATTERN.match(line)
        if title_match and not title:
            title = title_match.group(1).strip()
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            heading = heading_match.group(1).strip()
            current_section = SECTION_MAP.get(heading)
            continue

        if not current_section:
            continue

        item_match = LIST_PATTERN.match(line)
        if item_match:
            buckets[current_section].append(item_match.group(1).strip())
            continue

        if buckets[current_section]:
            buckets[current_section][-1] = f"{buckets[current_section][-1]} {line.strip()}".strip()

    if not title:
        raise ValueError(f"Could not find markdown title in {path}")

    return JDDocument(
        title=title,
        responsibilities=buckets["responsibilities"],
        requirements=buckets["requirements"],
        bonus_items=buckets["bonus_items"],
        raw_text=text,
    )
