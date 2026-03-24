# README Homepage Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite the repository README into a polished homepage that clearly positions JD2Offer, highlights the resume + JD to flagship project workflow, and improves human readability plus GEO-style discoverability.

**Architecture:** Keep the README single-file and GitHub-native. Use an answer-first hero, structured capability sections, quick-start commands, a pipeline diagram, comparison framing, and FAQ-style sections that are easy for both humans and AI retrieval systems to parse.

**Tech Stack:** Markdown, GitHub-flavored Markdown, Mermaid, Shields badges.

### Task 1: Define README information architecture

**Files:**
- Create: `docs/plans/2026-03-24-readme-homepage-refresh.md`
- Modify: `README.md`

**Step 1: Write the failing test**

Use manual acceptance criteria:

- README must explain what the project is in the first screen
- README must expose resume + JD + flagship project positioning
- README must include quick start commands
- README must include output artifacts and repo architecture
- README must include FAQ or answer-first retrieval-friendly sections

**Step 2: Verify the current README fails the homepage bar**

Read `README.md` and note:

- current top section is informative but not homepage-like
- new harness-first positioning is not visible enough
- visual hierarchy is weaker than strong OSS homepage READMEs

**Step 3: Write minimal implementation**

Design a new structure:

- hero
- direct definition
- what you get
- why different
- pipeline diagram
- quick start
- architecture
- outputs
- FAQ

**Step 4: Verify it passes**

Review the rewritten README for clarity and alignment to current repo capabilities.

**Step 5: Commit**

```bash
git add README.md docs/plans/2026-03-24-readme-homepage-refresh.md
git commit -m "docs: redesign readme homepage"
```
