# Self State Awareness Go / No-Go v1

## Required readiness checks

- Self has distinct Identity, Capability, and State layers.
- Self State includes Physical State, Cognitive State, Capability State, and
  Resource State.
- Self State is dynamic and does not redefine Self Identity.
- Runtime and Diagnostics produce a Self State Update Candidate.
- The Reducer remains the sole State mutation authority.
- Low battery, high load, high risk, and state recovery produce candidates for
  Attention adjustment without directly selecting Goal or Decision.
- Brain receives a state summary and constraints while retaining Goal,
  Decision, value, action, and Identity authority.
- Experience can reference State but cannot automatically rewrite Self.
- Current evidence can support recovery and prevents permanent degradation.

## Explicit prohibitions

This architecture-only phase has No Emotion State, No Personality Change, No
Role, No Role, No Social Runtime, No B, No automatic learning, No online learning, No
Action, No Action Runtime, No real model, No OCR, No SLAM, No Camera, and No
Hardware Runtime. No Hardware Runtime is enabled. There is No direct Reality mutation, No direct Goal mutation,
No direct Decision mutation, No automatic frequency adjustment, and No
Scheduler implementation. No Scheduler implementation is enabled.

The agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
