# Cognitive Conflict Resolution Boundary Contract v1

## Input boundary

Permitted inputs are governed references to multiple candidate space, Context, Goal, Survival, Mission, Attention, Information Value, Strategy, Depth, Hypothesis, Belief, Reasoning Lifecycle, Behavior Boundary/Candidate, Value Evaluation, Decision Candidate/Commitment, Mode, Experience/Library pattern, future emotion weight/preference/attention-bias candidate, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result, Action command, Permission grant, personality mutation, emotion output asserted as authority, Memory, Learning output, or Hive output asserted as authority are forbidden.

## Output boundary

All Conflict Detection, Classification, Evaluation, and Resolution outputs remain `candidate_only=true`, `not_fact=true`, `not_state=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Negative guards

- Conflict != Error.
- Conflict != Failure.
- Conflict != Decision.
- Resolution Candidate != Resolution.
- Emotion != Conflict Authority.
- Emotion != Direct Decision or Action.
- Experience != Truth.
- Confidence != Authority.
- Model Output != Direct Conflict Resolution.
- Conflict Filtering != Policy Enforcement.
- Reducer remains the only State Mutation Authority.
