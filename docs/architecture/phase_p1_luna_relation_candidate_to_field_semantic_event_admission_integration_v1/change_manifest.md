# Change Manifest

## Added

- Evaluation-only `RelationBearingFieldSemanticEventProjectionV1`.
- A thin projection from the existing `RelationCandidateV1` and real visual
  lineage into a real `FieldEventCandidateV1`.
- User-terminal Runner and fail-closed Verifier.
- Phase documentation.

## Reused

- Existing real YOLO Provider execution and Runtime Observation path.
- Existing Visual Evidence and EntityCandidate/Subject Binding path.
- Existing `RelationCandidateV1` and `admit_field_event(...)`.

## Not modified

- Field Event taxonomy or canonical Field ontology.
- Field Event Admission implementation.
- Field Reducer, FieldStateCandidate, Policy Registry, or sufficiency rules.
- A-Route, CState, Target, Memory, PCN, Provider, OCR, SLAM, or Action Runtime.

## Semantic boundaries

`Trace Reference != Semantic Consumption != Field State Representation !=
Field Truth`.

`Entity Candidate != Physical Identity`, `OBSERVED_IN_FIELD != BELONGS_TO_FIELD`,
and `Event Admission != Fact Admission`.

The existing Field-Conditioned Entity Semantics and Cross-Field Information
Reuse principle is preserved: Field-conditioned relation/meaning is not written
into Entity intrinsic attributes.

## Status

`ROUTE B` was verified by the user terminal and is closed for its declared
scope. The final result was `all_checks_passed=true`, `failed_checks=[]`,
`cognitive_logic_result=PASS`, `operational_result=PASS`, and
`final_decision=GO`. `ROUTE C` and `ROUTE D` remain deferred.

Current status: `GO — VERIFIED — PHASE CLOSED`.

No Runtime was executed by the Agent.
