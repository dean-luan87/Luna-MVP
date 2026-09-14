# Field Behavior / Experience Go / No-Go v1

## Required readiness checks

- Field Behavior is distinct from Action, Decision, Goal, Personality, Role,
  and Emotion.
- Behavior Candidate is generated from Field, Self, Goal, Experience, Rule,
  Dynamic, Capability, and Unknown context.
- Historical Action Pattern is a Pattern Candidate and requires current Field
  validation.
- Personal Preference is context-bound and is not Emotion, Personality, Role,
  Goal, Decision, or Action.
- Reality > Experience is explicit.
- Behavior can create Attention Bias Candidate but cannot modify Attention,
  Goal, Decision, or Action directly.
- Task and Field interfaces preserve Task identity and lifecycle.
- Emotion Attachment Candidate and Role Binding Placeholder are schema-only.
- Experience associations preserve provenance, confidence, context, time decay,
  and Unknowns.
- A Route reviews Behavior Candidate before any future Action Boundary.

## Explicit prohibitions

No Emotion Runtime, No Role System, No Social Relationship, No Personality
Switching, No B, No Prediction, No Action Execution, No automatic planning, No
automatic learning, No direct Reality mutation, No direct Goal mutation, and No
direct Decision mutation.

Current Field validation is mandatory. No Personality Switching, No automatic
learning, and No direct Decision mutation are permitted.

Current Field validation remains required. No automatic learning is permitted.

The current Field validation result is required.

The Agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
