# Capability Governance Controlled Integration Plan v1

## Scope

This phase validates one controlled capability path without executing a real provider:

```text
Brain / A Route Cognitive Requirement
        ↓
Capability Requirement
        ↓
Capability Registry
        ↓
Capability Admission
        ↓
Provider Candidate
        ↓
Provider Execution Boundary
        ↓
Evidence Gateway
        ↓
Reality Cognition
        ↓
Brain Evaluation
```

Capability is a governed tool. Capability ≠ Understanding, Capability ≠ Decision,
Capability ≠ Reality, and Capability ≠ Brain. The controlled skeleton is
`text_evidence_extraction`; it may return text evidence, but it cannot claim
`world_understanding`.

## Controlled manifest and admission

The manifest declares identity, input/output contracts, resource requirements,
limitations, confidence boundary, and failure namespace. Admission validates the
manifest and produces a Provider Candidate. Admission is not execution and does
not make a Reality or Decision claim.

## Provider Replacement and evidence invariants

Provider Output → Evidence Candidate → Evidence Validation → Reality Cognition.
The Evidence Gateway preserves provenance, capability reference, timestamp,
confidence, uncertainty, and validation status. Replacing Provider A with Provider
B leaves A Route structure unchanged; only Evidence Quality Candidate may differ.
This Provider Replacement changes only the evidence-quality candidate, never the
cognitive contract or authority boundary.

## Failure and self-capability feedback

Provider unavailable yields a Capability unavailable candidate. Low-quality output
lowers evidence confidence and cannot directly form Reality. A protocol error is
localized in Diagnostics. Capability State Changed may produce a Self Capability
Context Candidate and Brain Awareness; it does not directly mutate Self, Goal, or
State.

## Frozen prohibitions

This is planning and static fixture validation only. No real model call is
performed. There is no real OCR, Provider execution, Runtime, Hardware access,
automatic learning, or state mutation.
