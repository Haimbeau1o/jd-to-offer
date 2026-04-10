# CommentOps Project Overview Presentation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a clearer project-overview presentation layer so the moderation-agent project reads as a coherent business-to-architecture-to-evals system, with explicit documentation and artifact surfacing.

**Architecture:** Keep the current FastAPI + data-driven HTML approach. Add a new overview payload and route that organizes the project into business framing, architecture choice, LangGraph mapping, metrics, and deliverables, then expose key markdown/docs/artifacts as part of the page.

**Tech Stack:** FastAPI, Python content payloads, inline HTML/CSS, pytest

### Task 1: Lock the overview-page contract with tests

**Files:**
- Modify: `tests/test_commentops_app.py`
- Reference: `src/commentops_agent_lab/app.py`

**Step 1: Write the failing test**

Add a test for `/project-overview` asserting the page includes:
- `项目全景`
- `业务理解`
- `LangGraph 映射`
- `文档与产出`
- `2026-04-01-commentops-agent-architecture-and-eval-framework.md`

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_app.py::test_commentops_project_overview_page_explains_full_story -q`
Expected: FAIL because the route does not exist yet.

### Task 2: Add overview content model

**Files:**
- Modify: `src/commentops_agent_lab/content.py`

**Step 1: Add a `project_overview_payload()` function**

Include:
- narrative ladder from business to optimization
- architecture comparison cards
- LangGraph mapping
- metrics matrix
- deliverables / docs list

### Task 3: Implement the overview page

**Files:**
- Modify: `src/commentops_agent_lab/app.py`

**Step 1: Add nav entry**

Expose the overview page in the top navigation.

**Step 2: Render overview page**

Create a page that clearly sequences:
- business understanding
- problem abstraction
- architecture selection
- metric system
- docs and generated artifacts

### Task 4: Add one presentation-oriented markdown doc

**Files:**
- Create: `docs/examples/2026-04-01-commentops-project-storyboard.md`

**Step 1: Write a concise presentation script**

Summarize:
- how to introduce the project
- how to explain the architecture choice
- how to explain metrics and optimization loop
- what deliverables prove depth

### Task 5: Verify end-to-end

**Files:**
- Test: `tests/test_commentops_app.py`
- Test: `tests/test_commentops_agent_lab.py`
- Test: `tests/test_commentops_cli.py`
- Test: `tests/test_cli.py`

**Step 1: Run focused tests**

Run: `pytest tests/test_commentops_app.py -q`
Expected: PASS

**Step 2: Run regression suite**

Run: `pytest tests/test_commentops_agent_lab.py tests/test_commentops_cli.py tests/test_commentops_app.py tests/test_cli.py -q`
Expected: PASS
