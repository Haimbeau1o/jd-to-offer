# JD-to-Offer Skill System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Build a reusable skill plus local scripts that transform any target JD into a structured competency map, a web-verified knowledge tree, a flagship project blueprint, and interview-ready output files.

**Architecture:** Use a hybrid workflow. The skill handles high-judgment work such as JD interpretation, web research, resource curation, and project design. Local scripts handle deterministic work such as parsing the JD, mapping keywords to a competency taxonomy, scaffolding case folders, validating output schemas, and rendering markdown deliverables.

**Tech Stack:** Python 3.11, `typer`, `pydantic`, `pyyaml`, `jinja2`, `pytest`, Markdown templates, Codex Skill folder structure.

## Product Scope

The first version should accept a JD markdown file and output:

1. `01_jd_decomposition.md` — responsibilities, requirements, hidden expectations, competency weights
2. `02_knowledge_system.md` — fine-grained foundational knowledge tree with study order
3. `03_resource_pack.md` — latest high-quality resources, prioritizing official docs and primary papers
4. `04_project_blueprint.md` — one flagship project aligned to the JD, with architecture, milestones, and evaluation
5. `05_interview_assets.md` — resume bullets, project talking points, and likely interview questions

## Repo Layout To Build

```text
pyproject.toml
README.md
src/jd_offer/
  __init__.py
  cli.py
  parser.py
  taxonomy.py
  project_templates.py
  renderer.py
  schemas.py
  validators.py
skills/jd-to-offer/
  SKILL.md
  agents/openai.yaml
  scripts/
    run_case.py
    validate_case.py
  references/
    workflow.md
    output_contract.md
configs/
  competency_taxonomy.yaml
  resource_registry.yaml
  project_templates.yaml
examples/
  didi_2026_agent_jd.md
cases/
  .gitkeep
tests/
  test_cli.py
  test_parser.py
  test_taxonomy.py
  test_renderer.py
docs/examples/
  2026-03-09-didi-agent-jd-blueprint.md
docs/plans/
  2026-03-09-jd-to-offer-system.md
```

### Task 1: Bootstrap the Python package and CLI entry

**Files:**
- Create: `pyproject.toml`
- Create: `src/jd_offer/__init__.py`
- Create: `src/jd_offer/cli.py`
- Create: `tests/test_cli.py`

**Step 1: Write the failing test**

Create `tests/test_cli.py` with a minimal CLI smoke test:

```python
from typer.testing import CliRunner

from jd_offer.cli import app


def test_cli_shows_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "generate" in result.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli.py -v`

Expected: import or module failure because the package does not exist yet.

**Step 3: Write minimal implementation**

Create a Typer app with a `generate` command stub that accepts:

- `--input`
- `--company`
- `--role`
- `--outdir`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add pyproject.toml src/jd_offer/__init__.py src/jd_offer/cli.py tests/test_cli.py
git commit -m "feat: bootstrap jd-to-offer cli"
```

### Task 2: Implement JD parsing and normalized schema

**Files:**
- Create: `src/jd_offer/schemas.py`
- Create: `src/jd_offer/parser.py`
- Create: `tests/test_parser.py`
- Use fixture: `examples/didi_2026_agent_jd.md`

**Step 1: Write the failing test**

Create `tests/test_parser.py`:

```python
from pathlib import Path

from jd_offer.parser import parse_jd_markdown


def test_parse_jd_sections():
    result = parse_jd_markdown(Path("examples/didi_2026_agent_jd.md"))
    assert result.title == "滴滴26届春招-算法工程师（供需策略）"
    assert len(result.responsibilities) >= 5
    assert len(result.requirements) >= 6
    assert len(result.bonus_items) >= 3
```
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_parser.py -v`

Expected: parser not implemented.

**Step 3: Write minimal implementation**

Use a markdown parser or line-based parser that supports the current JD shape. Normalize into a Pydantic model with fields:

- `title`
- `responsibilities`
- `requirements`
- `bonus_items`
- `raw_text`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_parser.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/jd_offer/schemas.py src/jd_offer/parser.py tests/test_parser.py examples/didi_2026_agent_jd.md
git commit -m "feat: parse jd markdown into normalized schema"
```

### Task 3: Build a competency taxonomy and JD mapper

**Files:**
- Create: `configs/competency_taxonomy.yaml`
- Create: `src/jd_offer/taxonomy.py`
- Create: `tests/test_taxonomy.py`

**Step 1: Write the failing test**

Create `tests/test_taxonomy.py`:

```python
from pathlib import Path

from jd_offer.parser import parse_jd_markdown
from jd_offer.taxonomy import map_jd_to_competencies


def test_map_jd_to_competencies():
    jd = parse_jd_markdown(Path("examples/didi_2026_agent_jd.md"))
    result = map_jd_to_competencies(jd, Path("configs/competency_taxonomy.yaml"))
    tags = {item.name for item in result.items}
    assert "agent_system_design" in tags
    assert "post_training_alignment" in tags
    assert "rl_and_reward_design" in tags
    assert "ride_hailing_supply_demand" in tags
```
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_taxonomy.py -v`

Expected: taxonomy or mapping function missing.

**Step 3: Write minimal implementation**

Define a taxonomy YAML with:

- competency id
- display name
- trigger keywords
- foundational subtopics
- project signals
- interview signals

Implement a mapper that scores competencies using keyword hits plus section weighting.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_taxonomy.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add configs/competency_taxonomy.yaml src/jd_offer/taxonomy.py tests/test_taxonomy.py
git commit -m "feat: map jd content to reusable competency taxonomy"
```

### Task 4: Render case outputs from structured inputs

**Files:**
- Create: `src/jd_offer/project_templates.py`
- Create: `src/jd_offer/renderer.py`
- Create: `src/jd_offer/validators.py`
- Create: `tests/test_renderer.py`

**Step 1: Write the failing test**

Create `tests/test_renderer.py`:

```python
from pathlib import Path

from jd_offer.renderer import render_case_bundle


def test_render_case_bundle(tmp_path):
    outdir = tmp_path / "case"
    render_case_bundle(
        case_slug="didi-agent-2026",
        outdir=outdir,
        payload={
            "jd_decomposition": "x",
            "knowledge_system": "y",
            "resource_pack": "z",
            "project_blueprint": "a",
            "interview_assets": "b",
        },
    )
    assert (outdir / "01_jd_decomposition.md").exists()
    assert (outdir / "05_interview_assets.md").exists()
```
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_renderer.py -v`

Expected: renderer not implemented.

**Step 3: Write minimal implementation**

Render the five required markdown files and a `manifest.yaml` containing metadata, timestamps, and source inputs.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_renderer.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/jd_offer/project_templates.py src/jd_offer/renderer.py src/jd_offer/validators.py tests/test_renderer.py
git commit -m "feat: render reusable jd case bundles"
```

### Task 5: Create the Codex skill folder and workflow docs

**Files:**
- Create: `skills/jd-to-offer/SKILL.md`
- Create: `skills/jd-to-offer/agents/openai.yaml`
- Create: `skills/jd-to-offer/references/workflow.md`
- Create: `skills/jd-to-offer/references/output_contract.md`
- Create: `skills/jd-to-offer/scripts/run_case.py`
- Create: `skills/jd-to-offer/scripts/validate_case.py`

**Step 1: Write the failing validation step**

Run: `python /Users/liuche/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/jd-to-offer`

Expected: FAIL because the skill folder does not exist yet.

**Step 2: Initialize the skill**

Use the skill creator scaffold script to initialize the folder with `scripts` and `references` directories.

**Step 3: Write the skill body**

The skill should instruct the agent to:

1. Parse the JD locally
2. Map it to competencies
3. Use web browsing for the latest official docs and primary papers
4. Write the five case outputs
5. Build one project that is demoable and interviewable
6. Prefer reusable resource manifests over ad hoc prose

**Step 4: Validate the skill**

Run: `python /Users/liuche/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/jd-to-offer`

Expected: PASS.

**Step 5: Commit**

```bash
git add skills/jd-to-offer
git commit -m "feat: add jd-to-offer codex skill"
```

### Task 6: Add the Didi example case and curated resource pack

**Files:**
- Create: `docs/examples/2026-03-09-didi-agent-jd-blueprint.md`
- Create: `configs/project_templates.yaml`
- Create: `configs/resource_registry.yaml`
- Update: `examples/didi_2026_agent_jd.md`

**Step 1: Write the failing test or smoke check**

Define a smoke command in the CLI and assert it creates a case folder for the Didi JD.

```python
def test_generate_didi_case(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "generate",
            "--input",
            "examples/didi_2026_agent_jd.md",
            "--company",
            "didi",
            "--role",
            "agent-algorithm",
            "--outdir",
            str(tmp_path / "didi-case"),
        ],
    )
    assert result.exit_code == 0
    assert (tmp_path / "didi-case" / "01_jd_decomposition.md").exists()
```

**Step 2: Run the smoke test to verify it fails**

Run: `pytest tests/test_cli.py -v`

Expected: generate path not implemented.

**Step 3: Implement the example bundle**

Seed the Didi example with:

- competency weights
- fine-grained knowledge system
- curated resources
- flagship project blueprint
- interview assets

**Step 4: Run the smoke test to verify it passes**

Run: `pytest tests/test_cli.py -v`

Expected: PASS and output files created.

**Step 5: Commit**

```bash
git add docs/examples/2026-03-09-didi-agent-jd-blueprint.md configs/project_templates.yaml configs/resource_registry.yaml
git commit -m "feat: add didi jd example and resource templates"
```

### Task 7: Add README and verification workflow

**Files:**
- Create: `README.md`

**Step 1: Write the usage section**

Document:

- required inputs
- CLI examples
- skill usage entry point
- output folder contract
- how web-verified resources should be curated

**Step 2: Add verification commands**

Document:

```bash
pytest -v
python -m jd_offer.cli generate --input examples/didi_2026_agent_jd.md --company didi --role agent-algorithm --outdir cases/didi-agent-2026
python skills/jd-to-offer/scripts/validate_case.py cases/didi-agent-2026
```

**Step 3: Run verification**

Run the targeted tests first, then the full test suite.

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: document jd-to-offer workflow"
```

## Design Constraints

- Do not hardcode a single company or job family.
- Keep the taxonomy editable through YAML instead of code changes.
- Require web validation for resource recommendations.
- Prefer official docs and primary research papers over secondary summaries.
- Make the generated project blueprint demoable within 2 to 6 weeks.
- Keep outputs interview-oriented, not academic-only.

## Recommended First Milestone

Deliver a narrow but usable v0:

1. One JD input format: markdown text
2. One output format: markdown bundle
3. One supported example: the Didi JD in this repo
4. One project archetype: domain agent plus post-training loop

That is enough to validate the workflow before adding resume ingestion, personal gap analysis, or multiple role families.

Plan complete and saved to `docs/plans/2026-03-09-jd-to-offer-system.md`.

Execution options after approval:

1. Stay in this session and scaffold v0 end to end
2. Use the plan as the implementation contract for a later build session
