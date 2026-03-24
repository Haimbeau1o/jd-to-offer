from pathlib import Path

import yaml

from jd2offer_harness.harness.artifacts import initialize_case_workspace, load_case_manifest
from jd2offer_harness.harness.runner import HarnessRunner


def _write_resume(path: Path) -> None:
    path.write_text(
        """# 王五

## 个人简介

- 做过推荐策略、运营提效和 AI 工具工程化。

## 项目经历

- 负责 Python + FastAPI 服务，支持运营分析助手。
- 负责数据服务接口和评测脚本建设。

## 技能

- Python
- FastAPI
- SQL
""",
        encoding="utf-8",
    )


def _write_jd(path: Path) -> None:
    path.write_text(
        """# AI 平台工程师

## 岗位职责

1. 负责 Agent 系统设计与工具调用链路建设。
2. 负责平台评测体系和服务化落地。

## 任职要求

1. 熟悉 Python 与 FastAPI 等服务开发能力。
2. 具备评测、工程化和平台抽象经验。
3. 有 Agent 或工具调用项目经验优先。
""",
        encoding="utf-8",
    )


def _create_workspace(tmp_path: Path) -> Path:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "jd.md"
    outdir = tmp_path / "case"
    _write_resume(resume_path)
    _write_jd(jd_path)
    initialize_case_workspace(
        resume_path=resume_path,
        jd_path=jd_path,
        outdir=outdir,
        company="didi",
        role="ai-platform-engineer",
    )
    return outdir


def test_runner_intake_stage_writes_resume_evidence(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    result = runner.run_stage("intake")

    evidence_path = workspace / "stages" / "01-intake" / "resume_evidence.yaml"
    assert result.slug == "intake"
    assert result.status == "completed"
    assert evidence_path.exists()

    payload = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
    assert payload["candidate_name"] == "王五"
    assert "Python" in payload["skills"]
    assert any("FastAPI" in item for item in payload["experience_highlights"])


def test_runner_gap_mapping_stage_writes_gap_analysis(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    result = runner.run_stage("gap-mapping")

    analysis_path = workspace / "stages" / "03-gap-mapping" / "gap_analysis.yaml"
    assert result.slug == "gap-mapping"
    assert result.status == "completed"
    assert analysis_path.exists()

    payload = yaml.safe_load(analysis_path.read_text(encoding="utf-8"))
    assert "Python" in payload["matched_signals"]
    assert any("FastAPI" in item for item in payload["matched_signals"])
    assert any("Agent" in item for item in payload["missing_signals"])
    assert payload["coverage_summary"]


def test_runner_updates_manifest_stage_status_after_execution(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")

    manifest = load_case_manifest(workspace / "manifest.yaml")
    intake_stage = next(stage for stage in manifest.stages if stage.slug == "intake")
    assert intake_stage.status == "completed"


def test_runner_project_design_requires_gap_mapping_first(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)

    try:
        runner.run_stage("project-design")
    except ValueError as exc:
        assert "gap-mapping" in str(exc)
    else:
        raise AssertionError("expected project-design to require gap-mapping first")


def test_runner_project_design_writes_project_spec(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    result = runner.run_stage("project-design")

    spec_path = workspace / "stages" / "04-project-design" / "project_spec.yaml"
    assert result.slug == "project-design"
    assert result.status == "completed"
    assert spec_path.exists()

    payload = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    assert payload["archetype_id"] == "vertical_agent_system"
    assert payload["project_name"]
    assert payload["rationale"]
    assert "Intent Router" in payload["modules"]
    assert "architecture_diagram" in payload["visuals"]
    assert any("Agent" in item for item in payload["stretch_areas"])


def test_runner_visual_story_requires_project_design_first(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")

    try:
        runner.run_stage("visual-story")
    except ValueError as exc:
        assert "project-design" in str(exc)
    else:
        raise AssertionError("expected visual-story to require project-design first")


def test_runner_visual_story_writes_mermaid_and_talking_points(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    runner.run_stage("project-design")
    result = runner.run_stage("visual-story")

    story_path = workspace / "stages" / "05-visual-story" / "visual_story.yaml"
    assert result.slug == "visual-story"
    assert result.status == "completed"
    assert story_path.exists()

    payload = yaml.safe_load(story_path.read_text(encoding="utf-8"))
    assert payload["diagram_title"]
    assert "graph TD" in payload["diagram_mermaid"]
    assert payload["demo_flow"]
    assert payload["talking_points"]


def test_runner_interview_assets_writes_presentation_script(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    runner.run_stage("project-design")
    result = runner.run_stage("interview-assets")

    assets_path = workspace / "stages" / "06-interview-assets" / "interview_assets.yaml"
    assert result.slug == "interview-assets"
    assert result.status == "completed"
    assert assets_path.exists()

    payload = yaml.safe_load(assets_path.read_text(encoding="utf-8"))
    assert payload["resume_bullets"]
    assert payload["pitch_3min"]
    assert payload["pitch_10min_outline"]


def test_runner_bundle_render_requires_visual_story_and_interview_assets(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    runner.run_stage("project-design")

    try:
        runner.run_stage("bundle-render")
    except ValueError as exc:
        assert "visual-story" in str(exc)
    else:
        raise AssertionError("expected bundle-render to require visual-story and interview-assets first")


def test_runner_bundle_render_writes_final_bundle_outputs(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    runner.run_stage("project-design")
    runner.run_stage("visual-story")
    runner.run_stage("interview-assets")
    result = runner.run_stage("bundle-render")

    manifest_path = workspace / "stages" / "07-bundle-render" / "bundle_manifest.yaml"
    bundle_path = workspace / "outputs" / "final_case_bundle.md"
    assert result.slug == "bundle-render"
    assert result.status == "completed"
    assert manifest_path.exists()
    assert bundle_path.exists()

    manifest_payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    bundle_text = bundle_path.read_text(encoding="utf-8")
    assert manifest_payload["output_files"]
    assert "final_case_bundle.md" in manifest_payload["output_files"]
    assert "# " in bundle_text
    assert "```mermaid" in bundle_text
    assert "3 Minute Pitch" in bundle_text


def test_runner_evaluation_requires_bundle_render_first(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    runner.run_stage("project-design")
    runner.run_stage("visual-story")
    runner.run_stage("interview-assets")

    try:
        runner.run_stage("evaluation")
    except ValueError as exc:
        assert "bundle-render" in str(exc)
    else:
        raise AssertionError("expected evaluation to require bundle-render first")


def test_runner_evaluation_writes_score_report(tmp_path: Path) -> None:
    workspace = _create_workspace(tmp_path)

    runner = HarnessRunner(workspace)
    runner.run_stage("intake")
    runner.run_stage("gap-mapping")
    runner.run_stage("project-design")
    runner.run_stage("visual-story")
    runner.run_stage("interview-assets")
    runner.run_stage("bundle-render")
    result = runner.run_stage("evaluation")

    report_path = workspace / "stages" / "08-evaluation" / "evaluation_report.yaml"
    assert result.slug == "evaluation"
    assert result.status == "completed"
    assert report_path.exists()

    payload = yaml.safe_load(report_path.read_text(encoding="utf-8"))
    assert payload["scores"]["resume_grounding_score"] >= 0
    assert payload["scores"]["visual_completeness_score"] >= 0
    assert payload["overall_readiness"]
    assert payload["summary"]
