# Attention Experience Adaptation and Stability Go/No-Go v1

## Required checks

- Experience Candidate flows through Pattern Extraction and Validation before
  producing an Attention Prior Candidate.
- Field Attention Memory contains Field Context, Condition, Observed Pattern,
  Attention Requirement, and Outcome Feedback.
- Current Field, Historical Pattern, Self Capability, and Current Goal produce
  an Attention Prior Candidate, not a Decision.
- Familiarity states are Unknown Field, Learning Field, Stable Field, and
  Changed Field.
- Stable Pattern plus Reality Deviation produces an Attention Reactivation
  Candidate and Increase Observation Candidate.
- Attention Drift Candidate detects attraction, persistence, narrowing, omission,
  overgeneralization, and resource drift.
- Pattern Strength uses Experience Frequency, Validation Confidence, and Time
  Decay.
- Capability Change produces Attention Requirement Candidate and Observation
  Strategy Candidate only.
- Simulation Field → Historical Attention Pattern → Simulation Observation is a
  placeholder and B Route is not implemented. Attention Reactivation Candidate and Time Decay are mandatory terms. Observation Strategy Candidate is a candidate only.

## Explicit prohibitions

This architecture-only phase has No automatic learning, No automatic strategy
change, No Brain modification, No Goal modification, No Decision, No Action,
No Emotion Runtime, No Role Runtime, No Social Runtime, No B Runtime, No Model
Training, No Simulation Runtime, and No Runtime.

The agent performs V0 static checks only, does not run the Final Phase Verifier,
and stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. The user must execute
the phase verifier and return all required sections. No automatic strategy change is enabled. No B Route is enabled.

No Model Training is enabled.
