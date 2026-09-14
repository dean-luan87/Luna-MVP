# A3 Controlled DryRun Regression Evidence Checklist v1

Use this checklist only in a separately approved regression phase. It does not authorize a Runner, Verifier, Runtime, model, or output execution in the current design-only phase.

## Baseline Integrity

- [ ] Baseline identifier is `A3_COGNITIVE_ANALYSIS_CONTROLLED_DRYRUN_BASELINE_V1`.
- [ ] Canonical output remains `run1`; `run2` remains comparison evidence only.
- [ ] The six canonical output files and their reference inventory are present and unchanged.
- [ ] No unapproved baseline, warning-taxonomy, or output-directory reinterpretation is introduced.

## Contract Consistency

- [ ] Contract object names, required fields, enum values, invariants, and permission boundary match the frozen baseline.
- [ ] Direct input remains `CurrentCognitiveContextV1` by reference only.
- [ ] Field State mutation authority remains exclusively with `FieldStateReducer`.
- [ ] No new Case, Guard, Enum, Dataclass, or Contract field is introduced without an approved phase.

## Fixture Consistency

- [ ] Exactly eight immutable fixture case IDs are available.
- [ ] Case-to-planning mapping is unique and unchanged.
- [ ] Fixture serialization before and after validation is identical.
- [ ] Every local reference closes within its own fixture; dangling and cross-case counts are zero.

## Semantic Consistency

- [ ] Each case is recomputed against the semantic expectation matrix, not accepted from a Runner pass flag.
- [ ] Expected status, required reasons/warnings, evidence relation, and unresolved/unknown behavior match the frozen fixture.
- [ ] Aggregate case, warning, failure, and blocker counts are recomputed from case evidence.

## Permission Consistency

- [ ] `runtime_executed=false` and `simulation_only=true` remain true for every result.
- [ ] Observation execution, Decision execution, State writeback, Context writeback, and Snapshot writeback remain absent.
- [ ] No model, network, database, camera, OCR, SLAM, time, random, or automatic UUID capability is introduced.

## Guard Evidence Consistency

- [ ] All 24 guard IDs have static evidence and execution evidence.
- [ ] Guard evidence is recomputed independently; a summary `true` value is not sufficient proof.
- [ ] Any missing, contradictory, or stale proof produces a failed guard with its specific failure condition.
