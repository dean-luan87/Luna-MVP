# Upstream Asset Inventory v1

| Record | Reusable asset | Owner | Candidate-only | Reachable from target real caller |
|---|---|---|---|---|
| Capability Resolution | `universal_capability_slot_resolution_v1.py:resolve_scoped_capability_requirement` | Capability Governance | Yes | Dynamic real trial; not A-Route injection |
| Capability↔Model binding | `capability_model_provider_binding_controlled/types_v1.py:CapabilityModelBindingCandidateV1` | Capability Governance | Yes | Controlled fixtures only; no real producer |
| Runtime assessment | `logical_capability_runtime_admission_types_v1.py:RuntimeAdmissionAssessmentCandidateV1` | Runtime Admission | Yes | Dynamic real trial compatibility adapter |
| Executable Capability | `logical_capability_runtime_admission_types_v1.py:ExecutableCapabilityCandidateV1` | Runtime Admission | Yes | Dynamic real trial compatibility adapter |
| Model↔Provider binding | `capability_model_provider_binding_controlled/types_v1.py:ModelProviderBindingCandidateV1` | Provider Governance | Yes | Controlled fixtures only; no real producer |

The existing binding builders are explicitly synthetic-only input validators.
They cannot be promoted into a real producer by this phase. The missing
handoff is a governed, non-fixture producer for the two binding records.

