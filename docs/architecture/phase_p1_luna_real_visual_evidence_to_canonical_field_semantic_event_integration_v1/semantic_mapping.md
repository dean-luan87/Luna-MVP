# Semantic Mapping

## Canonical Event contract

The existing `FieldEventCandidateV1` contract requires an event id, event type,
Field reference, three temporal references, source chain, Evidence refs,
payload, and trace ref. `field_definition_observed` additionally has the
canonical observation semantics of original observation Evidence, temporal
fields, perspective scope, and Field scope. The new adapter supplies these
fields and then calls the existing `admit_field_event(...)` boundary.

The event payload records:

- `state_type=presence_state`;
- `perspective_scope` and `field_scope`;
- `target_type=field_definition` as the canonical observation vocabulary;
- `observed_object_class_candidate`;
- source visual Projection, Runtime Observation, detection, Evidence, and
  confidence references;
- `semantic_state_resolution_status=UNRESOLVED`.

## Presence-state boundary

The canonical `presence_state` registry allows a `boolean_or_enum` value and
recognizes `field_definition_observed` / `field_definition_asserted` source
events. The current visual detection does not resolve the required semantic
subject. Consequently `subject_ref_candidate=null` and
`semantic_value_candidate=null`; no `presence=true` is emitted.

## Separation of gates

The implementation preserves the following distinct boundaries:

`Semantic Event Admission != Evidence Sufficiency != Policy Selection != Fact Admission != Field Truth`

Admission may succeed while Reducer policy evaluation remains
`insufficient_evidence`. The existing minimum remains `2` Events and `2`
source IDs; detections from one YOLO invocation are not independent sources.

## Verified semantic boundaries

The final semantic projection remained candidate-only. Its canonical event
type was `field_definition_observed`, with `state_type=presence_state`, but
the subject and semantic value were unresolved:

- `semantic_state_resolution_status=UNRESOLVED`;
- `subject_ref_candidate=null`;
- `semantic_value_candidate=null`.

Consequently `observed_object_class_candidate=chair` was not converted to a
presence boolean, canonical subject, semantic target, physical identity,
Field Truth, or World Truth. Target binding remained
`EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE` with
`semantic_target_resolved=false`.

The following distinctions are frozen by the verified result:

`Detection Candidate != Canonical Subject`

`Canonical Semantic Event != Resolved Semantic State`

`Semantic Event Admission != Evidence Sufficiency`

`Evidence Sufficiency != Policy Selection`

`Event Admission != Fact Admission`

`Fact Admission != Field Truth Promotion`

`Multiple Detections From One Provider != Source Diversity`

The final admitted Event remained one Event from one source, so `1/1 < 2/2`
and `insufficient_evidence` was the expected fail-closed result. Twelve
detections from the same YOLO invocation were not counted as twelve
independent sources. `candidate_value={}` represented unresolved/no-state-
change candidate output, not an absence fact or resolved presence state.

Confidence lineage was preserved end to end:

`source_visual_confidence = field_projection_confidence = semantic_event_confidence = reducer_measured_confidence = 0.8794201016426086`

The code policy registry mismatch for
`insufficient_evidence_unresolved` and `presence_state` remains recorded as
`POLICY_TRACE_COMPATIBILITY_GAP`, classified as known contract consistency
debt and non-blocking for this phase.
