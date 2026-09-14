# A3 Translation Layer Freeze Checklist v1

## Boundary Checklist

- [x] Input is an Evidence/Context reference envelope only.
- [x] Source capability, Evidence, Context, provenance, and trace references are required.
- [x] Output is limited to a Cognitive Primitive Candidate.
- [x] `candidate_only=true` and `fact_status=not_fact` are required.
- [x] Primitive types are restricted to Entity, Relation, Semantic, Spatial, and Temporal candidates.
- [x] Fact, Decision, Action, State, Memory, and Learning admission are excluded.
- [x] Guard-1 through Guard-5 are frozen.
- [x] `runtime_authorized=false` remains unchanged.

## Evidence Checklist

- [x] Five fixed Validation Closure cases passed schema and Contract validation.
- [x] Semantic candidate boundary passed for OCR, Vision, Spatial, Audio, and Provenance Trace.
- [x] Evidence-to-Translation-to-Candidate provenance closure passed.
- [x] Independent Verifier did not invoke the Validation Runner, DryRun Runner, or Translation Skeleton.
- [x] run1/run2 canonical serialized outputs were equal.

## Regression Triggers

Any of the following invalidates this freeze and requires a controlled regression phase:

- request or candidate schema/field change;
- primitive type enum, candidate status, or boundary-flag change;
- Evidence/Context/provenance/source-capability/trace mapping change;
- Negative Guard inventory, assertion, or failure-level change;
- Translation Skeleton, fixture, serializer, validation runner, or independent verifier change;
- L1 Contract reference, Permission/Admission route, Traceability route, or Runtime boundary change;
- any proposal to bind real Evidence, invoke a model/service/database, write State, or authorize Runtime.

No item in this checklist grants Runtime, real Evidence, Fact admission, Decision, Action, or State mutation authority.

