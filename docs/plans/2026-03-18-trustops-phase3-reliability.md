# TrustOps Phase 3 Reliability Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add JD-aligned backend reliability primitives to both TrustOps portfolio repos: request idempotency, transactional outbox-based async handoff, retry/dead-letter states, and audit/ops metrics.

**Architecture:** Keep the existing `Go + Hertz` gateway as the main chain and `Python + FastAPI` as AI sidecar. Move async handoff responsibility from "request writes case then best-effort publish" to "transactionally persist case + idempotency record + outbox + audit log", then let a gateway-local outbox relay publish pending events and mark retry/dead-letter state in MySQL. Expose a small ops metrics API for interview/demo visibility.

**Tech Stack:** Go, Hertz, MySQL, Redis, RabbitMQ, sqlmock, miniredis, pytest, Docker Compose

### Task 1: Content Quality Persistence Upgrade

**Files:**
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/infra/mysql/init/001_init.sql`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/storage/repository.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/storage/storage_test.go`

**Step 1: Write the failing tests**

- Add tests for:
  - first ingest creates case + outbox + audit record
  - repeated ingest with same `event_id` returns existing case instead of inserting duplicate
  - ops metrics aggregates pending / dead-letter / idempotent replay counters

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./internal/storage -run 'Test(Ingest|OpsMetrics)' -v
```

Expected: FAIL because ingest transaction / metrics methods do not exist yet.

**Step 3: Write minimal implementation**

- Extend schema with:
  - `content_ingest_requests`
  - `content_outbox_events`
  - `content_audit_logs`
- Extend repository abstractions with:
  - idempotent ingest result type
  - outbox polling / status update methods
  - ops metrics query

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./internal/storage -run 'Test(Ingest|OpsMetrics)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform
git add infra/mysql/init/001_init.sql services/gateway-go/internal/storage/repository.go services/gateway-go/internal/storage/storage_test.go
git commit -m "feat: add content ingest idempotency and outbox persistence"
```

### Task 2: Content Quality Router and Relay

**Files:**
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/http/router.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/http/router_phase2_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/cmd/server/main.go`
- Create: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/mq/outbox_relay.go`
- Create: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/mq/outbox_relay_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/README.md`

**Step 1: Write the failing tests**

- Add tests for:
  - ingest response exposes `idempotent_replay`
  - new ops metrics endpoint returns outbox/audit counters
  - relay marks publish success and moves repeated failures to dead-letter state

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./internal/http ./internal/mq -run 'Test(Ingest|Metrics|Relay)' -v
```

Expected: FAIL because router still uses direct publish and relay does not exist.

**Step 3: Write minimal implementation**

- Switch ingest path to repository-led idempotent ingest
- Add `GET /api/v1/content/ops/metrics`
- Start relay ticker from `cmd/server/main.go`
- Relay updates outbox status as `pending -> retry -> dead_letter` and writes audit logs

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./internal/http ./internal/mq -run 'Test(Ingest|Metrics|Relay)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform
git add services/gateway-go/internal/http/router.go services/gateway-go/internal/http/router_phase2_test.go services/gateway-go/cmd/server/main.go services/gateway-go/internal/mq/outbox_relay.go services/gateway-go/internal/mq/outbox_relay_test.go README.md
git commit -m "feat: add content gateway outbox relay and ops metrics"
```

### Task 3: Ecommerce RiskOps Persistence Upgrade

**Files:**
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/infra/mysql/init/001_init.sql`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/storage/repository.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/storage/repository_test.go`

**Step 1: Write the failing tests**

- Add tests for:
  - first ingest creates case + outbox + audit record
  - repeated ingest with same idempotency key returns existing case
  - ops metrics aggregates retry / dead-letter / replay counters

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./internal/storage -run 'Test(Ingest|OpsMetrics)' -v
```

Expected: FAIL because idempotent ingest and metrics methods do not exist yet.

**Step 3: Write minimal implementation**

- Extend schema with:
  - `risk_ingest_requests`
  - `risk_outbox_events`
  - `risk_audit_logs`
- Extend repository with:
  - request fingerprint / explicit idempotency key support
  - transactional outbox persistence
  - ops metrics query

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./internal/storage -run 'Test(Ingest|OpsMetrics)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
git add infra/mysql/init/001_init.sql services/gateway-go/internal/storage/repository.go services/gateway-go/internal/storage/repository_test.go
git commit -m "feat: add riskops ingest idempotency and outbox persistence"
```

### Task 4: Ecommerce RiskOps Router and Relay

**Files:**
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/http/router.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/http/router_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/cmd/server/main.go`
- Create: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/mq/outbox_relay.go`
- Create: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/mq/outbox_relay_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/README.md`

**Step 1: Write the failing tests**

- Add tests for:
  - ingest returns `idempotent_replay` and resolved `idempotency_key`
  - new ops metrics endpoint returns outbox/audit counters
  - relay marks failure retries and dead-letter state after max attempts

**Step 2: Run test to verify it fails**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./internal/http ./internal/mq -run 'Test(Ingest|Metrics|Relay)' -v
```

Expected: FAIL because router still directly calls publisher and no relay exists.

**Step 3: Write minimal implementation**

- Accept optional `X-Idempotency-Key`, otherwise derive deterministic request fingerprint
- Switch ingest path to transactional repository ingest
- Add `GET /api/v1/risk/ops/metrics`
- Start relay ticker from `cmd/server/main.go`
- Update README with phase-3 reliability capabilities

**Step 4: Run test to verify it passes**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./internal/http ./internal/mq -run 'Test(Ingest|Metrics|Relay)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
git add services/gateway-go/internal/http/router.go services/gateway-go/internal/http/router_test.go services/gateway-go/cmd/server/main.go services/gateway-go/internal/mq/outbox_relay.go services/gateway-go/internal/mq/outbox_relay_test.go README.md
git commit -m "feat: add riskops outbox relay and ops metrics"
```
