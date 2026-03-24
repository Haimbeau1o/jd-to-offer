from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProjectSpec:
    archetype_id: str
    archetype_name: str
    project_name: str
    thesis: str
    rationale: str
    matched_resume_signals: list[str] = field(default_factory=list)
    target_jd_signals: list[str] = field(default_factory=list)
    modules: list[str] = field(default_factory=list)
    visuals: list[str] = field(default_factory=list)
    stretch_areas: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "archetype_id": self.archetype_id,
            "archetype_name": self.archetype_name,
            "project_name": self.project_name,
            "thesis": self.thesis,
            "rationale": self.rationale,
            "matched_resume_signals": self.matched_resume_signals,
            "target_jd_signals": self.target_jd_signals,
            "modules": self.modules,
            "visuals": self.visuals,
            "stretch_areas": self.stretch_areas,
        }

