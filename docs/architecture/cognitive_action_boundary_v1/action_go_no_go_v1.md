# Action Boundary Go / No-Go v1

## Required readiness checks

- Decision Candidate is separated from Action Intent, Action Request, and
  Action Command.
- Action Request includes decision_reference, intent, target, constraints,
  confidence, required_capability, and authorization_level.
- Permission classes distinguish low-risk, medium-risk, high-risk, and Safety
  Action Candidate handling.
- High-risk requests require authorization candidate from Brain/User.
- Action cannot directly modify Reality; External World Change must return as
  Evidence through Reality Update Candidate and Reducer.
- Action Failure produces Outcome Evidence and Cause Attribution Candidate, not
  an automatic Decision Failure.
- Action Capability interface uses Capability Governance and cannot directly
  call a model or Provider.
- Action Attention interface produces observation and monitoring candidates;
  Attention does not execute Action.
- Brain retains Goal, Decision, Value, and authorization authority.
- Reducer remains the sole State mutation authority.

## Explicit prohibitions

This architecture-only phase has No real Action Runtime, No hardware control,
No automatic execution, No robot movement, No payment, No external system
operation, No Emotion, No Role, No Social Runtime, No B, No real model, No OCR,
No SLAM, No Camera, No Hardware Runtime, and No Action execution. There is No
direct Reality mutation, No direct Goal mutation, and No direct Decision
mutation.

Safety Action Candidate is candidate-only.
The interface cannot directly call a model.
No external system operation is enabled.
No direct Reality mutation is enabled.
No direct Decision mutation is enabled.

The agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
