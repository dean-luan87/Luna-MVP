# -*- coding: utf-8 -*-
"""RGB Vision + SLAM Spatial Evidence Cross-Modal Integrated Closure — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure.rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_types_v1 import (
    ALIGNMENT_POLICY_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CROSS_MODAL_CANDIDATE_IDS,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    RGB_INTERFACE_ADAPTER_REF,
    RGB_VISION_COVERAGE_IDS,
    RGB_VISION_DRYRUN_REF,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_PLANNING_REF,
    ROBOFLOW_DATASET_DRYRUN_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
    SLAM_INTERFACE_ADAPTER_REF,
    SLAM_ROLE,
    SLAM_SPATIAL_COVERAGE_IDS,
    STAGE_REFS,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    VISION_HARDWARE_BASELINE,
    VISION_TEST_SOURCE_BACKUP_POOL_REF,
    VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF,
    CLOSURE_GOVERNANCE_RULES,
    CrossModalConflictAndUncertaintyPolicy,
    CrossModalEvidenceAlignmentPolicy,
    CrossModalEvidenceClosureProfile,
    CrossModalFieldSynthesisPathClosure,
    CrossModalSafetyBoundaryClosure,
    CrossModalStageRef,
    CrossModalTaskGuidancePathClosure,
    RGBVisionEvidenceCoverageRef,
    SLAMSpatialEvidenceCoverageRef,
    candidate_to_dict,
)

REGISTRY_ID = "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_registry_v1"
PROFILE_REF = "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_profile_v1"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
_STAGES: Tuple[CrossModalStageRef, ...] = (
    CrossModalStageRef(
        stage_ref="rgb_vision_evidence_chain_closure",
        phase_ref=RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
        expected_final_decision="RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        coverage=(
            "scene", "object", "region", "track", "dynamic_risk", "text", "spatial_hint",
            "attribute", "scene_relation", "color", "shape", "visual_symbol",
            "task_context", "task_risk",
        ),
    ),
    CrossModalStageRef(
        stage_ref="slam_backend_evidence_chain_closure",
        phase_ref=SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
        expected_final_decision="SLAM_BACKEND_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        coverage=(
            "pose", "motion", "health", "anchor", "relocalization", "drift", "region",
            "scene_relation", "semantic_place", "field_structure", "local_map",
            "uncertainty_hint",
        ),
    ),
    CrossModalStageRef(
        stage_ref="rtab_multi_export_spatial_evidence_replay_closure",
        phase_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
        expected_final_decision=(
            "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_GO"
        ),
        coverage=("spatial_evidence_candidate_bundle", "spatial_odometry_fusion_candidate"),
    ),
    CrossModalStageRef(
        stage_ref="field_task_guidance_safety_chain_closure",
        phase_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        expected_final_decision="FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        coverage=("field_task_guidance_candidate_only_safety_path",),
    ),
    CrossModalStageRef(
        stage_ref="runtime_governance_closure",
        phase_ref=GOVERNANCE_CLOSURE_REF,
        expected_final_decision=(
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        coverage=("controlled_runtime_governance_sealed",),
    ),
)

# --------------------------------------------------------------------------- #
# Cross-modal alignment policies
# --------------------------------------------------------------------------- #
_ALIGNMENT_POLICIES: Tuple[CrossModalEvidenceAlignmentPolicy, ...] = (
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="object_to_anchor_alignment",
        rgb_side="object_evidence_candidate",
        slam_side="anchor_candidate",
        purpose="attach seen objects to spatial anchors",
        rule="object identity must not directly become field fact",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="region_to_local_map_alignment",
        rgb_side="region_evidence_candidate",
        slam_side="local_map / field_structure candidate",
        purpose="align walkable regions / walls / doors / passages with local structure",
        rule="segmentation is not route activation",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="text_to_spatial_anchor_alignment",
        rgb_side="text_evidence_candidate",
        slam_side="anchor / pose context",
        purpose="attach signs / door numbers / entrance text to spatial position candidates",
        rule="OCR text is not fact",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="visual_symbol_to_field_context_alignment",
        rgb_side="color / shape / visual_symbol_candidate",
        slam_side="object / region / anchor / scene context",
        purpose="combine green arrow / red warning / yellow caution / icon / arrow direction with scene location",
        rule="symbol meaning candidate-only; no direct navigation/action/speech/fact_write",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="scene_relation_to_field_structure_alignment",
        rgb_side="scene_relation_candidate",
        slam_side="field_structure / semantic_place candidate",
        purpose="feed object/region/sign relations into field structure candidates",
        rule="scene relation is not final interpretation",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="tracking_to_motion_risk_alignment",
        rgb_side="track_evidence / dynamic_risk candidate",
        slam_side="motion / drift / health candidate",
        purpose="cross-judge dynamic objects vs self motion / localization health",
        rule="tracking is not action trigger",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="depth_vio_to_slam_pose_alignment",
        rgb_side="monocular_depth / VIO spatial_hint candidate",
        slam_side="pose / motion candidate",
        purpose="cross-validate local spatial hints with SLAM spatial evidence",
        rule="monocular depth / VIO / SLAM pose must not override field identity",
        supported=True,
    ),
    CrossModalEvidenceAlignmentPolicy(
        alignment_ref="uncertainty_conflict_alignment",
        rgb_side="low-confidence / OCR conflict / symbol ambiguity",
        slam_side="drift / relocalization / health / GPS mismatch",
        purpose="form uncertainty / conflict candidates",
        rule="conflict must not directly trigger action/speech/fact_write",
        supported=True,
    ),
)

# --------------------------------------------------------------------------- #
# Upstream sealed GO artifacts
# --------------------------------------------------------------------------- #
_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "phase_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1_smoke_v0/"
            "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_multi_export_spatial_evidence_replay_integrated_closure/"
            "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_types_v1.py"
        ),
        "verify_flag": "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
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
        "phase_ref": RGB_VISION_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1_smoke_v0/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_review_v1.json"
        ),
        "expected_go": "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_types_v1.py"
        ),
    },
    {
        "phase_ref": RGB_VISION_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1_smoke_v0/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun/"
            "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1.py"
        ),
    },
    {
        "phase_ref": ROBOFLOW_DATASET_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_v1_smoke_v0/"
            "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RGB_VISION_ROBOFLOW_DATASET_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun/"
            "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_types_v1.py"
        ),
    },
    {
        "phase_ref": VISION_TEST_SOURCE_BACKUP_POOL_REF,
        "artifact_rel": (
            "_tmp_eval_out/luna_vision_test_source_backup_pool_v1_smoke_v0/"
            "luna_vision_test_source_backup_pool_review_v1.json"
        ),
        "expected_go": "LUNA_VISION_TEST_SOURCE_BACKUP_POOL_GO",
        "module_rel": (
            "capabilities/field_understanding/luna_vision_test_source_backup_pool/"
            "luna_vision_test_source_backup_pool_types_v1.py"
        ),
    },
    {
        "phase_ref": VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF,
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_test_source_integrated_evidence_replay_dryrun_v1_smoke_v0/"
            "rgb_vision_test_source_integrated_evidence_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RGB_VISION_TEST_SOURCE_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rgb_vision_test_source_integrated_evidence_replay_dryrun/"
            "rgb_vision_test_source_integrated_evidence_replay_dryrun_types_v1.py"
        ),
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


def build_closure_profile_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        CrossModalEvidenceClosureProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            rgb_vision_evidence_chain_closure_ref=RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
            slam_backend_evidence_chain_closure_ref=SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
            rgb_interface_adapter_ref=RGB_INTERFACE_ADAPTER_REF,
            slam_interface_adapter_ref=SLAM_INTERFACE_ADAPTER_REF,
            vision_hardware_baseline=VISION_HARDWARE_BASELINE,
            slam_role=SLAM_ROLE,
            system_objective=SYSTEM_OBJECTIVE,
            target_entrypoint=TARGET_ENTRYPOINT,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            stage_refs=STAGE_REFS,
            alignment_policy_ids=ALIGNMENT_POLICY_IDS,
            cross_modal_candidate_ids=CROSS_MODAL_CANDIDATE_IDS,
            governance_rules=CLOSURE_GOVERNANCE_RULES,
        )
    )


def build_rgb_vision_coverage_ref_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionEvidenceCoverageRef(
            coverage_ref="cross_modal_rgb_vision_coverage_ref_v1",
            rgb_vision_coverage_ids=RGB_VISION_COVERAGE_IDS,
            rgb_vision_coverage_count=len(RGB_VISION_COVERAGE_IDS),
        )
    )


def build_slam_spatial_coverage_ref_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMSpatialEvidenceCoverageRef(
            coverage_ref="cross_modal_slam_spatial_coverage_ref_v1",
            slam_spatial_coverage_ids=SLAM_SPATIAL_COVERAGE_IDS,
            slam_spatial_coverage_count=len(SLAM_SPATIAL_COVERAGE_IDS),
        )
    )


def build_field_synthesis_path_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        CrossModalFieldSynthesisPathClosure(
            closure_ref="cross_modal_field_synthesis_path_closure_v1",
            rgb_evidence_adapter_required=True,
            slam_evidence_adapter_required=True,
            cross_modal_output_candidate_only=True,
            field_candidate_can_reference_cross_modal_evidence=True,
            field_candidate_cannot_write_fact=True,
        )
    )


def build_task_guidance_path_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        CrossModalTaskGuidancePathClosure(
            closure_ref="cross_modal_task_guidance_path_closure_v1",
            task_context_can_reference_object_text_region_symbol_anchor_field_structure=True,
            task_risk_can_reference_dynamic_risk_drift_health_conflict_uncertainty=True,
            field_task_guidance_candidate_only=True,
            guidance_candidate_remains_candidate=True,
            speech_gate_candidate_not_tts=True,
            action_safety_candidate_exists=True,
            observation_only_scope_preserved=True,
        )
    )


def build_conflict_uncertainty_policy_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        CrossModalConflictAndUncertaintyPolicy(
            policy_ref="cross_modal_conflict_and_uncertainty_policy_v1",
            ocr_symbol_mismatch_emits_conflict_candidate=True,
            object_segmentation_mismatch_emits_uncertainty_candidate=True,
            symbol_pose_mismatch_emits_spatial_consistency_or_conflict_candidate=True,
            relocalization_does_not_restore_runtime_trust=True,
            drift_only_increases_uncertainty=True,
            health_only_risk_evidence=True,
            gps_does_not_override_field_identity=True,
            conflict_not_direct_fact_write=True,
            conflict_not_direct_action_speech_navigation=True,
        )
    )


def build_safety_boundary_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        CrossModalSafetyBoundaryClosure(
            closure_ref="cross_modal_safety_boundary_closure_v1",
            rgb_first_hardware_baseline_preserved=(
                VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
            ),
            slam_role_spatial_evidence_provider=(SLAM_ROLE == "spatial_evidence_provider"),
            cognitive_world_reconstruction_objective_preserved=(
                SYSTEM_OBJECTIVE == "cognitive_world_reconstruction"
            ),
            object_identity_not_fact=True,
            ocr_text_not_fact=True,
            segmentation_not_route_activation=True,
            tracking_not_action_trigger=True,
            color_shape_symbol_not_fact=True,
            visual_symbol_requires_context_validation=True,
            monocular_depth_vio_slam_pose_not_field_identity=True,
            scene_relation_not_final_interpretation=True,
            scene_graph_not_final_field_identity=True,
            no_live_camera_sensor_gps_map_api_ros_imu=True,
            no_navigation_action_speech_fact_write=True,
        )
    )


def build_cross_modal_closure_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "closure_profile": build_closure_profile_v1(),
        "stage_refs": [candidate_to_dict(s) for s in _STAGES],
        "stage_ref_count": len(_STAGES),
        "rgb_vision_coverage_ref": build_rgb_vision_coverage_ref_v1(),
        "slam_spatial_coverage_ref": build_slam_spatial_coverage_ref_v1(),
        "alignment_policies": [candidate_to_dict(a) for a in _ALIGNMENT_POLICIES],
        "cross_modal_alignment_policy_count": len(_ALIGNMENT_POLICIES),
        "cross_modal_candidate_ids": list(CROSS_MODAL_CANDIDATE_IDS),
        "cross_modal_candidate_output_count": len(CROSS_MODAL_CANDIDATE_IDS),
        "field_synthesis_path_closure": build_field_synthesis_path_closure_v1(),
        "task_guidance_path_closure": build_task_guidance_path_closure_v1(),
        "conflict_uncertainty_policy": build_conflict_uncertainty_policy_v1(),
        "safety_boundary_closure": build_safety_boundary_closure_v1(),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_STAGES) != 5:
        issues.append("stage_ref_count_not_5")
    if len(_ALIGNMENT_POLICIES) < 8:
        issues.append("cross_modal_alignment_policy_count_lt_8")
    if len(CROSS_MODAL_CANDIDATE_IDS) < 13:
        issues.append("cross_modal_candidate_output_count_lt_13")

    seen_stage = set()
    for s in _STAGES:
        if s.stage_ref in seen_stage:
            issues.append(f"duplicate_stage_ref:{s.stage_ref}")
        seen_stage.add(s.stage_ref)
        if not s.expected_final_decision:
            issues.append(f"stage_missing_expected_decision:{s.stage_ref}")
        if not s.coverage:
            issues.append(f"stage_missing_coverage:{s.stage_ref}")
    for expected in STAGE_REFS:
        if expected not in seen_stage:
            issues.append(f"expected_stage_missing:{expected}")

    seen_align = set()
    for a in _ALIGNMENT_POLICIES:
        if a.alignment_ref in seen_align:
            issues.append(f"duplicate_alignment_ref:{a.alignment_ref}")
        seen_align.add(a.alignment_ref)
        if not a.supported:
            issues.append(f"alignment_not_supported:{a.alignment_ref}")
    for expected in ALIGNMENT_POLICY_IDS:
        if expected not in seen_align:
            issues.append(f"expected_alignment_missing:{expected}")

    return len(issues) == 0, issues
