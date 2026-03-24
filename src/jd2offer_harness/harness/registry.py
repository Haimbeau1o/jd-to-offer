from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class StageSpec:
    slug: str
    prompt_path: Path
    output_artifact: str
    dependencies: list[str] = field(default_factory=list)


class StageRegistry:
    def __init__(self, specs: list[StageSpec]) -> None:
        self._specs = {spec.slug: spec for spec in specs}

    def get(self, slug: str) -> StageSpec:
        try:
            return self._specs[slug]
        except KeyError as exc:
            raise ValueError(f"Unknown stage slug: {slug}") from exc

    def all(self) -> list[StageSpec]:
        return list(self._specs.values())


def default_stage_registry() -> StageRegistry:
    return StageRegistry(
        [
            StageSpec(
                slug="intake",
                prompt_path=Path("prompts/intake.md"),
                output_artifact="resume_evidence.yaml",
            ),
            StageSpec(
                slug="competency-analysis",
                prompt_path=Path("prompts/competency_analysis.md"),
                output_artifact="competency_graph.yaml",
                dependencies=["intake"],
            ),
            StageSpec(
                slug="gap-mapping",
                prompt_path=Path("prompts/gap_analysis.md"),
                output_artifact="gap_analysis.yaml",
                dependencies=["intake"],
            ),
            StageSpec(
                slug="project-design",
                prompt_path=Path("prompts/project_design.md"),
                output_artifact="project_spec.yaml",
                dependencies=["gap-mapping"],
            ),
            StageSpec(
                slug="visual-story",
                prompt_path=Path("prompts/visual_story.md"),
                output_artifact="visual_story.yaml",
                dependencies=["project-design"],
            ),
            StageSpec(
                slug="interview-assets",
                prompt_path=Path("prompts/interview_assets.md"),
                output_artifact="interview_assets.yaml",
                dependencies=["project-design"],
            ),
            StageSpec(
                slug="bundle-render",
                prompt_path=Path("prompts/bundle_render.md"),
                output_artifact="bundle_manifest.yaml",
                dependencies=["visual-story", "interview-assets"],
            ),
            StageSpec(
                slug="evaluation",
                prompt_path=Path("prompts/evaluation.md"),
                output_artifact="evaluation_report.yaml",
                dependencies=["bundle-render"],
            ),
        ]
    )
