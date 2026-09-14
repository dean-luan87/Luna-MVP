# Cognitive Assistance Boundary Contract v1

## Allowed candidate references

Capability Awareness, Context, Situation/Affordance, Behavior Boundary/Candidate, information, risk, option, Experience, Human Collaboration, provenance, and trace references may be read.

## Rejected inputs and effects

Robot control, physical action, embodied runtime, runtime controller, permission engine, autonomous execution, Action command, Decision result, raw model/provider output, State handle, Reducer command, Memory mutation, Learning runtime, and Hive authority are outside this layer.

## Negative guards

- Assistance != Action.
- Assistance != Autonomous Execution.
- Suggestion != Decision.
- Suggestion != Permission.
- Capability != Execution.
- Cognitive Capability != Physical Capability.
- Information Support != Action Execution.
- Understanding != Control.
- Observation != Intervention.
- Human Action Authority remains with the human.
- Experience != Human Preference Mutation.
- Reducer remains the only State Mutation Authority.

Outputs remain candidate-only, not fact, not state mutation, not decision, not action, not permission, not control, not autonomous execution, and not memory.
