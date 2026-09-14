# Current Capability Execution Chain

## Static chain

```text
A Current Need
  → CognitiveNeedCandidateV1
  → CapabilityRequirementV1
  → CapabilityScopeAssessmentV1
  → CapabilityResolutionCandidateV1
  → CapabilityInvocationCandidateV1 / Observation handoff
  → Provider admission candidate
  → Provider adapter
  → PerceptionEvidence / Observation candidate
  → A evidence reassessment
```

## Transition inventory

| Transition | Current source owner | Current target owner | Current contract | Runtime/admission state |
|---|---|---|---|---|
| Need → cognitive requirement | A / Brain-governed semantic boundary | Capability Governance input | `cognitive_need_capability_requirement_bridge_governance_v1.py` | Candidate-only; no model/provider selection |
| Requirement → scope | Capability Requirement Bridge | Capability Scope / Universal Slot Governance | `universal_capability_slot_resolution_v1.py` | Candidate scope assessment; no execution |
| Scope → logical resolution | Capability Registry / Universal Slot Governance | Capability Resolution | `CapabilityResolutionCandidateV1` | Resolves module, slot, implementation, model and provider refs; returns `READY_CANDIDATE`, `UNAVAILABLE_CANDIDATE`, or `DEGRADED_CANDIDATE` |
| Resolution → invocation handoff | Capability Admission / Universal Slot Governance | Observation Gateway / FPO boundary | `build_scoped_invocation_candidate()` | Handoff candidate only; no Provider/model execution. `READY_CANDIDATE` is not a complete physical/runtime admission |
| Model asset → technical admission | Model Manager / Model Governance | Capability Admission coordination | `yolo11n_external_provisioning_types_v1.py`, `yolo11n_readiness_types_v1.py`, `real_model_asset_admission_types_v1.py` | Candidate admission; consumes physical, checksum, dependency and contract evidence |
| Observation → Provider admission | Observation/FPO boundary | Provider Governance / FPO | `field_perception_real_vision_provider_adapter_v1.py` | Explicit provider admission candidate required; Provider cannot self-admit |
| Provider → evidence | Provider adapter | Observation Gateway / FPO, then A | `VisionProviderAdapterResultV1`, observation gateway types | Real path exists in the controlled trial; evidence remains candidate and not world truth |

## Exact readiness decision locations

- Logical module/slot/lifecycle/permission/resource readiness: `universal_capability_slot_resolution_v1.py`.
- Model contract and dependency compatibility: `model_contract_repository_resolver_v1.py`.
- Physical asset/path, declared-vs-observed checksum, and technical model
  admission: `yolo11n_external_provisioning_types_v1.py` and
  `yolo11n_readiness_types_v1.py`.
- Model registry/lifecycle admission: `model_manager_admission_v1.py`.
- Runtime health evidence: `runtime_health_checker_v1.py`.
- Provider invocation authorization: `build_vision_provider_admission_candidate_v1()`.
- The real single-invocation trial currently assembles these inputs and
  decisions; it is not yet a canonical unified Runtime Admission contract.

## Current gap

The chain has all relevant evidence producers, but no single explicit
contractual seam that says: logical capability resolution is complete, Runtime
Admission has accepted the executable asset/runtime/provider candidate, and
only then may a Provider invocation candidate be issued.

