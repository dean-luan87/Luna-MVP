# Luna Capability Execution Boundary Architecture v1

## Position

This boundary bridges L2 Cognitive Core and L4 Capability & Execution System.
L2 expresses what information or capability is needed; L4 selects an admitted
capability and returns evidence. The provider remains an implementation detail.

```text
L2 Cognitive Need
        ↓
Capability Request
        ↓
L1 Admission / Runtime Governance
        ↓
Capability Selection Boundary
        ↓
Execution Contract
        ↓
Provider Boundary (future)
        ↓
Evidence Return Gateway
        ↓
L2 Cognitive Update
```

## Core boundary rules

- A request names a capability need, never a model or provider.
- Admission checks registry, profile, permission, health, calibration, context,
  and resource budget before a candidate is available.
- Selection produces a Capability Candidate, not a Decision.
- Provider output is Evidence Candidate only; it cannot create Goal, modify
  Memory, control Brain, or write Reality.
- Failure produces Diagnostics, Degrade, Alternative, and Unknown candidates;
  it does not force a false fact.
- Capability Trace preserves request, selection, provider reference, evidence,
  validation, and cognitive update provenance.

No real model, hardware, camera, Provider, Runtime, or Action is connected in
this phase.

