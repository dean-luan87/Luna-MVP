# Decision Candidate Boundary Contract v1

## Input boundary

Allowed inputs are governed candidate references only: Survival, Mission, Context, Field/View, Attention, Information Value, Strategy, Depth, Hypothesis, Belief, Reasoning Lifecycle, Cognitive Constraint, Behavior Boundary, Behavior Candidate, Cognitive Value Evaluation, Experience/Library pattern, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result, Action command, permission grant, Memory, Learning output, or Hive/Library output asserted as authority are forbidden.

## Output boundary

All outputs remain `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`. They express only which options may enter a future Decision stage.

## Negative guards

- Decision Candidate != Decision.
- Decision Candidate != Action.
- Decision Candidate != Command.
- Decision Candidate != Permission.
- Decision Candidate != Policy.
- Decision Candidate != Behavior Execution.
- Conflict != Failure.
- Confidence != Authority.
- Experience != Automatic Shortcut.
- Knowledge != Authority or Permission.
- Mission != Survival Override.
- Model Output != Direct Decision Candidate Authority.
- Reducer remains the only State Mutation Authority.
