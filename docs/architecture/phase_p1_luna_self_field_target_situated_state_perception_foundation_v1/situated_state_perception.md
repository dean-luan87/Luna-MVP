# Situated State Perception

`SituatedStatePerceptionRequestV1` is an input binding for one temporal
assessment.  It references the existing `SelfPerceptualViewpointStateV1` and
`RelativeObservationStateV1`, plus Field, Target, Evidence, and provenance
references.

`situated_state_perception_engine_v1.py` materializes four
`SituatedConditionStateCandidateV1` records.  It then derives the state’s
`satisfied_condition_refs` from candidates whose status is `SATISFIED`.
Fixtures provide categorical observation candidates, not condition outcomes.

Every condition candidate is candidate-only and retains Self, Field, Target,
Relation, temporal, source, and provenance lineage.  It is not a World Truth
or a mutation of Self or Field.
