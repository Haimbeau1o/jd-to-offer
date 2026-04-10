# TrustOps Platform Design

**Goal:** Define a flagship project direction that strongly matches two target JD families: AI tooling / content quality data services and backend development / ecommerce security.

**Product Thesis:** Build one shared backend platform, then expose two domain shells through tenant configuration and scenario data:
- Content Quality & Data Services
- Ecommerce Security & Merchant Risk Operations

The platform is backend-first. AI is an enhancement layer, not the decision-making core. This keeps the project tightly aligned with the JDs' emphasis on backend engineering, data services, modular architecture, reliability, and business abstraction.

## Why This Direction Matches The JDs

### Shared capability core

Both JDs reward the same underlying strengths:
- Backend service engineering
- Business abstraction and modular architecture
- Data services and middleware usage
- Reliability, security, and performance optimization
- Cross-functional product / operations collaboration
- Pragmatic adoption of AI tooling or LLM engineering

### Where the two JDs differ

- The content-quality JD emphasizes:
  - tool online-ization
  - data services
  - Go/Python web service implementation
  - LLM engineering as a backend capability
  - reliability / security / performance of reusable modules
- The ecommerce-security JD emphasizes:
  - backend development for risk products
  - B-side merchant products and risk operations systems
  - strong CS fundamentals
  - logic abstraction and decomposition
  - exploratory technology adoption with AI Coding as a plus

The project should therefore present a stable backend platform core, then switch business framing instead of switching architecture.

## Product Definition

Project name:
- TrustOps Platform

One sentence:
- A Go-first risk and quality operations platform with shared event processing, rules, case workflows, data services, auditability, and Python-based AI copilot enhancements.

Primary value:
- Show that the candidate can turn ambiguous business workflows into reusable, online backend services with clear module boundaries, operational visibility, and explainable AI-assisted tooling.

## System Boundaries

### In scope

- Online backend API layer
- Event ingestion and normalization
- Rules-based evaluation and scoring
- Case / work-order workflow
- Data service APIs for operators and downstream systems
- Async task execution with MQ
- Metrics, audit logs, and traceability
- AI copilot for summarization, explanation, retrieval, and rule drafting assistance

### Out of scope

- Multi-agent orchestration
- RLHF / post-training pipelines
- Large-scale model training
- Heavy front-end product design
- Full microservice sprawl

These are intentionally excluded because they dilute the JD match.

## Shared Platform Modules

### 1. Ingress Gateway

Responsibilities:
- auth
- request validation
- rate limiting
- tenant isolation
- idempotency keys
- request / response audit hooks

JD mapping:
- high reliability
- high security
- online service engineering

### 2. Evaluation Engine

Responsibilities:
- rule matching
- risk / quality scoring
- signal aggregation
- reason codes
- configurable strategy routing

JD mapping:
- business abstraction
- architecture design
- reusable service modules

### 3. Case Workflow Service

Responsibilities:
- create and update cases
- state machine transitions
- assignment and ownership
- action logging
- retry / rollback safe transitions

JD mapping:
- B-side products
- operations collaboration
- backend product support

### 4. Data Service Layer

Responsibilities:
- event queries
- case search
- evidence lookup
- metric aggregation
- operator-oriented read APIs

JD mapping:
- data services
- reusable platform capabilities
- database and middleware usage

### 5. Async Task Bus

Responsibilities:
- consume ingestion jobs
- schedule re-evaluation
- batch backfills
- failure retry
- dead-letter handling

JD mapping:
- MQ
- Linux backend environment
- reliability and performance engineering

### 6. AI Copilot Sidecar

Responsibilities:
- case summary
- rule explanation
- similar-case retrieval
- operator troubleshooting suggestions
- rule draft generation

JD mapping:
- LLM engineering application
- AI Coding / AI tooling
- new technology adoption

## Unified Domain Model

Use one shared entity model for both domain shells:
- Event
- Signal
- Rule
- Case
- Action
- Evidence
- AuditLog

Business shells customize event sources and rule packs:
- Content quality shell:
  - content publish event
  - report event
  - moderation review event
- Ecommerce security shell:
  - merchant behavior event
  - product / listing event
  - order / campaign / account event

This is the core abstraction move that demonstrates backend design strength.

## Recommended Tech Stack

- Go 1.24+
- Hertz as the main web service framework
- Python 3.12 + FastAPI for AI copilot sidecar
- MySQL for transactional storage
- Redis for hot reads, caching, and short-lived coordination
- RabbitMQ for async workflows
- Prometheus + Grafana for metrics
- Pydantic for AI sidecar I/O contracts

Why this stack:
- Go-first matches the chosen project direction and both JDs' backend emphasis
- Python sidecar preserves AI augmentation without making AI the system core
- MySQL / Redis / MQ directly match the JD hard skills

## Demo Shells

### Shell A: Content Quality & Data Services

Demo scenarios:
- ingest a suspicious content event and generate a moderation case
- explain why a rule triggered and what evidence was used
- show operator-side case summary and related historical incidents
- replay a misclassification case and inspect which rule caused false positives

### Shell B: Ecommerce Security & Merchant Risk Operations

Demo scenarios:
- ingest a suspicious merchant event and create a risk case
- route a case through operator workflow and log actions
- compare rule hit-rate before and after a campaign-specific rule rollout
- use AI copilot to summarize a merchant risk trail and suggest next review steps

## Metrics That Matter

Platform metrics:
- ingest latency
- evaluation latency
- case creation success rate
- cache hit rate
- retry success rate
- dead-letter count

Business metrics:
- rule hit rate
- false positive review count
- operator handling latency
- case closure rate
- evidence completeness

AI enhancement metrics:
- summary usefulness score
- explanation grounding coverage
- similar-case retrieval precision

## Knowledge Points The Project Must Demonstrate

- Go service layering and middleware design
- database schema design, indexing, and query shaping
- Redis usage and cache consistency trade-offs
- MQ reliability patterns: retry, DLQ, idempotency, replay
- state machine and audit log design
- business-rule abstraction and extensibility
- structured AI service integration with clear fallbacks
- observability and operational debugging

## MVP Direction

Phase 1 should only build:
- Ingress Gateway
- Evaluation Engine
- Case Workflow
- Data Service read APIs
- one async worker
- one AI copilot endpoint
- one content-quality case flow
- one ecommerce-security case flow

This is enough to prove the shared architecture without overscoping the project.

## Implication For jd2offer

The current repository is too agent / RL oriented for these JDs. To support this direction, jd2offer should be extended with:
- new backend-platform competencies
- two new project templates
- template-aware narrative generation instead of ride-hailing-specific hardcoded copy
- example cases for both ByteDance-style JDs
