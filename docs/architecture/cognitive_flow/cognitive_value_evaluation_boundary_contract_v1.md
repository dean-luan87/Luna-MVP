# Cognitive Value Evaluation Boundary Contract v1

## Input boundary

Permitted inputs are governed references to Mission, Survival, Context, Attention, Information Value, Strategy, Cognitive Depth, Hypothesis, Belief, Reasoning Lifecycle, Cognitive Constraint, Behavior Boundary, Behavior Candidate, Field/View, Experience/Library pattern, provenance, and trace.

Forbidden inputs are raw model output, provider payload, Fact Store, State handle, Reducer command, Decision output, Action command, permission grant, Memory, Learning output, or Library/Hive output presented as authority.

## Output boundary

Output is only a Candidate Evaluation and must remain `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Negative guards

- Mission != Command.
- Mission != Action.
- Mission != Survival Override.
- Survival != Risk Avoidance Only.
- Value Evaluation != Decision.
- Value Evaluation != Action Selection.
- Value Evaluation != Reward Model or Reinforcement Learning Reward.
- Risk != Fact.
- Confidence != Authority.
- Experience != Truth or Automatic Shortcut.
- Knowledge != Permission.
- Model Output != Direct Behavior.
- Reducer remains the only State Mutation Authority.
