# Execution Order

The order is prerequisite-driven and intentionally excludes historical and
live-capability scripts.

## Stage 0 — preflight

Run the compile/import-compatible preflight from the terminal plan. Failure
stops all later stages.

## Stage 1 — foundation

Run Dataset/Case-dependent synthetic Evaluation Boundary, Observation Gateway,
Cognitive State Formation, A-Route replay, and White-box foundation. A P0
failure stops the plan; P1 embedded-check failures are recorded and stop the
dependent stage.

## Stage 2 — controlled replay cognition

Run and verify the A-Route controlled replay path. It must prove canonical
gateway admission, A-Route execution, and Cognitive State Formation execution.

## Stage 3 — Evaluation, White-box, Governance

Run and verify the one-case replay integration. Confirm Plane A, explicit
Plane B `NOT_EVALUATED`, Plane G, White-box V1, and an immutable archive.

## Stage 4 — minimum sufficient loop

Run and verify Case A and Case B. Confirm causal multi-cycle linkage and
execution-instance archive identity.

## Stage 5 — negative guards

Re-run the relevant existing verifiers for LIVE escalation, replay admission,
loop causality, and promotion/action boundaries. Do not create a new archive
collision by intentionally writing an identity-conflicting record.

## Stage 6 — read-only audit

Run the new audit reader after all preceding outputs exist. It reads `_eval_out`
and `evaluation_archive/level1_cognitive_runs/` and writes only audit reports
under `_eval_out`.

## Stage 7 — consolidated audit verifier

Run the new report verifier. It fails on any BLOCKER or MAJOR finding and does
not replace the individual component verifiers.
