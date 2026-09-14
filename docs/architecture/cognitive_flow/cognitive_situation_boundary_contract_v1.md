# Cognitive Situation Boundary Contract v1

## Allowed candidate references

Field Representation/View, object, Primitive, Concept, Relationship, Context, Experience, Knowledge, Attention, provenance, and trace references may be read.

## Rejected inputs and effects

Raw model/provider output, direct Decision, Action command, permission, Fact Store authority, State handle, Reducer command, Memory mutation, Situation Runtime, World Model, Simulation, Learning runtime, and Hive authority are outside this layer.

## Negative guards

- Situation != Fact.
- Situation != Context.
- Context != Situation.
- Situation != Decision.
- Situation != Action.
- Situation != Permission.
- Experience != Current Reality.
- Experience != Rule.
- Knowledge != Truth.
- Attention != Situation Authority.
- Unknown Situation != Failure.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not context, not decision, not action, not permission, and not memory.
