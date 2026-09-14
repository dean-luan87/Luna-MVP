# Change Manifest

## Added

- Evaluation-only `VisualEvidenceSubjectBindingCandidateV1` and case-result
  contracts.
- A thin integration engine that reuses the real visual projection,
  `EntityCandidateV1`, the existing canonical semantic-event projection,
  Field Event Admission, and the Field State Reducer.
- User-terminal Runner and fail-closed Verifier.
- Phase documentation.

## Not Modified

- Cognitive Primitive canonical contract or owner.
- Provider Runtime, YOLO adapter, OCR, Gateway, A-Route, CState,
  Situated Preconditions, Field Event Admission, Field Reducer, or Policy
  Registry.
- Evidence Sufficiency thresholds, Target Binding, Memory, or PCN semantics.

## Semantic Boundary

The new layer populates `subject_ref_candidate` with an L1
`EntityCandidateV1.entity_id`. It does not resolve physical/canonical subject
identity, does not set `presence=true`, and does not promote Field or World
Truth. `semantic_state_resolution_status` remains `UNRESOLVED` and
`semantic_value_candidate` remains `null`.

Candidate IDs include runtime observation, evidence, and detection references;
class labels alone cannot identify an entity. Visual confidence remains
observation confidence and is not identity-resolution confidence.

## Historical Follow-up

The prior Canonical Field Semantic Event phase remains
`GO — VERIFIED — PHASE CLOSED`. Its post-closure subject-reference audit
selected `ROUTE B — THIN_SUBJECT_BINDING_OVER_EXISTING_REFERENCE`; this phase
implements only that L1 candidate binding and does not reopen the prior phase.

`POLICY_TRACE_COMPATIBILITY_GAP` remains independent and intentionally
unmodified.

## Current Status

`GO — VERIFIED — PHASE CLOSED`

## Runtime Verification Repair History

The first user-terminal Runtime reached real Provider execution and the full
Entity Candidate / Subject Binding path. Verification then failed before a
valid result because the Runner emitted null frame dimensions and the Verifier
used an unsafe `None > 0` comparison.

Classification:

```text
RUNTIME_SUMMARY_FRAME_DIMENSION_INTEGRATION_GAP
VERIFIER_NULL_SAFETY_GAP
```

The Runner repair reads `frame_dimensions` from the same real
`ProviderNativeDetectionRecordV1` used by the visual evidence path. It does
not hardcode `5712 x 4284`, infer dimensions from bbox, or create a second
source. The Verifier repair is fail-closed null/type safety only.

No cognitive semantics, EntityCandidate contract, Subject Binding semantics,
Evidence Sufficiency, Reducer, or Policy Registry semantics changed. Negative
cases with `admission=null` remain semantic guard cases and are not forced
through Field Admission or Reducer.

## Closure Record

The final user-terminal verification completed with:

```text
all_checks_passed=true
failed_checks=[]
cognitive_logic_result=PASS
operational_result=PASS
final_decision=GO
validation_errors_empty=true
```

The real Runtime recorded 12 detections, 12 visual Evidence candidates, and
12 Entity Candidates. Frame dimensions were `5712 x 4284`, sourced from
`ProviderNativeDetectionRecordV1.frame_dimensions`. Subject binding was
`CANDIDATE_BOUND` at L1 while identity and semantic state resolution remained
`UNRESOLVED`.
