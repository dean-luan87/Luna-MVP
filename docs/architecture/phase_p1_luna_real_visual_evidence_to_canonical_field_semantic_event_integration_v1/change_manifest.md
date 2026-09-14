# Change Manifest

Added:

- evaluation-only `CanonicalFieldSemanticEventProjectionCandidateV1` and case
  result contracts;
- a thin semantic adapter reusing the previous real visual Projection engine,
  existing Field Event Admission, Field Kernel adapter, and Field State Reducer;
- user-terminal Runner and fail-closed Verifier;
- phase documentation.

Modified:

- no canonical Field Event, Field Reducer, Provider Runtime, YOLO adapter, OCR,
  Gateway, A-Route, CState, or Situated Preconditions implementation;
- no Evidence Sufficiency threshold or policy selection semantics.

The semantic adapter emits `field_definition_observed` as a candidate
observation event. It does not resolve the visual class to a semantic subject,
does not emit a boolean/enum presence value, and does not promote facts.

Confidence is now passed from the existing real visual Projection into the
semantic Event payload and Reducer confidence snapshot, removing the previous
integration's hardcoded `0.9` substitution.

Known policy trace note: the code policy registry's
`insufficient_evidence_unresolved` state-type list does not include
`presence_state`, while the state-type policy mapping does. This is recorded by
the Runner as `POLICY_TRACE_COMPATIBILITY_GAP`; it is not silently repaired in
this phase.

No Runtime was executed by the Agent.

## Closure record

The final user-terminal verification completed with
`all_checks_passed=true`, `failed_checks=[]`,
`cognitive_logic_result=PASS`, `operational_result=PASS`,
`final_decision=GO`, and `validation_errors_empty=true`.

The real path verified was:

`Real YOLO -> Runtime Observation -> Visual Evidence Candidate -> VisualEvidenceFieldProjectionCandidateV1 -> Canonical Field Semantic Projection -> FieldEventCandidateV1(event_type=field_definition_observed) -> admit_field_event(...) -> FieldKernelReducerAdapterV1 -> FieldStateReducerModuleV1`

The terminal run recorded real Provider/Model invocation, 12 detections, 12
visual Evidence candidates, and a `5712 x 4284` frame. The recorded Provider
result was not used. The confidence lineage was preserved as:

`source_visual_confidence = field_projection_confidence = semantic_event_confidence = reducer_measured_confidence = 0.8794201016426086`

The canonical Event remained compatible but unresolved at the semantic state
layer: `semantic_state_resolution_status=UNRESOLVED`,
`subject_ref_candidate=null`, and `semantic_value_candidate=null`. No
`presence=true` was fabricated. Detection class `chair` remained an
Observation Semantic Candidate, target binding remained unresolved, and no
Field/World Truth was promoted.

The `2` Event / `2` source Evidence Sufficiency contract was not changed.
The verified `1` admitted Event / `1` source result was expected
`insufficient_evidence`, `no_eligible_candidate`, and `no_state_change`.
The Reducer remained candidate-only with `candidate_value={}`,
`fact_admitted=false`, `persisted=false`, and no state-store write.

`POLICY_TRACE_COMPATIBILITY_GAP` is retained as known contract consistency
debt and non-blocking for this phase; Policy Registry and fallback semantics
were not modified. Historical `WAITING_FOR_USER_TERMINAL_VERIFICATION` is
retained as history only.

Current status: `GO — VERIFIED — PHASE CLOSED`.

## Post-closure follow-up

The subsequent Canonical Subject Reference Reuse Audit selected
`ROUTE B — THIN_SUBJECT_BINDING_OVER_EXISTING_REFERENCE`, reusing the existing
candidate-only `EntityCandidateV1` from the Cognitive Primitive Layer. The
follow-up does not reopen this closed phase and does not alter its verified
43/43 result or semantic-event/reducer behavior.
