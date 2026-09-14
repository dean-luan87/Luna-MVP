# Asset inventory

## Reused

| Asset | Location | Use |
|---|---|---|
| `CapabilityResolutionCandidateV1` | `model_manager/registries/universal_capability_slot/` | logical resolution reference |
| `CapabilityModelBindingCandidateV1` | `capability_model_provider_binding_controlled/types_v1.py` | Capability-owned binding reference |
| `ModelProviderBindingCandidateV1` | same binding package | Provider-owned binding reference |
| `RuntimeAdmissionAssessmentCandidateV1` | `logical_capability_to_runtime_admission_candidate_adapter_controlled/` | assessment output |
| `ExecutableCapabilityCandidateV1` | same Runtime Admission package | gated candidate output |
| model/provider/capability registries | existing declaration baseline | repository-backed source |

## Controlled or insufficient

- The old logical Runtime Admission adapter remains a controlled compatibility
  implementation and defaults to synthetic-only inputs.
- The new source reuses its assessment semantics but explicitly converts the
  repository-backed validation result to `synthetic_only=False`.
- No existing path was found that issued a non-fixture owner-composed Runtime
  Admission record before this phase.

## Ownership result

Runtime Admission owns executable eligibility assessment and candidate
lifecycle. It does not own any source declaration or Provider lifecycle.
