# Cognitive Behavior Candidate Boundary Contract v1

## Allowed inputs

Only governed references are permitted: Context, Field/Field View, Goal, Survival, Behavior Boundary, Belief, Hypothesis, Information Value, required evidence, Experience pattern reference, provenance, and trace.

Raw model output, provider payload, Fact Store, Memory, Learning output, State handle, Reducer command, Decision output, Action command, and permission grant are forbidden inputs.

## Output constraints

The output is `CognitiveBehaviorCandidateV1` with a Boundary reference. It must preserve candidate-only status and `not_fact`, `not_state`, `not_decision`, `not_action`, `not_permission`, and `not_memory` constraints.

## Frozen negative guards

- Behavior Candidate != Decision.
- Behavior Candidate != Action.
- Behavior Boundary != Permission.
- Belief != Behavior Authority.
- Experience != Automatic Selection.
- Survival != Action Command.
- Model Output != Direct Behavior.
- Reducer != Behavior Executor.

This contract creates no execution, admission, or State-mutation authority. Reducer remains the only State Mutation Authority.
