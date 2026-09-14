# Attention Adaptation and Stability Go/No-Go v1

## Required checks

- Attention Baseline records Field Pattern, Expected Attention Requirement, and
  Normal Observation Cost.
- Experience produces an Attention Pattern Candidate, then Validation, then a
  Future Allocation Candidate.
- A single event cannot change a long-term strategy.
- Familiarity distinguishes Unknown high/new Field from stable confidence and
  permits a cost reduction candidate only within a validated scope.
- New Evidence triggers Deviation Detection and an Attention Increase Candidate.
- Attention Drift Candidate covers attraction, persistence, narrowing, omission,
  overgeneralization, and resource drift.
- Experience does not directly control Attention.
- Capability Change produces an Attention Requirement Adjustment Candidate only.

## Explicit prohibitions

This architecture-only phase has No online learning, No automatic strategy
modification, No automatic policy update, No Brain modification, No Goal
modification, No Decision, No Action, No Emotion Runtime, No Role Runtime, No B
Route, and No Runtime.

The agent performs V0 static checks only, does not run the Final Phase Verifier,
and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. The user must execute
the phase verifier and return all required sections.

No automatic strategy modification and No Goal modification are enabled. No B
Route is enabled.

No B Route is enabled in this phase.
