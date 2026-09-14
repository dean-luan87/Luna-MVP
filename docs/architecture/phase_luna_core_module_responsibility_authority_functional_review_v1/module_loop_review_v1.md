# M05 Cognitive Loop — Module Review

## Identity and purpose

Canonical name: Cognitive Loop / Loop Engine. Evidence: `cognitive_dynamic_loop_engine_v1.py`, `cognitive_dynamic_loop_types_v1.py`, `cognitive_loop_governed_continuity_candidate_controlled/`, and `loop_semantic_to_mechanical_cutover_controlled/`. If removed, Luna loses durable work identity, state-version lineage, lifecycle persistence, pause/wait/resume mechanics, history, trace, and final freeze.

## Functions and authority

`CORE`: materialize identity, record state/ref/version, pause/wait/resume supplied state, supersede recorded refs, close/freeze/archive, append trace/provenance. `SUPPORTING`: deterministic bookkeeping. `COMPATIBILITY_ONLY`: old `_local_disposition`, resume interpretation, closure semantic helpers. Legacy semantic helpers are `REAL LEAKAGE` at old paths: they infer local disposition, resume/reconsideration, and closure meaning. Current cutover marks the controlled boundary mechanical-only but does not delete helpers.

Loop has no semantic authority. Responsibility is limited to validating supplied issuer/grant/scope/version and applying mechanical commands; semantic error belongs to A/Brain/Capability/other source owner.

## Inputs, outputs, state, lifecycle

Inputs: A/Brain-supplied semantic refs, mechanical commands, work/Concern/grant/state refs, trace/provenance. Outputs: recorded mechanical state, refs, pending/pause/wait/closure/freeze/outcome refs to A/Brain. State is `MECHANICAL_STATE`; source semantic content is reference-only. Lifecycle mechanics are Loop-owned/executed; semantic interpretation is external.

## Communication and negative boundaries

Allowed: A→Loop adapter, Brain/governance→Loop supplied refs, Loop→A/Brain mechanical return. Forbidden: Loop→Need/Sufficiency/Reconsideration/Next-step/B adoption/Capability/Observation/Concern decisions. Known bypass: old continuity engine functions and Dynamic Flow lifecycle-like computations.

## Walkthroughs

1. Normal: validate supplied KEEP/REPLAN/CLOSE input and persist corresponding command.
2. Blocked: stale state or invalid grant rejects command without inventing a semantic reason.
3. Changed state: record changed ref/version; A decides KEEP vs REPLAN; Loop records chosen mechanics.

## Overlap, gaps, evolution, disposition

Overlap: `AUTHORITY_LEAKAGE` in legacy continuity helpers; `SEMANTIC_OVERLAP` with Dynamic Flow and Task lifecycle. Gap: adapter cutover and fixture migration. Future Loop should expose a narrow mechanical surface: MATERIALIZE, RECORD_STATE_VERSION, RECORD_REFS, RECORD_NEED_REF, RECORD_REQUIREMENT_REF, RECORD_B_BRANCH_REF, PAUSE, WAIT, RESUME_RECORDED_STATE, SUPERSEDE_RECORDED_REF, CLOSE, FREEZE_FINAL_STATE, RECORD_OUTCOME_REF, ARCHIVE_HISTORY_BOUNDARY, APPEND_TRACE. **Disposition: NARROW**.

**Ledger summary:** authority = mechanical persistence only; responsibility = command validation/application; state = mechanical; receiver = A/Brain; confidence = high for seam, medium for legacy retirement.
