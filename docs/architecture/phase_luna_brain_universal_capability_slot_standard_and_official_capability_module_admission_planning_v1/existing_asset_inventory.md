# Existing asset inventory

## Reused canonical assets

- Capability identity/registry/lifecycle: `docs/architecture/luna_capability_governance_architecture_v1/`
- Model/provider resource admission: `capabilities/midplatform/model_manager/` and `docs/architecture/cognitive_model_manager_runtime_boundary_v1/`
- Provider boundary: existing Provider Governance and runtime-admission contracts
- Capability health/calibration: existing Capability Calibration and health contracts
- System diagnostics/maintenance: `capabilities/midplatform/system_maintenance_manager/`
- Capability Self: `docs/architecture/cognitive_self_capability_awareness_v1/` and `docs/architecture/cognitive_self_capability_profile_v1/`
- Self model boundary: `docs/architecture/luna_cognitive_self_model_architecture_v1/`
- Safety/constitutional authority: `docs/architecture/luna_system_constitution_governance_v1/`
- Resource governance: existing runtime resource and cognitive resource governance assets
- Brain capability requests: `brain_capability_request_contract_v1.json`
- Current visual reference: `capabilities/vision/registry/visual_capability_system_controlled/`
- Brain Golden Baseline: `capabilities/midplatform/core/brain_golden_baseline/`

## Findings

Capability Registry is the canonical capability owner. Existing registry
contracts define capability identity, schema, dependencies, lifecycle and
manifest interfaces, but no generic persistent Slot standard was found.
Existing visual manifests are capability-level records and must not become
the Universal Slot constitution.

Capability Self requires a narrow contract alignment under the existing
Cognitive Self Model / Capability Awareness owner. Brain Capability
Regulation requires a narrow candidate-governance boundary; it must not become
a second lifecycle writer.

No existing asset justifies an OCR, face, Safety, Audio, Official, or Market
slot type. No engineering mapping is performed here.
