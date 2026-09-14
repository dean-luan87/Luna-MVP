# Existing asset inventory

## Reused canonical assets

- Model ownership/admission: `capabilities/midplatform/model_manager/`
- Model contracts: `capabilities/midplatform/model_manager/model_contract_repository/`
- Capability registry: `capabilities/midplatform/model_manager/registries/capability_registry_v1.json`
- Stage-0 Vision registry: `capabilities/vision/registry/vision_registry.py`
- Provider interfaces: `capabilities/vision/interfaces/providers.py`
- Vision Manager: `capabilities/midplatform/vision_manager/module/`
- Observation Gateway: `capabilities/midplatform/core/observation_gateway/`
- Observation Manager: `capabilities/midplatform/observation_manager/module/`
- Active Observation Control/FPO: `capabilities/midplatform/field_perception_orchestrator/integration/`
- Brain Golden Baseline: `capabilities/midplatform/core/brain_golden_baseline/`
- System maintenance diagnostics: `capabilities/midplatform/system_maintenance_manager/module/`
- OCR Manager: `capabilities/midplatform/ocr_manager/module/`

## Existing capability/evidence families

Existing controlled or planning assets cover YOLO detection, OCR, tracking,
segmentation, SLAM/spatial evidence, evidence envelopes, observation
sufficiency, safety gates, rollback candidates, and learning candidates.

These are reusable capability/provider/evidence surfaces, not permission to
activate every capability.

The existing FPO assets provide Evidence Sufficiency and observation-control
semantics. No existing canonical SNSP or SRSK implementation was found;
therefore this alignment adds boundary documents only. It does not add a
knowledge-pack owner or cross-modal semantic runtime.

## Inventory gaps

No complete canonical Safety Vision Core slot constitution or dynamic Visual
Capability Warehouse registration protocol was found. This phase defines
those as governance contracts under existing Capability Governance and Model
Manager ownership; it does not create a new runtime owner.
