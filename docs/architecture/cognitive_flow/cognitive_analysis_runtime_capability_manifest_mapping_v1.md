# A3 Cognitive Analysis Runtime Capability Manifest Mapping v1

## Actual Asset Finding

The direct L1 governance scope contains `LunaCapabilityRegistryV1` at `capabilities/midplatform/model_manager/registries/capability_registry_v1.json`. No standalone Capability Manifest Schema was located there. This phase therefore maps a **candidate** to the existing Registry entry format; it does not introduce a parallel A3 manifest.

## Mapping

| A3 registration declaration | Existing Registry / governance target | mapping status |
| --- | --- | --- |
| `capability_id` | Registry entry `capability_id` | direct mapping: `cognitive_analysis_runtime` |
| `capability_label` | Registry entry `capability_label` | direct candidate mapping |
| `need_triggers` | Registry entry `need_triggers` | candidate declaration only; no routing trigger is enabled |
| `providers` | Registry entry `providers` | empty in this candidate; A3 Runtime is not a Model provider declaration |
| `capability_type` | no explicit field in current Registry entry | retained as admission metadata; no schema patch proposed |
| `capability_owner` | no explicit field in current Registry entry | retained as L1 ownership metadata; no new ownership system |
| `lifecycle_state` | existing lifecycle vocabulary in Model Registry State Machine | `candidate` only; no transition or activation |
| `required_contracts` | Model/Skill Admission and existing L1 Protocol references | admission record metadata, not a Registry schema extension |
| `protocol_dependencies` | Protocol Manager Registry/Admission interfaces | reference only |
| `diagnostics_binding` | Protocol Manager and Permission/Admission Diagnostics | reference only |

## Compatibility Decision

The mapping is compatible for a registration **candidate** because the required Registry entry keys are declared and no Registry content is changed. The missing standalone Manifest Schema and absent owner/type/lifecycle fields in current Registry entries remain governance notes for a future L1-owned admission process; they are not reasons to create a second schema.
