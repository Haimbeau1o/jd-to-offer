---
name: jd-to-offer
description: Transform a target job description into a structured competency map, a detailed knowledge system, a web-verified resource pack, a flagship project blueprint, and interview-ready output files. Use when a user wants to analyze a JD, prepare for a role, build a role-aligned project, or generate reusable study and project plans from hiring requirements.
---

# JD to Offer

## Overview

Use this skill to turn a JD into a reusable preparation bundle. Combine local deterministic scripts with web browsing: parse the JD locally, map it to a competency taxonomy, browse for current official docs and primary papers, then generate a case bundle that is strong enough for project planning, resume positioning, and interview preparation.

## Workflow

1. Run `python skills/jd-to-offer/scripts/run_case.py scaffold-research ...` or `python -m jd_offer.cli scaffold-research ...` to create a per-case research template.
2. Browse the web for current high-quality resources. Prefer official docs, official repos, and primary papers.
3. Save the verified resources into a YAML override file that follows the scaffolded template shape.
4. Run `python skills/jd-to-offer/scripts/run_case.py generate ... --resource-overrides <path>` to inject the latest resources into the output bundle.
5. Inspect the generated competency map and project blueprint. If the JD is domain-specific, refine the emphasis manually instead of rewriting the whole bundle.
6. Validate the output folder with `skills/jd-to-offer/scripts/validate_case.py`.
7. If the flagship project in this repo is part of the delivery, refresh its reusable artifacts with `driverops_agent_lab.cli evaluate`, `export-training-data`, and `export-failure-review`.

## Required Output Bundle

Always produce these files in the case folder:

- `01_jd_decomposition.md`
- `02_knowledge_system.md`
- `03_resource_pack.md`
- `04_project_blueprint.md`
- `05_interview_assets.md`
- `manifest.yaml`

Load `references/output_contract.md` if you need the exact file contract.

## Resource Curation Rules

- Browse for current links whenever the user asks for the latest or best resources.
- Prefer official documentation over blogs for frameworks and tooling.
- Prefer primary papers over derivative summaries for methods such as CoT, ReAct, PPO, DPO, or GRPO.
- Mark in the resource pack why each resource matters for the JD instead of dumping a long link list.
- If the JD is business-specific, include at least one primary or official resource that grounds the business domain.
- Keep the latest web findings in an override YAML so the generation pipeline stays reproducible.

## Project Design Rules

- Build one flagship project, not many fragmented demos.
- Make the project runnable or at least technically end-to-end explainable.
- Map every major subsystem back to one or more top JD competencies.
- Keep the scope achievable in 2-6 weeks unless the user asks for a larger plan.
- Emphasize metrics, failure cases, and evaluation, not just architecture diagrams.

## Flagship Project Artifact Rules

When the generated case uses `DriverOps Agent Lab` as the flagship project, also treat these files as reusable delivery artifacts:

- `examples/driverops/eval_report.json`: planner-aware evaluation snapshot
- `examples/driverops/training_samples.jsonl`: trace-rich SFT / preference seed data
- `examples/driverops/failure_review.json`: failure taxonomy and review-ready error cases

Do not regenerate them for unrelated JD-only requests. Refresh them when the user explicitly wants the runnable flagship project, the project demo to stay current, or the training/evaluation loop to be part of the deliverable.

## Scripts

- `scripts/run_case.py`: wrapper around the local CLI to scaffold research templates and generate a case bundle
- `scripts/validate_case.py`: verify the output folder contains the required files
- `driverops_agent_lab.cli evaluate`: refresh planner-aware evaluation artifacts for the flagship project
- `driverops_agent_lab.cli export-training-data`: export trace-rich training samples
- `driverops_agent_lab.cli export-failure-review`: export failure taxonomy and review artifacts

## References

- `references/workflow.md`: expanded step-by-step operating guide
- `references/output_contract.md`: required output semantics and quality bar
