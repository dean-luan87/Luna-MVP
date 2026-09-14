# Dynamic Flow retirement disposition

`DynamicCognitiveFlowEngineV1` should first be narrowed by contract, then by adapters, and only later by implementation removal.

## Retain

- candidate-only input validation;
- plan non-binding checks;
- deterministic state-version and transition construction;
- evidence/state-version acceptance bookkeeping;
- trace/provenance lineage;
- compatibility output needed by existing Dynamic Flow verification.

## Move to A

- current Need choice;
- Sufficiency judgment;
- Reconsideration judgment;
- Hypothesis invalidation interpretation;
- capability outcome interpretation;
- `CONTINUE`, `REQUEST_MORE_EVIDENCE`, `REPLAN`, `STOP_SUFFICIENT` semantic selection.

## Compatibility-only

The current output fields `current_minimum_need_ref`, `sufficiency_candidates`, `reconsiderations`, and `next_step_disposition` remain readable by verified fixtures until A-owned equivalents are consumed by all callers.

## Removal preconditions

All Dynamic Flow Runner/Verifier cases must be migrated or wrapped, real-input and single-invocation adapters must consume A decisions, and no direct caller may interpret Dynamic Flow output as authority.

