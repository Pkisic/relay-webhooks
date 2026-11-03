# Roadmap

Relay is delivered in milestones. Each milestone ends in a working, tested, documented state. The MVP is milestones 1–4; everything after is planned work.

Legend: ⬜ planned · 🔄 in progress · ✅ done

## MVP

### 1. Foundation ⬜
Project layout, typed configuration, async database layer, migrations, authentication (JWT for users, API keys for automation), health and readiness endpoints, structured logging, centralized error handling, CI (lint, type-check, tests), Docker Compose for local development.

### 2. Capture ⬜
Endpoint management and the public ingest route. Raw request storage with size limits, pagination, filtering and full-text search over captured requests.

### 3. Live feed and response rules ⬜
Real-time delivery of captured requests via Server-Sent Events backed by Redis pub/sub. Per-endpoint response configuration: status, body, headers, fixed or random delay, and failure injection (e.g. fail every Nth request).

### 4. Replay and verification ⬜
Outbound delivery with timeouts, retries and exponential backoff, plus a per-attempt log. Editable replays. HMAC signature verification presets (Stripe, GitHub, Slack) with human-readable failure reasons.

## Post-MVP

### 5. Monitors ⬜
Scheduled HTTP checks with assertions on status code, latency, JSON path values and response schema. Uptime percentage, incident tracking, and state-change notifications. Runs in a dedicated worker process.

### 6. Heartbeats and silence detection ⬜
Scheduled jobs call a heartbeat URL on success; Relay raises an alert when an expected ping does not arrive within its grace period. The same mechanism can watch a capture endpoint for unexpected silence (for example a provider that has disabled your webhook).

### 7. Notifications ⬜
Alert channels: email, Slack, Discord and signed outbound webhooks, delivered through the same retrying delivery pipeline used by replay.

### 8. Payload schema drift ⬜
Infer a JSON Schema from captured payloads per endpoint and flag added, removed or retyped fields when a sender's contract changes.

### 9. Hardening ⬜
Rate limiting, payload retention policies, metrics and tracing (Prometheus/OpenTelemetry), load testing, and a deployment guide.

## Ideas under consideration

- Tunnel agent to forward captured requests to a developer's localhost.
- Team workspaces and role-based access.
- Request collections and shareable, read-only capture links.
- OpenAPI-based contract checks against captured traffic.
