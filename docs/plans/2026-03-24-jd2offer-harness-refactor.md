# JD2Offer Harness Refactor Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Refactor the current `jd_offer` project into a harness-first system that can take a user's resume plus a target JD, decompose the target capabilities, and generate a grounded, evaluable, visualizable, and interview-ready flagship project bundle.

**Architecture:** Keep the current repo's strongest assets, including deterministic parsing, taxonomy configs, case bundle contracts, tests, and flagship project examples, but wrap all AI-heavy steps inside a stage-based harness with explicit inputs, outputs, artifacts, validators, evaluators, and revision loops. The system should be repository-legible first: every important rule, prompt, schema, run artifact, and evaluation report lives in the repo and can be re-run.

**Tech Stack:** Python 3.11, `typer`, `pydantic`, `pyyaml`, `jinja2`, `pytest`, Markdown, Mermaid, optional OpenAI-compatible LLM adapter, existing `driverops_agent_lab` artifacts as a reference project family rather than the only project destination.

## Current Repo Assessment

### What is already strong

- `jd_offer` already has a clear output contract: JD decomposition, knowledge system, resource pack, project blueprint, interview assets, and manifest.
- The repo already separates taxonomy, templates, resources, and rendering, which is a good starting point for a harness-driven design.
- `driverops_agent_lab` already proves a second important point: this repo can hold runnable project artifacts, evaluation outputs, training data, and failure review assets.
- Tests are in good shape for the current scope. `PYTHONPATH=src pytest -q` passes with `25 passed` on March 24, 2026.
- The docs show you are already thinking in terms of reusable platform patterns, not one-off scripts.

### What blocks your target outcome today

- The system only reads JD input. It cannot ground output in the user's resume, past projects, or actual evidence.
- The project selection logic is still mostly rules plus static templates, not AI-guided synthesis with validation.
- The flagship project path is overly coupled to one built-in example family: `DriverOps Agent Lab`.
- The current markdown generation is mostly one-shot rendering. There is no run artifact model, no stage trace, no retry/review loop, and no scoring harness for output quality.
- There is no explicit anti-hallucination layer to ensure generated project claims stay faithful to the user's real resume.
- There is no dedicated visual output layer for architecture diagrams, demo flow, or presentation-ready storytelling.

## Refactor Thesis

The current repo is valuable enough that a hard fork into a brand-new unrelated repository would throw away useful history. The better move is:

1. Keep this repository as the system of record.
2. Start the refactor in an isolated worktree and new branch.
3. Treat current `jd_offer` as the deterministic baseline pipeline.
4. Build a new harness layer beside it, then progressively migrate the old logic under that harness.

Recommended isolation strategy:

```bash
git worktree add .worktrees/jd2offer-harness -b codex/jd2offer-harness-refactor
```

Only if the refactor stabilizes and you want to productize it separately should we split it into a new repo later.

## What "Harness Engineering" Means Here

For this project, harness engineering should mean:

- AI is not a single prompt that writes the whole answer.
- Each stage has a contract: input schema, output schema, prompt template, validator, evaluator, and saved artifact.
- Every important stage is re-runnable and inspectable.
- Knowledge should live in the repo, not only in prompts or chat history.
- The system should be legible both to humans and to AI agents working on it later.

This is consistent with the agent-first repository pattern described in OpenAI's Harness Engineering post on February 11, 2026: treat the repository as the system of record, optimize for agent legibility, and use structured plans plus feedback loops instead of relying on one giant instruction blob. Source: [OpenAI - Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/).

## Target Product Behavior

The refactored system should accept two primary inputs:

- user resume
- target JD

It should then produce one grounded case workspace containing:

- target-role decomposition
- resume-to-JD gap map
- ordered knowledge graph
- flagship project thesis
- project architecture and module design
- milestone plan
- evaluation strategy
- visual assets such as Mermaid diagrams and demo flow
- interview and presentation script
- manifest and run traces
- evaluator reports for quality and grounding

The key product promise becomes:

> Given who the user already is and what role they want, generate the smallest convincing flagship project that bridges the gap and is strong enough to show, explain, and defend in interviews.

## Proposed Architecture

### 1. Domain layer

Create explicit typed models for:

- `ResumeDocument`
- `ResumeEvidence`
- `TargetJD`
- `CompetencyGraph`
- `GapAnalysis`
- `ProjectArchetype`
- `ProjectSpec`
- `VisualNarrative`
- `InterviewNarrative`
- `CaseRunManifest`
- `EvaluationReport`

This is the foundation that lets AI outputs be validated instead of trusted blindly.

### 2. Harness layer

Create a reusable stage runner with:

- stage registry
- prompt registry
- input/output schemas
- artifact persistence
- validation hooks
- scoring hooks
- revision hooks

Each stage should write artifacts to a predictable directory, for example:

```text
cases/<case_slug>/
  raw/
  normalized/
  stages/
    01_intake/
    02_competency_analysis/
    03_gap_mapping/
    04_project_design/
    05_visual_story/
    06_bundle_render/
    07_eval/
  outputs/
  manifest.yaml
```

### 3. Pipeline layer

Split the workflow into explicit stages:

1. `ingest_resume`
2. `ingest_jd`
3. `extract_resume_evidence`
4. `map_jd_competencies`
5. `build_gap_analysis`
6. `select_project_archetype`
7. `draft_project_spec`
8. `draft_visual_story`
9. `draft_interview_assets`
10. `render_case_bundle`
11. `evaluate_bundle`
12. `revise_until_threshold`

### 4. Knowledge layer

Move human- and AI-readable knowledge into repo-owned catalogs:

- `configs/competency_taxonomy.yaml`
- `configs/project_archetypes.yaml`
- `configs/evaluation_rubrics.yaml`
- `prompts/*.md`
- `docs/design/` and `docs/plans/`

The repo should make it easy for future agents to answer:

- what stages exist
- what a good output looks like
- how project archetypes are chosen
- how grounding is enforced
- how quality is scored

## Suggested New Package Layout

```text
src/jd2offer_harness/
  cli.py
  domain/
    resume.py
    jd.py
    competency.py
    project.py
    evaluation.py
  harness/
    runner.py
    registry.py
    prompts.py
    artifacts.py
    validators.py
    evaluators.py
  pipelines/
    intake.py
    analysis.py
    design.py
    packaging.py
  adapters/
    resume_parser.py
    jd_parser.py
    llm_client.py
  generators/
    knowledge_graph.py
    project_spec.py
    visuals.py
    interview_assets.py
  renderers/
    markdown_bundle.py
    manifest.py
prompts/
  extract_resume_evidence.md
  gap_analysis.md
  project_spec.md
  visual_story.md
  interview_assets.md
configs/
  competency_taxonomy.yaml
  project_archetypes.yaml
  evaluation_rubrics.yaml
tests/
  harness/
  pipelines/
  integration/
```

## Keep / Refactor / Retire

### Keep

- current output bundle contract
- competency taxonomy as seed data
- resource registry pattern
- research override pattern
- `driverops_agent_lab` as a reference project family and evaluation example
- current example JDs, generated bundles, and tests as regression fixtures

### Refactor

- `src/jd_offer/parser.py` into a general document ingestion layer
- `src/jd_offer/project_templates.py` into catalog-driven project archetypes plus richer spec generation
- `src/jd_offer/renderer.py` into a generic bundle renderer fed by structured stage artifacts
- current CLI into a new run-oriented CLI with explicit modes like `analyze`, `design-project`, `render-bundle`, `eval`, and `run-case`

### Retire or downgrade from core path

- direct one-shot markdown building as the primary generation mechanism
- hardcoded single-template bias toward `DriverOps Agent Lab`
- purely keyword-based selection as the final project selection authority

## Evaluation Harness

This is the most important missing piece.

Every case run should score at least these dimensions:

- `resume_grounding_score`: are claims traceable to the user's resume or explicitly labeled as proposed stretch work
- `jd_coverage_score`: do the top JD competencies map to the generated project
- `project_coherence_score`: do the modules, metrics, milestones, and demo story fit one project thesis
- `specificity_score`: is the output role-specific instead of generic AI jargon
- `presentation_readiness_score`: can the user explain the project in 3, 5, and 10 minute versions
- `visual_completeness_score`: does the case include architecture and demo-flow visuals
- `hallucination_risk_score`: does the system invent ungrounded personal experience

If a score is below threshold, the pipeline should revise only the failing stage instead of regenerating everything blindly.

## Project Archetype Strategy

Do not design every project from scratch.

Introduce a catalog of project archetypes, for example:

- vertical agent system
- AI-enhanced backend platform
- evaluation and post-training sandbox
- data operations copilot
- recommendation and decision-support system

Each archetype should define:

- best-fit JD signals
- best-fit resume signals
- module library
- metrics library
- visual patterns
- common interview questions

Then the harness selects and adapts an archetype instead of hallucinating the whole project surface.

## Recommended Phase Plan

### Phase 0: Isolation and baseline capture

**Outcome:** safe refactor workspace without disturbing current main branch.

Tasks:

- create isolated worktree and feature branch
- snapshot current tests and sample outputs
- document what is current baseline behavior and what must stay compatible

### Phase 1: New domain model and run manifest

**Outcome:** a typed foundation for resume plus JD plus project outputs.

Tasks:

- add new `jd2offer_harness` package
- define typed schemas for intake, analysis, design, and evaluation artifacts
- define run manifest and artifact directory contract
- add unit tests for core models and manifest I/O

### Phase 2: Resume-aware intake pipeline

**Outcome:** the system can read resume plus JD and normalize both.

Tasks:

- add resume parser and evidence extractor
- preserve current JD parser as an adapter
- add normalized JSON or YAML artifacts for both inputs
- add tests for Chinese resume and Chinese JD examples

### Phase 3: Harness runner and stage contracts

**Outcome:** generation becomes a sequence of inspectable stages instead of one command.

Tasks:

- implement stage registry and runner
- add prompt registry and artifact saving
- add schema validation and stage-level retry hooks
- add CLI commands for stage-by-stage execution

### Phase 4: Gap analysis and project design

**Outcome:** project generation becomes grounded in both the user's background and the target role.

Tasks:

- implement resume-to-JD gap analysis
- build project archetype catalog and selector
- generate structured `ProjectSpec`
- render milestone plan, metrics, module map, and demo scenarios

### Phase 5: Visual and speaking outputs

**Outcome:** the bundle becomes presentation-ready instead of only readable.

Tasks:

- add Mermaid architecture rendering
- add demo flow and user journey diagrams
- add 3-minute and 10-minute presentation scripts
- add resume bullets and interview Q&A grounded in the generated project

### Phase 6: Evaluation and revision loop

**Outcome:** the system can detect weak outputs and improve them.

Tasks:

- implement evaluation rubric config
- add evaluators for grounding, coverage, coherence, and speaking readiness
- add revision loop that targets low-scoring stages
- add regression fixtures for at least 2-3 different JD families

### Phase 7: Optional delivery surface

**Outcome:** easier user interaction if you want this to be a product instead of a CLI-only system.

Tasks:

- add lightweight web UI or notebook-style run viewer
- show stage artifacts, diagrams, scores, and final outputs
- allow user edits on resume evidence and project preference before final rendering

## What To Reuse From `driverops_agent_lab`

Do not throw it away.

Its real value is no longer "this is the only flagship project." Its value is:

- a reference implementation of how one project family can be rendered
- an example of planner, trace, evidence, memory, evaluation, and failure review artifacts
- a template for what "runnable and speakable" looks like

In the refactor, `driverops_agent_lab` should become one project family adapter under the new harness, not the whole product thesis.

## First Milestone Definition

The first real milestone should not be "AI writes prettier markdown."

It should be:

> Given one resume and one JD, produce a case bundle where every generated project claim is either grounded in resume evidence or explicitly marked as a proposed stretch artifact, and where the final project blueprint includes one architecture diagram, one demo flow, and one interview script.

If we reach that, the product meaningfully moves from a clever generator to a trustworthy job-project design system.

## Main Risks

- Over-designing the harness before one resume-aware happy path works
- Letting LLM generation outrun schema design and evaluation
- Keeping `driverops_agent_lab` too central, which would reintroduce template lock-in
- Generating visually rich output that is not actually grounded in the user's real background

## Recommendation

Proceed with a worktree-based refactor inside this repo, not a new disconnected repo. Build the new harness beside the current implementation, and use the current deterministic pipeline as a regression baseline while we introduce resume-aware analysis, stage contracts, evaluation, and presentation outputs.
