# Existing asset inventory

| Asset | Canonical owner | Finding |
|---|---|---|
| `capabilities/midplatform/model_manager/registries/capability_registry_v1.json` | Capability Registry / Governance | Closest existing Capability Module identity source; its `capability_id` is not a Slot. |
| `capabilities/midplatform/model_manager/registries/model_registry_v1.json` | Model Manager | Model and dependency metadata; never upgraded to Module identity. |
| Universal Slot package | Capability Registry / Governance | Verified generic Slot, admission, binding, resolution, Self projection and invocation candidate foundation. |
| `capabilities/midplatform/ocr_manager/module/` | OCR Manager | Implementation and evidence/supporting assets for existing text capabilities. |
| `capabilities/midplatform/slam_spatial_mapping_adapter_core_v1.py` | Spatial mapping integration | Implementation/supporting adapter for `spatial_mapping`. |
| S3 YOLO11n integration | FPO / provider boundary | Provider/model evidence path; not a capability identity. |
| Visual capability controlled package | Capability Registry reference integration | Useful lifecycle/channel reference; its safety-specific Slot is not canonical. |
| Capability Self awareness docs | Cognitive Self / Capability Awareness | Read-only Self projection boundary; no CSA field existed before this additive extension. |
| Golden Baseline | Brain Golden Baseline Governance | Candidate/truth, provenance, and negative guard boundary remains unchanged. |

Existing registry IDs with sufficient capability semantics for this catalog are
`object_detection`, `text_recognition`, `precise_ocr`, `spatial_mapping`, and
`unknown_scene_reasoning`. Safety environment and visual sensor health are
carried from the verified Slot foundation as controlled official Module
references, with their source gap explicitly retained.
