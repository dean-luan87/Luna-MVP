# Capability Governance Adjudication Summary v1

## Overall conclusion

Capability Governance is the independent logical functional-abstraction owner.
It preserves portability across models/providers and separates logical support
from runtime readiness.

## Target owner map

```text
A / Task functional requirement
        ↓
Capability Requirement
        ↓
Capability Scope
        ↓
Logical Capability Resolution / Slot
        ↓
Runtime Admission Assessment
        ↓
Executable Capability Candidate
        ↓
Provider Admission
        ↓
Provider / Observation execution
        ↓
Evidence or execution result
        ↓
A / Task / downstream owner
```

Inputs from Brain constraints, Attention, Role/Perspective relevance, Model
Manager mappings and System Diagnostics remain refs/evidence at their original
owners.

## Disposition

Capability Governance: **NARROW**.

Capability Registry, Slot, Scope and Logical Resolution: retain under
Capability Governance. Model Mapping: split shared contract. Runtime Admission
coordination: existing Capability Admission Governance function. Executable
Candidate: Runtime Admission boundary. Provider Admission/Invocation: Provider
Governance.

## Current status

Documentation-only review complete. No runtime, tests, providers, models,
checksum calculation or diagnostics probes were executed.
