from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class TargetJD:
    title: str
    responsibilities: list[str] = field(default_factory=list)
    requirements: list[str] = field(default_factory=list)
    bonus_items: list[str] = field(default_factory=list)

    @classmethod
    def from_markdown(cls, text: str) -> "TargetJD":
        lines = [line.strip() for line in text.splitlines()]
        title = "Untitled JD"
        buckets = {"responsibilities": [], "requirements": [], "bonus": []}
        current_section: str | None = None

        for raw in lines:
            if raw.startswith("# "):
                title = raw[2:].strip()
                continue
            if raw.startswith("## "):
                heading = raw[3:].strip().lower()
                if "岗位职责" in heading or "responsibilities" in heading:
                    current_section = "responsibilities"
                elif "任职要求" in heading or "requirements" in heading:
                    current_section = "requirements"
                elif "加分项" in heading or "bonus" in heading:
                    current_section = "bonus"
                else:
                    current_section = None
                continue

            if not raw or not current_section:
                continue

            if raw[0].isdigit() and raw[1] in ".、)":
                entry = raw[2:].strip()
            elif raw.startswith("- "):
                entry = raw[2:].strip()
            else:
                entry = raw

            if entry:
                buckets[current_section].append(entry)

        return cls(
            title=title,
            responsibilities=buckets["responsibilities"],
            requirements=buckets["requirements"],
            bonus_items=buckets["bonus"],
        )

    def to_dict(self) -> dict[str, Iterable[str] | str]:
        return {
            "title": self.title,
            "responsibilities": self.responsibilities,
            "requirements": self.requirements,
            "bonus_items": self.bonus_items,
        }
