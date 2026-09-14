# Observation Cycle Governance Go/No-Go v1

## Required readiness checks

- Observation lifecycle includes Created, Qualified, Allocated, Executing
  Candidate, Evidence Received, Evaluated, Completed, and Suspended.
- Observation Requirement is not Observation Execution.
- Priority considers Survival Impact, Goal Alignment, Reality Uncertainty,
  Temporal Urgency, Information Value, and Resource Cost.
- Persistence distinguishes Transient Observation, Persistent Observation, and
  Background Observation, each with a release condition.
- Evidence feedback follows Observation → Evidence → Reality Update Candidate
  → Field Reassessment.
- Observation does not directly change the Field; Reducer remains the sole
  State mutation authority.
- Failure follows Capability Failure → Evidence Quality Decline → Observation
  Retry Candidate → Alternative Capability Candidate. Observation Retry Candidate
  remains a candidate and is never an automatic retry.

Reducer remains the sole State mutation authority.

## Explicit prohibitions

This architecture-only phase has No real model call, No Camera Runtime, No OCR
Runtime, No SLAM Runtime, No Hardware Runtime, No Action Runtime, No Emotion
Engine, No Role System, No B Route, no Scheduler implementation, no automatic
retry, no automatic model switching, no online learning, and no direct Field
mutation.

No OCR Runtime, No Emotion Engine, and no automatic retry are enabled.

The agent performs V0 static checks only, does not run the Final Phase Verifier,
and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. The user must execute
the phase verifier and return all required sections.
