# Contract

## Reused canonical surfaces

The implementation reuses:

- `FieldStateCandidate` as the governed Field-side envelope;
- `CognitiveRelationInterpretationCandidateV1` as the cognitive candidate;
- `CognitiveStateFormationInputV1.relation_interpretation_candidates` as the
  typed read-only ingress;
- `CurrentWorldCandidateV1.relation_interpretation_refs` as the existing
  Current World handoff.

No second relation or meaning contract is introduced.

## Typed preservation

For every conditioned candidate, these fields are preserved:

`field_state_candidate_ref`, `subject_ref`, `predicate`, `object_ref`,
`relation_candidate_ref`, `relation_semantic_kind`, `evidence_refs`,
`source_refs`, `provenance_refs`, and `identity_resolution_status`.

The required boundary remains:

```text
predicate = OBSERVED_IN_FIELD
relation_semantic_kind = ENTITY_TO_FIELD_OBSERVATION_RELATION
candidate_only = true
fact_admitted = false
truth_declared = false
persistent_relation_declared = false
identity_resolution_status = UNRESOLVED
```

Role, Goal, Task, and Information Need references are attached from the
current cognitive request. Opaque Context references remain available at the
request, Attention, Hypothesis, and Current World layers; this phase does not
invent Context semantics.

## Semantic boundary

`OBSERVED_IN_FIELD != BELONGS_TO_FIELD`.

Conditioned interpretation is a cognitive candidate, not Field Truth, World
Truth, ownership, function, persistent identity, Target Binding, Memory, or
PCN state.

## Closure

The user-terminal result was:

```text
all_checks_passed=true
check_count=177
cognitive_logic_result=PASS
operational_result=PASS
failed_checks=[]
final_decision=GO
```

The implementation is closed at the existing candidate boundary. No new
meaning, identity, relation, memory, or decision contract was introduced.
