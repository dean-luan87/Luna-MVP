# Full Regression Inventory

This inventory is preparation only. None of the commands below are executed by the Agent in this phase.

## Foundation inventory

- Dataset Registry: registry contracts, registration, sample membership, version/invalidation checks.
- Level-1 Field Cognition Suite: case composition, assertion taxonomy, synthetic precedents.
- Evaluation Run Boundary: registered Dataset/Sample/Case linkage and evaluation-only boundary.
- Durable Archive: immutable identity, read-back validation, append-or-supersede behavior.
- Execution modes: `SYNTHETIC_CONTROLLED`, `CONTROLLED_REPLAY_RUNTIME`, and deferred `LIVE_RUNTIME` rejection.
- Observation Gateway: synthetic admission, replay admission, provenance/order checks, negative guards.
- A-Route Orchestration: ingress refs, replay execution proof, lifecycle/handoff guards, synthetic compatibility.
- Cognitive State Formation: candidate boundaries, runtime proof, Current World/Hypothesis generation, loop transitions.
- Minimum Sufficient Cognition Loop: sufficiency, gap, re-observation, next-cycle linkage, revision, stop.
- White-box V1: Trace/Profile/Gap contracts, observational-only flags, explicit unavailable metrics.
- Plane A: execution and loop behavior assertions.
- Plane B: explicit `NOT_EVALUATED` replay status.
- Plane G: G01–G20 governance assertions and one negative LIVE escalation.
- Previous negative guards and archive conflict behavior.

## Status

This historical inventory is superseded for execution ordering by the
current audit inventory at:

`docs/architecture/phase_p1_luna_level1_internal_full_regression_and_data_conformance_audit_v1/regression_inventory.md`

The superseding inventory corrects the former assumption that Dataset
Registry has a runnable CLI, records runner-only components without a
dedicated verifier, and includes the White-box foundation pair.

## Dependencies and order

1. Dataset Registry and Level-1 case contracts.
2. Observation Gateway admission and ARoute ingress.
3. Cognitive State Formation and loop proof.
4. White-box V1 collection.
5. Plane A/B/G result validation.
6. Archive write/read validation.

Live model/provider, sensor, Field, Decision, Task, Action, Memory, Learning, Knowledge, and Experience paths remain excluded.
