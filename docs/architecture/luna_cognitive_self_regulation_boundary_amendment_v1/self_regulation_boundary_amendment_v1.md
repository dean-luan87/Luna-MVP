# Self Regulation Boundary Amendment v1

## Purpose

This amendment extends the existing Self Regulation architecture with two stability principles without creating a new system:

1. Capability Failure Isolation: a capability failure is contained within its declared failure domain and does not collapse unrelated capabilities or the whole cognitive subject.
2. Self Preservation Governance: continuous stability and core cognitive function outrank capability improvement and performance optimization.

```text
Failure Event
    -> Capability Impact Analysis
    -> Dependency Evaluation
    -> Affected Capability Update
    -> Self State Update
    -> Degraded Operation / Recovery Candidate
```

```text
Stability > Core Cognitive Function > User Task > Capability Improvement > Optimization
```

## Scope

In scope:

- declaring capability failure domains and affected/unaffected capabilities;
- analyzing blast radius before degradation or recovery candidates;
- preserving unaffected capabilities and operational state;
- rejecting upgrades whose stability cost exceeds present fitness;
- comparing capability value, resource cost, risk, stability, and task requirement;
- amending Self Regulation permissions and dependency mappings.

Out of scope:

- Runtime implementation, automatic upgrade, automatic rollback, model switching, hardware control, learning execution, or emotion integration;
- modification of Capability Runtime, Model Manager, Provider, Constitution, Value, Identity, Goal, or Brain rules.

## Authority correction

Self Regulation observes, analyzes impact, proposes degradation/recovery/upgrade rejection, and requests Capability Governance. Capability Governance still owns admission. Model Manager supplies registered options. Calibration supplies evidence. Self Regulation cannot directly invoke or switch providers.

## Isolation invariant

```text
Camera failure -> Vision/OCR degradation candidate
Camera failure -/-> Speech, Memory, Conversation, or Identity failure
```

The system remains operational when at least one safe cognitive path remains. Unknown, reduced confidence, and affected-domain provenance must be explicit.
