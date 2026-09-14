# Cognitive Mode Switching Boundary Contract v1

## Input boundary

Allowed inputs are governed candidate references to Survival, Field/View/Dynamics, Context, Goal, Attention, Information Value, Strategy, Time Budget, Cognitive Depth, Hypothesis, Belief, Reasoning Lifecycle, Behavior Boundary, Decision Commitment, Experience pattern, provenance, and trace.

Raw model output, provider payload, Fact Store, State handle, Reducer command, Decision result, Action command, Permission grant, personality mutation, emotion engine output asserted as authority, Memory, Learning output, or Hive output asserted as authority are forbidden.

## Output boundary

All Mode Switching output is candidate-only: `not_fact`, `not_state`, `not_decision`, `not_action`, `not_permission`, and `not_memory`.

## Negative guards

- Mode != Decision.
- Mode != Action.
- Mode != Permission.
- Mode != Personality.
- Mode != Role.
- Mode != Emotion.
- Mode != Runtime Scheduler.
- Experience != Automatic Mode Switch.
- Field Dynamics != State Mutation.
- Confidence != Authority.
- Reducer remains the only State Mutation Authority.
