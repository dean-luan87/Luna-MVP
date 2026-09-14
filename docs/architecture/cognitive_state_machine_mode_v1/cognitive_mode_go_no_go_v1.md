# Cognitive State Machine and Mode Go/No-Go v1

## Required checks

- Runtime states include Idle, Observe, Engage, Analyze, Escalated, Recover,
  and Maintain.
- Cognitive modes include Survival Mode, Normal Mode, Focus Mode, Recovery
  Mode, and Maintenance Mode.
- Mode Transition Contract emits candidates from Reality change, Risk, Resource,
  Field, and Experience context.
- Mode affects Attention Budget Candidate but Attention does not select Mode.
- Runtime does not replace Brain; Brain retains Goal and Decision authority.
- Neural Fast Path is Stimulus → Neural Response Candidate → Runtime State
  Candidate → Attention Reallocation Candidate → Brain Escalation if needed.
- Experience changes mode priors only through current Reality/Self/Resource
  validation.
- Stability uses thresholds, hysteresis, cooldown, timeout, and recovery
  candidates to prevent oscillation.

## Explicit prohibitions

This architecture-only phase has No real model, No OCR, No SLAM, No Hardware
Runtime, No Action, No Emotion, No Role, No Social Runtime, No B Runtime, and
no automatic mode change. The agent performs V0 static checks only, does not
run the Final Phase Verifier, and stops at
`WAITING_FOR_USER_TERMINAL_VERIFICATION`.
Recovery Mode is a required mode. Runtime State Candidate is a required
candidate. No Hardware Runtime is enabled.
