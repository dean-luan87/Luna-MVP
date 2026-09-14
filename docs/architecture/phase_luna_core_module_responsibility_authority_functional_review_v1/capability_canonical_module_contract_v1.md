# Capability Governance Canonical Module Contract v1

## Adjudication

**Disposition: NARROW.** Capability Governance remains an independent logical
governance boundary. It owns capability identity, taxonomy, slots, scope and
logical resolution, and coordinates the existing Runtime Admission function
boundary. It does not own models, Providers, diagnostics, cognition or
execution.

## Canonical purpose

Capability Governance translates a Cognitive/Task functional requirement into
a governed capability scope and logical capability/slot resolution, preserves
portable model/provider mappings, and hands supplied runtime-readiness evidence
to Runtime Admission for an Executable Capability Candidate.

## Repository evidence

- `capabilities/registry/luna_capability_registry_v1.json` is a foundation
  registry of modules and explicitly does not create runtime loading services.
- Universal Slot assets define `CapabilityRequirementV1`,
  `CapabilityScopeAssessmentV1`, `CapabilityResolutionCandidateV1` and slot
  bindings under Capability Registry/Governance ownership.
- `CapabilityResolutionCandidateV1` is candidate-only and has
  `provider_invocation=False` and `model_inference=False`.
- The verified Runtime Admission adapter produces
  `RuntimeAdmissionAssessmentCandidateV1`, `ExecutableCapabilityCandidateV1`
  and `ProviderAdmissionInputCandidateV1` without probes or execution.
- The Real Capability trial now exposes the logical-resolution → Runtime
  Admission → executable-candidate seam before its existing Provider path.

## Authority

Capability Governance may authoritatively define and govern logical capability
contracts and candidate resolution. It may not choose a Provider or model for
execution, admit runtime health, load a model, invoke a Provider or create
evidence.

Responsibility follows the boundary: scope/resolution/mapping errors belong to
Capability Governance; asset/checksum/provisioning errors belong to Model
Manager/integrity governance; health evidence belongs to Diagnostics; runtime
admission belongs to Capability Admission Governance; execution belongs to
Provider Governance; Need belongs to A.

## Status

Conceptual ownership is strong. Remaining gaps are contract/adapter/runtime
consolidation, not evidence for a new Capability Manager.
