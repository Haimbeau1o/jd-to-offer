# CommentOps Architecture And Evals Reframe Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reframe the moderation-agent research content so it clearly starts from business understanding, abstracts the optimization problem, compares agent paradigms, defines evaluation methods, and closes the loop back into optimization.

**Architecture:** Keep the current FastAPI + data-driven page structure, but enrich `research_log_payload()` with business, architecture, and evaluation-specific sections sourced from official documents. Update the research page to surface those sections in a more explicit decision-making narrative, and add a companion markdown artifact for deeper interview/project explanation.

**Tech Stack:** FastAPI, inline HTML rendering, Python data payloads, pytest, markdown docs

### Task 1: Lock the new research narrative with tests

**Files:**
- Modify: `tests/test_commentops_app.py`
- Reference: `src/commentops_agent_lab/content.py`

**Step 1: Write the failing test**

Extend the research-log page test to assert the rendered page includes:
- `业务理解与优化目标`
- `问题抽象`
- `LangGraph`
- `Graph API`
- `评测指标`

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_app.py::test_commentops_research_log_page_contains_sources_and_eval_loop -q`
Expected: FAIL because the current page does not yet expose these architecture-specific concepts.

### Task 2: Rebuild the research content model

**Files:**
- Modify: `src/commentops_agent_lab/content.py`

**Step 1: Expand research sections**

Add sections for:
- business understanding and objective function
- problem abstraction and optimization points
- agent paradigm research
- LangGraph-style node selection rationale
- evaluation metrics and methods
- optimization loop

**Step 2: Expand official sources**

Add official sources covering:
- LangGraph workflows/Graph API/human-in-the-loop
- Anthropic agent architecture patterns
- TikTok moderation workflow / transparency / role requirements
- Meta high-impact human-review boundary
- OpenAI moderation and eval guidance

### Task 3: Update page rendering to reflect the new structure

**Files:**
- Modify: `src/commentops_agent_lab/app.py`

**Step 1: Replace generic side cards with decision-oriented cards**

Add right-side cards that explicitly summarize:
- recommended agent paradigm
- key business optimization points
- evaluation dimensions
- optimization loop

**Step 2: Keep existing links and readability**

Ensure the new structure still renders cleanly without changing routes.

### Task 4: Add a deeper markdown research artifact

**Files:**
- Create: `docs/examples/2026-04-01-commentops-agent-architecture-and-eval-framework.md`

**Step 1: Write the detailed sourced analysis**

Document:
- why this is not a classifier project
- why a bounded single-agent DAG is preferred over a supervisor multi-agent setup
- how LangGraph nodes would be selected from business state transitions
- what to evaluate online vs offline vs human-review stages
- how failures become SFT / preference / reward inputs

### Task 5: Verify end-to-end

**Files:**
- Test: `tests/test_commentops_app.py`
- Test: `tests/test_commentops_agent_lab.py`
- Test: `tests/test_commentops_cli.py`
- Test: `tests/test_cli.py`

**Step 1: Run focused tests**

Run: `pytest tests/test_commentops_app.py -q`
Expected: PASS

**Step 2: Run broader regression tests**

Run: `pytest tests/test_commentops_agent_lab.py tests/test_commentops_cli.py tests/test_commentops_app.py tests/test_cli.py -q`
Expected: PASS
