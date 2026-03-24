from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvaluationReport:
    scores: dict[str, float] = field(default_factory=dict)
    overall_readiness: str = ""
    summary: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "scores": self.scores,
            "overall_readiness": self.overall_readiness,
            "summary": self.summary,
        }
