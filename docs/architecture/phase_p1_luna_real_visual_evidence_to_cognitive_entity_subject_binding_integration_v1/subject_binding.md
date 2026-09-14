# Subject Binding

## Existing Contract

The implementation reuses `EntityCandidateV1` from the Cognitive Primitive
Layer. Its required inputs are an `entity_id`, `entity_type`, attributes,
evidence references, observation references, a trace reference, and provenance.
The contract defaults to `candidate_only=true` and `fact_admitted=false`.

The candidate is created through the existing `create_entity_candidate()` API;
no parallel visual/entity type is introduced.

## Candidate ID

The integration-level candidate ID is derived from the runtime observation,
evidence, and detection references:

```text
entity-candidate:visual:<runtime-observation-ref>:<evidence-ref>:<detection-ref>
```

It is never derived from `class_label` alone. Distinct detection references
therefore remain distinct candidates even when their class candidates match.

## Thin Binding Contract

`VisualEvidenceSubjectBindingCandidateV1` records:

- the `EntityCandidateV1` reference;
- source runtime observation, evidence, and detection references;
- the evaluation Field reference;
- `binding_status=CANDIDATE_BOUND`;
- `identity_resolution_status=UNRESOLVED`;
- the existing unresolved Target Binding status;
- trace and provenance references;
- `candidate_only=true`, `fact_admitted=false`, and `truth_declared=false`.

The binding is a relationship candidate, not an identity resolver.

## Semantic Event Mapping

The existing `field_definition_observed` semantic projection is copied only
through the previous integration helper and receives:

```text
subject_ref_candidate = EntityCandidateV1.entity_id
subject_reference_layer = L1
```

It deliberately retains:

```text
semantic_state_resolution_status = UNRESOLVED
semantic_value_candidate = null
```

Therefore candidate subject availability does not create `presence=true`.

## Final Runtime Record

The final user-terminal run recorded:

```text
execution_mode=LIVE_RUNTIME
provider_invoked=true
model_invoked=true
provider_real_execution_attempted=true
provider_real_execution_verified=true
recorded_provider_result_used=false
detection_count=12
real_visual_evidence_count=12
entity_candidate_count=12
frame_dimensions=5712 x 4284
frame_dimensions_source=ProviderNativeDetectionRecordV1.frame_dimensions
```

At least two real YOLO detections were `chair`, with approximate confidence
values `0.8794201016426086` and `0.727204442024231`. They received different
`EntityCandidateV1.entity_id` values. Same class therefore did not become
same entity identity.

The final binding remained L1 candidate-only:

```text
binding_status=CANDIDATE_BOUND
identity_resolution_status=UNRESOLVED
resolved_subject_layer_entered=false
persistent_identity_layer_entered=false
semantic_state_resolution_status=UNRESOLVED
semantic_value_candidate=null
semantic_target_resolved=false
```

## Explicit Non-Equivalences

```text
Detection Class != Entity Identity
Entity Candidate != Physical Entity Identity
Candidate Binding != Identity Resolution
subject_ref_candidate != resolved subject_ref
Entity Candidate != Target Binding
Entity Candidate != Memory Identity
Entity Candidate != Evidence Source
Semantic Event Admission != Fact Admission
Fact Admission != Field Truth
```
