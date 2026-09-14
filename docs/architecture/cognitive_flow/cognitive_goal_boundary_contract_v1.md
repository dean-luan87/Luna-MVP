# Cognitive Goal Understanding Boundary Contract v1

## Allowed candidate references

User Input, Context, Situation, Mission reference, Capability, Assistance, Affordance, Behavior Boundary, provenance, and trace references may be read.

## Rejected inputs and effects

Task Planner, Decision result, Action command, permission, Personality, Emotion, Identity, Mission System, raw model/provider output, State handle, Reducer command, Memory mutation, Learning runtime, and Hive authority are outside this layer.

## Negative guards

- Goal != Command.
- Goal != Decision.
- Goal != Action.
- Goal != Permission.
- Goal != Mission.
- Goal != Identity.
- Goal != Emotion.
- Goal != Context.
- Context != Goal.
- Goal != Capability.
- Capability != Goal Completion.
- Unknown Goal != Failure.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not command, not mission, not identity, not emotion, not decision, not action, not permission, and not memory.
