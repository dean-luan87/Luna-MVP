# Situation Understanding Go / No-Go v1

## Required readiness checks

- Situation Model combines Reality, Cognitive Field, Self State, Self
  Capability, Goal Context, and Attention Context. Self Capability is required.
- Situation includes Environment Context, Self Context, Goal Context, Constraint
  Context, Risk Context, and Unknown Context. Constraint Context is required.
- Reality and Situation remain distinct; Evidence Support, provenance,
  confidence, and Unknown are retained.
- The same Reality can yield different Situation Candidates for different Self.
- New Evidence creates Reality Update, Field Update, and Situation
  Reassessment Candidates. Situation Reassessment Candidates are required.
- Capability degradation can lower Situation Confidence without changing
  Reality.
- Situation can produce Attention candidates and Brain input but cannot create
  Decision, Action, Goal, Prediction, or Value Judgment. It cannot create Decision.
- Experience is a reference and cannot override current Reality Evidence.
- Brain may request re-observation while retaining Goal and Decision authority.
- Reducer remains the sole State mutation authority.

## Explicit prohibitions

This architecture-only phase has No Decision, No Action, No Prediction, No
Emotion, No Emotion, No Role, No Social Runtime, No B, No automatic learning,
No online learning, No online learning, No real model, No OCR, No SLAM, No Camera, No Hardware Runtime, and
No Runtime execution. There is No direct Reality mutation, No direct Goal
mutation, and No direct Decision mutation. No direct Goal mutation.

The agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
