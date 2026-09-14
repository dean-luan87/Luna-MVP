# Cognitive Field Capability Integration Model v1

This phase does not perform real model execution or real OCR. It also does not
perform real SLAM, Hardware Runtime, or Action Runtime.

## Phase boundary

This phase defines the governance bridge from a Cognitive Field's
`Observation Requirement` to an admitted capability and back to the
Reality Workspace. It is an architecture contract, not a model or hardware
implementation.

The governed chain is:

```text
Cognitive Field
    ↓
Observation Requirement
    ↓
Capability Registry
    ↓
Capability Admission
    ↓
Model Manager / Provider Candidate
    ↓
Provider Execution Boundary
    ↓
Evidence Gateway
    ↓
Evidence Candidate
    ↓
Reality Workspace
    ↓
Field Update
```

An Observation Requirement states what information is needed, why it is
needed, the acceptable uncertainty, and the resource boundary. It does not
name a model, open a sensor, create a Field, or issue an Action.

## Governance invariants

1. `Capability ≠ Understanding`, `Provider ≠ Reality`, and model output is
   never a direct Reality State mutation.
2. The Capability Registry describes admissible capability contracts. The
   Model Manager selects a Provider candidate without changing A Route logic.
3. The Evidence Gateway validates schema, provenance, timestamp, confidence,
   uncertainty, capability reference, and request/intent trace before evidence
   enters the Reality Workspace.
4. Human Feedback and model/provider output use the same Evidence Gateway; a
   model is not the only evidence source.
5. Provider replacement may change Evidence Quality Candidate only. It cannot
   change Field authority, Situation logic, Decision authority, Self identity,
   or Goal.
6. A capability cannot create a Cognitive Field, modify Reality, modify the
   Goal, or trigger Action. Failures become Capability Failure diagnostics.

## Failure return path

```text
Provider unavailable / low quality / protocol error
    ↓
Capability Failure
    ↓
Diagnostics
    ↓
Self Capability Candidate
    ↓
Field / A Route awareness
```

This is a candidate feedback path. It is not automatic learning and it does
not directly mutate the Self Model or Reality State.

## Current scope

The phase permits contracts, registry/admission schemas, fixture examples,
and static validation only. It does not perform real model execution, real
OCR, real SLAM, Hardware Runtime, Action Runtime, or B Simulation Runtime.
