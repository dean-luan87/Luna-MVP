# -*- coding: utf-8 -*-
"""Recognition Model System Admission and Invocation Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_system_admission_and_invocation_planning.recognition_model_system_admission_and_invocation_planning_types_v1 import (
    ADMISSION_ORDER,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    INVOCATION_FEASIBILITY_CHECK_ITEMS,
    MAIN_CHAIN_CLOSURE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    MODEL_FAMILY_IDS,
    PLANNING_GOVERNANCE_RULES,
    REJECT_IF_MISSING_FIELDS,
    REQUIRED_MODEL_OUTPUT_FIELDS,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelAdapterReadinessPolicy,
    RecognitionModelDataUsageDeferralPolicy,
    RecognitionModelFamilyAdmissionPolicy,
    RecognitionModelInputRequirementPolicy,
    RecognitionModelInvocationFeasibilityPolicy,
    RecognitionModelOutputRequirementPolicy,
    RecognitionModelRuntimeBoundaryPolicy,
    RecognitionModelSystemAdmissionPlanningProfile,
    RecognitionModelTuningDeferralPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "recognition_model_system_admission_and_invocation_planning_registry_v1"
PROFILE_REF = "recognition_model_system_admission_and_invocation_planning_profile_v1"

# --------------------------------------------------------------------------- #
# Per-family base definitions
# --------------------------------------------------------------------------- #
_FAMILY_DEFS: Tuple[Dict[str, Any], ...] = (
    {
        "model_family_id": "ocr_model_family",
        "examples": ("RapidOCR", "PaddleOCR", "Tesseract", "EasyOCR"),
        "target_candidate": ("text_evidence_candidate",),
        "output_check_required": ("text", "bbox_or_polygon", "confidence", "language", "orientation"),
    },
    {
        "model_family_id": "object_detection_model_family",
        "examples": ("YOLO", "RT-DETR", "GroundingDINO"),
        "target_candidate": ("object_evidence_candidate",),
        "output_check_required": ("label", "bbox", "confidence", "class_id_or_phrase"),
    },
    {
        "model_family_id": "segmentation_model_family",
        "examples": ("SAM", "Grounded SAM 2", "FastSAM", "semantic_segmentation_model"),
        "target_candidate": ("region_evidence_candidate",),
        "output_check_required": ("mask_or_polygon", "bbox", "label", "confidence"),
    },
    {
        "model_family_id": "tracking_model_family",
        "examples": ("ByteTrack", "DeepSORT", "supervision_tracking"),
        "target_candidate": ("track_evidence_candidate", "dynamic_risk_candidate"),
        "output_check_required": (
            "track_id",
            "bbox_sequence",
            "timestamp",
            "velocity_hint",
            "confidence",
        ),
    },
    {
        "model_family_id": "depth_spatial_hint_model_family",
        "examples": ("Depth Anything", "MiDaS", "ZoeDepth", "VIO_adapter"),
        "target_candidate": ("spatial_hint_candidate",),
        "output_check_required": ("depth_map_ref", "relative_depth", "motion_hint", "confidence"),
    },
    {
        "model_family_id": "visual_symbol_model_family",
        "examples": (
            "color_extraction",
            "shape_detection",
            "arrow_detection",
            "icon_detection",
            "visual_symbol_rules",
        ),
        "target_candidate": (
            "color_evidence_candidate",
            "shape_evidence_candidate",
            "visual_symbol_candidate",
        ),
        "output_check_required": (
            "color",
            "shape",
            "symbol_type",
            "direction",
            "region_ref",
            "confidence",
        ),
    },
    {
        "model_family_id": "scene_relation_model_family",
        "examples": ("scene_graph_extractor", "VLM_structured_output", "relation_model"),
        "target_candidate": ("scene_relation_candidate", "attribute_candidate"),
        "output_check_required": ("subject", "relation", "object", "region_ref", "confidence"),
    },
)


def _build_family_admission_policies() -> Tuple[RecognitionModelFamilyAdmissionPolicy, ...]:
    return tuple(
        RecognitionModelFamilyAdmissionPolicy(
            model_family_id=d["model_family_id"],
            examples=d["examples"],
            target_candidate=d["target_candidate"],
            invocation_check_required=True,
            output_check_required=d["output_check_required"],
            admission_planned=True,
        )
        for d in _FAMILY_DEFS
    )


def _build_invocation_feasibility_policies() -> Tuple[
    RecognitionModelInvocationFeasibilityPolicy, ...
]:
    return tuple(
        RecognitionModelInvocationFeasibilityPolicy(
            model_family_id=d["model_family_id"],
            callable_interface_defined=True,
            input_format_defined=True,
            output_schema_defined=True,
            local_or_target_runtime_requirement_declared=True,
            license_ref_required=True,
            model_origin_required=True,
            dependency_boundary_declared=True,
            resource_requirement_declared=True,
            offline_or_online_mode_declared=True,
            adapter_mapping_target_declared=True,
        )
        for d in _FAMILY_DEFS
    )


def _build_input_requirement_policies() -> Tuple[RecognitionModelInputRequirementPolicy, ...]:
    return tuple(
        RecognitionModelInputRequirementPolicy(
            model_family_id=d["model_family_id"],
            input_format_required=True,
            input_ref_required=True,
        )
        for d in _FAMILY_DEFS
    )


def _build_output_requirement_policies() -> Tuple[RecognitionModelOutputRequirementPolicy, ...]:
    return tuple(
        RecognitionModelOutputRequirementPolicy(
            model_family_id=d["model_family_id"],
            required_output_fields=REQUIRED_MODEL_OUTPUT_FIELDS,
            source_chain_required=True,
            confidence_required=True,
            adapter_mapping_ref_required=True,
            allowed_use_required=True,
            commercial_use_status_required=True,
        )
        for d in _FAMILY_DEFS
    )


def _build_adapter_readiness_policies() -> Tuple[RecognitionModelAdapterReadinessPolicy, ...]:
    return tuple(
        RecognitionModelAdapterReadinessPolicy(
            model_family_id=d["model_family_id"],
            adapter_mapping_target_declared=True,
            model_output_adapter_required=True,
            native_model_output_direct_to_field_blocked=True,
            all_model_outputs_become_evidence_candidate_first=True,
        )
        for d in _FAMILY_DEFS
    )


_FAMILY_ADMISSION = _build_family_admission_policies()
_INVOCATION_FEASIBILITY = _build_invocation_feasibility_policies()
_INPUT_REQUIREMENT = _build_input_requirement_policies()
_OUTPUT_REQUIREMENT = _build_output_requirement_policies()
_ADAPTER_READINESS = _build_adapter_readiness_policies()

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
        RecognitionModelSystemAdmissionPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001",
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            model_family_ids=MODEL_FAMILY_IDS,
            invocation_feasibility_check_items=INVOCATION_FEASIBILITY_CHECK_ITEMS,
            required_model_output_fields=REQUIRED_MODEL_OUTPUT_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            admission_order=ADMISSION_ORDER,
            governance_rules=PLANNING_GOVERNANCE_RULES,
        )
    )


def build_runtime_boundary_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelRuntimeBoundaryPolicy(
            policy_ref="recognition_model_runtime_boundary_policy_v1",
            model_invocation_execution_allowed=False,
            model_download_allowed=False,
            model_repo_clone_allowed=False,
            model_build_allowed=False,
            real_inference_allowed=False,
        )
    )


def build_tuning_deferral_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelTuningDeferralPolicy(
            policy_ref="recognition_model_tuning_deferral_policy_v1",
            model_tuning_deferred=True,
            invocation_before_tuning_order_enforced=True,
        )
    )


def build_data_usage_deferral_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RecognitionModelDataUsageDeferralPolicy(
            policy_ref="recognition_model_data_usage_deferral_policy_v1",
            dataset_usage_deferred=True,
            model_before_data_usage_order_enforced=True,
            real_recognition_dryrun_deferred=True,
        )
    )


def build_recognition_model_system_admission_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "planning_profile": build_planning_profile_v1(),
        "family_admission_policies": [candidate_to_dict(p) for p in _FAMILY_ADMISSION],
        "model_family_policy_count": len(_FAMILY_ADMISSION),
        "invocation_feasibility_policies": [
            candidate_to_dict(p) for p in _INVOCATION_FEASIBILITY
        ],
        "invocation_feasibility_policy_count": len(_INVOCATION_FEASIBILITY),
        "input_requirement_policies": [candidate_to_dict(p) for p in _INPUT_REQUIREMENT],
        "input_requirement_policy_count": len(_INPUT_REQUIREMENT),
        "output_requirement_policies": [candidate_to_dict(p) for p in _OUTPUT_REQUIREMENT],
        "output_requirement_policy_count": len(_OUTPUT_REQUIREMENT),
        "adapter_readiness_policies": [candidate_to_dict(p) for p in _ADAPTER_READINESS],
        "adapter_readiness_policy_count": len(_ADAPTER_READINESS),
        "runtime_boundary_policy": build_runtime_boundary_policy_v1(),
        "tuning_deferral_policy": build_tuning_deferral_policy_v1(),
        "data_usage_deferral_policy": build_data_usage_deferral_policy_v1(),
        "admission_order": list(ADMISSION_ORDER),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_FAMILY_ADMISSION) < 7:
        issues.append("model_family_policy_count_lt_7")
    if len(_INVOCATION_FEASIBILITY) < 7:
        issues.append("invocation_feasibility_policy_count_lt_7")
    if len(_OUTPUT_REQUIREMENT) < 7:
        issues.append("output_requirement_policy_count_lt_7")
    if len(_ADAPTER_READINESS) < 7:
        issues.append("adapter_readiness_policy_count_lt_7")

    seen = set()
    for p in _FAMILY_ADMISSION:
        if p.model_family_id in seen:
            issues.append(f"duplicate_model_family:{p.model_family_id}")
        seen.add(p.model_family_id)
        if not p.admission_planned:
            issues.append(f"family_admission_not_planned:{p.model_family_id}")
        if not p.invocation_check_required:
            issues.append(f"family_invocation_check_not_required:{p.model_family_id}")
        if not p.output_check_required:
            issues.append(f"family_output_check_empty:{p.model_family_id}")
    for expected in MODEL_FAMILY_IDS:
        if expected not in seen:
            issues.append(f"expected_model_family_missing:{expected}")

    # invocation feasibility: every check item must be True for every family.
    for p in _INVOCATION_FEASIBILITY:
        d = candidate_to_dict(p)
        for item in INVOCATION_FEASIBILITY_CHECK_ITEMS:
            if d.get(item) is not True:
                issues.append(f"invocation_check_not_set:{p.model_family_id}:{item}")

    if len(ADMISSION_ORDER) != 7:
        issues.append("admission_order_count_not_7")

    return len(issues) == 0, issues
