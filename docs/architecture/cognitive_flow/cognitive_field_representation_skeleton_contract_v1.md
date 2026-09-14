# Cognitive Field Representation Skeleton Contract v1

## Candidate fields

The immutable candidate contains `field_candidate_id`, Context/Snapshot/Primitive/Concept references, temporal/spatial/task/attention scopes, relevance partition, uncertainty, provenance, trace, and candidate status. It fixes `candidate_only=true`, `field_state=false`, `not_state=true`, and `not_fact=true`.

## Input boundary

Only pre-existing Primitive, Concept, Context, Temporal, Spatial, Task, Attention, Snapshot, provenance, and trace references are structurally accepted. Raw model output, provider payload, Memory, Fact, Decision, Action, State Handle, database reference, and reducer command are rejected by the builder.

## Output boundary

The serializer emits a candidate envelope only. It emits no State, Snapshot mutation, temporal-history update, Fact, Decision, Action, Memory, or Learning operation. It has no external invocation path.

## Prohibited fields

`state_id`, `snapshot_write_target`, `fact_id`, `decision_id`, `action_id`, and `memory_target` are absent by contract and rejected at input.
