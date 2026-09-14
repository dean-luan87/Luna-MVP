# -*- coding: utf-8 -*-
"""Recognition Model Output Adapter Integration Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_output_adapter_integration_planning.recognition_model_output_adapter_integration_planning_types_v1 import (
    ADAPTER_MAPPING_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MAIN_CHAIN_CLOSURE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    MODEL_FAMILY_IDS,
    PLANNING_GOVERNANCE_RULES,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_MODEL_OUTPUT_FIELDS,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SCENARIO_IDS,
    SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelAdmissionBoundaryPolicy,
    RecognitionModelCandidateMappingPolicy,
    RecognitionModelFamilyPolicy,
    RecognitionModelOutputAdapterIntegrationPlanningProfile,
    RecognitionModelOutputAdapterMappingPolicy,
    RecognitionModelOutputSchemaPolicy,
    RecognitionModelSafetyBoundaryPolicy,
    RecognitionModelScenarioPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "recognition_model_output_adapter_integration_planning_registry_v1"
PROFILE_REF = "recognition_model_output_adapter_integration_planning_profile_v1"

# --------------------------------------------------------------------------- #
# Model families
# --------------------------------------------------------------------------- #
_MODEL_FAMILIES: Tuple[RecognitionModelFamilyPolicy, ...] = (
    RecognitionModelFamilyPolicy(
        model_family_id="ocr_model_family",
        model_examples=("RapidOCR", "PaddleOCR", "Tesseract", "EasyOCR"),
        output_schema=("text", "bbox", "polygon", "confidence", "language", "orientation"),
        maps_to=("text_evidence_candidate",),
        boundary="OCR output is not fact",
        registered=True,
    ),
    RecognitionModelFamilyPolicy(
        model_family_id="object_detection_model_family",
        model_examples=("YOLO", "RT-DETR", "GroundingDINO"),
        output_schema=("label", "bbox", "confidence", "class_id", "phrase"),
        maps_to=("object_evidence_candidate",),
        boundary="object identity is not fact",
        registered=True,
    ),
    RecognitionModelFamilyPolicy(
        model_family_id="segmentation_model_family",
        model_examples=("SAM", "Grounded SAM 2", "FastSAM", "semantic_segmentation_model"),
        output_schema=("mask", "polygon", "bbox", "label", "confidence"),
        maps_to=("region_evidence_candidate",),
        boundary="segmentation is not route activation",
        registered=True,
    ),
    RecognitionModelFamilyPolicy(
        model_family_id="tracking_model_family",
        model_examples=("ByteTrack", "DeepSORT", "supervision_tracking"),
        output_schema=("track_id", "bbox_sequence", "velocity_hint", "confidence"),
        maps_to=("track_evidence_candidate", "dynamic_risk_candidate"),
        boundary="tracking is not action trigger",
        registered=True,
    ),
    RecognitionModelFamilyPolicy(
        model_family_id="depth_spatial_hint_model_family",
        model_examples=("Depth Anything", "MiDaS", "ZoeDepth", "VIO_export_adapter"),
        output_schema=("relative_depth", "depth_map_ref", "motion_hint", "confidence"),
        maps_to=("spatial_hint_candidate",),
        boundary="depth / VIO does not override field identity",
        registered=True,
    ),
    RecognitionModelFamilyPolicy(
        model_family_id="visual_symbol_model_family",
        model_examples=(
            "color_extraction",
            "shape_detection",
            "arrow_detection",
            "icon_detection",
            "visual_symbol_rules",
        ),
        output_schema=("color", "shape", "direction", "symbol_type", "region_ref", "confidence"),
        maps_to=(
            "color_evidence_candidate",
            "shape_evidence_candidate",
            "visual_symbol_candidate",
            "symbol_meaning_candidate",
        ),
        boundary="color / shape / symbol is not fact; symbol meaning requires context validation",
        registered=True,
    ),
    RecognitionModelFamilyPolicy(
        model_family_id="scene_relation_model_family",
        model_examples=("scene_graph_extractor", "VLM_structured_output", "relation_model"),
        output_schema=("subject", "relation", "object", "region_ref", "confidence"),
        maps_to=("scene_relation_candidate", "attribute_candidate"),
        boundary="scene relation is not final interpretation",
        registered=True,
    ),
)

# --------------------------------------------------------------------------- #
# Adapter mapping policies
# --------------------------------------------------------------------------- #
_ADAPTER_MAPPINGS: Tuple[RecognitionModelOutputAdapterMappingPolicy, ...] = (
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="text_output_to_text_evidence_mapping",
        model_native_input="text / OCR polygon / bbox / confidence",
        luna_candidate_output="text_evidence_candidate",
        boundary="OCR text not fact",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="detection_output_to_object_evidence_mapping",
        model_native_input="detection bbox / label / confidence",
        luna_candidate_output="object_evidence_candidate",
        boundary="object identity not fact",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="segmentation_output_to_region_evidence_mapping",
        model_native_input="segmentation mask / polygon / semantic region label",
        luna_candidate_output="region_evidence_candidate",
        boundary="segmentation not route activation",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="tracking_output_to_track_dynamic_risk_mapping",
        model_native_input="track sequence / track_id / velocity_hint",
        luna_candidate_output="track_evidence_candidate / dynamic_risk_candidate",
        boundary="tracking not action trigger",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="depth_output_to_spatial_hint_mapping",
        model_native_input="depth map / relative depth / motion hint",
        luna_candidate_output="spatial_hint_candidate",
        boundary="depth / VIO not field identity",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="visual_symbol_output_mapping",
        model_native_input="color / shape / icon / arrow",
        luna_candidate_output=(
            "color_evidence_candidate / shape_evidence_candidate / "
            "visual_symbol_candidate / symbol_meaning_candidate"
        ),
        boundary="symbol meaning requires context validation",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="scene_relation_output_mapping",
        model_native_input="relation triplet / scene graph output",
        luna_candidate_output="scene_relation_candidate / attribute_candidate",
        boundary="scene relation not final interpretation",
        adapter_required=True,
        supported=True,
    ),
    RecognitionModelOutputAdapterMappingPolicy(
        adapter_mapping_id="uncertainty_conflict_output_mapping",
        model_native_input="uncertainty / conflict / low confidence",
        luna_candidate_output=(
            "cross_modal_uncertainty_candidate / cross_modal_conflict_candidate"
        ),
        boundary="conflict does not directly write fact / trigger action",
        adapter_required=True,
        supported=True,
    ),
)

# --------------------------------------------------------------------------- #
# Planning scenarios
# --------------------------------------------------------------------------- #
_SCENARIOS: Tuple[RecognitionModelScenarioPolicy, ...] = (
    RecognitionModelScenarioPolicy(
        scenario_id="ocr_model_output_adapter_planning",
        planned_output="OCR text / bbox / confidence -> text_evidence_candidate",
        boundary="OCR text not fact",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="object_detection_model_output_adapter_planning",
        planned_output="label / bbox / confidence -> object_evidence_candidate",
        boundary="object identity not fact",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="segmentation_model_output_adapter_planning",
        planned_output="mask / polygon / region label -> region_evidence_candidate",
        boundary="segmentation not route activation",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="tracking_model_output_adapter_planning",
        planned_output="track_id / trajectory / velocity_hint -> track / dynamic_risk candidate",
        boundary="tracking not action trigger",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="depth_spatial_hint_model_output_adapter_planning",
        planned_output="depth / VIO / motion hint -> spatial_hint_candidate",
        boundary="depth / VIO not field identity",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="visual_symbol_model_output_adapter_planning",
        planned_output=(
            "color / shape / arrow / icon -> color / shape / visual_symbol / symbol_meaning candidate"
        ),
        boundary="symbol meaning requires context validation",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="scene_relation_model_output_adapter_planning",
        planned_output="subject-relation-object / scene graph -> scene_relation / attribute candidate",
        boundary="scene relation not final interpretation",
        expected_result="supported",
    ),
    RecognitionModelScenarioPolicy(
        scenario_id="invalid_model_output_blocked",
        planned_output=(
            "missing source_chain / license_ref / model native direct to Field / OCR fact_write / "
            "segmentation route activation / tracking direct action / symbol direct navigation / "
            "depth overrides field identity"
        ),
        boundary="must be blocked / rejected",
        expected_result="blocked",
    ),
)

# --------------------------------------------------------------------------- #
# Candidate mapping table
# --------------------------------------------------------------------------- #
_CANDIDATE_MAPPING: Tuple[Dict[str, str], ...] = (
    {"native": "text / OCR polygon", "candidate": "text_evidence_candidate"},
    {"native": "detection bbox / label", "candidate": "object_evidence_candidate"},
    {"native": "segmentation mask / semantic region", "candidate": "region_evidence_candidate"},
    {"native": "track sequence", "candidate": "track_evidence_candidate / dynamic_risk_candidate"},
    {"native": "depth map / relative depth", "candidate": "spatial_hint_candidate"},
    {
        "native": "color / shape / icon / arrow",
        "candidate": "color_evidence_candidate / shape_evidence_candidate / visual_symbol_candidate",
    },
    {
        "native": "relation triplet / scene graph",
        "candidate": "scene_relation_candidate / attribute_candidate",
    },
    {
        "native": "uncertainty / conflict / low confidence",
        "candidate": "cross_modal_uncertainty_candidate / cross_modal_conflict_candidate",
    },
)

# --------------------------------------------------------------------------- #
# Upstream sealed GO artifacts
# --------------------------------------------------------------------------- #
_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": MAIN_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_evidence_main_chain_closure/"
            "phase_one_environment_cognition_evidence_main_chain_closure_types_v1.py"
        ),
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
    },
    {
        "phase_ref": RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_evidence_chain_integrated_closure/"
            "rgb_vision_evidence_chain_integrated_closure_types_v1.py"
        ),
        "verify_flag": "rgb_vision_evidence_chain_closure_go_verified",
    },
    {
        "phase_ref": SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_backend_evidence_chain_integrated_closure_v1_smoke_v0/"
            "slam_backend_evidence_chain_integrated_closure_review_v1.json"
        ),
        "expected_go": "SLAM_BACKEND_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_backend_evidence_chain_integrated_closure/"
            "slam_backend_evidence_chain_integrated_closure_types_v1.py"
        ),
        "verify_flag": "slam_backend_evidence_chain_closure_go_verified",
    },
    {
        "phase_ref": RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_types_v1.py"
        ),
        "verify_flag": "rgb_slam_cross_modal_closure_go_verified",
    },
    {
        "phase_ref": FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
    },
    {
        "phase_ref": GOVERNANCE_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_types_v1.py"
        ),
        "verify_flag": "runtime_governance_closure_go_verified",
    },
    {
        "phase_ref": INTERFACE_LAYER_GOVERNANCE_REF,
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "verify_flag": "interface_layer_governance_verified",
    },
    {
        "phase_ref": MODEL_ADMISSION_GOVERNANCE_REF,
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "verify_flag": "model_admission_governance_verified",
    },
)


def build_planning_profile_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelOutputAdapterIntegrationPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-Recognition-Model-Output-Adapter-Integration-Planning-v1-001",
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            target_entrypoint=TARGET_ENTRYPOINT,
            target_chain_ref=TARGET_CHAIN_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            model_family_ids=MODEL_FAMILY_IDS,
            adapter_mapping_ids=ADAPTER_MAPPING_IDS,
            scenario_ids=SCENARIO_IDS,
            required_model_output_fields=REQUIRED_MODEL_OUTPUT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            governance_rules=PLANNING_GOVERNANCE_RULES,
        )
    )


def build_output_schema_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelOutputSchemaPolicy(
            policy_ref="recognition_model_output_schema_policy_v1",
            required_model_output_fields=REQUIRED_MODEL_OUTPUT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
        )
    )


def build_candidate_mapping_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelCandidateMappingPolicy(
            policy_ref="recognition_model_candidate_mapping_policy_v1",
            native_output_direct_to_field_blocked=True,
            all_model_outputs_become_evidence_candidate_first=True,
            candidate_mapping=_CANDIDATE_MAPPING,
        )
    )


def build_safety_boundary_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelSafetyBoundaryPolicy(
            policy_ref="recognition_model_safety_boundary_policy_v1",
            ocr_output_not_fact=True,
            object_identity_not_fact=True,
            segmentation_not_route_activation=True,
            tracking_not_action_trigger=True,
            depth_vio_not_field_identity=True,
            color_shape_symbol_not_fact=True,
            visual_symbol_requires_context_validation=True,
            scene_relation_not_final_interpretation=True,
            field_task_guidance_candidate_only=True,
            guidance_candidate_remains_candidate=True,
            speech_gate_candidate_not_tts=True,
            action_safety_candidate_exists=True,
        )
    )


def build_admission_boundary_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelAdmissionBoundaryPolicy(
            policy_ref="recognition_model_admission_boundary_policy_v1",
            model_output_adapter_required=True,
            native_model_output_direct_to_field_blocked=True,
            source_chain_required=True,
            license_ref_required=True,
            model_origin_required=True,
            confidence_required=True,
            adapter_mapping_ref_required=True,
        )
    )


def build_recognition_model_planning_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "planning_profile": build_planning_profile_v1(),
        "model_families": [candidate_to_dict(m) for m in _MODEL_FAMILIES],
        "model_family_policy_count": len(_MODEL_FAMILIES),
        "adapter_mappings": [candidate_to_dict(a) for a in _ADAPTER_MAPPINGS],
        "adapter_mapping_policy_count": len(_ADAPTER_MAPPINGS),
        "scenarios": [candidate_to_dict(s) for s in _SCENARIOS],
        "scenario_count": len(_SCENARIOS),
        "output_schema_policy": build_output_schema_policy_v1(),
        "candidate_mapping_policy": build_candidate_mapping_policy_v1(),
        "safety_boundary_policy": build_safety_boundary_policy_v1(),
        "admission_boundary_policy": build_admission_boundary_policy_v1(),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_MODEL_FAMILIES) < 7:
        issues.append("model_family_policy_count_lt_7")
    if len(_ADAPTER_MAPPINGS) < 8:
        issues.append("adapter_mapping_policy_count_lt_8")
    if len(_SCENARIOS) < 8:
        issues.append("scenario_count_lt_8")

    seen_family = set()
    for m in _MODEL_FAMILIES:
        if m.model_family_id in seen_family:
            issues.append(f"duplicate_model_family:{m.model_family_id}")
        seen_family.add(m.model_family_id)
        if not m.registered:
            issues.append(f"model_family_not_registered:{m.model_family_id}")
        if not m.maps_to:
            issues.append(f"model_family_missing_maps_to:{m.model_family_id}")
    for expected in MODEL_FAMILY_IDS:
        if expected not in seen_family:
            issues.append(f"expected_model_family_missing:{expected}")

    seen_map = set()
    for a in _ADAPTER_MAPPINGS:
        if a.adapter_mapping_id in seen_map:
            issues.append(f"duplicate_adapter_mapping:{a.adapter_mapping_id}")
        seen_map.add(a.adapter_mapping_id)
        if not (a.adapter_required and a.supported):
            issues.append(f"adapter_mapping_not_ready:{a.adapter_mapping_id}")
    for expected in ADAPTER_MAPPING_IDS:
        if expected not in seen_map:
            issues.append(f"expected_adapter_mapping_missing:{expected}")

    seen_sc = set()
    for s in _SCENARIOS:
        if s.scenario_id in seen_sc:
            issues.append(f"duplicate_scenario:{s.scenario_id}")
        seen_sc.add(s.scenario_id)
    for expected in SCENARIO_IDS:
        if expected not in seen_sc:
            issues.append(f"expected_scenario_missing:{expected}")

    return len(issues) == 0, issues
