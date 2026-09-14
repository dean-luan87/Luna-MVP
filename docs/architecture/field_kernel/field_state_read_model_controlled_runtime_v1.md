# Field State Read Model Controlled Runtime v1

## Phase

Phase-P1-Field-Kernel-Field-State-Read-Model-Controlled-Read-Runtime-v1-001

## Reuse Confirmation

This runtime reuses the existing formal read contract surface only:

- FieldStateReadQuery / FieldStateReadResult
- read_field_state(query, state_candidate)
- existing read boundary flags
- deterministic JSON serialization behavior from contract dryrun

It does not modify module six-status semantics.

## Controlled Source Strategy

- source adapter is pure in-memory and single-call
- source_mode is frozen to:
  - candidate_available
  - candidate_unavailable
  - candidate_malformed
  - source_rejected
- runtime_source_connected is always false
- external_io_executed is always false
- candidate_only is always true

## Fixed Runtime Strategy

- candidate_available: call read_field_state(query, state_candidate)
- candidate_unavailable: call read_field_state(query, None) and map to runtime_unavailable
- candidate_malformed: call read_field_state(query, malformed_candidate) and map to runtime_unavailable
- source_rejected: runtime_rejected, read API not invoked
- runtime request invalid: runtime_rejected, read API not invoked
- contained exception: runtime_error_contained

Final rejection/error split:

- predictable contract rejection stays in runtime_rejected
- only `runtime_contained:*` classified failures enter runtime_error_contained
- runtime_rejected does not call read_field_state and keeps read_status empty with read_result {}

## Runtime Status Mapping

- runtime_completed: read_ready
- runtime_partial: partial_projection / insufficient_state / stale_state
- runtime_unavailable: candidate_unavailable / candidate_malformed / state_unavailable
- runtime_rejected: invalid runtime request / source_rejected / query_rejected
- runtime_error_contained: any contained runtime exception

## Boundary Invariants

- runtime_attempted=true only after request validation passes
- read_api_invoked=false for runtime_rejected before read stage
- external_io_executed=false
- state_mutation_executed=false
- runtime_loop_executed=false
- candidate_only=true
- no persistence, no downstream dispatch, no real model execution

## Determinism Rules

- same runtime request yields identical source_status, runtime_status, read_status, read_result, trace_ref, replay_key, boundary_flags and stable JSON
- no current time, UUID, random value, absolute workspace path, or traceback in formal envelope fields
