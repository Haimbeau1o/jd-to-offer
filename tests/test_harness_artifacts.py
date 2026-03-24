from pathlib import Path

import yaml

from jd2offer_harness.harness.artifacts import (
    DEFAULT_STAGE_NAMES,
    initialize_case_workspace,
    load_case_manifest,
)


def _write_resume(path: Path) -> None:
    path.write_text(
        """# 张三

## 个人简介

- 负责过 AI 平台和后端服务开发。

## 项目经历

- 做过一个面向运营的智能分析助手。

## 技能

- Python
- FastAPI
""",
        encoding="utf-8",
    )


def _write_jd(path: Path) -> None:
    path.write_text(
        """# AI 平台工程师

## 岗位职责

1. 负责 Agent 系统设计与工具调用链路建设。
2. 负责把业务需求抽象成可复用的平台能力。

## 任职要求

1. 熟悉 Python 与服务化开发。
2. 具备评测与工程化落地能力。

## 加分项

1. 有可视化演示项目经验。
""",
        encoding="utf-8",
    )


def test_initialize_case_workspace_creates_layout_and_manifest(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "target_jd.md"
    outdir = tmp_path / "cases" / "ai-platform"
    _write_resume(resume_path)
    _write_jd(jd_path)

    workspace = initialize_case_workspace(
        resume_path=resume_path,
        jd_path=jd_path,
        outdir=outdir,
        company="acme",
        role="ai-platform-engineer",
    )

    assert workspace.root == outdir
    assert (outdir / "raw" / "resume.md").exists()
    assert (outdir / "raw" / "jd.md").exists()
    assert (outdir / "normalized" / "resume_document.yaml").exists()
    assert (outdir / "normalized" / "target_jd.yaml").exists()
    assert (outdir / "outputs").exists()

    for stage_name in DEFAULT_STAGE_NAMES:
        assert any(path.name.endswith(stage_name) for path in (outdir / "stages").iterdir())

    manifest = load_case_manifest(outdir / "manifest.yaml")
    assert manifest.company == "acme"
    assert manifest.role == "ai-platform-engineer"
    assert manifest.source_resume == str(resume_path)
    assert manifest.source_jd == str(jd_path)
    assert [stage.slug for stage in manifest.stages] == DEFAULT_STAGE_NAMES
    assert all(stage.status == "pending" for stage in manifest.stages)

    resume_doc = yaml.safe_load((outdir / "normalized" / "resume_document.yaml").read_text(encoding="utf-8"))
    target_jd = yaml.safe_load((outdir / "normalized" / "target_jd.yaml").read_text(encoding="utf-8"))
    assert resume_doc["name"] == "张三"
    assert "Python" in resume_doc["skills"]
    assert target_jd["title"] == "AI 平台工程师"
    assert len(target_jd["responsibilities"]) == 2

