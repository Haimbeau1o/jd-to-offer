# JD2Offer TrustOps Expansion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend `jd2offer` so it can accurately analyze backend-platform JDs, generate role-specific case bundles for content quality and ecommerce security, and recommend a shared `TrustOps Platform` flagship project instead of falling back to the current agent-only templates.

**Architecture:** Keep the current deterministic pipeline shape: parse JD markdown, map it to a taxonomy, select resources, select a project template, then render a case bundle. Expand the taxonomy and templates for backend-platform roles, then refactor the renderer so project blueprint and interview copy come from template-specific domain metadata instead of hardcoded ride-hailing text.

**Tech Stack:** Python 3.12, Typer, Pydantic, PyYAML, pytest, Markdown case bundles, YAML config-driven taxonomy/templates/resources.

### Task 1: Add fixture JDs for the two ByteDance role families

**Files:**
- Create: `examples/bytedance_2026_content_quality_ai_tool_jd.md`
- Create: `examples/bytedance_2026_ecom_security_backend_jd.md`
- Modify: `tests/test_parser.py`

**Step 1: Write the failing test**

Add parser coverage for the new fixture files:

```python
from pathlib import Path

from jd_offer.parser import parse_jd_markdown


def test_parse_content_quality_jd_sections() -> None:
    jd = parse_jd_markdown(Path("examples/bytedance_2026_content_quality_ai_tool_jd.md"))
    assert "AI工具开发工程师" in jd.title
    assert len(jd.responsibilities) == 3
    assert len(jd.requirements) >= 5


def test_parse_ecom_security_jd_sections() -> None:
    jd = parse_jd_markdown(Path("examples/bytedance_2026_ecom_security_backend_jd.md"))
    assert "电商安全" in jd.title
    assert len(jd.responsibilities) == 3
    assert len(jd.requirements) >= 5
```

**Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src pytest tests/test_parser.py -v
```

Expected: FAIL because the fixture files do not exist yet.

**Step 3: Write minimal implementation**

Create exact markdown fixtures mirroring the user-provided JDs with sections:
- `# 标题`
- `## 岗位职责`
- `## 任职要求`
- `## 加分项` only when present

**Step 4: Run test to verify it passes**

Run:

```bash
PYTHONPATH=src pytest tests/test_parser.py -v
```

Expected: PASS for the new parser fixture tests.

**Step 5: Commit**

```bash
git add examples/bytedance_2026_content_quality_ai_tool_jd.md examples/bytedance_2026_ecom_security_backend_jd.md tests/test_parser.py
git commit -m "test: add backend jd parser fixtures"
```

### Task 2: Extend the competency taxonomy for backend-platform roles

**Files:**
- Modify: `configs/competency_taxonomy.yaml`
- Modify: `tests/test_taxonomy.py`

**Step 1: Write the failing test**

Add explicit taxonomy expectations for both new JDs:

```python
def test_map_content_quality_jd_to_backend_platform_competencies() -> None:
    jd = parse_jd_markdown(Path("examples/bytedance_2026_content_quality_ai_tool_jd.md"))
    result = map_jd_to_competencies(jd, TAXONOMY_PATH)
    tags = {item.name for item in result.items}
    assert "backend_service_engineering" in tags
    assert "data_infra_and_middleware" in tags
    assert "service_reliability_security" in tags
    assert "llm_application_engineering" in tags


def test_map_ecom_security_jd_to_backend_platform_competencies() -> None:
    jd = parse_jd_markdown(Path("examples/bytedance_2026_ecom_security_backend_jd.md"))
    result = map_jd_to_competencies(jd, TAXONOMY_PATH)
    tags = {item.name for item in result.items}
    assert "backend_service_engineering" in tags
    assert "business_abstraction_and_architecture" in tags
    assert "trust_safety_domain" in tags
```

**Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src pytest tests/test_taxonomy.py -v
```

Expected: FAIL because those competency names do not exist yet.

**Step 3: Write minimal implementation**

Add these taxonomy entries with JD-focused keywords, subtopics, project signals, and interview signals:
- `backend_service_engineering`
- `data_infra_and_middleware`
- `service_reliability_security`
- `business_abstraction_and_architecture`
- `llm_application_engineering`
- `trust_safety_domain`

Use trigger keywords from the two JDs only. Good examples:
- backend / 后端开发 / 高质量代码 / Golang / Go / Java / FastAPI / Gin / Hertz
- Redis / MySQL / 消息队列 / 数据服务 / Linux
- 高可靠 / 高安全 / 高性能 / 稳定性 / 性能
- 抽象 / 拆分 / 架构设计 / 模块化 / 通用服务模块
- 大模型 / LLM / AI Coding / 工具线上化 / 工程化应用
- 内容质量 / 风险发现 / 电商安全 / 商家 / 运营产品 / 安全业务

**Step 4: Run test to verify it passes**

Run:

```bash
PYTHONPATH=src pytest tests/test_taxonomy.py -v
```

Expected: PASS with both new JDs mapping to meaningful backend competencies.

**Step 5: Commit**

```bash
git add configs/competency_taxonomy.yaml tests/test_taxonomy.py
git commit -m "feat: add backend platform competency taxonomy"
```

### Task 3: Add primary resources for backend-platform competencies

**Files:**
- Modify: `configs/resource_registry.yaml`
- Modify: `tests/test_research.py`

**Step 1: Write the failing test**

Add resource selection tests:

```python
def test_select_resources_for_content_quality_backend_jd() -> None:
    jd = parse_jd_markdown(Path("examples/bytedance_2026_content_quality_ai_tool_jd.md"))
    competencies = map_jd_to_competencies(jd, TAXONOMY)
    selected = select_resources(competencies, BASE_RESOURCES)
    titles = {item.title for item in selected}
    assert "Hertz" in "".join(titles) or "FastAPI" in "".join(titles)
    assert "Redis" in "".join(titles)


def test_select_resources_for_ecom_security_backend_jd() -> None:
    jd = parse_jd_markdown(Path("examples/bytedance_2026_ecom_security_backend_jd.md"))
    competencies = map_jd_to_competencies(jd, TAXONOMY)
    selected = select_resources(competencies, BASE_RESOURCES)
    titles = {item.title for item in selected}
    assert "RabbitMQ" in "".join(titles) or "MySQL" in "".join(titles)
```

**Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src pytest tests/test_research.py -v
```

Expected: FAIL because no backend-platform resources are tagged for the new competencies.

**Step 3: Write minimal implementation**

Add official / primary resources for:
- Hertz docs
- FastAPI docs
- Redis docs
- MySQL docs
- RabbitMQ docs
- Go docs
- one trust-and-safety or abuse-detection primary source

Tag them with the new competencies, not with the old ride-hailing or RL-only tags.

**Step 4: Run test to verify it passes**

Run:

```bash
PYTHONPATH=src pytest tests/test_research.py -v
```

Expected: PASS with sensible backend resources selected for the new roles.

**Step 5: Commit**

```bash
git add configs/resource_registry.yaml tests/test_research.py
git commit -m "feat: add backend platform resource registry entries"
```

### Task 4: Add two new project templates for the domain shells

**Files:**
- Modify: `configs/project_templates.yaml`
- Modify: `tests/test_generate.py`

**Step 1: Write the failing test**

Add generation assertions that require new template IDs:

```python
def test_generate_content_quality_case_uses_content_quality_template(tmp_path: Path) -> None:
    outdir = tmp_path / "content-quality-case"
    result = runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/bytedance_2026_content_quality_ai_tool_jd.md",
            "--company",
            "bytedance",
            "--role",
            "content-quality-ai-tool",
            "--outdir",
            str(outdir),
        ],
    )
    assert result.exit_code == 0
    assert "content_quality_ai_platform" in (outdir / "manifest.yaml").read_text(encoding="utf-8")


def test_generate_ecom_security_case_uses_security_template(tmp_path: Path) -> None:
    outdir = tmp_path / "ecom-security-case"
    result = runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/bytedance_2026_ecom_security_backend_jd.md",
            "--company",
            "bytedance",
            "--role",
            "ecom-security-backend",
            "--outdir",
            str(outdir),
        ],
    )
    assert result.exit_code == 0
    assert "ecommerce_riskops_platform" in (outdir / "manifest.yaml").read_text(encoding="utf-8")
```

**Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src pytest tests/test_generate.py -v
```

Expected: FAIL because those templates do not exist.

**Step 3: Write minimal implementation**

Add two new templates:
- `content_quality_ai_platform`
- `ecommerce_riskops_platform`

Both should share the same architectural backbone:
- Go API layer
- rule evaluation
- case workflow
- data service APIs
- MQ worker
- Python AI copilot

But the demo scenarios and business framing must differ:
- content quality / moderation / data services
- ecommerce security / merchant risk / operations workflow

**Step 4: Run test to verify it passes**

Run:

```bash
PYTHONPATH=src pytest tests/test_generate.py -v
```

Expected: PASS with each JD selecting its own template.

**Step 5: Commit**

```bash
git add configs/project_templates.yaml tests/test_generate.py
git commit -m "feat: add trustops project templates"
```

### Task 5: Remove ride-hailing hardcodes from rendered bundle content

**Files:**
- Modify: `src/jd_offer/schemas.py`
- Modify: `src/jd_offer/project_templates.py`
- Modify: `tests/test_generate.py`

**Step 1: Write the failing test**

Add content assertions for the new outputs:

```python
def test_content_quality_case_mentions_quality_domain_not_driver_ops(tmp_path: Path) -> None:
    outdir = tmp_path / "content-quality-case"
    runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/bytedance_2026_content_quality_ai_tool_jd.md",
            "--company",
            "bytedance",
            "--role",
            "content-quality-ai-tool",
            "--outdir",
            str(outdir),
        ],
    )
    blueprint = (outdir / "04_project_blueprint.md").read_text(encoding="utf-8")
    interview = (outdir / "05_interview_assets.md").read_text(encoding="utf-8")
    assert "司机经营" not in blueprint
    assert "司机经营" not in interview
    assert "内容质量" in blueprint


def test_security_case_mentions_security_domain_not_driver_ops(tmp_path: Path) -> None:
    outdir = tmp_path / "security-case"
    runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/bytedance_2026_ecom_security_backend_jd.md",
            "--company",
            "bytedance",
            "--role",
            "ecom-security-backend",
            "--outdir",
            str(outdir),
        ],
    )
    blueprint = (outdir / "04_project_blueprint.md").read_text(encoding="utf-8")
    assert "司机经营" not in blueprint
    assert "电商安全" in blueprint
```

**Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src pytest tests/test_generate.py -v
```

Expected: FAIL because the current renderer still writes ride-hailing-specific copy.

**Step 3: Write minimal implementation**

Refactor the template schema so each template can provide domain-aware narrative fields. Add fields such as:

```python
class ProjectTemplate(BaseModel):
    id: str
    name: str
    summary: str
    use_when: list[str] = Field(default_factory=list)
    tech_stack: list[str] = Field(default_factory=list)
    modules: list[str] = Field(default_factory=list)
    milestones: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    demo_scenarios: list[str] = Field(default_factory=list)
    business_problems: list[str] = Field(default_factory=list)
    resume_bullets: list[str] = Field(default_factory=list)
    storyline: list[str] = Field(default_factory=list)
    self_intro: list[str] = Field(default_factory=list)
```

Then update the rendering helpers to use those fields instead of hardcoded driver-specific copy.

**Step 4: Run test to verify it passes**

Run:

```bash
PYTHONPATH=src pytest tests/test_generate.py -v
```

Expected: PASS with domain-appropriate blueprint and interview copy.

**Step 5: Commit**

```bash
git add src/jd_offer/schemas.py src/jd_offer/project_templates.py tests/test_generate.py
git commit -m "refactor: make case rendering template-aware"
```

### Task 6: Guard against empty competency matches

**Files:**
- Modify: `src/jd_offer/project_templates.py`
- Modify: `tests/test_generate.py`

**Step 1: Write the failing test**

Add a regression test:

```python
def test_generate_does_not_silently_fallback_when_no_template_matches(tmp_path: Path) -> None:
    outdir = tmp_path / "bad-case"
    result = runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/bytedance_2026_ecom_security_backend_jd.md",
            "--company",
            "bytedance",
            "--role",
            "ecom-security-backend",
            "--outdir",
            str(outdir),
            "--taxonomy",
            "tests/fixtures/empty_taxonomy.yaml",
        ],
    )
    assert result.exit_code != 0
    assert "No matching competencies" in result.stdout or "No compatible project template" in result.stdout
```

**Step 2: Run test to verify it fails**

Run:

```bash
PYTHONPATH=src pytest tests/test_generate.py -v
```

Expected: FAIL because selection currently falls back silently.

**Step 3: Write minimal implementation**

Update selection logic:
- if `competencies.items` is empty, raise a clear `ValueError`
- if best template overlap is `0`, raise a clear `ValueError`

Suggested implementation:

```python
def select_project_template(competencies: CompetencyMap, path: Path) -> ProjectTemplate:
    if not competencies.items:
        raise ValueError("No matching competencies found for this JD. Extend the taxonomy first.")
    templates = load_project_templates(path)
    ranked: list[tuple[int, ProjectTemplate]] = []
    top_names = set(competencies.top_names)
    for template in templates:
        ranked.append((len(top_names.intersection(template.use_when)), template))
    ranked.sort(key=lambda item: (-item[0], item[1].id))
    best_score, best_template = ranked[0]
    if best_score == 0:
        raise ValueError("No compatible project template found for mapped competencies.")
    return best_template
```

**Step 4: Run test to verify it passes**

Run:

```bash
PYTHONPATH=src pytest tests/test_generate.py -v
```

Expected: PASS with an explicit failure instead of a misleading fallback.

**Step 5: Commit**

```bash
git add src/jd_offer/project_templates.py tests/test_generate.py
git commit -m "fix: reject empty competency template fallback"
```

### Task 7: Generate committed example cases for both JDs

**Files:**
- Create: `cases/bytedance-content-quality-2026/01_jd_decomposition.md`
- Create: `cases/bytedance-content-quality-2026/02_knowledge_system.md`
- Create: `cases/bytedance-content-quality-2026/03_resource_pack.md`
- Create: `cases/bytedance-content-quality-2026/04_project_blueprint.md`
- Create: `cases/bytedance-content-quality-2026/05_interview_assets.md`
- Create: `cases/bytedance-content-quality-2026/manifest.yaml`
- Create: `cases/bytedance-ecom-security-2026/01_jd_decomposition.md`
- Create: `cases/bytedance-ecom-security-2026/02_knowledge_system.md`
- Create: `cases/bytedance-ecom-security-2026/03_resource_pack.md`
- Create: `cases/bytedance-ecom-security-2026/04_project_blueprint.md`
- Create: `cases/bytedance-ecom-security-2026/05_interview_assets.md`
- Create: `cases/bytedance-ecom-security-2026/manifest.yaml`

**Step 1: Write the validation command**

Run:

```bash
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/bytedance_2026_content_quality_ai_tool_jd.md \
  --company bytedance \
  --role content-quality-ai-tool \
  --outdir cases/bytedance-content-quality-2026
```

Run:

```bash
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/bytedance_2026_ecom_security_backend_jd.md \
  --company bytedance \
  --role ecom-security-backend \
  --outdir cases/bytedance-ecom-security-2026
```

**Step 2: Validate the generated output**

Run:

```bash
python skills/jd-to-offer/scripts/validate_case.py cases/bytedance-content-quality-2026
python skills/jd-to-offer/scripts/validate_case.py cases/bytedance-ecom-security-2026
```

Expected: both directories contain the required six files.

**Step 3: Commit**

```bash
git add cases/bytedance-content-quality-2026 cases/bytedance-ecom-security-2026
git commit -m "docs: add trustops-aligned jd case bundles"
```

### Task 8: Document the new supported role family in the README

**Files:**
- Modify: `README.md`

**Step 1: Write the failing expectation**

Manually verify the README is missing these concepts:
- backend-platform roles
- content-quality example
- ecommerce-security example
- TrustOps Platform positioning

**Step 2: Write minimal implementation**

Update these sections:
- overview
- current capabilities
- quick start
- directory explanation

Add a short note that the repository now supports:
- agent / post-training cases
- backend-platform trust-and-safety cases

**Step 3: Verify**

Run:

```bash
rg -n "TrustOps|content quality|ecommerce security|backend-platform" README.md
```

Expected: the new terminology is present.

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: describe trustops backend-platform support"
```

### Task 9: Final verification

**Files:**
- Verify only

**Step 1: Run focused tests**

```bash
PYTHONPATH=src pytest tests/test_parser.py tests/test_taxonomy.py tests/test_research.py tests/test_generate.py tests/test_cli.py -v
```

Expected: PASS

**Step 2: Run full test suite**

```bash
PYTHONPATH=src pytest -v
```

Expected: PASS

**Step 3: Re-generate the old didi case to catch regressions**

```bash
PYTHONPATH=src python -m jd_offer.cli generate \
  --input examples/didi_2026_agent_jd.md \
  --company didi \
  --role agent-algorithm \
  --resource-overrides examples/didi_2026_verified_resources.yaml \
  --outdir /tmp/didi-agent-regression
```

Expected: PASS, with the original agent-aligned content still rendering correctly.

**Step 4: Commit**

```bash
git add -A
git commit -m "test: verify trustops jd expansion end to end"
```
