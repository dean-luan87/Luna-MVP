# Logical vs Executable Capability Boundary

## Current state

The current Universal Slot resolution path can return a logical
`READY_CANDIDATE` and can build a `CapabilityInvocationCandidateV1`. The
invocation candidate is explicitly non-executing, but its construction is not
gated by a unified physical/runtime admission result. The Real Capability
trial performs the missing technical checks separately.

## Required conceptual split

```text
Capability Requirement
  → Scope Assessment
  → Logical Capability Resolution
  → Runtime Admission Assessment
       - governed model asset/path
       - model contract and dependency evidence
       - declared/observed integrity
       - resource/device/runtime health
       - Provider qualification/admission
  → Executable Capability Candidate
  → Observation / Provider Invocation
  → Evidence
```

This is a contract boundary, not a request to create a Runtime Admission
Manager. Existing Capability Admission, Model Manager, Provider Governance,
Runtime Health and Observation/FPO assets should compose the assessment.

## Authority rules

- A asks for the information/capability category; it does not choose a model,
  path, Provider, dependency status, device, or checksum.
- Brain governs global safety, permission, resources and capability request
  policy; it does not inspect files or calculate checksums.
- Model Manager owns model identity and model metadata/evidence.
- Capability Admission decides whether the complete candidate may become
  executable.
- Observation/FPO owns the evidence acquisition boundary.
- Loop records requirement, resolution, admission, execution and evidence
  refs mechanically.

