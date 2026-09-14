# Cognitive Constraint Boundary Contract v1

## Input boundary

Permitted inputs are governed references to Survival, Current Cognitive Context, Attention, Information Value, Strategy, Cognitive Depth, Hypothesis, Belief, Reasoning Lifecycle, Behavior Boundary, Minimum Sufficient Field Understanding, Field/View, Goal, Experience pattern, provenance, and trace.

Forbidden inputs are raw model output, provider payload, Fact Store, State handle, Reducer command, Decision output, Action command, permission grant, Memory, Learning output, or Hive output presented as authority.

## Output boundary

The only output is `CognitiveConstraintCandidateV1`: candidate-only, `not_fact`, `not_state`, `not_decision`, `not_action`, `not_permission`, and `not_memory`. It can indicate a constraint condition or required evidence; it cannot enforce a rule.

## Frozen negative guards

- Cognitive Constraint != Decision.
- Cognitive Constraint != Safety Rule Database.
- Cognitive Constraint != Action Controller.
- Risk != Fact.
- Unknown != Failure.
- Confidence != Permission.
- Experience != Shortcut Authority.
- Model Output != Direct Constraint Authority.
- Reducer remains the only State Mutation Authority.

No constraint candidate may change Field State, Context, Memory, Permission scope, or the governing Constitution/Protocol.
