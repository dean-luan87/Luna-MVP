# Reducer Mapping

The Reducer continues to consume only admitted events:

`Field Event Admission -> reducer_input_candidate ->
FieldKernel/FieldStateReducer -> FieldStateCandidate`

The reduction handoff now preserves admitted event mappings so the relation
state reduction path can explicitly validate and read:

`subject_ref`, `predicate`, `object_ref`, `relation_candidate_ref`, and
`relation_semantic_kind`.

The typed value is constructed only for the relation state type when the
existing `multi_event_consensus` selection is made. It is not an opaque copy
of `event.payload`.

Evidence sufficiency remains unchanged:

`minimum_event_count=2` and `source_diversity_requirement=2`.

The real YOLO case has one source and remains `insufficient_evidence`. The
two-source case is explicitly
`CONTROLLED_MULTI_SOURCE_SEMANTIC_REDUCER_TEST`; it is not real multi-source
observation.

No state store write, fact admission, Field Truth promotion, or A-Route call
is added.

