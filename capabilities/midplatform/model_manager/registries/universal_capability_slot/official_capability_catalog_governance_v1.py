"""Static Official Capability Catalog and CSA mapping governance."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from .official_capability_catalog_types_v1 import (
    ASSET_CLASS_VALUES,
    CapabilityAssetMappingV1,
    CapabilitySemanticAnnotationV1,
    OfficialCapabilityCatalogEntryV1,
    OfficialCapabilityCatalogV1,
    SlotCompatibilityMappingV1,
)

CATALOG_ID = "luna-official-capability-catalog"
CATALOG_VERSION = "v1"
SLOT_CONTRACT_REF = "UniversalCapabilitySlotV1"


def _csa(
    module_ref: str,
    purpose: str,
    problem_classes: Tuple[str, ...],
    situations: Tuple[str, ...],
    contribution: Tuple[str, ...],
    boundaries: Tuple[str, ...],
    non_capabilities: Tuple[str, ...],
    requirement_hints: Tuple[str, ...],
) -> CapabilitySemanticAnnotationV1:
    return CapabilitySemanticAnnotationV1(
        capability_semantic_annotation_id=f"csa:{module_ref}:v1",
        module_ref=module_ref,
        semantic_purpose=purpose,
        applicable_problem_classes=problem_classes,
        applicable_situation_descriptions=situations,
        expected_contribution=contribution,
        capability_boundaries=boundaries,
        known_non_capabilities=non_capabilities,
        typical_requirement_hints=requirement_hints,
    )


def _entry(
    module_ref: str,
    domain: str,
    requirement_class: str,
    csa_ref: str,
    implementation_refs: Tuple[str, ...],
    model_refs: Tuple[str, ...],
    provider_refs: Tuple[str, ...],
    health_refs: Tuple[str, ...] = (),
    recovery_refs: Tuple[str, ...] = (),
) -> OfficialCapabilityCatalogEntryV1:
    return OfficialCapabilityCatalogEntryV1(
        catalog_entry_id=f"catalog:{module_ref}:v1",
        module_ref=module_ref,
        capability_domain=domain,
        requirement_class=requirement_class,
        csa_ref=csa_ref,
        implementation_refs=implementation_refs,
        model_refs=model_refs,
        provider_refs=provider_refs,
        slot_compatibility_refs=("compatibility:universal-slot-v1",),
        resource_refs=(f"resource-profile:{module_ref}",),
        permission_refs=("permission:capability-governance",),
        health_refs=health_refs or (f"health:{module_ref}",),
        recovery_refs=recovery_refs or (f"recovery:{module_ref}",),
        provenance_refs=(f"provenance:official-catalog:{module_ref}",),
        lifecycle_refs=("capability_lifecycle_contract_v1", "MODULE_LIFECYCLE_STATES"),
    )


def _mapping(
    asset: str,
    owner: str,
    classification: str,
    module: str,
    implementation: str,
    model: str,
    provider: str,
    supporting: str,
    csa: str,
    confidence: str,
    reason: str,
    gap: str,
) -> CapabilityAssetMappingV1:
    return CapabilityAssetMappingV1(
        existing_asset=asset,
        current_owner=owner,
        classification=classification,
        mapped_capability_module=module,
        implementation_ref=implementation,
        model_ref=model,
        provider_ref=provider,
        supporting_asset_ref=supporting,
        csa_ref=csa,
        mapping_confidence=confidence,
        mapping_reason=reason,
        conflict_or_gap=gap,
    )


def build_official_capability_catalog() -> OfficialCapabilityCatalogV1:
    annotations = (
        _csa(
            "official.safety.environment",
            "Provide minimum candidate evidence for safety-relevant environment awareness.",
            ("safety_environment_awareness", "basic_obstacle_awareness", "pedestrian_vehicle_risk"),
            ("roadway or shared-space observation", "obstacle or edge risk screening"),
            ("candidate safety-relevant detections", "risk-oriented evidence references"),
            ("minimum evidence domain only", "requires Gateway and governance consumers"),
            ("World Truth", "effective Field Rule", "Action authority", "exhaustive recognition"),
            ("MANDATORY_SAFETY", "Safety Vision Channel", "candidate evidence"),
        ),
        _csa(
            "official.system.sensor_health",
            "Expose candidate state about visual sensor health and availability.",
            ("visual_sensor_health", "perception_degradation"),
            ("sensor quality or availability review", "maintenance diagnosis"),
            ("health and degradation references", "maintenance input"),
            ("does not repair or mutate hardware", "does not certify external reality"),
            ("provider execution", "runtime repair", "World Truth"),
            ("SYSTEM_REQUIRED", "health governance", "maintenance reference"),
        ),
        _csa(
            "object_detection",
            "Detect configured object or environmental regions as evidence candidates.",
            ("common_object_awareness", "environment_region_detection"),
            ("task observation requiring object or region candidates",),
            ("object candidate references", "region and observation evidence"),
            ("class candidates are not facts", "does not resolve social or field rules"),
            ("World Truth", "Action", "semantic sufficiency", "complete scene understanding"),
            ("OPTIONAL", "observation requirement", "Evidence Gateway"),
        ),
        _csa(
            "text_recognition",
            "Produce candidate text evidence for text-bearing visual observations.",
            ("basic_text_recognition", "place_or_sign_text"),
            ("visible text or shopfront observation",),
            ("text candidate references", "readability evidence"),
            ("not guaranteed exact OCR", "does not infer effective Field Rule"),
            ("World Truth", "intent", "decision", "learning"),
            ("OPTIONAL", "text_content need", "candidate text output"),
        ),
        _csa(
            "precise_ocr",
            "Produce more targeted candidate text evidence when precise reading is requested.",
            ("precise_ocr", "small_text_reading", "shopfront_sign_text"),
            ("small or task-relevant text region",),
            ("fine-grained text candidate references", "region-attributed text evidence"),
            ("precision is not truth", "requires observation and evidence governance"),
            ("World Truth", "semantic folding", "automatic learning", "Action authority"),
            ("OPTIONAL", "precise_ocr requirement", "evidence sufficiency"),
        ),
        _csa(
            "spatial_mapping",
            "Produce candidate spatial map or anchor evidence for spatial tasks.",
            ("spatial_mapping", "navigation_map", "spatial_anchor_evidence"),
            ("navigation or spatial context request",),
            ("map and spatial-reference candidates", "temporal spatial evidence"),
            ("not a World Model owner", "does not authorize motion or action"),
            ("text recognition", "World Truth", "runtime navigation execution"),
            ("OPTIONAL", "navigation_map need", "spatial evidence"),
        ),
        _csa(
            "unknown_scene_reasoning",
            "Expose candidate visual evidence for unresolved scene or high-uncertainty situations.",
            ("unknown_scene", "high_uncertainty", "scene_identity_candidate"),
            ("unresolved visual situation",),
            ("uncertainty and scene evidence references", "candidate alternatives"),
            ("not a fact admission path", "not a semantic authority or Decision owner"),
            ("World Truth", "Intent mutation", "Decision", "Learning execution"),
            ("OPTIONAL", "unknown-scene need", "Gateway evidence"),
        ),
    )
    csa = {item.module_ref: item.capability_semantic_annotation_id for item in annotations}
    entries = (
        _entry("official.safety.environment", "SAFETY_ENVIRONMENT_AWARENESS", "MANDATORY_SAFETY", csa["official.safety.environment"], ("foundation:controlled-safety-module",), ("model-asset:safety-environment:controlled"), ("provider-contract:safety-environment:controlled"), recovery_refs=("rollback:safety-environment",)),
        _entry("official.system.sensor_health", "VISUAL_SENSOR_HEALTH", "SYSTEM_REQUIRED", csa["official.system.sensor_health"], ("foundation:controlled-sensor-health-module",), ("model-asset:sensor-health:controlled"), ("provider-contract:sensor-health:controlled")),
        _entry("object_detection", "COMMON_OBJECT_ENVIRONMENT_AWARENESS", "OPTIONAL", csa["object_detection"], ("model_manager:capability-runtime-boundary",), ("detection_v1",), ("capability_registry:object_detection",)),
        _entry("text_recognition", "BASIC_OCR", "OPTIONAL", csa["text_recognition"], ("ocr_manager:module",), ("ocr_v1", "qwen_vl"), ("capability_registry:text_recognition",)),
        _entry("precise_ocr", "ENHANCED_OCR", "OPTIONAL", csa["precise_ocr"], ("ocr_manager:module",), ("ocr_v1", "paddleocr_v1"), ("capability_registry:precise_ocr",)),
        _entry("spatial_mapping", "SPATIAL_UNDERSTANDING", "OPTIONAL", csa["spatial_mapping"], ("slam_spatial_mapping_adapter_core_v1",), ("slam_v1",), ("capability_registry:spatial_mapping",)),
        _entry("unknown_scene_reasoning", "UNKNOWN_SCENE_EVIDENCE", "OPTIONAL", csa["unknown_scene_reasoning"], ("model_manager:capability-runtime-boundary",), ("qwen_vl", "internvl2_5", "gemini_vision"), ("capability_registry:unknown_scene_reasoning",)),
    )
    mappings = (
        _mapping("capabilities/midplatform/model_manager/registries/capability_registry_v1.json", "Capability Registry", "SUPPORTING_ASSET", "object_detection; text_recognition; precise_ocr; spatial_mapping; unknown_scene_reasoning", "", "", "", "canonical capability definitions and provider mappings", "", "HIGH", "Existing registry capability_id is the closest canonical Module identity source.", "Registry has no CSA field; this catalog is an additive projection."),
        _mapping("capabilities/midplatform/model_manager/registries/model_registry_v1.json", "Model Manager", "SUPPORTING_ASSET", "", "", "", "", "model admission and dependency metadata", "", "HIGH", "Model registry defines model assets, not Luna capability identity.", "Must not be promoted to Capability Module."),
        _mapping("detection_v1", "Model Manager / Provider Governance", "MODEL", "object_detection", "", "detection_v1", "capability_registry:object_detection", "", "csa:object_detection:v1", "HIGH", "Registry maps this model to object_detection.", "Model is an implementation dependency."),
        _mapping("ocr_v1", "Model Manager / Provider Governance", "MODEL", "text_recognition; precise_ocr", "", "ocr_v1", "capability_registry:text_recognition; capability_registry:precise_ocr", "", "csa:text_recognition:v1; csa:precise_ocr:v1", "HIGH", "The same OCR asset supports two existing capability identities.", "Capability identity remains separate from model identity."),
        _mapping("slam_v1", "Model Manager / Provider Governance", "MODEL", "spatial_mapping", "", "slam_v1", "capability_registry:spatial_mapping", "", "csa:spatial_mapping:v1", "HIGH", "Existing registry explicitly maps SLAM to spatial_mapping.", "VIO/trajectory semantics are not separately established."),
        _mapping("mobile_sam_v1", "Model Manager", "MODEL", "MAPPING_REVIEW_REQUIRED:segmentation", "", "mobile_sam_v1", "", "model_test_lens/model_panels/vision_segmentation", "", "MEDIUM", "Model registry exposes segmentation capability metadata.", "No canonical capability registry entry proves a distinct Official Module."),
        _mapping("capabilities/midplatform/field_perception_orchestrator/integration/yolo11n_single_frame_execution", "Field Perception Orchestrator", "PROVIDER", "object_detection", "field_perception_real_vision_provider_adapter_v1", "model-asset:yolo11n:weights-v1", "S3-Y11 provider boundary", "Observation Gateway / B1 evidence integration", "csa:object_detection:v1", "MEDIUM", "The S3 asset is a bounded provider execution path producing evidence; it is not a capability identity.", "Model is not in the canonical model_registry_v1.json mapping for object_detection."),
        _mapping("capabilities/vision/registry/visual_capability_system_controlled/visual_capability_system_types_v1.py:SafetyCapabilitySlotV1", "Visual Capability reference integration", "SUPPORTING_ASSET", "official.safety.environment; official.system.sensor_health", "visual capability controlled skeleton", "", "", "visual reference lifecycle/routing types", "csa:official.safety.environment:v1; csa:official.system.sensor_health:v1", "MEDIUM", "Reference implementation supplies safety and sensor-health categories.", "SafetyCapabilitySlotV1 is visual-specific and must not become a Universal Slot type."),
        _mapping("capabilities/midplatform/slam_spatial_mapping_adapter_core_v1.py", "Spatial Mapping supporting integration", "IMPLEMENTATION", "spatial_mapping", "capabilities/midplatform/slam_spatial_mapping_adapter_core_v1.py", "slam_v1", "capability_registry:spatial_mapping", "spatial mapping evidence adapters", "csa:spatial_mapping:v1", "HIGH", "Adapter implements a registered spatial_mapping capability dependency.", "No separate VIO capability identity established."),
        _mapping("capabilities/midplatform/ocr_manager/module/", "OCR Manager", "IMPLEMENTATION", "text_recognition; precise_ocr", "ocr_manager/module", "ocr_v1", "capability_registry:text_recognition; capability_registry:precise_ocr", "OCR evidence envelope, request, diagnostics", "csa:text_recognition:v1; csa:precise_ocr:v1", "HIGH", "OCR Manager is a capability implementation/supporting boundary, not a new registry.", "Enhanced/basic distinction remains at capability contract level."),
        _mapping("VIO / pose / trajectory assets", "No singular canonical owner identified", "SUPPORTING_ASSET", "MAPPING_REVIEW_REQUIRED:vio_pose_trajectory", "", "", "", "existing spatial/SLAM diagnostic assets", "", "MAPPING_REVIEW_REQUIRED", "Static inventory found SLAM/spatial assets but no authoritative VIO Capability Module record.", "Do not create a VIO module in this phase."),
        _mapping("Face-related visual assets", "No official capability record identified", "SUPPORTING_ASSET", "MAPPING_REVIEW_REQUIRED:face_related", "", "", "", "visual reference only", "", "MAPPING_REVIEW_REQUIRED", "No canonical official face capability asset was identified in the inspected Registry/Model mappings.", "No Face Capability Module or CSA is created."),
    )
    slot_mappings = tuple(
        SlotCompatibilityMappingV1(
            module_ref=entry.module_ref,
            slot_contract_ref=SLOT_CONTRACT_REF,
            compatibility_refs=entry.slot_compatibility_refs,
        )
        for entry in entries
    )
    return OfficialCapabilityCatalogV1(
        catalog_id=CATALOG_ID,
        catalog_version=CATALOG_VERSION,
        entries=entries,
        annotations=annotations,
        asset_mappings=mappings,
        slot_mappings=slot_mappings,
    )


def validate_catalog(catalog: OfficialCapabilityCatalogV1) -> List[str]:
    issues: List[str] = []
    entry_modules = {entry.module_ref for entry in catalog.entries}
    annotation_modules = {annotation.module_ref for annotation in catalog.annotations}
    annotation_ids = {annotation.capability_semantic_annotation_id for annotation in catalog.annotations}
    if not catalog.catalog_id or not catalog.catalog_version:
        issues.append("CATALOG_ID_OR_VERSION_MISSING")
    if catalog.market_governance_status != "DEFERRED":
        issues.append("MARKET_GOVERNANCE_NOT_DEFERRED")
    for entry in catalog.entries:
        if entry.origin != "OFFICIAL":
            issues.append(f"NON_OFFICIAL_CATALOG_ENTRY:{entry.module_ref}")
        if entry.module_ref not in annotation_modules or entry.csa_ref not in annotation_ids:
            issues.append(f"CSA_MISSING_OR_INVALID:{entry.module_ref}")
        if not entry.slot_compatibility_refs:
            issues.append(f"SLOT_COMPATIBILITY_MISSING:{entry.module_ref}")
    for annotation in catalog.annotations:
        if annotation.module_ref not in entry_modules:
            issues.append(f"ORPHAN_CSA:{annotation.module_ref}")
        if annotation.semantic_depth != "MINIMAL":
            issues.append(f"CSA_DEPTH_NOT_MINIMAL:{annotation.module_ref}")
        if any((annotation.semantic_authority, annotation.world_truth_authority, annotation.action_authority)):
            issues.append(f"CSA_AUTHORITY_VIOLATION:{annotation.module_ref}")
        if not annotation.candidate_only or not annotation.descriptive_only:
            issues.append(f"CSA_BOUNDARY_VIOLATION:{annotation.module_ref}")
        if annotation.dynamic_semantic_expansion or annotation.dynamic_semantic_folding or annotation.semantic_sufficiency_execution:
            issues.append(f"CSA_DYNAMIC_SEMANTICS_EXECUTED:{annotation.module_ref}")
    for mapping in catalog.asset_mappings:
        if mapping.classification not in ASSET_CLASS_VALUES:
            issues.append(f"UNKNOWN_ASSET_CLASS:{mapping.existing_asset}")
        if mapping.mapping_confidence not in {"HIGH", "MEDIUM", "LOW", "MAPPING_REVIEW_REQUIRED"}:
            issues.append(f"UNKNOWN_MAPPING_CONFIDENCE:{mapping.existing_asset}")
        if mapping.classification in {"MODEL", "PROVIDER"} and mapping.mapped_capability_module == mapping.existing_asset:
            issues.append(f"MODEL_OR_PROVIDER_AS_MODULE:{mapping.existing_asset}")
    if not all(item.generic_slot_only and not item.safety_slot_specialization for item in catalog.slot_mappings):
        issues.append("SPECIALIZED_SLOT_MAPPING")
    if not catalog.candidate_only or catalog.runtime_execution or catalog.provider_invocation or catalog.model_inference:
        issues.append("RUNTIME_BOUNDARY_VIOLATION")
    return issues
