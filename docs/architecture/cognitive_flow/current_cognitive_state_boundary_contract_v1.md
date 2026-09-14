# Current Cognitive State Boundary Contract v1

## Input boundary

Allowed inputs are governed references to Role, Field/View, Current Context, Goal, Survival, Cognitive Mode, Attention, Hypothesis, Belief, Reasoning Lifecycle, Decision Candidate/Resolution/Commitment, Time/Attention/Information/Energy Budget, Experience/Learning Candidate, future emotion interpretation/priority candidate, provenance, and trace.

Raw model output, provider payload, Field State handle, Snapshot write target, Fact Store, Reducer command, Decision result, Action command, Permission grant, personality mutation, emotion output asserted as authority, Memory, Learning execution output, or Hive authority output are forbidden.

## Output boundary

All Current Cognitive State outputs remain `candidate_only=true`, `not_fact=true`, `not_state_mutation=true`, `not_decision=true`, `not_action=true`, `not_permission=true`, and `not_memory=true`.

## Negative guards

- Cognitive State != Field State.
- Cognitive State != Memory.
- Cognitive State != Personality.
- Cognitive State != Emotion.
- Cognitive State != Decision.
- Cognitive State != Action.
- Cognitive State != State Store or State Machine.
- Experience != Cognitive State Authority.
- Emotion != Cognitive State Authority.
- Cognitive State != Reducer replacement.
- Reducer remains the only State Mutation Authority.
