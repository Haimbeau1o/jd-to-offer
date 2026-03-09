---
name: jd-to-offer
description: Transform a target job description into a structured competency map, a detailed knowledge system, a web-verified resource pack, a flagship project blueprint, and interview-ready output files. Use when a user wants to analyze a JD, prepare for a role, build a role-aligned project, or generate reusable study and project plans from hiring requirements.
---

# JD to Offer

## Overview

Use this skill to turn a JD into a reusable preparation bundle. Combine local deterministic scripts with web browsing: parse the JD locally, map it to a competency taxonomy, browse for current official docs and primary papers, then generate a case bundle that is strong enough for project planning, resume positioning, and interview preparation.

## Workflow

1. Run `skills/jd-to-offer/scripts/run_case.py` or `python -m jd_offer.cli generate ...` to parse the JD and scaffold the five required output files.
2. Inspect the generated competency map and knowledge system. If the JD is domain-specific, refine the emphasis manually instead of rewriting the whole bundle.
3. Browse the web for current high-quality resources. Prefer official docs, official repos, and primary papers. Refresh stale links before finalizing the resource pack.
4. Upgrade the project blueprint so it is demoable, technically coherent, and aligned with the top-ranked competencies.
5. Validate the output folder with `skills/jd-to-offer/scripts/validate_case.py`.

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

## Project Design Rules

- Build one flagship project, not many fragmented demos.
- Make the project runnable or at least technically end-to-end explainable.
- Map every major subsystem back to one or more top JD competencies.
- Keep the scope achievable in 2-6 weeks unless the user asks for a larger plan.
- Emphasize metrics, failure cases, and evaluation, not just architecture diagrams.

## Scripts

- `scripts/run_case.py`: wrapper around the local CLI to generate a case bundle
- `scripts/validate_case.py`: verify the output folder contains the required files

## References

- `references/workflow.md`: expanded step-by-step operating guide
- `references/output_contract.md`: required output semantics and quality bar
