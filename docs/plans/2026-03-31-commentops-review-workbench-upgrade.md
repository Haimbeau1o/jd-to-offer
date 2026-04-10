# CommentOps Review Workbench Upgrade Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Upgrade the existing `commentops_agent_lab` from a minimal moderation API into a reviewer-oriented comment governance workbench that better demonstrates business workflow design, policy-grounded decisioning, escalation control, appeal awareness, and evaluation outputs aligned with the CQC JD.

**Architecture:** Keep a single-agent moderation workflow, but enrich the surrounding system. The upgraded flow should model the real review chain: case intake, context loading, policy retrieval, similar-case retrieval, risk signal synthesis, decision policy, queue routing, reviewer notes, and offline business-aware evaluation. The web demo should become a small review console rather than a raw JSON playground.

**Tech Stack:** Python 3.11, FastAPI, Pydantic, Typer, pytest, lightweight in-memory retrieval over YAML/JSONL fixtures, HTML/CSS/vanilla JS review console.

### Task 1: Expand the review contract and business entities

**Files:**
- Modify: `src/commentops_agent_lab/schemas.py`
- Modify: `examples/commentops/cases/sample_review_cases.jsonl`
- Test: `tests/test_commentops_agent_lab.py`

**Step 1: Write failing tests**

Add tests that require the response to include:
- queue routing
- business impact notes
- similar cases
- user risk signals
- appeal or override hints

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_agent_lab.py -v`

Expected: FAIL because the schema and agent do not yet expose the new fields.

**Step 3: Write minimal implementation**

Extend the contract so one review response can represent:
- case metadata
- risk inputs
- policy evidence
- routed queue
- recommended next actions
- reviewer notes
- similar cases

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_commentops_agent_lab.py -v`

Expected: PASS.

### Task 2: Add richer fixtures and retrieval inputs

**Files:**
- Modify: `examples/commentops/policies/comment_policy_v1.yaml`
- Modify: `examples/commentops/cases/sample_review_cases.jsonl`
- Modify: `src/commentops_agent_lab/data.py`
- Test: `tests/test_commentops_agent_lab.py`

**Step 1: Write failing tests**

Add tests that require:
- explicit review queue assignment for risky cases
- similar historical cases for contextual comments
- user risk flags for repeat offenders or appealed users

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_agent_lab.py -v`

Expected: FAIL because the fixtures do not yet carry enough metadata.

**Step 3: Write minimal implementation**

Expand fixtures with:
- account-level risk hints
- policy version
- reporter counts
- historical adjudications
- appeal or override status

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_commentops_agent_lab.py -v`

Expected: PASS.

### Task 3: Upgrade the moderation agent into a review workflow engine

**Files:**
- Modify: `src/commentops_agent_lab/agent.py`
- Test: `tests/test_commentops_agent_lab.py`

**Step 1: Write failing tests**

Add tests that require:
- ambiguous comments route to a human review queue
- explicit threats route to a priority queue
- repeat-risk users receive stronger review notes
- similar cases are surfaced for contextual ambiguity

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_agent_lab.py -v`

Expected: FAIL because the agent only returns a minimal decision.

**Step 3: Write minimal implementation**

Implement:
- risk signal synthesis
- queue routing
- similar-case lookup
- business impact summary
- recommended reviewer actions

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_commentops_agent_lab.py -v`

Expected: PASS.

### Task 4: Extend evaluation and training exports

**Files:**
- Modify: `src/commentops_agent_lab/eval.py`
- Modify: `src/commentops_agent_lab/training_data.py`
- Modify: `tests/test_commentops_cli.py`

**Step 1: Write failing tests**

Add tests that require new report metrics such as:
- auto-pass rate
- auto-reject rate
- human-review rate
- queue routing accuracy

Add training export checks for:
- queue metadata
- similar-case metadata
- business tags

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_cli.py -v`

Expected: FAIL because exports are too shallow.

**Step 3: Write minimal implementation**

Upgrade evaluation and data export so they can support interview storytelling and future post-training.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_commentops_cli.py -v`

Expected: PASS.

### Task 5: Replace the raw JSON playground with a review workbench

**Files:**
- Modify: `src/commentops_agent_lab/app.py`

**Step 1: Write failing tests**

No separate UI test required in this phase. Validate via endpoint and manual review.

**Step 2: Write minimal implementation**

Upgrade the demo page into a moderation workbench with:
- case presets
- policy hits panel
- decision card
- queue routing card
- risk signals card
- similar cases section
- reviewer recommendation panel

**Step 3: Verify manually**

Run:

```bash
PYTHONPATH=src python -m commentops_agent_lab.cli serve --host 127.0.0.1 --port 8002
```

Open:
- `http://127.0.0.1:8002/demo`
- `http://127.0.0.1:8002/docs`

### Task 6: Refresh artifacts and full verification

**Files:**
- Modify: `README.md`
- Create or refresh: `examples/commentops/eval/baseline_eval_report.json`
- Create or refresh: `examples/commentops/eval/sft_samples.jsonl`
- Create or refresh: `examples/commentops/eval/preference_pairs.jsonl`

**Step 1: Run full verification**

Run:

```bash
pytest tests/test_commentops_agent_lab.py tests/test_commentops_cli.py tests/test_cli.py -q
PYTHONPATH=src python -m commentops_agent_lab.cli evaluate --outpath examples/commentops/eval/baseline_eval_report.json
PYTHONPATH=src python -m commentops_agent_lab.cli export-sft --outpath examples/commentops/eval/sft_samples.jsonl
PYTHONPATH=src python -m commentops_agent_lab.cli export-preferences --outpath examples/commentops/eval/preference_pairs.jsonl
```

**Step 2: Confirm outcomes**

Expected:
- tests pass
- eval report contains business-aware metrics
- exports contain richer metadata for downstream training or review analysis
