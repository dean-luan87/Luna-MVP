# Capability Runtime Contract Whitebox v1

## Request-to-evidence trace

```text
Observation Requirement
        ↓
Capability Request
        ↓
Capability Admission
        ↓
Resource / Permission / State Review
        ↓
Provider Invocation Candidate
        ↓
Raw Evidence Candidate
        ↓
Evidence Gateway
        ↓
Reality Update Candidate
        ↓
Reducer
```

## Boundary assertions

- Request is Capability-level, not Model-level.
- Attention creates priority candidates; it does not execute a Model.
- Provider sees least-privilege scoped input, not Goal, Brain Intent, full
  Field, Identity, Value, or Decision.
- Provider output is Evidence Candidate, not Reality, Situation, Goal,
  Decision, or Action.
- Admission, resource allocation, and invocation are candidates only.
- Failure returns Diagnostics, Self Capability, Attention, or Alternative
  Capability candidates.
- Evidence Gateway and Reducer remain mandatory.

No real model call, No OCR, No SLAM, No Camera, No Hardware, No Provider
Runtime, No Action Runtime, No automatic execution, No automatic learning, No
Provider-to-Brain, No Provider-to-Decision, and No B are included.

Alternative Capability is a candidate. No Provider Runtime and No
Provider-to-Brain are included.

No Provider-to-Brain is included.
