# ROUTE D assimilation contract

## Adapter input

`RelationStateAssimilationAdapterV1` accepts a reducer-governed
`FieldStateCandidate` only when:

- `state_type=entity_field_observation_relation_state`;
- `candidate_value` contains `subject_ref`, `predicate`, `object_ref`,
  `relation_candidate_ref`, and `relation_semantic_kind`;
- `predicate=OBSERVED_IN_FIELD`;
- `relation_semantic_kind=ENTITY_TO_FIELD_OBSERVATION_RELATION`;
- `candidate_only=true`, `fact_admitted=false`, `truth_declared=false`;
- `persistent_relation_declared=false` and
  `identity_resolution_status=UNRESOLVED`.

The adapter rejects unsupported state types, empty or incomplete values,
`BELONGS_TO_FIELD`, truth/persistence/identity promotion, and a raw
`RelationCandidate` without a Field State envelope.

## Compatible A-Route handoff

Existing `ARouteIngressRefsV1.relation_refs` remains the reference carrier.
The optional `relation_interpretation_candidates` field is additive and
preserves the typed candidate through `CognitiveStateFormationInputV1`.
`CognitiveRelationInterpretationCandidateV1` carries the read-only typed
semantic refs and provenance. `CurrentWorldCandidateV1` continues to expose
relation interpretation refs only; no new Current World relation owner is
created.

`Event/State ownership` remains with Field State Reducer / Field Kernel.
`Relation interpretation` and `CurrentWorldCandidate` remain owned by
Cognitive State Formation. A-Route orchestrates and consumes read-only
candidates.

`OBSERVED_IN_FIELD != BELONGS_TO_FIELD` and
`Candidate != Fact != Field Truth != World Truth` remain mandatory.

## Admission normalization

`ARouteOrchestrationEngineV1` normalizes admission information channels before
creating `CognitiveStateFormationInputV1`. `ControlledReplayAdmissionV1`
provides `required_information_refs` and `available_information_refs` only;
its evidence-binding and inherited-information channels are absent by
contract. `ObservationGatewayRuntimeAdmissionV1` provides all four channels.
The mapping is explicit and mode-specific. No replay field is renamed into a
LIVE-only field, and no admission contract is widened for A-Route convenience.

## Closure boundary

The final verified path is:

`FieldStateCandidate`
→ `RelationStateAssimilationAdapterV1`
→ `ARouteIngressRefsV1`
→ `CognitiveStateFormationInputV1`
→ `CognitiveRelationInterpretationCandidateV1`
→ `CurrentWorldCandidateV1.relation_interpretation_refs`

This proves typed relation semantics entered A-Route rather than only an
opaque relation reference. It remains candidate-only and preserves
`identity_resolution_status=UNRESOLVED`.
