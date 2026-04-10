# Didi Freight Algorithm Prep Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Build a role-specific preparation pack for the Didi 2026 freight algorithm role, centered on one flagship demo, one interviewable project narrative adapted from internship work, and one AI-native system design playbook.

**Architecture:** Use a single integrated project instead of several scattered mini demos. The recommended core artifact is `FreightStrategyLab`: a lightweight freight marketplace sandbox that combines supply-demand forecasting, dispatch scoring, subsidy/uplift simulation, traffic allocation, offline evaluation, and an explanation layer. Around this core artifact, produce a resume-ready project story, interview assets, and a “how I would build this with Codex” system-design answer.

**Tech Stack:** Python 3.11, pandas, numpy, scikit-learn, LightGBM/XGBoost, OR-Tools, EconML/CausalML or doubly robust uplift baseline, PyTorch, FastAPI, Streamlit or lightweight web UI, Plotly, Markdown.

## Recommended Direction

### Option A: One integrated `FreightStrategyLab` project

- Best choice if the goal is “one thing that can both demo and interview well.”
- Strongest alignment to JD keywords: dispatch, pricing/subsidy, traffic allocation, causal inference, forecasting, LLM landing.
- Lets the user tell one coherent story: understand business -> model market -> make decisions -> evaluate value.

### Option B: Three separate mini projects

- Easier to start quickly.
- Weaker interview impact because the work looks fragmented and harder to narrate as one business system.

### Option C: Pure paper reproduction

- Good for theory depth.
- Weakest for “business understanding + rapid execution + can ship demo.”

**Recommendation:** Choose Option A. One integrated project is the most efficient way to prove business understanding, algorithm basics, and engineering ownership at the same time.

## Role Translation

This JD is not asking for a generic “AI application.” It is asking for someone who can think like a freight marketplace algorithm engineer.

The business objects that need to appear in the project are:

- freight orders
- drivers / trucks / vehicle types
- regions and time windows
- price / subsidy / payout
- order exposure / traffic distribution
- marketplace efficiency metrics

The algorithm layers that should appear in the project are:

- supply-demand forecasting
- dispatch or matching optimization
- subsidy or pricing intervention
- traffic allocation or ranking
- causal or counterfactual evaluation

The LLM part should be a plus point, not the core of the project. In this role, LLM is best positioned as:

- an operator copilot that explains why a strategy is chosen
- a natural-language analysis layer over structured algorithm outputs
- a report generator for decision review

It should not replace the core matching, pricing, or causal logic.

## Success Criteria

The plan is successful when all of the following are true:

- You can open one demo and explain, in 5 minutes, how the freight market state becomes dispatch / subsidy / traffic decisions.
- You have one project description that can replace or heavily rewrite one internship entry on the resume.
- You can answer a 10-minute system-design question about a freight intelligent trading system without drifting into empty buzzwords.
- You can explain the basic ideas of causal inference, matching/optimization, forecasting, and offline evaluation without obvious gaps.
- You have clear evidence artifacts: screenshots, metrics table, architecture diagram, demo script, and resume bullets.

## Default Timeline

Use a 4-week core plan plus 1 stretch week.

### Week 1

- Freeze scope, business framing, and metrics.
- Build the market simulator and the offline data schema.
- Finish the project blueprint and the interview narrative skeleton.

### Week 2

- Build forecasting and dispatch baselines.
- Define the KPI board for marketplace efficiency.
- Prepare the first stable demo scenario.

### Week 3

- Add subsidy/uplift logic and traffic allocation logic.
- Add offline comparison between baseline and improved policy.
- Start writing resume bullets and project story.

### Week 4

- Build the UI and explanation layer.
- Finish the system-design answer and Codex workflow playbook.
- Run mock interviews and harden weak knowledge points.

### Stretch Week 5

- Polish metrics, visuals, README-style explanation, and FAQ.
- Add one LLM-assisted analysis feature if the core pipeline is already stable.

## Repo Layout To Build

```text
examples/
  didi_2026_freight_algo_jd.md
  freight_strategy/
    sample_market_day.json
    sample_orders.json
    sample_drivers.json
    baseline_eval_report.json
    improved_eval_report.json
cases/
  didi-freight-2026/
    01_jd_decomposition.md
    02_knowledge_system.md
    03_resource_pack.md
    04_project_blueprint.md
    05_interview_assets.md
src/
  freight_strategy_lab/
    __init__.py
    schemas.py
    data.py
    forecast.py
    dispatch.py
    subsidy.py
    traffic.py
    eval.py
    app.py
    cli.py
tests/
  freight_strategy_lab/
    test_data.py
    test_forecast.py
    test_dispatch.py
    test_subsidy.py
    test_traffic.py
docs/
  examples/
    2026-04-10-didi-freight-demo-script.md
    2026-04-10-didi-freight-system-design-answer.md
    2026-04-10-didi-freight-resume-reframe.md
  plans/
    2026-04-10-didi-freight-algo-prep-plan.md
```

## Core Metrics To Use Everywhere

Do not let the project become a generic model playground. Every module should map back to marketplace metrics.

Recommended KPI set:

- order match rate
- driver response / acceptance rate
- average pickup distance or empty-load distance proxy
- on-time fulfillment rate
- subsidy spend
- incremental completion gain
- subsidy ROI
- traffic exposure concentration or fairness proxy
- city / region level stability

## Task 1: Freeze the freight problem framing

**Files:**

- Create: `examples/didi_2026_freight_algo_jd.md`
- Create: `cases/didi-freight-2026/01_jd_decomposition.md`
- Create: `cases/didi-freight-2026/02_knowledge_system.md`
- Create: `cases/didi-freight-2026/03_resource_pack.md`

**Deliverables:**

- A clean JD file saved into the repo.
- A role decomposition that translates the JD into capability axes.
- A knowledge checklist ordered by urgency.
- A resource pack focused on freight dispatch, causal inference, uplift, optimization, and marketplace ranking.

**Execution Steps:**

1. Save the JD exactly as provided, then normalize the key responsibilities into five ability axes:
   - market modeling
   - dispatch optimization
   - subsidy / pricing strategy
   - traffic allocation / growth
   - LLM-assisted decision support
2. Write the hidden expectations explicitly:
   - the role wants business efficiency, not just model accuracy
   - causal thinking matters because subsidy value is incremental, not correlational
   - optimization matters because matching and exposure are resource allocation problems
3. Build a knowledge order that starts with basics you must speak fluently:
   - forecasting basics
   - bipartite matching / assignment / min-cost intuition
   - uplift / treatment effect / DID / doubly robust intuition
   - ranking and multi-objective scoring
4. Create a resource list with primary sources or strong official docs.

**Verification:**

- The decomposition can answer “why this is a freight strategy role rather than a generic ML role.”
- The knowledge checklist has a clear “must know / should know / stretch” order.

## Task 2: Design the flagship project blueprint

**Files:**

- Create: `cases/didi-freight-2026/04_project_blueprint.md`
- Create: `docs/examples/2026-04-10-didi-freight-demo-script.md`

**Deliverables:**

- A single project definition that can support demo, resume, and interview answers.
- A stable 5-minute demo script.

**Recommended Project Name:** `FreightStrategyLab`

**Project Thesis:** Build a freight marketplace sandbox that simulates market states and compares how different algorithm policies affect dispatch efficiency, subsidy ROI, and traffic distribution quality.

**Required Demo Views:**

- Dispatch Center: given orders and trucks, choose matches and explain why.
- Subsidy Studio: under a fixed budget, decide who should receive incentive and estimate incremental gains.
- Traffic Allocator: decide how order leads or exposure should be distributed across drivers or carriers.
- Strategy Review: compare baseline vs improved policy on KPI deltas.

**Execution Steps:**

1. Define one city-day freight market snapshot as the basic unit of analysis.
2. Define entities:
   - order: origin, destination, cargo type, weight/volume, deadline, price sensitivity
   - driver/truck: location, vehicle type, capacity, availability window, historical acceptance tendency
   - market: region, hour, demand intensity, supply intensity, weather/event tag
3. Define three algorithm scenarios:
   - dispatch optimization
   - targeted subsidy
   - traffic allocation
4. Define one common KPI board so that every scenario looks like part of the same system.

**Verification:**

- A stranger can understand the business problem in one paragraph.
- The three algorithm scenarios share the same data schema and KPI board.
- The demo script starts from business pain, not from model names.

## Task 3: Build the synthetic freight market data layer

**Files:**

- Create: `src/freight_strategy_lab/__init__.py`
- Create: `src/freight_strategy_lab/schemas.py`
- Create: `src/freight_strategy_lab/data.py`
- Create: `examples/freight_strategy/sample_market_day.json`
- Create: `examples/freight_strategy/sample_orders.json`
- Create: `examples/freight_strategy/sample_drivers.json`
- Create: `tests/freight_strategy_lab/test_data.py`

**Deliverables:**

- A synthetic market generator that can produce consistent order, driver, and region states.
- Reusable schemas for all downstream modules.

**Execution Steps:**

1. Define Pydantic or dataclass schemas for:
   - `FreightOrder`
   - `DriverProfile`
   - `MarketCell`
   - `DispatchDecision`
   - `SubsidyDecision`
   - `TrafficAllocationDecision`
2. Generate synthetic but plausible features:
   - order urgency
   - trip distance
   - expected payout
   - vehicle compatibility
   - predicted acceptance probability
   - predicted fulfillment risk
3. Add scenario knobs:
   - peak hour vs off-peak
   - high demand / low supply
   - budget tight vs budget loose
   - fairness-sensitive vs efficiency-first
4. Save fixed example snapshots so demo outputs are reproducible.

**Verification:**

- `pytest tests/freight_strategy_lab/test_data.py -v`
- Example data can be loaded without missing fields.
- Dispatch, subsidy, and traffic modules can all read the same schema.

## Task 4: Build forecasting and dispatch baselines

**Files:**

- Create: `src/freight_strategy_lab/forecast.py`
- Create: `src/freight_strategy_lab/dispatch.py`
- Create: `tests/freight_strategy_lab/test_forecast.py`
- Create: `tests/freight_strategy_lab/test_dispatch.py`

**Deliverables:**

- A simple demand/supply gap estimator.
- A dispatch baseline and an improved dispatch policy.

**Execution Steps:**

1. Start with a light baseline, not a heavy deep model:
   - demand prediction: regression or bucketed classification
   - supply prediction: active vehicle count or availability score
2. Convert forecast outputs into a dispatch score:
   - fulfillment probability
   - pickup cost
   - detour cost
   - vehicle compatibility
   - urgency weight
3. Implement two dispatch policies:
   - baseline greedy rule
   - improved optimization-aware rule using OR-Tools assignment or a constrained score maximization
4. Produce a comparison table:
   - match rate
   - average pickup distance
   - on-time rate proxy
   - driver utilization proxy

**Verification:**

- `pytest tests/freight_strategy_lab/test_forecast.py -v`
- `pytest tests/freight_strategy_lab/test_dispatch.py -v`
- Improved dispatch must beat the baseline on at least one business KPI without collapsing others.

## Task 5: Build subsidy and traffic allocation modules

**Files:**

- Create: `src/freight_strategy_lab/subsidy.py`
- Create: `src/freight_strategy_lab/traffic.py`
- Create: `tests/freight_strategy_lab/test_subsidy.py`
- Create: `tests/freight_strategy_lab/test_traffic.py`

**Deliverables:**

- A targeted subsidy module with clear incremental-thinking logic.
- A traffic allocation module that looks like a real marketplace ranking or exposure problem.

**Execution Steps:**

1. For subsidy:
   - start with a simple uplift proxy or T-learner style treatment-effect estimate
   - if causal tooling is too heavy, use a doubly robust or counterfactual-inspired offline estimate and explain the limits honestly
   - convert estimated uplift into budgeted treatment allocation
2. For traffic allocation:
   - define exposure candidates such as order recommendations, lead distribution, or driver-facing opportunity ranking
   - rank by a multi-objective score that includes conversion proxy, margin proxy, fairness penalty, and supply-balance term
3. Make the business distinction explicit:
   - dispatch solves “who gets matched now”
   - subsidy solves “who should be incentivized”
   - traffic allocation solves “who should see which opportunity”
4. Build one comparison report:
   - baseline random or heuristic allocation
   - improved targeted policy

**Verification:**

- `pytest tests/freight_strategy_lab/test_subsidy.py -v`
- `pytest tests/freight_strategy_lab/test_traffic.py -v`
- The demo can explain why a high-propensity user is not always the best subsidy target.

## Task 6: Build evaluation and the demo surface

**Files:**

- Create: `src/freight_strategy_lab/eval.py`
- Create: `src/freight_strategy_lab/app.py`
- Create: `src/freight_strategy_lab/cli.py`
- Create: `examples/freight_strategy/baseline_eval_report.json`
- Create: `examples/freight_strategy/improved_eval_report.json`

**Deliverables:**

- One offline evaluation entry point.
- One lightweight app that can be used in interviews.

**Execution Steps:**

1. Expose two CLI entry points:
   - `simulate`
   - `evaluate`
2. Build a minimal app with four tabs:
   - market snapshot
   - dispatch result
   - subsidy result
   - traffic result
3. In every tab, show both:
   - decision output
   - business explanation
4. Add one “strategy review” panel:
   - baseline KPIs
   - improved KPIs
   - business interpretation

**Verification:**

- `PYTHONPATH=src python -m freight_strategy_lab.cli evaluate`
- `PYTHONPATH=src python -m freight_strategy_lab.cli simulate`
- The UI can support a 5-minute interview walk-through without requiring code reading.

## Task 7: Rewrite one internship into a freight-strategy project story

**Files:**

- Create: `cases/didi-freight-2026/05_interview_assets.md`
- Create: `docs/examples/2026-04-10-didi-freight-resume-reframe.md`

**Deliverables:**

- One rewritten project narrative that can replace or heavily upgrade one internship bullet group.
- Resume bullets, STAR stories, and likely follow-up questions.

**Execution Steps:**

1. Pick the closest source internship and map it to one of these templates:
   - recommendation / ads / ranking internship -> traffic allocation and growth strategy
   - operations strategy / subsidy / user growth internship -> targeted incentive and ROI optimization
   - forecasting / risk / data mining internship -> supply-demand prediction plus dispatch decision support
2. Rewrite the project into this structure:
   - business problem
   - data and features
   - algorithm approach
   - evaluation and gain
   - trade-offs and next step
3. Write resume bullets that sound like marketplace work instead of generic modeling work.
4. Prepare answers for three likely attacks:
   - “How much of this was real business impact?”
   - “Why is this causal rather than pure prediction?”
   - “Why is this optimization rather than simple if-else rules?”

**Verification:**

- Each bullet contains a business objective, algorithm method, and measurable outcome.
- The story can survive follow-up questions about assumptions and limitations.

## Task 8: Build the knowledge-closing and AI-native development playbook

**Files:**

- Create: `docs/examples/2026-04-10-didi-freight-system-design-answer.md`
- Modify: `docs/plans/2026-04-10-didi-freight-algo-prep-plan.md`

**Deliverables:**

- One knowledge gap tracker.
- One scenario answer for “design a freight intelligent trading system.”
- One Codex-first development workflow.

**Execution Steps:**

1. Split knowledge closing into four tracks:
   - business: freight marketplace mechanics, dispatch, subsidy ROI, traffic allocation
   - algorithm: forecasting, matching, uplift/causal, ranking
   - engineering: service design, evaluation, data contracts, experiment pipeline
   - expression: resume wording, demo narration, system design answer
2. For every track, define:
   - core concepts
   - one notebook or implementation exercise
   - one interview question set
3. Write the AI-native workflow explicitly:
   - use Codex to draft schemas, tests, and scaffolding
   - use Codex to generate baseline modules and comparison harnesses
   - keep the human responsible for assumptions, KPI selection, sanity checks, and business interpretation
   - use LLMs to accelerate iteration, not to outsource judgment
4. Build the standard answer to the scenario question:
   - define the market
   - define the objectives and guardrails
   - design prediction, decision, and evaluation layers
   - explain offline-to-online iteration
   - explain where LLM helps and where it should stay out

**Verification:**

- You can explain the system in layers: data -> forecast -> decision -> evaluation -> iteration.
- You can explain one concrete Codex workflow without sounding like you only “prompted and hoped.”

## Must-Have Knowledge Order

If time is limited, learn in this order:

1. Matching / assignment basics for dispatch
2. Uplift / causal intuition for subsidy
3. Ranking and multi-objective scoring for traffic allocation
4. Marketplace KPI design and trade-offs
5. One lightweight forecasting baseline
6. One clean system-design answer
7. LLM landing as an analysis/copilot layer

## What Not To Do

- Do not make the core demo a generic chat agent.
- Do not claim RL or causal inference if you cannot explain the evaluation assumptions.
- Do not overbuild dynamic pricing if you do not have credible data support.
- Do not optimize only accuracy; always report business KPIs.
- Do not let the project become three disconnected notebooks with no common narrative.

## Minimum Viable Version

If time becomes very tight, cut scope to this:

- one reproducible city-day simulator
- one dispatch baseline vs improved policy
- one targeted subsidy comparison
- one dashboard with KPI deltas
- one rewritten project story
- one 10-minute system-design answer

This is enough to be interviewable. Everything else is a multiplier, not the core.

## Assumptions

- No real freight marketplace data is currently available, so the first version should be synthetic plus clearly stated assumptions.
- One prior internship exists that can be reframed toward recommendation, growth strategy, or data mining.
- The immediate goal is interview readiness and business credibility, not production-grade algorithm optimality.
