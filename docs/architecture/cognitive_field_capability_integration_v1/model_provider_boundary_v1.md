# Model Provider Boundary v1

## Model Manager role

The Model Manager manages Provider identity, version, supported capability,
input/output boundaries, known limitations, resource profile, and admission
status. It does not understand the world, create a Field, or make a Decision.

```text
Capability Registry
    ↓
Model Manager
    ↓
Provider Candidate
    ↓
Provider Execution Boundary
    ↓
Evidence Gateway
```

## Provider limits

A Provider supplies a local Evidence candidate. Provider output is not a Fact,
not Reality, not Situation, and not a Decision. The Provider cannot bypass the
Evidence Gateway, bypass the Reducer, modify the Reality Workspace, create a
Cognitive Field, trigger Action, or change the original Intent. The Provider
cannot bypass the Evidence Gateway under any execution path.

Provider Replacement is required to be interface-compatible. Provider A and
Provider B can be compared through Evidence provenance, confidence, quality,
cost, latency candidate, and failure trace. Replacement must not alter A Route
rules or Brain authority.

## Current execution boundary

This phase defines no real model execution and no real Provider execution.
Model Manager and Provider are contract-level candidates only. No real OCR,
no real SLAM, No Hardware Runtime, and No Action Runtime are enabled.
