# Field State Read Model Contract DryRun v1

## Phase

Phase-P1-Field-Kernel-Field-State-Read-Model-Contract-DryRun-v1-001

## Scope

Contract fixtures + dry-run validation only.

## Covered Areas

1. legal read scenarios
2. six-status priority conflicts
3. invalid query rejection rules
4. invalid state candidate downgrade/rejection rules
5. deterministic projection ordering
6. deterministic JSON serialization
7. replay/trace/provenance preservation
8. boundary invariants and immutability

## Fixed Priority

1. query_rejected
2. state_unavailable
3. stale_state
4. insufficient_state
5. partial_projection
6. read_ready

## DryRun Constraints

- no reducer modification
- no registry/manifest/baseline/dependency map change
- no real state store
- no state write
- no model execution
- no action or task execution
- no runtime loop

## Output Expectations

- total contract scenarios: 45
- deterministic serialization via json sort_keys=true
- runtime_executed=false
- boundary flags identical to controlled skeleton
- provenance_refs passed through without reorder
