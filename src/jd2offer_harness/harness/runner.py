from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from jd2offer_harness.domain.delivery import BundleManifest
from jd2offer_harness.domain.evaluation import EvaluationReport
from jd2offer_harness.domain.project import ProjectSpec
from jd2offer_harness.domain.story import InterviewAssets, VisualStory
from jd2offer_harness.harness.artifacts import (
    DEFAULT_STAGE_NAMES,
    load_case_manifest,
    save_case_manifest,
)
from jd2offer_harness.domain.analysis import GapAnalysis, ResumeEvidence
from jd2offer_harness.harness.prompts import load_prompt_template
from jd2offer_harness.harness.registry import StageRegistry, default_stage_registry


@dataclass
class StageResult:
    slug: str
    status: str
    notes: list[str] = ()


class HarnessRunner:
    def __init__(self, workspace_path: Path, registry: StageRegistry | None = None) -> None:
        self.workspace_path = workspace_path
        self.registry = registry or default_stage_registry()

    def stage_names(self) -> Iterable[str]:
        return DEFAULT_STAGE_NAMES

    def run_stage(self, slug: str) -> StageResult:
        spec = self.registry.get(slug)
        if spec.dependencies:
            self._ensure_stage_dependencies(spec.dependencies, slug)
        if slug == "intake":
            evidence = self._build_resume_evidence()
            self._write_stage_payload(slug, spec.output_artifact, evidence.to_dict())
        elif slug == "gap-mapping":
            analysis = self._build_gap_analysis()
            self._write_stage_payload(slug, spec.output_artifact, analysis.to_dict())
        elif slug == "project-design":
            project_spec = self._build_project_spec()
            self._write_stage_payload(slug, spec.output_artifact, project_spec.to_dict())
        elif slug == "visual-story":
            visual_story = self._build_visual_story()
            self._write_stage_payload(slug, spec.output_artifact, visual_story.to_dict())
        elif slug == "interview-assets":
            interview_assets = self._build_interview_assets()
            self._write_stage_payload(slug, spec.output_artifact, interview_assets.to_dict())
        elif slug == "bundle-render":
            bundle_manifest = self._build_bundle_manifest()
            self._write_stage_payload(slug, spec.output_artifact, bundle_manifest.to_dict())
        elif slug == "evaluation":
            evaluation_report = self._build_evaluation_report()
            self._write_stage_payload(slug, spec.output_artifact, evaluation_report.to_dict())
        _ = load_prompt_template(spec.prompt_path)
        self._mark_stage_completed(slug)
        return StageResult(slug=slug, status="completed")

    def _build_resume_evidence(self) -> ResumeEvidence:
        resume_data = self._load_yaml(self.workspace_path / "normalized" / "resume_document.yaml")
        return ResumeEvidence(
            candidate_name=resume_data.get("name", ""),
            summary=resume_data.get("summary", ""),
            experience_highlights=list(resume_data.get("experiences", [])),
            skills=list(resume_data.get("skills", [])),
        )

    def _build_gap_analysis(self) -> GapAnalysis:
        resume_data = self._load_yaml(self.workspace_path / "normalized" / "resume_document.yaml")
        jd_data = self._load_yaml(self.workspace_path / "normalized" / "target_jd.yaml")
        resume_text = "\n".join(
            [
                str(resume_data.get("summary", "")),
                *[str(item) for item in resume_data.get("experiences", [])],
                *[str(item) for item in resume_data.get("skills", [])],
            ]
        ).lower()
        jd_signals = [
            *[str(item) for item in jd_data.get("responsibilities", [])],
            *[str(item) for item in jd_data.get("requirements", [])],
        ]

        matched_signals: list[str] = []
        for skill in [str(item) for item in resume_data.get("skills", [])]:
            if skill.lower() in " ".join(jd_signals).lower() and skill not in matched_signals:
                matched_signals.append(skill)

        missing_signals = [signal for signal in jd_signals if not self._signal_matches_resume(signal, resume_text)]
        coverage_summary = (
            f"Matched {len(matched_signals)} explicit resume signals; "
            f"{len(missing_signals)} JD signals still need project support."
        )
        return GapAnalysis(
            matched_signals=matched_signals,
            missing_signals=missing_signals,
            coverage_summary=coverage_summary,
        )

    def _build_project_spec(self) -> ProjectSpec:
        manifest = load_case_manifest(self.workspace_path / "manifest.yaml")
        gap_analysis = self._load_yaml(self.workspace_path / "stages" / "03-gap-mapping" / "gap_analysis.yaml")
        archetypes = self._load_yaml(Path("configs/project_archetypes.yaml")).get("archetypes", [])
        target_jd = self._load_yaml(self.workspace_path / "normalized" / "target_jd.yaml")
        matched_resume_signals = [str(item) for item in gap_analysis.get("matched_signals", [])]
        missing_signals = [str(item) for item in gap_analysis.get("missing_signals", [])]
        jd_text = "\n".join(
            [*[str(item) for item in target_jd.get("responsibilities", [])], *[str(item) for item in target_jd.get("requirements", [])]]
        ).lower()
        resume_text = "\n".join([*matched_resume_signals, *missing_signals]).lower()

        scored: list[tuple[int, dict[str, object]]] = []
        for archetype in archetypes:
            jd_score = sum(
                1 for signal in archetype.get("best_fit_jd_signals", []) if str(signal).lower() in jd_text
            )
            resume_score = sum(
                1 for signal in archetype.get("best_fit_resume_signals", []) if str(signal).lower() in resume_text
            )
            scored.append((jd_score * 2 + resume_score, archetype))
        scored.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
        best = scored[0][1]

        thesis = (
            f"Build one {best['name']} that uses {', '.join(matched_resume_signals[:2] or ['existing engineering strengths'])} "
            f"to cover JD gaps such as {', '.join(missing_signals[:2] or ['role-specific stretch areas'])}."
        )
        rationale = (
            f"Selected {best['name']} because the resume already shows {', '.join(matched_resume_signals[:2] or ['relevant foundations'])}, "
            f"while the JD still emphasizes {', '.join(missing_signals[:2] or ['project evidence gaps'])}."
        )
        company_name = manifest.company or "Target"
        project_name = f"{company_name.title()} {best['name']}"
        return ProjectSpec(
            archetype_id=str(best["id"]),
            archetype_name=str(best["name"]),
            project_name=project_name,
            thesis=thesis,
            rationale=rationale,
            matched_resume_signals=matched_resume_signals,
            target_jd_signals=[*[str(item) for item in target_jd.get("responsibilities", [])], *[str(item) for item in target_jd.get("requirements", [])]],
            modules=[str(item) for item in best.get("modules", [])],
            visuals=[str(item) for item in best.get("visuals", [])],
            stretch_areas=missing_signals[:3],
        )

    def _build_visual_story(self) -> VisualStory:
        project_spec = self._load_yaml(self.workspace_path / "stages" / "04-project-design" / "project_spec.yaml")
        modules = [str(item) for item in project_spec.get("modules", [])]
        diagram_title = f"{project_spec.get('project_name', 'Flagship Project')} Architecture"
        diagram_mermaid = self._build_mermaid(modules)
        demo_flow = [
            f"Open with the project thesis: {project_spec.get('thesis', '')}",
            f"Walk through the core request path across {', '.join(modules[:3])}.",
            f"Close with stretch areas such as {', '.join(project_spec.get('stretch_areas', [])[:2])}.",
        ]
        talking_points = [
            str(project_spec.get("rationale", "")),
            f"Why this project is credible from the resume: {', '.join(project_spec.get('matched_resume_signals', [])[:2])}.",
            f"Why it covers the JD: {', '.join(project_spec.get('target_jd_signals', [])[:2])}.",
        ]
        return VisualStory(
            diagram_title=diagram_title,
            diagram_mermaid=diagram_mermaid,
            demo_flow=demo_flow,
            talking_points=talking_points,
        )

    def _build_interview_assets(self) -> InterviewAssets:
        project_spec = self._load_yaml(self.workspace_path / "stages" / "04-project-design" / "project_spec.yaml")
        project_name = str(project_spec.get("project_name", "Flagship Project"))
        modules = [str(item) for item in project_spec.get("modules", [])]
        resume_bullets = [
            f"Designed and scoped `{project_name}` to bridge resume strengths and target JD gaps.",
            f"Structured the flagship project around {', '.join(modules[:3])} to keep the story technically coherent.",
            f"Prepared the project for interview delivery with visuals, demo flow, and stretch areas.",
        ]
        pitch_3min = (
            f"{project_name} is a single flagship project that starts from my existing strengths in "
            f"{', '.join(project_spec.get('matched_resume_signals', [])[:2] or ['engineering'])} and deliberately covers "
            f"{', '.join(project_spec.get('stretch_areas', [])[:2] or ['the target JD gaps'])}."
        )
        pitch_10min_outline = [
            "Business problem and JD fit",
            f"Architecture walk-through: {', '.join(modules[:4])}",
            "Why the project is grounded in prior experience",
            "Stretch areas, risks, and next iteration plan",
        ]
        return InterviewAssets(
            resume_bullets=resume_bullets,
            pitch_3min=pitch_3min,
            pitch_10min_outline=pitch_10min_outline,
        )

    def _build_bundle_manifest(self) -> BundleManifest:
        project_spec = self._load_yaml(self.workspace_path / "stages" / "04-project-design" / "project_spec.yaml")
        visual_story = self._load_yaml(self.workspace_path / "stages" / "05-visual-story" / "visual_story.yaml")
        interview_assets = self._load_yaml(self.workspace_path / "stages" / "06-interview-assets" / "interview_assets.yaml")

        outputs_dir = self.workspace_path / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        bundle_path = outputs_dir / "final_case_bundle.md"
        bundle_path.write_text(
            self._render_final_bundle(project_spec, visual_story, interview_assets),
            encoding="utf-8",
        )

        return BundleManifest(
            output_files=[bundle_path.name],
            included_artifacts=[
                "stages/04-project-design/project_spec.yaml",
                "stages/05-visual-story/visual_story.yaml",
                "stages/06-interview-assets/interview_assets.yaml",
            ],
            summary=f"Rendered final bundle for {project_spec.get('project_name', 'flagship project')}.",
        )

    def _build_evaluation_report(self) -> EvaluationReport:
        rubrics = self._load_yaml(Path("configs/evaluation_rubrics.yaml")).get("rubrics", [])
        project_spec = self._load_yaml(self.workspace_path / "stages" / "04-project-design" / "project_spec.yaml")
        visual_story = self._load_yaml(self.workspace_path / "stages" / "05-visual-story" / "visual_story.yaml")
        interview_assets = self._load_yaml(self.workspace_path / "stages" / "06-interview-assets" / "interview_assets.yaml")
        bundle_manifest = self._load_yaml(self.workspace_path / "stages" / "07-bundle-render" / "bundle_manifest.yaml")

        matched_resume_signals = list(project_spec.get("matched_resume_signals", []))
        stretch_areas = list(project_spec.get("stretch_areas", []))
        jd_signals = list(project_spec.get("target_jd_signals", []))
        has_mermaid = "graph TD" in str(visual_story.get("diagram_mermaid", ""))
        has_demo_flow = bool(visual_story.get("demo_flow"))
        has_pitch = bool(interview_assets.get("pitch_3min")) and bool(interview_assets.get("pitch_10min_outline"))
        has_bundle = bool(bundle_manifest.get("output_files"))

        scores: dict[str, float] = {}
        for rubric in rubrics:
            name = str(rubric.get("name", ""))
            if name == "resume_grounding_score":
                score = min(1.0, 0.4 + 0.2 * len(matched_resume_signals))
            elif name == "jd_coverage_score":
                score = min(1.0, len(jd_signals[:4]) / 4 if jd_signals else 0.0)
            elif name == "project_coherence_score":
                score = 1.0 if project_spec.get("thesis") and len(project_spec.get("modules", [])) >= 3 else 0.5
            elif name == "visual_completeness_score":
                score = 1.0 if has_mermaid and has_demo_flow else 0.4
            elif name == "presentation_readiness_score":
                score = 1.0 if has_pitch else 0.4
            else:
                score = 0.0
            scores[name] = round(score, 2)

        average = sum(scores.values()) / len(scores) if scores else 0.0
        overall_readiness = "ready_for_mock_interview" if average >= 0.8 and has_bundle else "needs_revision"
        summary = (
            f"Bundle average score={average:.2f}; "
            f"resume signals={len(matched_resume_signals)}, stretch areas={len(stretch_areas)}, bundle_files={len(bundle_manifest.get('output_files', []))}."
        )
        return EvaluationReport(
            scores=scores,
            overall_readiness=overall_readiness,
            summary=summary,
        )

    def _signal_matches_resume(self, signal: str, resume_text: str) -> bool:
        keywords = [token for token in self._tokenize(signal) if len(token) >= 2]
        return any(keyword.lower() in resume_text for keyword in keywords)

    def _tokenize(self, value: str) -> list[str]:
        tokens = []
        buffer = []
        for char in value:
            if char.isalnum() or char in {"+", "#"}:
                buffer.append(char)
                continue
            if buffer:
                tokens.append("".join(buffer))
                buffer = []
        if buffer:
            tokens.append("".join(buffer))
        return tokens

    def _stage_dir(self, slug: str) -> Path:
        index = DEFAULT_STAGE_NAMES.index(slug) + 1
        return self.workspace_path / "stages" / f"{index:02d}-{slug}"

    def _write_stage_payload(self, slug: str, filename: str, payload: dict[str, object]) -> Path:
        target = self._stage_dir(slug) / filename
        target.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return target

    def _load_yaml(self, path: Path) -> dict[str, object]:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    def _mark_stage_completed(self, slug: str) -> None:
        manifest_path = self.workspace_path / "manifest.yaml"
        manifest = load_case_manifest(manifest_path)
        for stage in manifest.stages:
            if stage.slug == slug:
                stage.status = "completed"
                break
        save_case_manifest(manifest_path, manifest)

    def _ensure_stage_dependencies(self, dependencies: list[str], slug: str) -> None:
        manifest = load_case_manifest(self.workspace_path / "manifest.yaml")
        statuses = {stage.slug: stage.status for stage in manifest.stages}
        missing = [dependency for dependency in dependencies if statuses.get(dependency) != "completed"]
        if missing:
            raise ValueError(f"{slug} requires completed stages: {', '.join(missing)}")

    def _build_mermaid(self, modules: list[str]) -> str:
        if not modules:
            return "graph TD\n  A[Project] --> B[Delivery]"
        lines = ["graph TD"]
        for index, module in enumerate(modules, start=1):
            lines.append(f"  N{index}[\"{module}\"]")
            if index > 1:
                lines.append(f"  N{index-1} --> N{index}")
        return "\n".join(lines)

    def _render_final_bundle(
        self,
        project_spec: dict[str, object],
        visual_story: dict[str, object],
        interview_assets: dict[str, object],
    ) -> str:
        modules = [str(item) for item in project_spec.get("modules", [])]
        demo_flow = [str(item) for item in visual_story.get("demo_flow", [])]
        resume_bullets = [str(item) for item in interview_assets.get("resume_bullets", [])]
        pitch_outline = [str(item) for item in interview_assets.get("pitch_10min_outline", [])]
        lines = [
            f"# {project_spec.get('project_name', 'Flagship Project')}",
            "",
            "## Thesis",
            "",
            str(project_spec.get("thesis", "")),
            "",
            "## Rationale",
            "",
            str(project_spec.get("rationale", "")),
            "",
            "## Modules",
            "",
            *[f"- {item}" for item in modules],
            "",
            "## Architecture",
            "",
            "```mermaid",
            str(visual_story.get("diagram_mermaid", "")),
            "```",
            "",
            "## Demo Flow",
            "",
            *[f"- {item}" for item in demo_flow],
            "",
            "## Resume Bullets",
            "",
            *[f"- {item}" for item in resume_bullets],
            "",
            "## 3 Minute Pitch",
            "",
            str(interview_assets.get("pitch_3min", "")),
            "",
            "## 10 Minute Pitch Outline",
            "",
            *[f"- {item}" for item in pitch_outline],
            "",
        ]
        return "\n".join(lines)
