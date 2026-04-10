# JD Resume LaTeX Skill Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Build a professional resume-adaptation workflow and skill that turns a target JD into deep role analysis, evidence-backed internship packaging, and high-signal LaTeX resume output.

**Architecture:** Reuse the existing `jd_offer` pipeline for JD parsing, competency mapping, and research overrides. Add a new resume-focused layer that converts JD analysis and evidence packs into resume narrative decisions, LaTeX content decisions, and traceable packaging artifacts linked back to sources and claim boundaries.

**Tech Stack:** Python 3.11, Typer CLI, Pydantic, Markdown case bundles, YAML research overrides, LaTeX (AltaCV-based external project at `/Volumes/passport/简历/latex-resume`), `latexmk`, `pdftotext`.

## Current State Assessment

- The repo already has a stable `jd_offer` workflow that produces:
  - `01_jd_decomposition.md`
  - `02_knowledge_system.md`
  - `03_resource_pack.md`
  - `04_project_blueprint.md`
  - `05_interview_assets.md`
- The repo already contains Didi- and RingConn-related research and packaging drafts in:
  - `docs/examples/2026-04-10-ringconn-internship-packaging.md`
  - `docs/examples/2026-04-10-ringconn-to-didi-freight-final-packaging.md`
  - `docs/plans/2026-04-10-didi-freight-master-plan.md`
  - `cases/didi-agent-2026/`
- The external LaTeX resume project is the source of truth for final resume rendering:
  - `/Volumes/passport/简历/latex-resume/main.tex`
  - `/Volumes/passport/简历/latex-resume/profile.tex`
  - `/Volumes/passport/简历/latex-resume/content.tex`
- The main gap is not raw JD parsing. The gap is turning analysis into:
  - sharper resume storytelling
  - more role-specific LaTeX presentation
  - evidence-backed internship packaging
  - a reusable skill with traceable outputs

## Design Principles

1. Treat JD analysis as a business-and-technical decomposition problem, not keyword matching.
2. Treat internship packaging as evidence-constrained positioning, not free-form embellishment.
3. Treat LaTeX design as information hierarchy engineering, not template swapping.
4. Preserve one source of truth for final resume content in `/Volumes/passport/简历/latex-resume`.
5. Require every strong claim to map back to one of:
   - user-confirmed fact
   - repo artifact
   - official company/business source
   - official product/documentation source
   - primary paper or official engineering material

## Task 1: Freeze the resume output contract

**Files:**
- Modify: `skills/jd-to-offer/references/output_contract.md`
- Create: `docs/examples/2026-04-10-resume-output-contract.md`
- Create: `configs/resume_rendering_rules.yaml`

**Step 1: Define resume deliverables**

Write the exact outputs the future workflow must produce:
- JD deep-dive memo
- evidence-backed packaging memo
- resume bullet candidates
- LaTeX rendering instructions
- final content sync checklist

**Step 2: Define claim-boundary rules**

Require each experience bullet to be labeled as:
- confirmed fact
- inferred but defensible packaging
- forbidden / unsupported claim

**Step 3: Define rendering rules**

Specify:
- maximum bullets per experience
- bullet length budget
- metric display rules
- section ordering rules
- when to use left-column tags, right-column bullets, or highlight sections

**Step 4: Review contract**

Check that the contract can support both:
- role-specific resume editing
- later interview/storytelling expansion

## Task 2: Upgrade JD analysis from keyword hits to role dissection

**Files:**
- Modify: `configs/competency_taxonomy.yaml`
- Modify: `src/jd_offer/project_templates.py`
- Create: `configs/jd_analysis_frames.yaml`
- Create: `docs/examples/2026-04-10-jd-analysis-method.md`

**Step 1: Add a deeper JD analysis frame**

For each JD, decompose:
- explicit responsibilities
- explicit requirements
- bonus signals
- hidden business targets
- implied evaluation metrics
- preferred proof forms in resume/interview

**Step 2: Add role-specific lenses**

Support at least:
- algorithm / strategy roles
- AI application / agent roles
- AI backend roles
- generic backend roles

**Step 3: Add proof mapping**

For each top competency, define what counts as proof:
- internship proof
- project proof
- paper / competition proof
- skill-tag proof

**Step 4: Add “must prove / can bridge / must not fake” output**

This becomes the core bridge from JD analysis into resume packaging.

## Task 3: Build an evidence-backed internship packaging system

**Files:**
- Create: `configs/experience_packaging_frames.yaml`
- Create: `docs/examples/2026-04-10-internship-packaging-method.md`
- Create: `examples/source_packs/`
- Create: `examples/source_packs/ringconn_source_pack.md`

**Step 1: Define the packaging frame**

Every internship packaging pass should produce:
- core storyline
- transferable competencies
- quantifiable outcomes
- defensible bridge to target role
- forbidden overclaims

**Step 2: Define source categories**

Collect and normalize:
- company official docs / product pages
- official industry reports / statistics
- official engineering docs
- primary papers
- user-confirmed work scope
- repo or demo artifacts

**Step 3: Build a source pack format**

For each source pack, record:
- source URL or file path
- source type
- exact business or technical signal it supports
- experiences or bullets it may justify
- claim ceiling

**Step 4: Pilot on RingConn**

Use `RingConn` as the first fully closed-loop example:
- truth boundary
- transferable signal extraction
- final 1-sentence summary
- final 3-bullet set
- interview bridge sentence

## Task 4: Redesign LaTeX presentation around information hierarchy

**Files:**
- Modify: `/Volumes/passport/简历/latex-resume/main.tex`
- Modify: `/Volumes/passport/简历/latex-resume/content.tex`
- Modify: `/Volumes/passport/简历/latex-resume/profile.tex`
- Create: `/Volumes/passport/简历/latex-resume/resume-modern-blue-strategy.tex`
- Create: `docs/examples/2026-04-10-latex-resume-design-audit.md`

**Step 1: Audit the current layout**

Identify what should be reduced or removed for formal applications:
- photo dependency
- decorative “我的一天” module
- left-column density
- ATS-unfriendly icon extraction
- overly broad skill tags

**Step 2: Borrow the right ideas from strong resume projects**

Reference:
- AltaCV for column structure and tags
- Awesome-CV for strong section rhythm and headline polish
- moderncv for conservative professionalism
- billryan/resume for Chinese engineering resume compactness

**Step 3: Implement stronger visual hierarchy**

Prioritize:
- high-signal header
- tighter experience blocks
- bolded action/result phrases
- stable metric callouts
- role-specific highlight box instead of generic personal-expression modules

**Step 4: Add render verification**

For each generated resume variant:
- compile with `latexmk`
- inspect first-page visual balance
- run `pdftotext -layout`
- verify key fields survive extraction cleanly

## Task 5: Create the resume-focused skill

**Files:**
- Create: `skills/jd-resume-latex/SKILL.md`
- Create: `skills/jd-resume-latex/agents/openai.yaml`
- Create: `skills/jd-resume-latex/references/workflow.md`
- Create: `skills/jd-resume-latex/references/source_rules.md`
- Create: `skills/jd-resume-latex/references/latex_rules.md`
- Optional create: `skills/jd-resume-latex/scripts/`

**Step 1: Define trigger scope**

The skill should trigger when users ask to:
- adapt resume to a JD
- deeply analyze a role before modifying resume
- repackage an internship for a target position
- output LaTeX-ready resume content

**Step 2: Keep it layered**

The skill should do work in this order:
1. analyze JD deeply
2. gather or load source pack
3. choose packaging strategy
4. generate resume bullets and proof mapping
5. emit LaTeX edit instructions or apply edits
6. verify rendered output

**Step 3: Reuse existing repo assets**

Do not replace `jd-to-offer`. Instead:
- call or mirror its JD parsing and research workflow
- add resume-specific logic on top
- keep output artifacts reproducible in the repo

**Step 4: Validate the skill**

Run:
- skill validation
- one Didi case
- one AI backend case
- one generic backend case

## Task 6: Close the loop with repo artifacts and tests

**Files:**
- Modify: `README.md`
- Create: `tests/test_resume_contract.py`
- Create: `tests/test_resume_packaging.py`
- Create: `tests/test_resume_renderer_workflow.py`
- Create: `docs/examples/2026-04-10-ringconn-resume-adaptation-demo.md`

**Step 1: Add contract tests**

Verify that generated outputs include:
- claim boundaries
- source links
- proof mapping
- LaTeX rendering decisions

**Step 2: Add example-case verification**

Test that the RingConn example produces:
- no forbidden freight overclaims
- a transferable competency bridge
- a final bullet set within rendering limits

**Step 3: Update documentation**

Document:
- how the new skill relates to `jd-to-offer`
- where final resume edits happen
- how to add new source packs and role variants

## Recommended Execution Order

1. Task 4 first: stabilize LaTeX presentation and rendering rules.
2. Task 2 next: deepen JD analysis so later resume decisions have a better upstream signal.
3. Task 3 next: build evidence-backed packaging on RingConn as the first closed-loop example.
4. Task 5 next: formalize the workflow into a reusable skill.
5. Task 6 last: add tests, docs, and demo validation.

## External References To Benchmark Against

- AltaCV: https://github.com/liantze/AltaCV
- Awesome-CV: https://github.com/posquit0/Awesome-CV
- moderncv: https://github.com/xdanaux/moderncv
- billryan/resume: https://github.com/billryan/resume
- RingConn official app/features grounding: https://ringconn.com/pages/app-features
- Google OR-Tools official docs: https://developers.google.com/optimization
- Microsoft EconML official docs: https://www.pywhy.org/EconML/index.html

## Success Criteria

- A new JD can be decomposed into business targets, proof expectations, and resume priorities without hand-wavy reasoning.
- A target internship can be repackaged professionally without crossing truth boundaries.
- The LaTeX resume surfaces the most relevant proof in the first screenful.
- Rendered PDFs remain readable by both humans and text extraction tooling.
- The resulting skill is reusable, source-backed, and auditable.
