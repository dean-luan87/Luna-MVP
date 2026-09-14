# Relation Semantic Event Mapping

The thin projection maps the existing candidate relation without creating a
new relation owner:

| Relation candidate | Field Event payload |
|---|---|
| `relation_id` | `relation_candidate_ref` |
| `subject_ref` | `subject_ref` and `entity_candidate_ref` |
| `predicate=OBSERVED_IN_FIELD` | `predicate` |
| `object_ref` | `object_ref` and `field_ref` |
| `evidence_refs` | `evidence_refs` |
| Entity provenance detection refs | `source_detection_refs` |
| Runtime observation | `runtime_observation_ref` |
| L1 binding | `subject_binding_ref` |

The event payload also carries:

```text
relation_semantic_kind = ENTITY_TO_FIELD_OBSERVATION_RELATION
relation_semantic_status = CANDIDATE_ONLY
candidate_only = true
fact_admitted = false
truth_declared = false
persistent_relation_declared = false
identity_resolution_status = UNRESOLVED
```

The event is a real `FieldEventCandidateV1`. The existing Admission API is the
only admission boundary used. Admission copies the structured payload into its
`reducer_input_candidate`, preserving the relation lineage; it does not mean
Fact Admission, relation truth, Field Truth, or World Truth.

The existing `field_relation_observed` taxonomy is not repurposed. The
evaluation-level event type is `entity_field_relation_observed`, with the
explicit semantic kind above. No Field ontology or registry entry is changed.

The current Field context remains `field:visual-frame:v1` with its existing
controlled-context semantics. `OBSERVED_IN_FIELD` does not mean belongs to,
contains, ownership, function, persistence, or Field-conditioned meaning.
