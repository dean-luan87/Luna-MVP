# Cognitive Capability Awareness Boundary Contract v1

## Allowed candidate references

Affordance, Situation, Current Context, Current Cognitive State, Resource, Experience, provenance, and trace references may be read.

## Rejected inputs and effects

Identity, Personality, Emotion, Self Model Runtime, Decision result, Action command, Action Permission, raw model/provider output, State handle, Reducer command, Memory mutation, Learning runtime, and Hive authority are outside this layer.

## Negative guards

- Capability != Affordance.
- Capability != Permission.
- Capability != Identity.
- Capability != Personality.
- Capability != Emotion.
- Capability != Decision.
- Capability != Action.
- Confidence != Authority.
- Unknown Capability != Unable.
- Experience != Current Capability.
- Experience != Reality.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not self model, not identity, not personality, not emotion, not decision, not action, not permission, and not memory.
