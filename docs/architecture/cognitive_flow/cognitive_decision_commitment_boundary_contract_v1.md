# Decision Commitment Boundary Contract v1

## Input boundary

Only governed candidate references may enter: Decision Candidate/Choice Space, Value Evaluation, Context, Goal, Survival, Mission, Cognitive Constraint, Behavior Boundary, Belief, Hypothesis, Reasoning Lifecycle, Experience/Library pattern, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result, Action command, Permission grant, Memory, Learning output, or Hive/Library output asserted as authority are forbidden.

## Output boundary

All Commitment, stopping, termination, delay, reversal, and escalation artifacts are candidate-only: `not_fact`, `not_state`, `not_decision`, `not_action`, `not_permission`, and `not_memory`.

## Negative guards

- Decision Commitment != Decision.
- Commitment != Action.
- Commitment != Command.
- Stopping != Truth.
- Reasoning Termination != Decision.
- Delay != Action Execution.
- Reversal Candidate != State/History Rewrite.
- Escalation != External Invocation.
- Experience != Automatic Commitment.
- Mission != Survival Override.
- Confidence != Authority.
- Reducer remains the only State Mutation Authority.
