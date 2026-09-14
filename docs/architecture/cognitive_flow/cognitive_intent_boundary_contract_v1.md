# Cognitive Intent Understanding Boundary Contract v1

## Allowed candidate references

Language Input, user behavior signal, Context, Situation, Goal, Assistance, provenance, and trace references may be read.

## Rejected inputs and effects

Personality, Identity, Emotion State, Social Relationship, raw model/provider output, Decision result, Action command, permission, State handle, Reducer command, Memory mutation, Emotion Engine, Language Runtime, Learning runtime, and Hive authority are outside this layer.

## Negative guards

- Intent != Command.
- Intent != Goal.
- Intent != Decision.
- Intent != Action.
- Intent != Permission.
- Intent != Emotion.
- Intent != Personality.
- Intent != Identity.
- Goal != Intent Completion.
- Context != Intent Authority.
- Unknown Intent != Failure.
- Language != Direct Action Authority.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not command, not goal, not emotion, not personality, not identity, not decision, not action, not permission, and not memory.
