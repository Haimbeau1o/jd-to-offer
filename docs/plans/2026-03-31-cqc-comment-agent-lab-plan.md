# CQC Comment Agent Lab Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Build a new repository centered on a comment-moderation review Agent that demonstrates the exact capabilities implied by the Douyin CQC JD: business-oriented Agent design, policy-grounded decisioning, workflow automation, lightweight post-training, human-in-the-loop operations, and measurable quality improvement.

**Architecture:** The project should separate three loops. The online loop handles comment review with routing, policy retrieval, evidence extraction, decision aggregation, and escalation. The offline loop evaluates precision, recall, escalation strategy, audit quality, latency, and simulated business impact. The data flywheel loop converts disagreement cases, appeal cases, and hard samples into SFT or preference data so the system can continuously improve instead of staying as a static demo.

**Tech Stack:** Python 3.11, FastAPI, Pydantic, SQLite or PostgreSQL, BM25 plus optional vector retrieval, OpenAI-compatible model endpoint or vLLM, PyTorch plus TRL for SFT and preference tuning, pytest, lightweight reviewer demo UI.

## JD Deep Analysis

### What this role really is

This is not a pure base-model research role and not a simple prompt-engineering application role.

The core of the JD is: take a real moderation workflow in the comment domain, identify where large models can either automate decisions or significantly improve reviewer efficiency and quality, then build an auditable Agent or workflow system that can survive real business constraints.

The key phrase is not just `大模型`, but `审核 Agent`, `评论方向`, `业务流程`, `收益`, `持续优化`, and `全生命周期管理`.

That means the interviewer will care about whether we can answer all of these questions:

- Which moderation stages should stay rule-based, which should become model-based, and which should be handled by an Agent plus human review?
- How do we make an LLM decision auditable enough for a safety or trust workflow?
- How do we measure business gain instead of only reporting model-side metrics?
- How do we plug the model into data, rules, strategy operations, and deployment, not just into a demo page?
- When do we use prompt plus tools, and when do we need SFT or preference optimization?

### Core capability map hidden inside the JD

1. `评论审核业务建模`
   - Understand the unique challenges of comment moderation: short text, slang, sarcasm, context dependence, conversation chains, repeated offenders, and category overlap.
   - Translate moderation problems into concrete decision states such as `pass`, `reject`, `escalate`, `need more context`, and `need policy lookup`.

2. `Agent or Workflow design`
   - Build an automated chain rather than a single classifier.
   - Show routing, tool invocation, fallback logic, confidence gating, and failure recovery.

3. `策略与业务收益设计`
   - Link model actions to business KPIs such as reviewer throughput, auto-review coverage, miss rate, wrong-kill rate, appeal overturn rate, and latency.
   - Explain why a given workflow actually improves quality or efficiency.

4. `后训练与数据闭环`
   - Show that model behavior can be improved by SFT or preference-style optimization.
   - Use hard cases, disagreement cases, and appeal cases as training signals.

5. `跨团队协作与生命周期管理`
   - Make room for rule teams, policy teams, data teams, and operations teams inside the system design.
   - Represent how test, gray release, policy changes, and feedback loops are managed.

6. `部署与持续优化`
   - Think about confidence thresholds, fallback, observability, error taxonomies, and model version management.
   - Avoid building something that only works as a notebook demo.

### Hidden expectations the JD does not say explicitly

- The role probably values `auditable moderation` more than fancy reasoning traces.
- The role probably expects `rules + retrieval + model + human escalation` instead of “one LLM decides everything”.
- The role likely values `safe automation boundaries` more than raw automation rate.
- The role likely expects a framework for `policy updates and fast iteration`, because moderation categories and standards change often.
- The role expects we can talk to both algorithm and operations stakeholders, so the project must expose levers that operations can understand.

## Why We Should Create a New Repository

The current repo is optimized around `JD -> flagship project -> interview assets`, and its built-in flagship project is `DriverOps Agent Lab`.

That structure is reusable, but the business domain is not.

For this JD, directly reusing the driver or supply-demand project would create the wrong signal:

- The business language is wrong: we need reviewer workflow, policy grounding, risk categories, and audit decisions, not recommendation or driver strategy.
- The core tools are different: we need policy lookup, comment context retrieval, user history, risk aggregation, and escalation queues.
- The core metrics are different: we need hit rate, wrong-kill rate, appeal overturn rate, reviewer efficiency, and audit latency.
- The core story is different: we need trust and safety operations, not user-side intelligent assistance.

The right move is to create a new repo, while reusing only the good patterns from the current one:

- deterministic case generation thinking
- one flagship project instead of many scattered demos
- offline evaluation artifacts
- training-data export and failure review mindset

## Solution Options

### Option A: Reviewer Copilot

Build a sidecar assistant for human moderators. It reads comment text, fetches policy clauses, suggests risk labels, highlights evidence spans, and drafts the recommendation for human confirmation.

Strengths:

- Very realistic and easy to explain
- Naturally matches cross-team collaboration
- Lower risk and faster MVP

Weaknesses:

- Agent depth is limited
- Harder to show full automation strategy
- Post-training story is weaker unless extended

### Option B: Comment Moderation Agent Lab

Build a full review workflow system that can decide `pass`, `reject`, or `escalate`, with tool usage, policy grounding, evidence output, confidence gating, failure review, and data export for SFT or preference training.

Strengths:

- Best match to the JD wording
- Covers workflow, Agent, business optimization, and post-training in one project
- Easier to map every subsystem back to a JD bullet

Weaknesses:

- Scope is larger
- Requires careful boundary design to stay realistic

### Option C: Moderation Post-Training Sandbox

Build a training and evaluation platform focused on moderation data curation, SFT, DPO, and reward design, with minimal online workflow.

Strengths:

- Strong on model optimization narrative
- Good for algorithm-heavy interviews

Weaknesses:

- Weak on business workflow and lifecycle management
- Misses much of the Agent wording in the JD

### Recommendation

Choose `Option B: Comment Moderation Agent Lab`.

This is the only direction that naturally covers all five JD responsibilities at once:

- business problem discovery
- workflow and Agent design
- tool and algorithm integration
- cross-team lifecycle management
- deployment and continuous optimization

## Recommended Flagship Project

### Repository name

`commentops-agent-lab`

### One-line positioning

An end-to-end comment-governance Agent lab for policy-grounded moderation decisions, reviewer escalation, evaluation, and post-training data flywheel.

### Core user story

Given a user comment, its conversation context, lightweight account signals, and current moderation policies, the system should:

1. identify the risk scenario
2. fetch the relevant policy and similar historical cases
3. extract risky evidence spans
4. decide `pass`, `reject`, or `escalate`
5. provide a short reviewer-facing rationale
6. log failures and disagreements for later iteration

### Why this project matches the JD tightly

- `基于业务挖掘可自动审核或提效场景`
  - Show which categories are suitable for auto-pass, auto-reject, and human escalation.
- `制定大模型应用策略`
  - Show confidence thresholds, decision policy, and ROI trade-offs.
- `通过 Workflow、Agent、SFT 解决业务问题`
  - Show the whole workflow, then export hard cases for SFT and preference optimization.
- `推动从测试到应用的全生命周期管理`
  - Show eval sets, failure taxonomy, versioning, and policy refresh workflow.
- `协调资源并正确部署持续优化`
  - Show how policy, data, ops, and modeling fit together.

## Product Scope

### MVP capabilities

- Comment ingestion with thread context
- Policy retrieval and clause citation
- Risk category routing
- Evidence span extraction
- Decisioning with `pass`, `reject`, `escalate`
- Reviewer-facing explanation
- Failure review export
- Offline evaluation report

### Phase 2 capabilities

- Similar-case retrieval
- User history or repeat-risk features
- Confidence calibration and threshold tuning
- Preference data export from reviewer disagreement
- Lightweight SFT baseline

### Phase 3 capabilities

- Policy change simulation
- Queue-level business analysis
- Shadow deployment report
- Appeal-case replay and regression suite

### Explicit non-goals

- Do not build a giant multi-agent platform in v1.
- Do not chase multimodal moderation unless the JD expands beyond comments.
- Do not over-invest in fancy UI before the evaluation and workflow story is solid.

## System Design

### Main workflow

```text
Comment Input
  -> Context Loader
  -> Risk Router
  -> Policy Retriever
  -> Evidence Extractor
  -> Decision Aggregator
      -> pass
      -> reject
      -> escalate
  -> Reviewer Rationale
  -> Audit Log
  -> Failure Review / Training Export
```

### Core tools

- `load_comment_context`: fetch parent comment, thread snippet, and discussion direction
- `retrieve_policy_clauses`: fetch the most relevant moderation standards
- `search_similar_cases`: surface historically similar adjudicated cases
- `lookup_user_risk_signals`: provide lightweight structured risk hints
- `record_decision_trace`: persist rationale, evidence, and action outcome

### Core entities

- `CommentCase`: raw comment, thread context, author profile, language features
- `PolicyClause`: category, severity, allowed patterns, prohibited patterns, examples
- `ReviewDecision`: label, confidence, supporting clauses, evidence spans, escalation reason
- `ReviewOutcome`: final adjudication, reviewer override, appeal result, latency, business tags

### Decision policy

- High-confidence, policy-grounded harmful cases can be auto-reject candidates
- Low-risk, high-certainty benign cases can be auto-pass candidates
- Ambiguous, contextual, or sensitive cases must escalate
- The system must always log why a case was escalated rather than silently failing

## Metrics That Matter

### Model or workflow metrics

- Category precision and recall
- Policy citation accuracy
- Evidence span quality
- Escalation precision
- Tool success rate
- End-to-end latency

### Business metrics

- Auto-review coverage under risk constraints
- Wrong-kill rate
- Missed-violation rate
- Reviewer throughput uplift
- Appeal overturn rate
- Queue backlog reduction

### Interview-friendly narrative

The strongest framing is:

`I did not optimize for maximal automation. I optimized for safe automation boundaries, explainable decisions, and a feedback loop that improves reviewer efficiency without increasing risk.`

## Planned Repository Layout

```text
commentops-agent-lab/
  README.md
  pyproject.toml
  docs/
    domain/
      moderation-taxonomy.md
      policy-lifecycle.md
      evaluation-spec.md
    architecture/
      workflow.md
      data-flywheel.md
  src/commentops_agent_lab/
    __init__.py
    cli.py
    api.py
    app.py
    schemas.py
    domain/
      decision_policy.py
      moderation_taxonomy.py
    workflows/
      review_agent.py
      escalation_policy.py
    tools/
      context_loader.py
      policy_retriever.py
      similar_case_search.py
      risk_lookup.py
    retrieval/
      policy_index.py
      case_index.py
    evaluators/
      offline_eval.py
      metrics.py
    training/
      export_sft_data.py
      export_preference_data.py
    data/
      fixtures.py
  examples/
    policies/
      comment_policy_v1.yaml
    cases/
      sample_review_cases.jsonl
    eval/
      baseline_eval_report.json
      failure_review.json
  tests/
    test_cli.py
    test_review_agent.py
    test_policy_retriever.py
    test_escalation_policy.py
    test_offline_eval.py
```

## Execution Plan

### Task 1: Freeze the domain model and moderation contract

**Files:**

- Create: `README.md`
- Create: `docs/domain/moderation-taxonomy.md`
- Create: `src/commentops_agent_lab/schemas.py`
- Create: `tests/test_review_agent.py`

**Steps:**

1. Write tests that define the core request and response contract for a review case.
2. Model `CommentCase`, `PolicyClause`, `ReviewDecision`, and `ReviewOutcome`.
3. Freeze the allowed moderation actions as `pass`, `reject`, `escalate`.
4. Verify the schema can represent ambiguity and escalation reasons.

**Run:**

```bash
pytest tests/test_review_agent.py -v
```

**Expected:**

The first passing test should confirm the repo already knows how to represent a full moderation case before any Agent logic exists.

### Task 2: Build policy and case retrieval foundations

**Files:**

- Create: `examples/policies/comment_policy_v1.yaml`
- Create: `examples/cases/sample_review_cases.jsonl`
- Create: `src/commentops_agent_lab/tools/policy_retriever.py`
- Create: `src/commentops_agent_lab/tools/context_loader.py`
- Create: `src/commentops_agent_lab/retrieval/policy_index.py`
- Create: `tests/test_policy_retriever.py`

**Steps:**

1. Prepare a small but realistic policy file with categories, severity, and examples.
2. Prepare sample review cases with benign, harmful, contextual, and ambiguous comments.
3. Implement retrieval that returns relevant policy clauses and thread context.
4. Verify the retriever surfaces the expected policy for obvious cases.

**Run:**

```bash
pytest tests/test_policy_retriever.py -v
```

### Task 3: Implement the single-agent moderation workflow

**Files:**

- Create: `src/commentops_agent_lab/workflows/review_agent.py`
- Create: `src/commentops_agent_lab/domain/decision_policy.py`
- Create: `src/commentops_agent_lab/tools/risk_lookup.py`
- Modify: `tests/test_review_agent.py`

**Steps:**

1. Write failing tests for three golden paths: clear benign, clear harmful, ambiguous contextual case.
2. Implement a review workflow that calls retrieval tools and emits a structured decision.
3. Add confidence gating so uncertain cases escalate instead of over-asserting.
4. Verify the workflow produces a reviewer-facing rationale and evidence spans.

**Run:**

```bash
pytest tests/test_review_agent.py -v
```

### Task 4: Add escalation policy and audit logging

**Files:**

- Create: `src/commentops_agent_lab/workflows/escalation_policy.py`
- Create: `src/commentops_agent_lab/api.py`
- Create: `src/commentops_agent_lab/app.py`
- Create: `tests/test_escalation_policy.py`

**Steps:**

1. Define explicit escalation triggers such as low confidence, policy conflict, insufficient context, or high-risk category.
2. Implement structured audit logs for each decision.
3. Expose a minimal API endpoint for review requests and returned traces.
4. Verify high-risk ambiguity escalates deterministically.

**Run:**

```bash
pytest tests/test_escalation_policy.py -v
```

### Task 5: Build offline evaluation and failure review artifacts

**Files:**

- Create: `src/commentops_agent_lab/evaluators/offline_eval.py`
- Create: `src/commentops_agent_lab/evaluators/metrics.py`
- Create: `tests/test_offline_eval.py`
- Create: `examples/eval/baseline_eval_report.json`
- Create: `examples/eval/failure_review.json`

**Steps:**

1. Define evaluation metrics for moderation accuracy, escalation quality, and policy grounding.
2. Run the workflow against the sample dataset.
3. Export an evaluation report and a failure taxonomy file.
4. Verify the artifacts can support resume and interview narratives.

**Run:**

```bash
pytest tests/test_offline_eval.py -v
python -m commentops_agent_lab.cli evaluate --outdir examples/eval
```

### Task 6: Add data flywheel export for SFT and preference learning

**Files:**

- Create: `src/commentops_agent_lab/training/export_sft_data.py`
- Create: `src/commentops_agent_lab/training/export_preference_data.py`
- Modify: `README.md`

**Steps:**

1. Convert successful traces into structured SFT samples.
2. Convert reviewer disagreement or appeal cases into preference pairs.
3. Document how failure review feeds model improvement.
4. Keep the first version small and explainable rather than over-optimized.

**Run:**

```bash
python -m commentops_agent_lab.cli export-sft --outpath examples/eval/sft_samples.jsonl
python -m commentops_agent_lab.cli export-preferences --outpath examples/eval/preference_pairs.jsonl
```

### Task 7: Package the project as an interview-ready flagship demo

**Files:**

- Modify: `README.md`
- Create: `docs/architecture/workflow.md`
- Create: `docs/architecture/data-flywheel.md`

**Steps:**

1. Write the project narrative in recruiter-friendly and interviewer-friendly language.
2. Add one diagram for workflow and one diagram for the feedback loop.
3. Make sure every major module maps back to one JD responsibility.
4. Document what is real, what is simulated, and what would be productionized next.

## Suggested Delivery Phases

### Phase 0: Planning

- Lock project name, scope boundary, and evaluation story
- Freeze the moderation taxonomy and sample categories

### Phase 1: MVP workflow

- Finish policy retrieval, single-agent review flow, and escalation

### Phase 2: Evaluation

- Produce baseline report, failure review, and business metric framing

### Phase 3: Model-improvement story

- Export SFT and preference data
- Add one lightweight post-training experiment or simulated training pipeline

### Phase 4: Interview packaging

- Polish README, architecture docs, and demo cases
- Prepare resume bullets and project talking points

## Final Recommendation

The new repo should not present itself as “an AI that automatically censors comments”.

It should present itself as:

`a policy-grounded comment review Agent with safe automation boundaries, human escalation, and a measurable optimization loop.`

That framing is both technically stronger and much more aligned with how this JD describes value creation.
