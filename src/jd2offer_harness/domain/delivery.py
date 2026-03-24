from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BundleManifest:
    output_files: list[str] = field(default_factory=list)
    included_artifacts: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "output_files": self.output_files,
            "included_artifacts": self.included_artifacts,
            "summary": self.summary,
        }
