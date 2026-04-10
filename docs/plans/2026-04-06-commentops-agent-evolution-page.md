# CommentOps Agent Evolution Page Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a new CommentOps demo page that clearly explains how this moderation agent evolves from prototype to engineering system, including metrics, optimization levers, ROI framing, and a big-tech-informed roadmap.

**Architecture:** Add one new structured content payload plus one new HTML page route to the existing FastAPI demo. Reuse the current `content.py` + `app.py` pattern so the page stays consistent with `project-overview`, `workflow`, and `research-log`, while introducing a more explicit “operating model” view that ties together maturity assessment, evaluation strategy, optimization roadmap, and ROI gates.

**Tech Stack:** Python, FastAPI, existing inline HTML/CSS rendering in `src/commentops_agent_lab/app.py`, structured page payloads in `src/commentops_agent_lab/content.py`, pytest + FastAPI TestClient.

## Why This Page

The current demo already answers:

- what the project is: `/project-overview`
- how the online chain works: `/workflow`
- what external research informed the framing: `/research-log`
- how a case runs end-to-end: `/demo`

What is still missing is a page that answers:

- why this is not a toy agent
- how the system should evolve iteratively
- which metrics define “good”
- which optimizations belong to evidence vs decision vs routing vs harness vs learning
- when an upgrade is worth the ROI

This new page should become the bridge between technical architecture and engineering/product judgment.

## Recommended Page Positioning

Use a new page called `工程进化` with route `/agent-evolution`.

This is the recommended option over two alternatives:

1. **Recommended: hybrid narrative + dashboard page**
   Best for interview demos and self-study.
   It can combine maturity assessment, metrics, roadmap, and ROI in one coherent page.

2. **Alternative: pure metrics dashboard**
   Stronger for operational feel, weaker for explaining architecture and iteration logic.

3. **Alternative: long-form strategy page**
   Easier to write, but duplicates existing docs and feels less like a productized demo page.

The recommended page should feel like an “operating model wall”:

- current maturity
- next milestones
- evaluation scorecards
- ROI and sequencing logic

## Target User Outcomes

After reading the page, a viewer should be able to answer:

1. What stage is this moderation agent currently at?
2. What engineering gaps still separate it from a production-shaped system?
3. Which metrics matter most, and why not just accuracy?
4. How should the system evolve from V0 to V5?
5. Which improvements are high-ROI now, and which should wait?

## Proposed Content Structure

### Section 1: Page Hero

**Purpose:** Frame the page as “how this becomes an engineering system.”

**Must communicate:**

- this is not another workflow page
- this page is about maturity, metrics, evolution, and ROI
- the system should grow by evidence, not by complexity theatre

**Key copy themes:**

- “From demo to operating system”
- “Safe automation boundary”
- “Measure before scaling”
- “Upgrade where ROI is positive”

### Section 2: Current Maturity Snapshot

**Purpose:** Show what already exists vs what is still prototype-level.

**Recommended layout:**

- one maturity headline such as `当前阶段：V2.5 / bounded workflow prototype`
- three columns:
  - already built
  - known gaps
  - next priorities

**Must reference current project reality:**

- already has case schema
- already has policy hit / risk signals / queue routing
- already has basic eval and failure review artifacts
- still lacks retrieval decision policy, harness, richer regression, reviewer/appeal loop, explicit ROI instrumentation

### Section 3: Engineering Layers

**Purpose:** Explain where optimizations belong.

**Recommended five-layer framing:**

- `Evidence Layer`
- `Decision Boundary Layer`
- `Ops Routing Layer`
- `Harness / Safety Layer`
- `Learning Flywheel Layer`

Each layer should answer:

- what problem it solves
- what the current prototype already does
- what the next upgrade is
- what metric tells us it improved

### Section 4: Evaluation Framework

**Purpose:** Make the metric system explicit and interview-ready.

**Metric groups to show:**

- `Online Quality`
- `Operational Efficiency`
- `Governance Stability`
- `Economics / ROI`

**Metrics to include:**

- `action_accuracy`
- `policy_grounding_rate`
- `high_risk_recall`
- `over_enforcement_proxy`
- `under_enforcement_proxy`
- `queue_routing_accuracy`
- `human_review_rate`
- `evidence_ready_rate`
- `reviewer_override_rate`
- `appeal_overturn_rate`
- `policy_version_regression_rate`
- `tool_failure_recovery_rate`
- `cost_per_1k_cases`
- `manual_review_hours_saved`
- `marginal_quality_gain_per_cost_unit`

**Important:** do not fake live numbers. The page should distinguish:

- metrics already implemented
- metrics planned next
- metrics that require future instrumentation

### Section 5: Agent Evolution Roadmap

**Purpose:** Show the system evolves in stages, not by random feature stacking.

**Recommended stages:**

- `V0` classifier / rigid workflow baseline
- `V1` bounded policy-grounded workflow
- `V2` richer evidence + routing + shadow audit
- `V3` eval platform + regression + failure taxonomy
- `V4` reviewer / appeal / learning loop
- `V5` durable execution + stronger harness + selective specialization

Each stage should include:

- what capability gets added
- what business problem it addresses
- what new metric gate must be met
- why it is worth or not worth doing yet

### Section 6: ROI Sequencing

**Purpose:** Prevent the page from sounding like complexity for complexity’s sake.

**Recommended framing:**

- “Do now”
- “Do when volume rises”
- “Do only after evidence of need”

**Immediate high-ROI upgrades:**

- retrieval decision policy
- slice/regression evals
- failure harness
- reviewer/appeal data model

**Medium-term ROI upgrades:**

- shadow audit instrumentation
- adjudication memory
- exposure-aware prioritization

**Deferred upgrades unless justified:**

- multi-agent specialization
- heavy multimodal pipeline
- complex reward learning

### Section 7: Big-Tech Pattern Mapping

**Purpose:** Tie project choices to publicly known industry practice.

**Sources to map:**

- TikTok:
  automated review + additional review + appeal + transparency
- Meta:
  AI scales operations but high-impact decisions keep human judgment
- YouTube:
  exposure-based governance + policy quality + appeals + consistency
- OpenAI:
  eval-first optimization + trace grading + feedback flywheel
- Anthropic:
  start simple, use agents only when needed, engineer tools seriously

This section should not be a literature dump. It should explicitly answer:

- “what did this source change in our design thinking?”

## Page Data Model Proposal

Create a new payload function:

- `agent_evolution_payload() -> dict`

Recommended top-level keys:

- `title`
- `summary`
- `hero_chips`
- `maturity_snapshot`
- `engineering_layers`
- `metric_groups`
- `roadmap_stages`
- `roi_buckets`
- `industry_mappings`
- `references`

This keeps the page content structured and testable.

## UI / UX Proposal

### Visual Direction

Keep the current visual system for consistency, but make this page more “control room” than “documentation wall”.

Recommended visual blocks:

- hero with maturity chip
- stage ladder / horizontal rail for V0-V5
- metric cards grouped by category
- matrix table for `Layer x Current x Next x Metric`
- ROI board with three columns
- reference cards with “why it matters”

### Avoid

- overly dense prose blocks
- fake KPI numbers
- too much animation
- complex custom graph rendering unless needed

### Nice-to-have interactions

- click a roadmap stage to reveal “capability / metric / ROI / risk”
- click a layer to see “current implementation vs next milestone”

These interactions are optional and should not block the first implementation.

## File-Level Implementation Plan

### Task 1: Add failing tests for the new page and data route

**Files:**
- Modify: `tests/test_commentops_app.py`
- Test: `tests/test_commentops_app.py`

**Step 1: Write the failing test**

Add tests for:

- `/agent-evolution`
- `/agent-evolution-data`
- navigation includes the new page

Test expectations should include:

- HTTP 200
- page contains `工程进化`
- page contains `ROI`
- page contains `当前成熟度`
- page contains `评测指标`
- page contains `TikTok`, `Meta`, `YouTube`, `OpenAI`, `Anthropic`

**Step 2: Run test to verify it fails**

Run:

```bash
pytest -q tests/test_commentops_app.py -k evolution
```

Expected:

- FAIL because route and content do not yet exist

### Task 2: Add structured content payload for the new page

**Files:**
- Modify: `src/commentops_agent_lab/content.py`
- Test: `tests/test_commentops_app.py`

**Step 1: Add `agent_evolution_payload()`**

Include:

- maturity snapshot
- engineering layers
- metric groups
- roadmap stages
- ROI buckets
- industry mappings

**Step 2: Keep content grounded in current project**

The payload must explicitly separate:

- `current prototype already has`
- `next upgrades`
- `future instrumentation needed`

This is critical to keep the page honest and interview-safe.

**Step 3: Add source references**

Use the same source quality bar as existing pages.

### Task 3: Add route, nav item, and page renderer

**Files:**
- Modify: `src/commentops_agent_lab/app.py`
- Test: `tests/test_commentops_app.py`

**Step 1: Add nav item**

Extend `_render_nav()` with:

- key: `evolution`
- label: `工程进化`
- href: `/agent-evolution`

**Step 2: Add data endpoint**

Add:

- `@app.get("/agent-evolution-data")`

**Step 3: Add HTML page route**

Add:

- `@app.get("/agent-evolution", response_class=HTMLResponse)`

**Step 4: Implement page renderer**

Create a renderer similar in style to:

- `render_project_overview_page()`
- `render_research_log_page()`

The page should render:

- hero
- maturity snapshot
- layer matrix
- metric framework
- roadmap
- ROI board
- industry mapping

### Task 4: Add minimal front-end interactions

**Files:**
- Modify: `src/commentops_agent_lab/app.py`
- Test: `tests/test_commentops_app.py`

**Step 1: Keep first version simple**

Use plain HTML + a little JS for:

- expanding roadmap stages
- highlighting current stage

**Step 2: Do not overbuild**

No separate frontend bundle.
No new framework.
No heavy chart library.

### Task 5: Verify consistency with current project story

**Files:**
- Modify: `src/commentops_agent_lab/content.py`
- Optional Modify: `docs/examples/2026-04-05-commentops-agent-learning-handbook.md`
- Test: `tests/test_commentops_app.py`

**Step 1: Ensure terminology is consistent**

Terms must line up with current docs:

- bounded single-agent workflow
- evidence / decision / routing / learning
- safe automation boundary
- failure taxonomy

**Step 2: Avoid content drift**

If the new page uses a stronger claim than current code/doc reality supports, soften it.

### Task 6: Run verification

**Files:**
- Test: `tests/test_commentops_app.py`

**Step 1: Run focused tests**

```bash
pytest -q tests/test_commentops_app.py
```

Expected:

- PASS

**Step 2: Optional runtime verification**

```bash
PYTHONPATH=src python -m commentops_agent_lab.cli serve
```

Then manually inspect:

- `/agent-evolution`
- navigation continuity with `/project-overview`, `/workflow`, `/research-log`

## Recommended Content Decisions

These decisions should be locked before implementation:

1. **Audience priority**
   Primary audience should be interview/demo viewers, not internal operators.

2. **Tone**
   Engineering-judgment first, not hype.

3. **Metric philosophy**
   Show metric definitions and instrumentation status.
   Do not invent operational numbers.

4. **Current maturity honesty**
   Position the current system as a strong prototype with evaluation/closure foundations, not as a production-ready moderation platform.

5. **ROI philosophy**
   Use directional ROI framing, not fabricated business impact.

## Risks To Watch

- The page duplicates `project-overview` instead of extending it.
- The page becomes too text-heavy and loses demo value.
- The page overclaims maturity versus current code reality.
- ROI content becomes generic consulting language instead of concrete engineering sequencing.
- Too many interactions increase scope without improving clarity.

## Success Criteria

The page is successful if:

- a viewer can explain the current maturity stage in one sentence
- a viewer can name at least four metric categories beyond accuracy
- a viewer can explain why multi-agent is not the immediate next step
- a viewer can explain the top three high-ROI upgrades
- the page feels like part of the demo, not a detached essay

## Suggested Implementation Order

1. Tests
2. Payload
3. Route + nav
4. Static page rendering
5. Light interactions
6. Verification

## Execution Handoff

Plan complete and saved to `docs/plans/2026-04-06-commentops-agent-evolution-page.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
