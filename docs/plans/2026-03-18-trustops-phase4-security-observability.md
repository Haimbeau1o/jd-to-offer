# TrustOps Phase 4 Security And Observability Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add JD-aligned backend platform capabilities to both TrustOps portfolio repos: API key authentication, Redis-backed rate limiting, audit-log query APIs, Prometheus-style `/metrics`, and database-backed worker-side consumer deduplication.

**Architecture:** Keep the current `Go + Hertz + MySQL + Redis + RabbitMQ` main chain intact and treat AI as a sidecar only. Gateway services gain request security and observability primitives, while worker services gain persistent consumer dedup tables so repeated queue deliveries do not create duplicate downstream effects. Shared design stays simple: env-driven API keys, Redis first for rate limiting with safe in-memory fallback, MySQL audit/dedup state, and plain-text metrics exposition for demo and interview visibility.

**Tech Stack:** Go, Hertz, MySQL, Redis, RabbitMQ, sqlmock, miniredis, pytest, Docker Compose

### Task 1: Ecommerce RiskOps Gateway Security, Audit Query, And Prometheus Metrics

**Files:**
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/infra/mysql/init/001_init.sql`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/storage/repository.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/storage/repository_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/http/router.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/http/router_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/config/config.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/internal/config/config_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/cmd/server/main.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go/cmd/server/main_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/README.md`

**Step 1: Write the failing tests**

- Add router tests for:
  - missing `X-API-Key` returns `401`
  - invalid `X-API-Key` returns `403`
  - repeated requests past configured limit return `429`
  - `GET /api/v1/risk/cases/:case_id/audit-logs` returns newest-first audit rows
  - `GET /metrics` returns Prometheus text including ingest, replay, pending outbox, dead-letter, audit-log, auth reject, and rate-limit reject counters
- Add storage tests for:
  - audit log query returns limited newest-first rows
  - ops metrics still aggregate DB-backed counters after audit query support is added

**Step 2: Run tests to verify they fail**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./internal/http ./internal/storage ./cmd/server -run 'Test(Ingest|Auth|Rate|Audit|Metrics|Build)' -v
```

Expected: FAIL because auth middleware, limiter wiring, audit-log query method, and `/metrics` exposition do not exist yet.

**Step 3: Write minimal implementation**

- Extend schema with `risk_worker_processed_events` for the later worker task.
- Add `AuditLog` model plus `ListAuditLogs(ctx, caseID, limit)` to the repository interface and implementations.
- Add env-driven security config:
  - `GATEWAY_API_KEYS=ops-key-1,ops-key-2`
  - `GATEWAY_RATE_LIMIT_RPM=60`
  - `GATEWAY_RATE_LIMIT_PREFIX=riskops`
- Add API key auth middleware using `X-API-Key`.
- Add Redis-backed fixed-window or token-bucket limiter; if Redis is unavailable, keep a bounded in-memory limiter so local demo still runs.
- Track runtime counters for auth rejects and rate-limit rejects and render them from `/metrics` as Prometheus text.
- Keep `/healthz` unauthenticated; require auth for ingest, case query, audit query, and metrics routes.

**Step 4: Run tests to verify they pass**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./internal/http ./internal/storage ./cmd/server -run 'Test(Ingest|Auth|Rate|Audit|Metrics|Build)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
git add infra/mysql/init/001_init.sql services/gateway-go/internal/storage/repository.go services/gateway-go/internal/storage/repository_test.go services/gateway-go/internal/http/router.go services/gateway-go/internal/http/router_test.go services/gateway-go/internal/config/config.go services/gateway-go/internal/config/config_test.go services/gateway-go/cmd/server/main.go services/gateway-go/cmd/server/main_test.go README.md
git commit -m "feat: add riskops gateway security and observability"
```

### Task 2: Ecommerce RiskOps Worker Consumer Dedup

**Files:**
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/infra/mysql/init/001_init.sql`
- Create: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/internal/storage/processed_events.go`
- Create: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/internal/storage/processed_events_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/internal/consumer/processor.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/internal/consumer/processor_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/internal/config/config.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/internal/config/config_test.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker/cmd/worker/main.go`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/README.md`

**Step 1: Write the failing tests**

- Add storage tests for:
  - first acquire for `event_id` succeeds
  - duplicate acquire for the same `event_id` returns `already_processed`
  - failed processing can be marked and observed
- Add consumer tests for:
  - duplicate event is skipped without running business side effects twice
  - successful processing marks the event as processed

**Step 2: Run tests to verify they fail**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker
go test ./internal/consumer ./internal/storage ./internal/config ./cmd/worker -run 'Test(Parse|Process|Dedup|Load)' -v
```

Expected: FAIL because there is no persistent processed-event repository or worker wiring yet.

**Step 3: Write minimal implementation**

- Add `risk_worker_processed_events` table with:
  - `event_id` primary key
  - `case_id`
  - `status`
  - `consumer_name`
  - `processed_at`
  - `last_error`
- Implement MySQL-backed repository for:
  - `TryStart(eventID, caseID, consumerName)`
  - `MarkProcessed(eventID)`
  - `MarkFailed(eventID, lastError)`
- Update worker config with:
  - `WORKER_STORAGE_BACKEND`
  - `WORKER_MYSQL_DSN`
- Wire the worker main loop to acquire dedup state before calling `ProcessMessage`.
- Keep duplicate deliveries as `Ack` + skip to model idempotent consumers rather than repeated side effects.

**Step 4: Run tests to verify they pass**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker
go test ./internal/consumer ./internal/storage ./internal/config ./cmd/worker -run 'Test(Parse|Process|Dedup|Load)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
git add infra/mysql/init/001_init.sql services/worker/internal/storage/processed_events.go services/worker/internal/storage/processed_events_test.go services/worker/internal/consumer/processor.go services/worker/internal/consumer/processor_test.go services/worker/internal/config/config.go services/worker/internal/config/config_test.go services/worker/cmd/worker/main.go README.md
git commit -m "feat: add riskops worker dedup persistence"
```

### Task 3: Content Quality Gateway Security, Audit Query, And Prometheus Metrics

**Files:**
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/infra/mysql/init/001_init.sql`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/storage/repository.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/storage/storage_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/http/router.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/http/router_phase2_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/config/config.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/internal/config/config_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/cmd/server/main.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go/cmd/server/main_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/README.md`

**Step 1: Write the failing tests**

- Add router/storage tests for:
  - missing or invalid `X-API-Key` on ingest and case query
  - rate-limited ingest returns `429`
  - `GET /api/v1/content/cases/:case_id/audit-logs` returns case audit history
  - `GET /metrics` returns Prometheus text for total cases, idempotent replays, pending outbox, dead-letter outbox, audit logs, auth rejects, and rate-limit rejects

**Step 2: Run tests to verify they fail**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./internal/http ./internal/storage ./cmd/server -run 'Test(Ingest|Auth|Rate|Audit|Metrics|Build|ProcessOutbox)' -v
```

Expected: FAIL because the content gateway still lacks auth/limit middleware, audit-log query, and Prometheus output.

**Step 3: Write minimal implementation**

- Add `AuditLog` query support to `CaseRepository`.
- Add env-driven API key auth and limiter config mirroring the ecommerce repo.
- Keep legacy JSON ops endpoint for demo compatibility if convenient, but add `/metrics` plain text as the canonical observability endpoint.
- Remove reliance on the unused router publisher path if it is no longer needed after outbox relay.
- Track auth reject and rate-limit reject runtime counters.

**Step 4: Run tests to verify they pass**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./internal/http ./internal/storage ./cmd/server -run 'Test(Ingest|Auth|Rate|Audit|Metrics|Build|ProcessOutbox)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform
git add infra/mysql/init/001_init.sql services/gateway-go/internal/storage/repository.go services/gateway-go/internal/storage/storage_test.go services/gateway-go/internal/http/router.go services/gateway-go/internal/http/router_phase2_test.go services/gateway-go/internal/config/config.go services/gateway-go/internal/config/config_test.go services/gateway-go/cmd/server/main.go services/gateway-go/cmd/server/main_test.go README.md
git commit -m "feat: add content gateway security and observability"
```

### Task 4: Content Quality Worker Refactor And Consumer Dedup

**Files:**
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/infra/mysql/init/001_init.sql`
- Create: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/internal/consumer/processor.go`
- Create: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/internal/consumer/processor_test.go`
- Create: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/internal/storage/processed_events.go`
- Create: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/internal/storage/processed_events_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/internal/config/config.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/internal/config/config_test.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/services/worker/cmd/worker/main.go`
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/README.md`

**Step 1: Write the failing tests**

- Extract tests first for:
  - parsing valid and invalid content case events
  - duplicate `event_id` is skipped and only one side effect is logged
  - worker config loads MySQL-backed dedup settings

**Step 2: Run tests to verify they fail**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/worker
go test ./internal/consumer ./internal/storage ./internal/config ./cmd/worker -run 'Test(Parse|Process|Dedup|Load)' -v
```

Expected: FAIL because content worker logic is still inline in `cmd/worker/main.go` and no dedup storage exists.

**Step 3: Write minimal implementation**

- Add `content_worker_processed_events` table with the same core fields as the ecommerce repo.
- Extract parsing and processing logic into `internal/consumer/processor.go`.
- Add MySQL-backed processed-event repository.
- Extend worker config with storage backend and MySQL DSN values.
- Update main loop to:
  - parse event
  - attempt dedup acquire
  - skip duplicate deliveries with `Ack`
  - mark success or failure in MySQL

**Step 4: Run tests to verify they pass**

Run:

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform/services/worker
go test ./internal/consumer ./internal/storage ./internal/config ./cmd/worker -run 'Test(Parse|Process|Dedup|Load)' -v
```

Expected: PASS.

**Step 5: Commit**

```bash
cd /Volumes/passport/简历/trustops-content-quality-platform
git add infra/mysql/init/001_init.sql services/worker/internal/consumer/processor.go services/worker/internal/consumer/processor_test.go services/worker/internal/storage/processed_events.go services/worker/internal/storage/processed_events_test.go services/worker/internal/config/config.go services/worker/internal/config/config_test.go services/worker/cmd/worker/main.go README.md
git commit -m "feat: add content worker dedup persistence"
```

### Task 5: Cross-Repo Verification, Push, And Delivery

**Files:**
- Modify: `/Volumes/passport/简历/trustops-content-quality-platform/README.md`
- Modify: `/Volumes/passport/简历/trustops-ecommerce-riskops-platform/README.md`

**Step 1: Run repository verification**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/gateway-go
go test ./...
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/worker
go test ./...
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform/services/ai-copilot
python3 -m pytest -q
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
docker compose config >/tmp/trustops-ecommerce-compose.out

cd /Volumes/passport/简历/trustops-content-quality-platform/services/gateway-go
go test ./...
cd /Volumes/passport/简历/trustops-content-quality-platform/services/worker
go test ./...
cd /Volumes/passport/简历/trustops-content-quality-platform/services/ai-copilot
python3 -m pytest -q
cd /Volumes/passport/简历/trustops-content-quality-platform
docker compose config >/tmp/trustops-content-compose.out
```

Expected: all Go tests pass, Python tests pass, and compose files resolve successfully.

**Step 2: Commit final README/docs deltas if needed**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
git add README.md
git commit -m "docs: refresh riskops phase 4 capabilities"

cd /Volumes/passport/简历/trustops-content-quality-platform
git add README.md
git commit -m "docs: refresh content phase 4 capabilities"
```

**Step 3: Push**

Run:

```bash
cd /Volumes/passport/简历/trustops-ecommerce-riskops-platform
git push origin codex/runtime-skeleton

cd /Volumes/passport/简历/trustops-content-quality-platform
git push origin codex/runtime-skeleton
```

Expected: both repos are available remotely with phase-4 security and observability updates.
