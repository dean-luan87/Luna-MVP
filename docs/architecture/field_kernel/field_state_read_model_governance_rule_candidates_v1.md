# Field State Read Model Governance Rule Candidates v1

## Status

All rules in this document are candidate-only and are not promoted to L1 global enforcement in this phase.

## A. Module-Level Stable Rule Candidates

1. Reducer is the only Field State mutation authority.
2. Read Model only owns read/query/projection authority.
3. Read Model must not write state or admit facts.
4. Six-state priority is fixed:
   query_rejected > state_unavailable > stale_state > insufficient_state > partial_projection > read_ready
5. Runtime five-state set is fixed:
   runtime_completed, runtime_partial, runtime_unavailable, runtime_rejected, runtime_error_contained
6. Predictable contract rejection must not enter contained-error routing.
7. Rejection path must not call read API to fabricate a business result.
8. trace/replay/version/provenance must be preserved.
9. Input objects must remain immutable.
10. Candidate outputs must not be upgraded into facts.

## B. L1 Cross-Module Candidate Rules

1. Mutation authority must be singular.
2. Read and write authority must be separated.
3. Predictable rejection and unexpected exception must be routed separately.
4. Exception containment must not fabricate a normal business result.
5. Verifier must not implicitly repeat runner execution.
6. Runtime boundary flags must be explicit in outputs.
7. Candidate outputs must include provenance/trace/version.
8. Module integration requires skeleton, contract dry-run, and controlled runtime evidence first.

## Admission Note

This document remains a candidate governance asset until a later Protocol Governance Admission phase explicitly promotes any rule.
