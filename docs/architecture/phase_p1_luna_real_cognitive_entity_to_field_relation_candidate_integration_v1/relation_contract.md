# Relation Contract and Ownership

## Reused canonical contract

`RelationCandidateV1` is defined in
`capabilities/cognitive_flow/cognitive_primitives/types_v1.py` and is created
through `create_relation_candidate()` in `api_v1.py`.

Its actual fields are:

```text
relation_id
subject_ref
predicate
object_ref
evidence_refs
trace_ref
provenance_refs
schema_version
candidate_only
fact_admitted
```

The phase uses:

```text
subject_ref = EntityCandidateV1.entity_id
predicate   = OBSERVED_IN_FIELD
object_ref  = field:visual-frame:v1
```

`evidence_refs`, `trace_ref`, and `provenance_refs` retain the visual
observation lineage. The relation contract has no confidence field. Therefore
visual observation confidence is not copied into relation confidence;
relation confidence is reported as unavailable.

## Meaning boundary

`OBSERVED_IN_FIELD` is an observation-linked candidate relation. It does not
mean:

```text
Observed In Field != Belongs To Field
Observed In Field != Persistent Presence
Observed In Field != Ownership
Observed In Field != Function
Observed In Field != Field-conditioned Meaning
```

The Field reference is a controlled context candidate, not a resolved physical
Field identity. The relation is candidate-only and `fact_admitted=false`.

The following boundaries remain explicit:

```text
Detection Class != Entity Identity
Entity Candidate != Physical Object Identity
Candidate Binding != Identity Resolution
Entity Candidate != Target Binding
Entity Candidate != Memory Identity
Entity Candidate != Evidence Source
Semantic Event Admission != Fact Admission
Fact Admission != Field Truth
```

## Ownership

The Cognitive Primitive Layer owns `RelationCandidateV1` construction. The
evaluation integration is only an adapter from the already existing real
visual/entity candidate path. It does not modify Field Kernel authority, Field
Event Admission, Reducer policy, Evidence Sufficiency, Target Binding, Memory,
or PCN.

This is the first runtime relation-level integration of the canonical
Field-conditioned entity principle. It is not Field-conditioned semantic
meaning resolution and does not implement cross-Field identity or meaning
reuse.

