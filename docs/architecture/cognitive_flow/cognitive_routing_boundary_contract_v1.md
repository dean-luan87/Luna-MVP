# Cognitive Routing Boundary Contract v1

## Allowed candidate references

Context, Situation, Intent, Goal, Information Gap, Survival/risk, time/resource/depth/mode candidates, Experience/Knowledge, and provenance/trace references may be read.

## Rejected inputs and effects

Deep Reasoning Runtime, LLM Chain, model invocation, Simulation, World Model Runtime, Decision result, Action command, permission, Emotion State/Engine authority, raw provider output, State handle, Reducer command, Memory mutation, Learning runtime, and Hive authority are outside this layer.

## Future emotion interface

Future Emotion Engine may provide `Emotion State Candidate -> Cognitive Bias Candidate -> Routing Adjustment Candidate`; it cannot directly select a route, modify a goal, create Decision, Action, or permission.

## Negative guards

- Routing != Answer.
- Routing != Decision.
- Routing != Action.
- Routing != Permission.
- Routing != Intelligence Level.
- Deep Reasoning != Better Answer.
- More Compute != Better Outcome.
- Experience != Automatic Routing.
- Confidence != Authority.
- Emotion != Routing Authority.
- Route != Runtime Invocation.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not decision, not action, not permission, and not memory.
