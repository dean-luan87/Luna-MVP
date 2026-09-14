# Capability Registry / Manifest / Baseline Inventory

## Current ownership

| Responsibility | Current owner | Evidence |
|---|---|---|
| Logical capability identity/schema/contract | Capability Registry / Capability Governance | `capability_registry_v1.json`, governance architecture |
| Capability lifecycle and admission coordination | Capability Governance / Capability Admission | `capability_governance_model_v1.json`, admission contract |
| Slot binding and logical readiness projection | Universal Capability Slot Governance | `universal_capability_slot_types_v1.py` |
| Model and provider options | Model Manager / Provider Governance | registries and model contract repository |
| Quality baseline/calibration evidence | Capability Calibration | governance model and calibration assets |
| Resource/permission constraints | Capability Governance plus existing Resource/Permission governance | requirement and resolution contracts |
| Executable invocation | Capability Runtime / Observation-FPO boundary | Explicitly not implemented as a general runtime in the inspected contracts |

## Logical versus executable result

`CapabilityResolutionCandidateV1` is primarily a logical/module/slot
resolution result. It preserves model/provider refs and can say
`READY_CANDIDATE`, but its checks are registry, lifecycle, binding, permission,
resource, implementation and compatibility checks. It does not, by itself,
prove the current physical model file, dependency health, checksum integrity,
device readiness, or Provider admission.

`CapabilityInvocationCandidateV1` is explicitly a handoff candidate and does
not execute a Provider, model, camera, or Runtime. The current bridge can build
it after logical `READY_CANDIDATE`, so its name must not be interpreted as proof
of executable admission.

## Finding

The registry architecture already distinguishes capability from model and
Provider in principle. The implementation contract needs an explicit
intermediate Runtime Admission assessment before an executable capability
candidate is exposed.

