# Capability State Model v1

## State vocabulary

```text
Capability State
├── Available
├── Degraded
├── Limited
├── Unavailable
└── Unknown
```

Available means the admitted capability currently meets its declared
boundary. Degraded means quality or reliability is reduced. Limited means a
known subset of the contract remains usable. Unavailable means no admissible
provider path is currently available. Unknown means state evidence is
insufficient.

## State evidence

State Evaluation may use Provider diagnostics, Hardware diagnostics, resource
availability, protocol health, evidence quality, and repeated failure
feedback. These are Capability State Update Candidates, not direct mutations.
Resource availability is a state input.

```text
Capability Failure
      ↓
Diagnostics
      ↓
Capability State Update Candidate
      ↓
Reducer validation
      ↓
Self Capability Awareness
```

Provider Replacement may change evidence quality or confidence, but it must
not change Capability Identity, Self Identity, Goal, Decision, or Reality.

## Boundaries

Capability State is not Reality State and is not a Decision. It does not infer
that the world is unsafe merely because a sensor is Degraded. It reports a
limitation so A Route and Brain can calibrate confidence. The Reducer remains
the sole State mutation authority. Reducer remains the sole State mutation
authority. No automatic state mutation, online learning, model training,
hardware control, or action execution is allowed. No online learning. resource availability remains a governed input. Reducer remains the sole State mutation authority.
