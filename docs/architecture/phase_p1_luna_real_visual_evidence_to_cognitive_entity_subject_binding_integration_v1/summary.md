# Summary

This phase adds the missing L1 candidate reference between visual evidence and
the existing canonical Field semantic-event projection:

```text
Real YOLO
  -> Runtime Observation
  -> Visual Evidence
  -> EntityCandidateV1
  -> VisualEvidenceSubjectBindingCandidateV1
  -> field_definition_observed Candidate
  -> Field Admission
  -> Field Reducer
```

The Entity Candidate is linked to evidence and observation provenance. Its ID
is not a class-only ID, and it is not a physical or persistent identity.

The semantic Event may now contain a non-null:

```text
subject_ref_candidate
```

but this does not change:

```text
identity_resolution_status = UNRESOLVED
semantic_state_resolution_status = UNRESOLVED
semantic_value_candidate = null
semantic_target_resolved = false
```

Evidence Sufficiency remains `2 events / 2 sources`; one YOLO invocation,
multiple detections, Entity Candidates, and binding candidates do not create
source diversity. Reducer behavior therefore remains candidate-only and
fail-closed.

The phase does not enter L2 resolved subject identity or L3 persistent Memory
identity. It does not mutate Field, World, Memory, or PCN state and does not
execute Decision, Task, Action, device, or camera control.

The first terminal Runtime reached real YOLO and binding but exposed a summary
lineage defect: dimensions were read from the semantic projection, which does
not contain them. The corrected lineage is:

```text
ProviderNativeDetectionRecordV1.frame_dimensions
  -> Runner.frame_dimensions
```

The Verifier now fails safely for missing or invalid dimension values instead
of crashing. This is an integration/verification contract repair, not a change
to cognition or identity semantics.

The final user-terminal verification recorded:

```text
all_checks_passed=true
failed_checks=[]
cognitive_logic_result=PASS
operational_result=PASS
final_decision=GO
validation_errors_empty=true
```

It verified real YOLO invocation, 12 detections, 12 visual Evidence
candidates, 12 Entity Candidates, and `5712 x 4284` dimensions from
`ProviderNativeDetectionRecordV1.frame_dimensions`.

The same-class runtime evidence included two `chair` detections with
approximate confidences `0.8794201016426086` and `0.727204442024231`; their
candidate IDs were different. The confidence lineage remained:

```text
source_visual_confidence
= field_projection_confidence
= semantic_event_confidence
= reducer_measured_confidence
= 0.8794201016426086
```

The unchanged sufficiency contract means `1 Event / 1 Source < 2 Events / 2
Sources`, so `insufficient_evidence` remains expected fail-closed behavior.
`POLICY_TRACE_COMPATIBILITY_GAP` remains known, non-blocking, independent debt.

Current status: `GO — VERIFIED — PHASE CLOSED`.

## Post-closure architectural addendum

Future Entity work must follow the [Field-Conditioned Entity Semantics &
Cross-Field Information Reuse Principle v1](../../field_conditioned_entity_semantics_and_cross_field_information_reuse_v1.md):
cross-Field information reuse is permitted as a governed candidate/reference,
while Field-conditioned semantic meaning remains independent. This reference
does not reopen or alter the closed phase.
