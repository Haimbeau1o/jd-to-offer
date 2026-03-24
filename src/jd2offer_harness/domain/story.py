from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VisualStory:
    diagram_title: str
    diagram_mermaid: str
    demo_flow: list[str] = field(default_factory=list)
    talking_points: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "diagram_title": self.diagram_title,
            "diagram_mermaid": self.diagram_mermaid,
            "demo_flow": self.demo_flow,
            "talking_points": self.talking_points,
        }


@dataclass
class InterviewAssets:
    resume_bullets: list[str] = field(default_factory=list)
    pitch_3min: str = ""
    pitch_10min_outline: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "resume_bullets": self.resume_bullets,
            "pitch_3min": self.pitch_3min,
            "pitch_10min_outline": self.pitch_10min_outline,
        }
