from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class ResumeDocument:
    name: str
    summary: str
    experiences: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)

    @classmethod
    def from_markdown(cls, text: str) -> "ResumeDocument":
        lines = [line.rstrip() for line in text.splitlines()]
        name = "Unknown"
        summary_lines: list[str] = []
        experiences: list[str] = []
        skills: list[str] = []
        current_section: str | None = None

        for raw_line in lines:
            if raw_line.startswith("# "):
                name = raw_line[2:].strip()
                current_section = None
                continue
            if raw_line.startswith("## "):
                current_section = raw_line[3:].strip().lower()
                continue
            if not raw_line or not current_section:
                if not current_section and raw_line:
                    summary_lines.append(raw_line.strip())
                continue

            if "- " in raw_line:
                entry = raw_line.split("-", 1)[1].strip()
            else:
                entry = raw_line.strip()

            if current_section in {"项目经历", "项目经验", "experiences"}:
                if entry:
                    experiences.append(entry)
            elif current_section in {"技能", "skills"}:
                if entry:
                    skills.append(entry)
            else:
                summary_lines.append(entry)

        summary = " ".join(summary_lines).strip()
        return cls(name=name, summary=summary, experiences=experiences, skills=skills)

    def to_dict(self) -> dict[str, Iterable[str] | str]:
        return {
            "name": self.name,
            "summary": self.summary,
            "experiences": self.experiences,
            "skills": self.skills,
        }
