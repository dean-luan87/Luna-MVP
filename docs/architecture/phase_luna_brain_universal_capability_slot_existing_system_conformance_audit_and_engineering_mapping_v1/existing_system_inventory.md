# Existing System Inventory

## Canonical reusable assets

| Concern | Existing asset | Finding |
|---|---|---|
| Capability ownership | `luna_capability_governance_architecture_v1/capability_owner_definition_v1.json` | Capability Registry owns identity, schema, contract, dependencies, and lifecycle. |
| Registry boundary | `capability_registry_boundary_v1.json` | Registry answers what capabilities exist and is not a scheduler or Model Manager. |
| Admission | `capability_admission_hierarchy_v1.json` | Capability Admission is primary; model, provider, and runtime qualification are subordinate gates. |
| Lifecycle | `capability_lifecycle_contract_v1.json` | Candidate/Registered/Testing/Active/Degraded/Suspended/Retired exists; no generic Slot lifecycle. |
| Health | `capability_health_model_v1.json` | Health and degradation are candidate-only and distinct from identity. |
| Model | `model_manager_boundary_v1.json` | Model identity, versions, resources, and compatibility remain Model Manager concerns. |
| Provider | `provider_boundary_v1.json` | Provider isolation and evidence gateway boundary are already explicit. |
| Self | `cognitive_self_capability_awareness_v1/` | Current capability state, limitations, provenance, and Self boundaries exist. |
| Self history | `cognitive_self_capability_profile_v1/capability_memory_interface_v1.json` | Memory/experience references exist, but not Slot binding history. |
| Safety | `luna_system_constitution_governance_v1/` | Safety, unknown preservation, authorization, and constitutional hierarchy exist. |
| Resources | `runtime_resource_governance_contract_v1.json` | Compute, energy, memory, time, and sensor availability are governed inputs. |
| Maintenance | `system_maintenance_manager/module/` | Diagnostics, model asset issues, dependency issues, remediation, and rollback-related candidates exist. |
| Brain requests | `brain_capability_request_contract_v1.json` | Brain requests capability purpose and constraints, not named models or providers. |
| Self regulation | `self_regulation_capability_interface_v1.json` | Self may propose health/recovery/degradation adjustments but cannot switch models or bypass admission. |
| Baseline | `brain_golden_baseline/` | Golden Baseline remains the cross-phase governance boundary. |

## Overlaps and gaps

- The existing Registry `capability_id` is the closest Module identity, but
  it does not represent a persistent Slot.
- Existing lifecycle contracts describe capability state, not separate Slot
  binding state and Module lifecycle state.
- Existing health and maintenance contracts support degradation evidence, but
  no generic Slot recovery/history record was found.
- Existing Self contracts support current and historical awareness by
  reference, but do not define a Slot-to-Module history projection.
- Existing resource, permission, integrity, and compatibility evidence can be
  reused by future Slot admission.

## Parallel-owner risks

The main risk is treating the visual integration package as a generic Registry
or treating `SafetyCapabilitySlotV1` as a constitutional Slot type. Both must
remain narrow reference structures until a future conformance implementation
is approved.
