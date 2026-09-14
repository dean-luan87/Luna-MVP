# Decision Resolution Boundary Contract v1

## Input boundary

Allowed inputs are governed references to Context, Goal, Mission Constraint, Survival Constraint, Behavior Boundary, Behavior Candidate, Decision Candidate/Choice Space, Risk Candidate, Value Evaluation, Time Budget, Cognitive Constraint, Belief/Hypothesis, Experience/Library pattern, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result, Action command, permission grant, policy mutation, Memory, Learning output, or Hive/Library authority output are forbidden.

## Output boundary

All Resolution artifacts remain `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Negative guards

- Decision Resolution != Decision.
- Decision Resolution != Action.
- Resolution Path != Command.
- Confidence != Authority.
- Value != Truth.
- Experience != Shortcut.
- Mission != Survival Override.
- Model Output != Direct Choice.
- Constraint Filtering != Policy Enforcement.
- Reversibility != Permission.
- Reducer != Decision Authority.
- Reducer remains the only State Mutation Authority.
