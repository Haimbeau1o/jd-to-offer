# CommentOps Workflow Zoomable Canvas Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rebuild the workflow page into a zoomable, pannable SVG-based moderation chain so the online path is visually complete, interactive, and no longer obstructed by runtime detail panels.

**Architecture:** Keep the current FastAPI + vanilla HTML/JS stack. Reuse the node/edge coordinates already defined in `src/commentops_agent_lab/content.py`, render them inside an inline SVG viewport, and manage pan/zoom with lightweight client-side state instead of introducing React Flow.

**Tech Stack:** FastAPI, inline HTML/CSS/JavaScript, SVG, pytest, FastAPI TestClient

### Task 1: Lock the new interaction contract with tests

**Files:**
- Modify: `tests/test_commentops_app.py`
- Reference: `src/commentops_agent_lab/app.py`

**Step 1: Write the failing test**

Add assertions that `/workflow` contains:
- a zoomable SVG canvas container such as `workflowCanvasShell` / `workflowSvg`
- zoom controls such as `zoomInView`, `zoomOutView`, `resetView`
- a minimap anchor such as `workflowMinimap`
- interaction copy describing drag/pan/zoom behavior

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_commentops_app.py::test_commentops_workflow_page_contains_interactive_chain -q`
Expected: FAIL because the current workflow page only renders lane rows and has no canvas/minimap controls.

### Task 2: Rebuild the workflow page layout

**Files:**
- Modify: `src/commentops_agent_lab/app.py`
- Reference: `src/commentops_agent_lab/content.py`

**Step 1: Update layout structure**

Change the workflow page to:
- left column top: preset cases
- left column bottom: main workflow canvas panel
- right column: current run, node detail, references

**Step 2: Add SVG canvas scaffolding**

Render:
- an inline `<svg>` with a stable `viewBox`
- edges from payload coordinates
- clickable node groups using the existing absolute positions
- active/current node styling based on preset execution state

**Step 3: Add zoom/pan controls**

Implement:
- drag-to-pan
- zoom in / zoom out buttons
- reset / fit view
- wheel zoom inside the canvas region only

**Step 4: Add bottom-left minimap**

Render a compact overview map inside the main canvas panel and allow click-to-focus / jump viewport behavior.

### Task 3: Strengthen research and implementation traceability

**Files:**
- Modify: `src/commentops_agent_lab/content.py`
- Modify: `src/commentops_agent_lab/app.py`

**Step 1: Add implementation research references**

Add official references covering:
- SVG `viewBox`
- SVG scripting / event handling
- React Flow viewport, controls, minimap concepts as benchmark references

**Step 2: Reflect the design rationale in UI**

Show brief copy explaining:
- why the page now uses a zoomable canvas
- why the minimap is placed away from `Current Run`
- why the stack still avoids a heavier node-editor runtime for now

### Task 4: Verify end-to-end

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

**Step 3: Manual verification**

Run the app and inspect:
- `/demo`
- `/workflow`
- `/research-log`

Confirm:
- presets switch
- workflow canvas zooms/pans cleanly
- minimap stays inside the lower-left corner of the canvas
- right-side runtime panels no longer overlap the main chain
