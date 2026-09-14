# Self Capability Awareness Go / No-Go v1

## Required readiness checks

- Capability Identity is distinct from Provider Identity.
- Capability State includes Available, Degraded, Limited, Unavailable, and
  Unknown.
- Capability Confidence is calibrated evidence-production confidence and is
  not Fact or Reality. Capability Confidence is not Reality.
- Self Capability State includes identity, capability, resource, health,
  limitation, confidence, unknowns, and provenance.
- Capability Failure flows through Diagnostics to a Capability State Update
  Candidate and Self Capability Awareness. Capability State Update Candidate
  is required.
- Capability degradation can produce an Observation Cost increase and an
  Attention Reallocation Candidate. Attention Reallocation Candidate is
  required.
- Brain receives capability boundaries and confidence candidates; Brain retains
  Goal and Decision authority.
- Provider Replacement cannot change the cognitive subject.
- Reducer remains the sole State mutation authority.

## Explicit prohibitions

This architecture-only phase has No real model, No OCR, No SLAM, No Camera,
No Hardware Runtime, No Action, No Emotion, No Role, No Social Runtime, and
No B Runtime. There is No online learning, No automatic Self Model rewrite,
No direct Reality mutation, and No automatic frequency adjustment.

The agent performs V0 static checks only, does not run the Final Phase
Verifier, and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`.
