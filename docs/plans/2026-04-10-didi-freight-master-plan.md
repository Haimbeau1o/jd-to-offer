# Didi Freight Preparation Master Plan

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.

**Goal:** Build a Didi freight interview preparation pack that turns the `RingConn` internship into a truthful but role-aligned technical story, pairs it with one flagship freight strategy demo, and finishes with one system-design / vibe-coding answer that can survive follow-up questions.

**Architecture:** Use a three-layer evidence stack. Layer 1 is `RingConn` as the technical base for forecasting, segmentation, offline evaluation, and productization. Layer 2 is `FreightStrategyLab` as the business-core project proving dispatch, subsidy, traffic allocation, and causal evaluation. Layer 3 is one freight intelligent trading system design answer that explains how the same logic would scale in production and how Codex can accelerate delivery.

**Tech Stack:** Markdown, Python 3.11, pandas, numpy, scikit-learn, LightGBM/XGBoost, OR-Tools, EconML/CausalML, FastAPI, Streamlit, Plotly, Mermaid, Markdown-based interview assets.

## Current State Assessment

- The repo already supports a `JD -> knowledge system -> project blueprint -> interview assets` workflow through `jd_offer`; see `README.md`.
- The repo already contains `RingConn` positioning and freight preparation notes:
  - `docs/examples/2026-04-10-ringconn-to-didi-freight-positioning.md`
  - `docs/examples/2026-04-10-ringconn-internship-packaging.md`
  - `docs/plans/2026-04-10-didi-freight-algo-prep-plan.md`
- The freight direction is documented, but `FreightStrategyLab` has not yet been implemented as a runnable package in `src/`.
- Therefore the real gap is not idea generation. The gap is turning the idea into three interview-ready artifacts:
  - a sharper `RingConn` story with hard boundaries
  - a freight-native demo with metrics and business logic
  - a production-grade system-design narrative

## Core Judgment

### What `RingConn` can prove

- continuous time-series modeling
- feature engineering and data mining
- user/sample segmentation
- offline evaluation and version comparison
- translating data capabilities into product functionality

### What `RingConn` cannot prove on its own

- freight business understanding
- dispatch optimization
- subsidy ROI design
- causal inference for strategy incrementality
- market-level traffic allocation

### Strategic implication

- `RingConn` should be the second proof, not the first proof.
- The first proof must be a new freight strategy project.
- The third proof must be knowledge depth and system-design fluency.

## Task 1: Freeze the truthful `RingConn` packaging

**Files:**
- Reference: `docs/examples/2026-04-10-ringconn-to-didi-freight-positioning.md`
- Reference: `docs/examples/2026-04-10-ringconn-internship-packaging.md`
- Later handoff target: `/Volumes/passport/简历/latex-resume`

**Deliverables:**
- One final title
- One 1-sentence summary
- Three final bullets
- One 60-90 second interview script
- One explicit list of claims that must not appear

**Execution Steps:**

1. Inventory actual work done in `RingConn` and tag each item as:
   - forecasting / recognition
   - segmentation / personalization
   - offline evaluation
   - data pipeline / productization
   - unsupported claim
2. Choose one dominant storyline:
   - preferred: time-series modeling + segmentation + evaluation
   - backup: data pipeline + algorithm landing
3. Rewrite the internship to emphasize:
   - dynamic noisy data
   - user heterogeneity
   - metrics and iteration
   - product landing
4. Explicitly ban freight-core overclaims:
   - dispatch
   - subsidy
   - causal inference
   - operations research
   - freight growth
5. Prepare one bridge sentence from `RingConn` to freight:
   - what transfers
   - what does not
   - what the new project will cover

**Verification:**

- A skeptical interviewer should conclude: “This candidate has transferable modeling ability, but is not faking freight business experience.”
- Every bullet should still be defensible if asked “what exactly did you implement?”

## Task 2: Build the freight knowledge pack for interview prep

**Files:**
- Reference: `docs/plans/2026-04-10-didi-freight-algo-prep-plan.md`
- Create: `docs/examples/2026-04-10-didi-freight-knowledge-pack.md`

**Deliverables:**
- A business map of the freight marketplace
- A technical map by topic and interview depth
- A reading list with primary sources
- A “must know / should know / stretch” ordering

**Knowledge Structure:**

### Business fundamentals

- marketplace objects: shipper, order, driver, truck, region, time window, price, subsidy, payout
- marketplace goals: match rate, response rate, fulfillment rate, empty-load distance proxy, subsidy spend, ROI, exposure fairness, regional stability
- marketplace tensions:
  - short-term conversion vs long-term supply health
  - local optimal dispatch vs system-level efficiency
  - gross completion vs incremental subsidy value

### Algorithm fundamentals

- forecasting:
  - demand volume
  - supply availability
  - response / fulfillment likelihood
- optimization:
  - assignment intuition
  - vehicle routing / time-window intuition
  - scoring vs hard-constraint matching
- intervention:
  - pricing / subsidy policy
  - uplift / heterogeneous treatment effect
  - offline counterfactual evaluation
- traffic allocation:
  - order exposure ranking
  - multi-objective scoring
  - fairness / concentration trade-offs

### LLM positioning

- operator copilot
- strategy explanation layer
- report / review generator
- not a replacement for dispatch or subsidy logic

**Recommended Primary Sources:**

- Didi Global 2023 20-F for freight marketplace framing
- China Ministry of Transport 2024 transport statistics for road freight scale
- Google OR-Tools docs for assignment and routing primitives
- `econml` and `causalml` docs/repos for treatment-effect tooling
- Didi / ride-hailing dispatch papers for marketplace dispatch design
- Uber engineering causal ML material for marketplace incrementality thinking

**Verification:**

- You can answer “why is this a freight strategy role instead of generic ML?” in 60 seconds.
- You can explain each major metric without drifting into vague business language.

## Task 3: Define the flagship demo as `FreightStrategyLab`

**Files:**
- Reference: `docs/plans/2026-04-10-didi-freight-algo-prep-plan.md`
- Planned create: `src/freight_strategy_lab/`
- Planned create: `tests/freight_strategy_lab/`
- Planned create: `docs/examples/2026-04-10-didi-freight-demo-script.md`

**Deliverables:**
- One coherent demo rather than several weak mini-projects
- One 5-minute demo script
- One metrics board
- One baseline vs improved policy comparison

**Project Thesis:**

Build a lightweight freight marketplace sandbox that turns market state into four connected decisions:

1. demand / supply forecast
2. dispatch scoring
3. subsidy / uplift policy
4. traffic allocation and offline evaluation

**MVP Modules:**

- `data.py`: synthetic market-day generation
- `forecast.py`: demand / supply / response baselines
- `dispatch.py`: score-based matching plus simple assignment constraint
- `subsidy.py`: targeted incentive policy with uplift proxy
- `traffic.py`: exposure allocation and ranking
- `eval.py`: KPI board and scenario comparison
- `app.py`: lightweight dashboard and explanation layer

**Business Story To Demonstrate:**

- Morning demand surge in a few regions
- Uneven driver availability by vehicle type
- Baseline policy over-spends subsidy and still misses fulfillment
- Improved policy increases completion and improves subsidy ROI
- Traffic allocation avoids over-concentrating exposure on a small driver subset

**Verification:**

- In 5 minutes you can show state -> decision -> metric impact.
- In 10 minutes you can answer “why each module exists in the business loop?”

## Task 4: Prepare the system-design / vibe-coding scenario answer

**Files:**
- Create: `docs/examples/2026-04-10-didi-freight-system-design-vibe-coding.md`

**Deliverables:**
- One scenario prompt
- One production system architecture answer
- One “how I would build this quickly with Codex” answer
- One risk / observability / evaluation checklist

**Recommended Scenario Prompt:**

Design a freight intelligent trading system for an intra-city freight platform. Given real-time orders, driver supply, vehicle constraints, regional demand shifts, and limited subsidy budget, the system must decide order exposure, dispatch priority, and targeted incentives while balancing completion rate, fulfillment timeliness, subsidy ROI, and marketplace fairness.

**Architecture Outline:**

- data layer:
  - order, driver, vehicle, region, and policy events
- feature layer:
  - short-horizon supply-demand features
  - driver response features
  - region-time pressure indicators
- decision layer:
  - forecast service
  - dispatch scorer / matcher
  - subsidy policy service
  - traffic allocator
- explanation layer:
  - operator copilot for “why this policy”
  - report generation for strategy review
- governance:
  - guardrails, fallback rules, budget caps, monitoring, and replay evaluation

**Vibe-Coding Narrative:**

- Use Codex to scaffold modules, schemas, evaluation harnesses, and dashboards quickly.
- Keep hard constraints explicit in typed schemas and deterministic business rules.
- Let the LLM accelerate analysis, documentation, and operator explanation, not replace core optimization and evaluation.

**Verification:**

- The answer should sound like marketplace engineering, not generic AI app design.
- The LLM should appear as leverage, not as magical decision logic.

## Task 5: Sequence the three proofs into one interview narrative

**Files:**
- Create: `docs/examples/2026-04-10-didi-freight-interview-storyline.md`

**Deliverables:**
- One 90-second self-introduction arc
- One 3-minute project explanation
- One 10-minute system-design arc

**Narrative Order:**

1. `RingConn` proves technical base:
   - dynamic data
   - segmentation
   - evaluation
2. `FreightStrategyLab` proves freight-native problem solving:
   - dispatch
   - subsidy
   - traffic allocation
   - offline evaluation
3. System design proves scale thinking:
   - architecture
   - metrics
   - fallback
   - observability
   - operator workflow

**Verification:**

- The three pieces should feel complementary, not repetitive.
- If the interviewer cuts you short after any one layer, you still sound complete.

## Recommended Source List

- Didi Global 2023 20-F: https://www.sec.gov/Archives/edgar/data/1764757/000110465924053916/tm2329116-7_20f.htm
- Ministry of Transport 2024 statistics bulletin: https://www.gov.cn/lianbo/bumen/202506/content_7028627.htm
- Google OR-Tools assignment guide: https://developers.google.com/optimization/assignment/assignment_example
- Google OR-Tools vehicle routing guide: https://developers.google.com/optimization/routing/vrp
- `econml` repository: https://github.com/py-why/econml
- `causalml` repository: https://github.com/uber/causalml
- Didi KDD 2018 dispatch paper: https://www.kdd.org/kdd2018/accepted-papers/view/large-scale-order-dispatch-in-on-demand-ride-sharing-platforms-a-learning-a
- Didi order dispatch paper on arXiv: https://arxiv.org/abs/2202.05118
- Uber engineering, causal inference in marketplace ML: https://www.uber.com/en-GB/blog/causal-inference-at-uber/

## Success Criteria

- `RingConn` sounds technically relevant without sounding fake.
- The freight demo covers the business core missing from the internship.
- The system-design answer shows production judgment, not only notebook-level modeling.
- The knowledge pack gives you a clean study order for interview prep.

## Next Decision

After this master plan, the next execution order should be:

1. finalize `RingConn` bullets and interview script
2. write the freight knowledge pack
3. write the freight system-design / vibe-coding doc
4. implement `FreightStrategyLab` in code
