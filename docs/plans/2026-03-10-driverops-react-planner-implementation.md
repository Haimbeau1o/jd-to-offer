# DriverOps ReAct/Planner Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Upgrade `DriverOps Agent Lab` from an intent-router demo into a lightweight ReAct/Planner agent with grounded answers, explicit execution state, fallback handling, and a path into richer training/evaluation loops.

**Architecture:** Split the current single-pass agent into `planner -> executor -> grounded answer -> evaluator`. The planner builds a small action plan from query, driver context, and memory. The executor runs step-by-step, records observations, and supports fallback or early stop. Final answers must cite evidence from observations, making the execution trace reusable for future SFT, preference, and reward-oriented data generation.

**Tech Stack:** Python 3.12, FastAPI, Typer, Pydantic, pytest, JSON/JSONL artifacts.

## Scope

This plan is intentionally split into two phases:

1. **Phase A: Stronger ReAct/Planner Agent**
2. **Phase B: Richer Training/Evaluation Flywheel**

Phase A is required first because it produces the execution traces and failure modes that Phase B depends on.

## Expected Deliverables

After Phase A, the project should additionally support:

- planner state objects (`PlanStep`, `Observation`, `ExecutionState`)
- step-by-step execution instead of fixed tool branching
- grounded answers with evidence items and stop reasons
- fallback-aware execution and richer evaluation metrics

After Phase B, the project should additionally support:

- trace-rich training samples
- failure taxonomy artifacts
- preference/reward-ready export schemas
- extended evaluation reports

### Task 1: Add planner-state schemas

**Files:**
- Modify: `src/driverops_agent_lab/schemas.py`
- Test: `tests/test_driverops_agent_lab.py`

**Step 1: Write the failing test**

Add tests that expect the agent response to include structured planner/execution fields such as:

- `plan`
- `observations`
- `stop_reason`

Expected usage shape:

```python
response = agent.run(...)
assert response.plan
assert response.observations
assert response.stop_reason in {"completed_with_full_evidence", "completed_with_partial_evidence", "fallback_due_to_missing_data"}
```

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: FAIL because planner-state fields do not exist yet.

**Step 3: Write minimal implementation**

Add Pydantic models for:

- `PlanStep`
- `Observation`
- `ExecutionState`
- grounded answer fields on the agent response model

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/schemas.py tests/test_driverops_agent_lab.py
git commit -m "feat: add planner state schemas"
```

### Task 2: Replace fixed branching with planner + executor loop

**Files:**
- Modify: `src/driverops_agent_lab/agent.py`
- Modify: `src/driverops_agent_lab/tools.py`
- Test: `tests/test_driverops_agent_lab.py`

**Step 1: Write the failing test**

Add tests that assert:

- the plan contains 2-4 steps
- steps run in order
- observations are generated from executed tools
- different intents yield different plan structures

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: FAIL because execution is still direct branching.

**Step 3: Write minimal implementation**

Implement:

- `build_plan(query, profile, recent_memory)`
- `execute_plan(plan, context)`
- observation recording per step
- early-stop / skip support for missing evidence or already-satisfied goals

Keep the planner lightweight and deterministic. Do not introduce real LLM calls in this task.

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/agent.py src/driverops_agent_lab/tools.py tests/test_driverops_agent_lab.py
git commit -m "feat: add planner executor loop"
```

### Task 3: Add grounded answers and fallback semantics

**Files:**
- Modify: `src/driverops_agent_lab/agent.py`
- Modify: `src/driverops_agent_lab/schemas.py`
- Test: `tests/test_driverops_agent_lab.py`

**Step 1: Write the failing test**

Add assertions for:

- evidence items in final response
- recommendations tied to specific observations
- explicit `stop_reason`
- partial-evidence fallback behavior

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: FAIL because the response is not grounded yet.

**Step 3: Write minimal implementation**

Upgrade the final answer payload to include:

- `answer_summary`
- `evidence_items`
- `recommendations`
- `risk_notes`
- `stop_reason`

Support at least these stop reasons:

- `completed_with_full_evidence`
- `completed_with_partial_evidence`
- `fallback_due_to_missing_data`

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/agent.py src/driverops_agent_lab/schemas.py tests/test_driverops_agent_lab.py
git commit -m "feat: ground recommendations with evidence"
```

### Task 4: Upgrade evaluation for planner metrics

**Files:**
- Modify: `src/driverops_agent_lab/eval.py`
- Modify: `src/driverops_agent_lab/cli.py`
- Test: `tests/test_driverops_cli.py`
- Create example: `examples/driverops/eval_report.json`

**Step 1: Write the failing test**

Extend evaluation tests to assert the report contains:

- `plan_validity`
- `step_execution_success_rate`
- `evidence_coverage`
- `fallback_rate`

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_cli.py -v`

Expected: FAIL because the report lacks planner-aware metrics.

**Step 3: Write minimal implementation**

Compute the new metrics from execution traces and grounded answer payloads.

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_cli.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/eval.py src/driverops_agent_lab/cli.py tests/test_driverops_cli.py examples/driverops/eval_report.json
git commit -m "feat: add planner-aware evaluation metrics"
```

### Task 5: Add minimal long-term memory layer

**Files:**
- Modify: `src/driverops_agent_lab/memory.py`
- Modify: `src/driverops_agent_lab/agent.py`
- Test: `tests/test_driverops_agent_lab.py`

**Step 1: Write the failing test**

Add tests that assert the agent can retain simple long-term preferences such as:

- preferred peak windows
- recurring campaign preference
- recent recommended zones

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: FAIL because only recent query history exists today.

**Step 3: Write minimal implementation**

Keep this YAGNI:

- no external database
- use in-memory long-term profile enrichment for now
- planner can read these fields when constructing future plans

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_agent_lab.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/memory.py src/driverops_agent_lab/agent.py tests/test_driverops_agent_lab.py
git commit -m "feat: add lightweight long-term memory"
```

### Task 6: Extend training-data exports from traces

**Files:**
- Modify: `src/driverops_agent_lab/training_data.py`
- Modify: `src/driverops_agent_lab/cli.py`
- Test: `tests/test_driverops_cli.py`
- Create example: `examples/driverops/training_samples.jsonl`

**Step 1: Write the failing test**

Add tests that expect exported records to contain:

- plan steps
- observations
- grounded answer sections
- stop reason
- metadata for future SFT / preference / reward usage

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_cli.py -v`

Expected: FAIL because the current export is too shallow.

**Step 3: Write minimal implementation**

Upgrade training exports to include trace-rich fields, but keep the schema simple and JSONL-friendly.

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_cli.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/training_data.py src/driverops_agent_lab/cli.py tests/test_driverops_cli.py examples/driverops/training_samples.jsonl
git commit -m "feat: export trace-rich training samples"
```

### Task 7: Add failure taxonomy and review artifacts

**Files:**
- Create: `src/driverops_agent_lab/failure_review.py`
- Modify: `src/driverops_agent_lab/eval.py`
- Modify: `src/driverops_agent_lab/cli.py`
- Test: `tests/test_driverops_cli.py`
- Create example: `examples/driverops/failure_review.json`

**Step 1: Write the failing test**

Add tests that expect a failure review export to categorize issues such as:

- planning_error
- missing_evidence
- wrong_tool_choice
- weak_recommendation
- fallback_triggered

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src pytest tests/test_driverops_cli.py -v`

Expected: FAIL because no failure taxonomy exists.

**Step 3: Write minimal implementation**

Generate a structured review artifact from evaluation results to support future data flywheel work.

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src pytest tests/test_driverops_cli.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add src/driverops_agent_lab/failure_review.py src/driverops_agent_lab/eval.py src/driverops_agent_lab/cli.py tests/test_driverops_cli.py examples/driverops/failure_review.json
git commit -m "feat: add failure taxonomy exports"
```

## Skill-Update Rule For This Work

Do **not** update `skills/jd-to-offer/` after every code change.
Only make a minimal skill update if one of these becomes true:

1. The user workflow changes in a repeatable way
2. The required case outputs change
3. A reusable execution artifact becomes mandatory for future projects

Likely minimal future skill additions, if warranted:

- “flag flagship projects that lack planner traces”
- “prefer evidence-grounded recommendations in project blueprints”
- “include failure-taxonomy outputs when training loops are part of the role”

## Recommended Execution Order

1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Task 6
7. Task 7

This order keeps the data model ahead of execution, execution ahead of evaluation, and evaluation ahead of training artifacts.

Plan complete and saved to `docs/plans/2026-03-10-driverops-react-planner-implementation.md`.

Execution options after approval:

1. Subagent-Driven (this session)
2. Parallel Session (separate)
