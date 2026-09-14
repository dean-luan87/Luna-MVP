# Relation State Contract

## State mapping

The minimal explicit mapping is:

| Item | Value |
|---|---|
| State type | `entity_field_observation_relation_state` |
| Source event type | `entity_field_relation_observed` |
| Relation kind | `ENTITY_TO_FIELD_OBSERVATION_RELATION` |
| Predicate | `OBSERVED_IN_FIELD` |
| State value shape | typed object |
| Support policy | existing `multi_event_consensus` |

`presence_state` is not reused, and the existing Field↔Field
`field_relation_observed` / `FieldRelationV1` semantics are not changed.

## Typed value

`EntityFieldRelationStateValueV1` is stored inside the existing
`FieldStateCandidate.candidate_value` and contains:

- `relation_candidate_ref`
- `subject_ref`
- `predicate`
- `object_ref`
- `relation_semantic_kind`
- `evidence_refs`
- `source_refs`
- `trace_ref`
- `provenance_refs`

The value also freezes `candidate_only=true`, `fact_admitted=false`,
`truth_declared=false`, `persistent_relation_declared=false`, and
`identity_resolution_status=UNRESOLVED`.

`OBSERVED_IN_FIELD` means observation-linked relation in the current Field
context. It does not mean `BELONGS_TO_FIELD`, ownership, persistence, or
Field Truth.

