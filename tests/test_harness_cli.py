from pathlib import Path

from typer.testing import CliRunner

from jd2offer_harness.cli import app


runner = CliRunner()


def test_harness_cli_shows_init_case_command() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "init-case" in result.stdout


def test_harness_cli_init_case_creates_workspace(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "jd.md"
    outdir = tmp_path / "case"

    resume_path.write_text(
        """# 李四

## 项目经历

- 负责推荐系统与数据服务。

## 技能

- Python
- SQL
""",
        encoding="utf-8",
    )
    jd_path.write_text(
        """# 推荐策略工程师

## 岗位职责

1. 负责推荐策略平台建设。

## 任职要求

1. 熟悉 Python。
""",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "init-case",
            "--resume",
            str(resume_path),
            "--jd",
            str(jd_path),
            "--outdir",
            str(outdir),
            "--company",
            "didi",
            "--role",
            "strategy-engineer",
        ],
    )

    assert result.exit_code == 0
    assert "Initialized harness case" in result.stdout
    assert (outdir / "manifest.yaml").exists()
    assert (outdir / "normalized" / "resume_document.yaml").exists()


def test_harness_cli_run_stage_executes_gap_mapping(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "jd.md"
    outdir = tmp_path / "case"

    resume_path.write_text(
        """# 赵六

## 项目经历

- 做过 Python 服务和评测平台。

## 技能

- Python
- FastAPI
""",
        encoding="utf-8",
    )
    jd_path.write_text(
        """# AI 工程平台

## 岗位职责

1. 负责 Agent 与工具调用平台建设。

## 任职要求

1. 熟悉 Python 和 FastAPI。
""",
        encoding="utf-8",
    )

    init_result = runner.invoke(
        app,
        [
            "init-case",
            "--resume",
            str(resume_path),
            "--jd",
            str(jd_path),
            "--outdir",
            str(outdir),
            "--company",
            "didi",
            "--role",
            "ai-platform",
        ],
    )
    assert init_result.exit_code == 0

    intake_result = runner.invoke(
        app,
        [
            "run-stage",
            "--workspace",
            str(outdir),
            "--stage",
            "intake",
        ],
    )
    assert intake_result.exit_code == 0

    run_result = runner.invoke(
        app,
        [
            "run-stage",
            "--workspace",
            str(outdir),
            "--stage",
            "gap-mapping",
        ],
    )

    assert run_result.exit_code == 0
    assert "Completed stage gap-mapping" in run_result.stdout
    assert (outdir / "stages" / "03-gap-mapping" / "gap_analysis.yaml").exists()


def test_harness_cli_run_stage_executes_project_design(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "jd.md"
    outdir = tmp_path / "case"

    resume_path.write_text(
        """# 钱七

## 项目经历

- 负责 Python + FastAPI 服务和运营工具平台。

## 技能

- Python
- FastAPI
""",
        encoding="utf-8",
    )
    jd_path.write_text(
        """# Agent 平台工程师

## 岗位职责

1. 负责 Agent 与工具调用平台建设。

## 任职要求

1. 熟悉 Python 和 FastAPI。
2. 具备评测和平台抽象能力。
""",
        encoding="utf-8",
    )

    init_result = runner.invoke(
        app,
        [
            "init-case",
            "--resume",
            str(resume_path),
            "--jd",
            str(jd_path),
            "--outdir",
            str(outdir),
            "--company",
            "didi",
            "--role",
            "agent-platform",
        ],
    )
    assert init_result.exit_code == 0

    intake_result = runner.invoke(
        app,
        ["run-stage", "--workspace", str(outdir), "--stage", "intake"],
    )
    assert intake_result.exit_code == 0

    gap_result = runner.invoke(
        app,
        [
            "run-stage",
            "--workspace",
            str(outdir),
            "--stage",
            "gap-mapping",
        ],
    )
    assert gap_result.exit_code == 0

    design_result = runner.invoke(
        app,
        [
            "run-stage",
            "--workspace",
            str(outdir),
            "--stage",
            "project-design",
        ],
    )

    assert design_result.exit_code == 0
    assert "Completed stage project-design" in design_result.stdout
    assert (outdir / "stages" / "04-project-design" / "project_spec.yaml").exists()


def test_harness_cli_run_stage_executes_visual_story(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "jd.md"
    outdir = tmp_path / "case"

    resume_path.write_text(
        """# 孙八

## 项目经历

- 做过 Python 平台服务、评测和运营提效工具。

## 技能

- Python
- FastAPI
""",
        encoding="utf-8",
    )
    jd_path.write_text(
        """# Agent 平台工程师

## 岗位职责

1. 负责 Agent 平台和工具调用建设。

## 任职要求

1. 熟悉 Python 和 FastAPI。
2. 具备可视化表达能力。
""",
        encoding="utf-8",
    )

    assert runner.invoke(
        app,
        [
            "init-case",
            "--resume",
            str(resume_path),
            "--jd",
            str(jd_path),
            "--outdir",
            str(outdir),
            "--company",
            "didi",
            "--role",
            "agent-platform",
        ],
    ).exit_code == 0
    assert runner.invoke(
        app,
        ["run-stage", "--workspace", str(outdir), "--stage", "intake"],
    ).exit_code == 0
    assert runner.invoke(
        app,
        ["run-stage", "--workspace", str(outdir), "--stage", "gap-mapping"],
    ).exit_code == 0
    assert runner.invoke(
        app,
        ["run-stage", "--workspace", str(outdir), "--stage", "project-design"],
    ).exit_code == 0

    story_result = runner.invoke(
        app,
        ["run-stage", "--workspace", str(outdir), "--stage", "visual-story"],
    )

    assert story_result.exit_code == 0
    assert "Completed stage visual-story" in story_result.stdout
    assert (outdir / "stages" / "05-visual-story" / "visual_story.yaml").exists()


def test_harness_cli_run_stage_executes_evaluation(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.md"
    jd_path = tmp_path / "jd.md"
    outdir = tmp_path / "case"

    resume_path.write_text(
        """# 周九

## 项目经历

- 做过 Python 服务、平台工具和评测系统。

## 技能

- Python
- FastAPI
""",
        encoding="utf-8",
    )
    jd_path.write_text(
        """# Agent 平台工程师

## 岗位职责

1. 负责 Agent 平台和工具调用建设。

## 任职要求

1. 熟悉 Python 和 FastAPI。
2. 具备评测和可视化表达能力。
""",
        encoding="utf-8",
    )

    assert runner.invoke(
        app,
        [
            "init-case",
            "--resume",
            str(resume_path),
            "--jd",
            str(jd_path),
            "--outdir",
            str(outdir),
            "--company",
            "didi",
            "--role",
            "agent-platform",
        ],
    ).exit_code == 0
    for stage in ["intake", "gap-mapping", "project-design", "visual-story", "interview-assets", "bundle-render"]:
        assert runner.invoke(
            app,
            ["run-stage", "--workspace", str(outdir), "--stage", stage],
        ).exit_code == 0

    eval_result = runner.invoke(
        app,
        ["run-stage", "--workspace", str(outdir), "--stage", "evaluation"],
    )

    assert eval_result.exit_code == 0
    assert "Completed stage evaluation" in eval_result.stdout
    assert (outdir / "stages" / "08-evaluation" / "evaluation_report.yaml").exists()
