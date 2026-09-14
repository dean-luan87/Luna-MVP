# Cognitive Behavior Boundary Contract v1

## Input contract

The future layer may consume only governed references: Current Cognitive Context, Field, Field Identity/Affordance, Survival Constraint, Goal, Belief, Risk, required evidence, provenance, and trace. Raw model output, provider payload, Fact Store, State handle, Decision, Action command, Reducer command, Memory, and Learning output are excluded.

## Output contract

`BehaviorBoundaryCandidateV1` can express allowed, restricted, and unknown behavior candidates, risk references, evidence requirements, provenance, and trace. It must remain candidate-only, `not_fact`, `not_state`, `not_decision`, `not_action`, and `not_memory`.

## Frozen negative guards

- Behavior Boundary != Action Permission.
- Behavior Boundary != Decision.
- Constraint != Command.
- Risk != Fact.
- Belief != Action.
- Experience != Permission.
- Field Affordance != User Intent.
- Model Output != Direct Behavior.
- Reducer != Behavior Controller.

The only State Mutation Authority remains the Reducer. This contract adds no execution authority and does not modify any existing contract.
