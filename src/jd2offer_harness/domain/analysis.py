from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ResumeEvidence:
    candidate_name: str
    summary: str
    experience_highlights: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_name": self.candidate_name,
            "summary": self.summary,
            "experience_highlights": self.experience_highlights,
            "skills": self.skills,
        }


@dataclass
class GapAnalysis:
    matched_signals: list[str] = field(default_factory=list)
    missing_signals: list[str] = field(default_factory=list)
    coverage_summary: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "matched_signals": self.matched_signals,
            "missing_signals": self.missing_signals,
            "coverage_summary": self.coverage_summary,
        }
