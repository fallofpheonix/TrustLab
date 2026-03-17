# Test Cases (Critical Paths)

## Backend API
- Health endpoint returns `200` with `{"status":"ok"}`.
- Conditions endpoint returns configured cue conditions.
- Assignment endpoint validates participant id format and deterministic assignment.
- Events endpoint accepts valid payloads and rejects malformed/invalid payloads.
- Metrics endpoint returns aggregate latency and distribution fields.

## Logging / Data Integrity
- Concurrent event appends do not lose entries.
- JSONL lines remain parseable under concurrent writes.
- CSV header appears exactly once.
- Event count reflects writes.

## Domain logic
- Assignment distribution remains roughly even over large participant set.
- Event validation enforces participant format, decision values, timestamp skew, and latency bounds.
- Session registry supports thread-safe concurrent session creation.

## Manual UI flow
- Task page loads and renders recommendation text.
- User can complete accept/reject action and receive persisted event log.
