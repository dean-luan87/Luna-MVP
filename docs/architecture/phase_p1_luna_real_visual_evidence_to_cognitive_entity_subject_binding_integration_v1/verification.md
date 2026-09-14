# Verification

## Verification Mode

The Runner and Verifier are user-terminal artifacts. The Agent did not execute
Python, YOLO, Provider Runtime, OCR, or verification commands.

The expected execution mode is `LIVE_RUNTIME` for the reused real YOLO source;
the new subject-binding layer itself is evaluation-only and candidate-only.

## Required Checks

The fail-closed Verifier checks:

- real Provider/Model invocation and no recorded-result fallback;
- runtime observation, evidence, bbox, frame dimensions, and provenance;
- reuse of `EntityCandidateV1` rather than a duplicate contract;
- observation/evidence-derived candidate ID;
- L1 subject reference and populated `subject_ref_candidate`;
- candidate binding with unresolved identity resolution;
- unresolved semantic state and null semantic value;
- unresolved Target Binding;
- unchanged `minimum_event_count=2` and `source_diversity_requirement=2`;
- `insufficient_evidence` / `no_eligible_candidate` fail-closed behavior;
- visual confidence lineage distinct from identity-resolution status;
- preservation of `POLICY_TRACE_COMPATIBILITY_GAP`;
- no Field/World Truth, Memory/PCN mutation, or Decision/Task/Action/device
  behavior.

The same-class negative case requires distinct candidate IDs for distinct
detection references. A matching class label is not treated as physical
identity.

## Expected Semantic Result

The positive case should have a non-null L1 `subject_ref_candidate`, while
remaining unresolved at L2:

```text
subject_reference_layer = L1
resolved_subject_layer_entered = false
persistent_identity_layer_entered = false
identity_resolution_status = UNRESOLVED
semantic_state_resolution_status = UNRESOLVED
semantic_value_candidate = null
```

The existing one-event/one-source evidence sufficiency contract remains
insufficient and does not change because of an Entity Candidate or binding
candidate.

## First Terminal Attempt and Repair

The first user-terminal attempt entered the real YOLO and subject-binding
runtime successfully. It then produced:

```text
frame_dimensions.width = null
frame_dimensions.height = null
```

The direct cause was a summary projection reading `frame_width` and
`frame_height` from the semantic projection object, which does not own those
fields. The real dimensions were already present in the same Provider result's
`ProviderNativeDetectionRecordV1.frame_dimensions` and in the reused visual
projection's `frame_width` / `frame_height`.

The repair is classified as:

```text
RUNTIME_SUMMARY_FRAME_DIMENSION_INTEGRATION_GAP
VERIFIER_NULL_SAFETY_GAP
```

The Runner now propagates dimensions from the real Provider detection record.
The Verifier treats missing, `None`, boolean, non-numeric, or non-positive
dimensions as a failed check rather than raising `TypeError`; invalid data
cannot silently pass.

This was not a cognitive, subject-binding, Provider execution, or Reducer
failure. The first attempt did not establish a valid verifier result. After
repair, the final user-terminal verification completed with:

```text
all_checks_passed=true
failed_checks=[]
cognitive_logic_result=PASS
operational_result=PASS
final_decision=GO
validation_errors_empty=true
```

The final Runtime recorded 12 detections, 12 visual Evidence candidates, and
12 Entity Candidates, with `frame_dimensions=5712 x 4284` sourced from
`ProviderNativeDetectionRecordV1.frame_dimensions`. The phase is now
`GO — VERIFIED — PHASE CLOSED` for the declared L1 scope.

The verified confidence lineage was:

```text
source_visual_confidence
= field_projection_confidence
= semantic_event_confidence
= reducer_measured_confidence
= 0.8794201016426086
```

This remains visual observation confidence and is not identity-resolution
confidence. The sufficiency contract remained:

```text
1 Event / 1 Source < 2 Events / 2 Sources
evaluation_status = insufficient_evidence
```

That result is expected fail-closed behavior, not a Runtime failure. The
`POLICY_TRACE_COMPATIBILITY_GAP` remains known, non-blocking, independent debt
and was not repaired in this phase.
