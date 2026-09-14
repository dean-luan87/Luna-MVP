# Cognitive Field Representation DryRun Contract v1

Each fixture emits `CognitiveFieldRepresentationCandidateV1` with the required identity, Context, Primitive, Concept, temporal, spatial, task, attention, relevance, uncertainty, provenance, and trace fields. Every candidate fixes `candidate_only=true`, `field_state=false`, `not_state=true`, and `not_fact=true`.

All runtime, provider, model, SLAM, Field Kernel mutation, Reducer, State/Snapshot/history mutation, Fact, Decision, Action, Memory, and Learning flags are false. Fixture provenance retains evidence/source, Concept binding, source-capability, and matching trace references.
