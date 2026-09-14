# A3 Cognitive Analysis Runtime Capability Registration Plan v1

## Scope

This phase prepares a **registration candidate** for A3 Cognitive Analysis Runtime. It is not a Registry write, Capability activation, permission grant, Runtime execution, or authorization decision. `runtime_authorized=false` remains fixed.

## Existing Governance Ownership

- **Capability Registry:** `capabilities/midplatform/model_manager/registries/capability_registry_v1.json`
- **Lifecycle reference:** `capabilities/midplatform/model_manager/lifecycle/model_registry_state_machine_v1.py`
- **Protocol Manager Registry interface:** `capabilities/midplatform/protocol_manager/module/protocol_manager_registry_adapter_v1.py`
- **Admission reference:** `LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1` and existing Permission / Admission governance

The Registry and Protocol Manager retain governance ownership. A3 owns only its declaration candidate and must not create a separate Registry, Manifest, lifecycle, or authorization model.

## Candidate Declaration

| field | candidate value | handling |
| --- | --- | --- |
| `capability_id` | `cognitive_analysis_runtime` | stable identity; absent from the current Registry at planning time |
| `capability_owner` | `L1 Protocol Governance / Cognitive Flow` | ownership declaration, not a new owner system |
| `lifecycle_state` | `candidate` | existing lifecycle vocabulary; not routing- or execution-eligible |
| `required_contracts` | Model/Skill Admission, Permission/Admission, Runtime Boundary, Input/Output Candidate, Symmetry, Traceability | references only |
| `protocol_dependencies` | Protocol Manager registry/admission route and Permission & Admission Manager | no invocation or registration |
| `diagnostics_binding` | Protocol Manager Diagnostics and Permission/Admission Diagnostics | future reporting route only |

## Controlled Registration Boundary

The candidate maps the existing Registry entry fields and is statically validated against the Registry reference. It does not open a Registry write path, declare a provider, trigger admission, grant permission, or activate Runtime. Any actual record must be created only through the existing L1 governance process after human review.
