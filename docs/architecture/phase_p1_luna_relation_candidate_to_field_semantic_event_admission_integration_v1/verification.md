# Verification

## Verification mode

The Runner uses `LIVE_RUNTIME` only for the already existing real YOLO
Provider path. The Agent does not execute Runtime. Field Reducer and A-Route
are deliberately not invoked in this phase.

## Positive case

`ENTITY_FIELD_RELATION_SEMANTIC_EVENT_ADMITTED` verifies:

`Real YOLO -> Runtime Observation -> Visual Evidence -> EntityCandidateV1 -> Subject Binding -> RelationCandidateV1 -> Relation-bearing Field Semantic Event -> FieldEventCandidateV1 -> admit_field_event(...)`

The verifier checks Provider/Model execution metadata, Runtime Observation,
Evidence, Entity Candidate, Relation Candidate, explicit semantic kind,
relation payload identity, complete detection/evidence/entity/binding/runtime
lineage, and `admission_status=admitted_event`.

Admission remains candidate-only:

`candidate_only=true`, `fact_admitted=false`, `truth_declared=false`, and
`persistent_relation_declared=false`.

## Negative guards

The Runner includes guards for:

- relation event is not Field Truth;
- `OBSERVED_IN_FIELD` is not `BELONGS_TO_FIELD`;
- admission does not create a persistent relation;
- relation does not resolve physical identity or Target;
- relation, Entity Candidate, and Subject Binding are not source diversity;
- an unresolved Field ref is rejected by the existing Admission contract.

## Preserved boundaries

Evidence Sufficiency remains `2 Events / 2 Sources`. The phase does not invoke
the Reducer and does not change `POLICY_TRACE_COMPATIBILITY_GAP`. Field State
relation representation (`ROUTE C`) and A-Route relation consumption (`ROUTE
D`) remain deferred.

The existing Field-conditioned Entity Semantics principle remains in force:
stable Entity/class knowledge may be reused, while Field-conditioned relations
and meanings are not intrinsic Entity attributes.

## Closure result

The final user-terminal result was:

```text
all_checks_passed=true
failed_checks=[]
cognitive_logic_result=PASS
operational_result=PASS
final_decision=GO
validation_errors_empty=true
```

The result verified explicit relation semantic projection, preservation of the
Relation/Entity/Subject-Binding/Observation lineage through
`FieldEventCandidateV1`, and `admission_status=admitted_event` without Fact or
Field Truth promotion.

Current status: `GO — VERIFIED — PHASE CLOSED`.
