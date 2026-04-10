---
name: jd-resume-latex
description: Use when adapting a resume to a target JD, packaging one internship or project to fit a role, producing LaTeX-ready resume edits, or checking whether resume claims, source evidence, and final rendering form a complete closed loop.
---

# JD Resume LaTeX

## Overview

Turn a target JD into resume decisions, not just notes. Use this skill to decide what the resume must prove, which experience should carry that proof, how far each packaging claim can go, and how to sync the final wording into the LaTeX source of truth.

Keep the workflow evidence-first. A stronger sentence is only valid when it is backed by:
- user-confirmed facts
- local repo artifacts
- official company or product sources
- official docs or primary papers

## Workflow

### 1. Build or reuse the JD understanding layer

Start from the best available JD artifact:
- If the user gives a JD markdown file, parse it and generate or refresh a case bundle.
- If this repo already contains a role pack, reuse it instead of redoing work.
- If the role is business-specific, add one layer above keyword matching:
  - what business loop is being optimized
  - what metrics matter
  - what proof forms the interviewer expects

Prefer reusing:
- `skills/jd-to-offer`
- `cases/`
- `docs/examples/`
- `docs/plans/`

Load `references/workflow.md` for the operating sequence.

### 2. Derive the proof map

For the target role, always produce three buckets:

- `Must Prove`
  The most important capabilities the resume needs to establish directly.
- `Can Bridge`
  Adjacent skills that can be transferred from a different domain with a clear explanation.
- `Must Not Fake`
  Capabilities that sound tempting but are not supported by the candidate's actual work.

If the role is highly domain-specific, do not let one internship overclaim the domain. Instead:
- let the internship prove transferable technical base
- let one project or blueprint prove domain learning
- let interview assets explain the bridge

Load `references/source-rules.md` before finalizing bullets.

### 3. Package one experience with claim ceilings

For the chosen internship or project, write:
- one dominant storyline
- one one-sentence summary
- up to three final bullets
- one interview bridge sentence
- one explicit forbidden-claims list

Every bullet must stay inside one of these levels:
- `confirmed`: directly supported by known facts or artifacts
- `defensible`: stronger wording that is still consistent with the evidence
- `forbidden`: overclaim, unsupported metric, or fake domain ownership

When multiple storylines are possible, choose the one that:
- proves the top JD requirements fastest
- stays closest to real work done
- leaves the fewest holes under follow-up questions

### 4. Convert resume decisions into LaTeX edits

The final resume source of truth is not this repo. It is the external LaTeX project:
- `/Volumes/passport/简历/latex-resume`

Do not maintain a second long-lived resume body in this repo unless the user explicitly wants an intermediate draft.

Use these targets:
- `profile.tex` for role title and identity fields
- `content.tex` for bullets, section ordering, skill tags, and highlights
- `resume-*.tex` thin entry files only when a dedicated mode or theme variant is needed

Load `references/latex-rules.md` before editing.

### 5. Verify the closed loop

Before claiming the chain is complete, verify all of these:
- the JD proof map is explicit
- each bullet has a clear source ceiling
- the chosen experience does not overclaim business ownership
- the LaTeX file has been updated in the real source-of-truth project
- the PDF compiles
- `pdftotext -layout` still shows the important fields and sections cleanly enough

## Output Contract

The minimum acceptable output from this skill is:
- JD proof map
- experience packaging memo
- final resume bullets
- LaTeX sync instructions or actual edits
- verification evidence

## Reuse First

Before writing anything from scratch, check whether these already exist and are reusable:
- `docs/resume_latex_reference.md`
- `docs/examples/2026-04-10-ringconn-internship-packaging.md`
- `docs/examples/2026-04-10-ringconn-to-didi-freight-final-packaging.md`
- freight or Didi-related packs under `docs/examples/` and `docs/plans/`

## Common Mistakes

- Treating JD adaptation as keyword replacement instead of proof selection
- Letting one internship fake a full business domain it never touched
- Writing more than three weak bullets instead of three strong bullets
- Editing generated PDFs instead of the LaTeX source project
- Optimizing only for appearance and forgetting text extraction or verification

## Quick Start

If the user says “按这个 JD 改简历”, do this in order:

1. Build or reuse the JD understanding layer.
2. Write `Must Prove / Can Bridge / Must Not Fake`.
3. Pick the one experience that should carry the proof.
4. Produce one-sentence summary, three bullets, and forbidden claims.
5. Sync the final wording to `/Volumes/passport/简历/latex-resume/content.tex`.
6. Compile and inspect the PDF plus `pdftotext`.
