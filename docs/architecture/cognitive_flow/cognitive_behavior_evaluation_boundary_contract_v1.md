# Cognitive Behavior Evaluation Boundary Contract v1

## Input boundary

Only governed candidate references may be evaluated: Behavior Candidate, Behavior Boundary, Cognitive Constraint, Context, Field/View, Goal, Survival, Belief, Hypothesis, Information Value, Experience pattern, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision output, Action command, permission grant, Memory, Learning output, and Hive/Library output presented as authority are forbidden.

## Output boundary

The output is `CognitiveBehaviorEvaluationCandidateV1`. It describes possible value, cost, risk, uncertainty, and reversibility only. It does not rank as a final choice, emit an action, grant permission, or change State.

## Frozen negative guards

- Behavior Evaluation != Decision.
- Evaluation Rank != Selection.
- Evaluation != Action.
- Value != Permission.
- Risk != Fact.
- Confidence != Authority.
- Experience != Automatic Preference.
- Model Output != Direct Evaluation Authority.
- Reducer != Behavior Evaluator.

Reducer remains the only State Mutation Authority. No evaluation may mutate Field, Context, State, Memory, or the governing Constitution/Protocol.
