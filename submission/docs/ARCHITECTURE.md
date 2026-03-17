# Architecture / Design

## Layered structure

- `src/trustlab/config`
  - Environment-driven settings (`Settings`) and path resolution.
- `src/trustlab/core`
  - Domain entities and invariants:
    - `EventRecord` + event payload validation
    - `ParticipantSession` + trial state
- `src/trustlab/services`
  - Stateless and stateful domain services:
    - deterministic condition assignment (`ConditionAssignmentService`)
    - in-memory session coordination (`SessionRegistry`)
- `src/trustlab/api`
  - HTTP adapter layer:
    - endpoint routing
    - request parsing and response shaping
    - middleware for CORS, per-IP rate limits, and metrics
- `src/trustlab/storage`
  - Persistence boundary:
    - `EventStore` abstraction
    - async file logger (`AtomicEventLogger`) writing JSONL + CSV
    - optional SQLite implementation
- `src/trustlab/utils`
  - condition configuration loading and structural checks

## Design decisions

1. **Deterministic assignment without DB**
   - SHA-256 of `participant_id` provides stable assignment across restarts.
2. **Asynchronous logging**
   - write queue prevents request threads from blocking on disk I/O.
3. **Resilience over strictness for reads**
   - malformed JSONL lines are skipped rather than crashing analysis.
4. **Minimal but intentional boundaries**
   - clear domain/service/api/storage boundaries without adding framework overhead.

## Tradeoffs
- Session state is in-memory by design (adequate for local study runs, non-distributed setup).
- Metrics use rolling in-memory samples instead of external observability systems.
