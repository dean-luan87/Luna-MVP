# -*- coding: utf-8 -*-
"""RGB Vision Evidence Chain Integrated Closure — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rgb_vision_evidence_chain_integrated_closure.rgb_vision_evidence_chain_integrated_closure_types_v1 import (
    CANDIDATE_TYPE_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPTH_HARDWARE_DEFAULT,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    RGB_VISION_DRYRUN_REF,
    RGB_VISION_PLANNING_REF,
    ROBOFLOW_DATASET_DRYRUN_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
    SOURCE_COVERAGE_IDS,
    STAGE_REFS,
    SYMBOL_MEANING_MAPPINGS,
    SYMBOL_MEANING_REFS,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TOF_STEREO_DEPTH_ROLE,
    VISION_HARDWARE_BASELINE,
    VISION_TEST_SOURCE_BACKUP_POOL_REF,
    VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF,
    CLOSURE_GOVERNANCE_RULES,
    RGBVisionCandidateTypeCoverageClosure,
    RGBVisionDatasetTestSourceClosure,
    RGBVisionEvidenceChainClosureProfile,
    RGBVisionEvidenceChainStageRef,
    RGBVisionReplayPathClosure,
    RGBVisionSafetyBoundaryClosure,
    RGBVisionSourceCoverageClosure,
    RGBVisionVisualSymbolEvidenceExtensionClosure,
    candidate_to_dict,
)

REGISTRY_ID = "rgb_vision_evidence_chain_integrated_closure_registry_v1"
PROFILE_REF = "rgb_vision_evidence_chain_integrated_closure_profile_v1"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
_STAGES: Tuple[RGBVisionEvidenceChainStageRef, ...] = (
    RGBVisionEvidenceChainStageRef(
        stage_ref="rgb_vision_integrated_planning",
        phase_ref=RGB_VISION_PLANNING_REF,
        expected_final_decision="RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_PLANNING_GO",
        coverage=(
            "rgb_first_hardware_baseline",
            "source_policies",
            "replay_scenario_planning",
        ),
    ),
    RGBVisionEvidenceChainStageRef(
        stage_ref="rgb_vision_integrated_dryrun",
        phase_ref=RGB_VISION_DRYRUN_REF,
        expected_final_decision="RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        coverage=(
            "scene", "object", "region", "track", "dynamic_risk", "text",
            "spatial_hint", "scene_relation",
        ),
    ),
    RGBVisionEvidenceChainStageRef(
        stage_ref="roboflow_dataset_integrated_dryrun",
        phase_ref=ROBOFLOW_DATASET_DRYRUN_REF,
        expected_final_decision="RGB_VISION_ROBOFLOW_DATASET_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        coverage=("roboflow_as_external_rgb_vision_test_source",),
    ),
    RGBVisionEvidenceChainStageRef(
        stage_ref="vision_test_source_backup_pool",
        phase_ref=VISION_TEST_SOURCE_BACKUP_POOL_REF,
        expected_final_decision="LUNA_VISION_TEST_SOURCE_BACKUP_POOL_GO",
        coverage=("14_registered_test_sources", "license_source_admission"),
    ),
    RGBVisionEvidenceChainStageRef(
        stage_ref="vision_test_source_integrated_replay",
        phase_ref=VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF,
        expected_final_decision="RGB_VISION_TEST_SOURCE_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO",
        coverage=("roboflow", "coco", "ade20k", "textocr", "visual_genome"),
    ),
)

# --------------------------------------------------------------------------- #
# Upstream sealed GO artifacts
# --------------------------------------------------------------------------- #
_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "verify_flag": "rgb_vision_integrated_planning_go_verified",
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
        "verify_flag": "rgb_vision_integrated_dryrun_go_verified",
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
        "verify_flag": "roboflow_dataset_integrated_dryrun_go_verified",
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
        "verify_flag": "vision_test_source_backup_pool_go_verified",
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
        "verify_flag": "vision_test_source_integrated_replay_go_verified",
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
        RGBVisionEvidenceChainClosureProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            vision_test_source_integrated_replay_ref=VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF,
            vision_test_source_backup_pool_ref=VISION_TEST_SOURCE_BACKUP_POOL_REF,
            slam_backend_evidence_chain_closure_ref=SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            vision_hardware_baseline=VISION_HARDWARE_BASELINE,
            system_objective=SYSTEM_OBJECTIVE,
            depth_hardware_default=DEPTH_HARDWARE_DEFAULT,
            tof_stereo_depth_role=TOF_STEREO_DEPTH_ROLE,
            target_entrypoint=TARGET_ENTRYPOINT,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            stage_refs=STAGE_REFS,
            source_coverage_ids=SOURCE_COVERAGE_IDS,
            candidate_type_ids=CANDIDATE_TYPE_IDS,
            governance_rules=CLOSURE_GOVERNANCE_RULES,
        )
    )


def build_source_coverage_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionSourceCoverageClosure(
            closure_ref="rgb_vision_source_coverage_closure_v1",
            source_coverage_ids=SOURCE_COVERAGE_IDS,
            source_coverage_count=len(SOURCE_COVERAGE_IDS),
            all_sources_covered=len(SOURCE_COVERAGE_IDS) >= 13,
        )
    )


def build_candidate_type_coverage_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionCandidateTypeCoverageClosure(
            closure_ref="rgb_vision_candidate_type_coverage_closure_v1",
            candidate_type_ids=CANDIDATE_TYPE_IDS,
            candidate_type_coverage_count=len(CANDIDATE_TYPE_IDS),
            all_candidate_types_covered=len(CANDIDATE_TYPE_IDS) >= 11,
        )
    )


def build_dataset_test_source_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionDatasetTestSourceClosure(
            closure_ref="rgb_vision_dataset_test_source_closure_v1",
            backup_pool_not_training_admission=True,
            backup_pool_not_runtime_admission=True,
            dataset_download_allowed=False,
            training_use_allowed=False,
            license_ref_required_for_all=True,
            dataset_ref_required_for_all=True,
            annotation_origin_required_for_all=True,
            sample_origin_required_for_all=True,
            roboflow_license_per_dataset_required=True,
            commercial_use_unknown_until_verified=True,
            non_commercial_sources_research_test_only=True,
            dataset_label_not_fact=True,
            annotation_as_evidence_candidate=True,
        )
    )


def build_replay_path_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionReplayPathClosure(
            closure_ref="rgb_vision_replay_path_closure_v1",
            adapter_mapping_required=True,
            source_admission_required=True,
            source_chain_preserved=True,
            confidence_preserved=True,
            origin_metadata_preserved=True,
            field_candidate_path_closed=True,
            task_candidate_path_closed=True,
            guidance_candidate_path_closed=True,
            guidance_candidate_remains_candidate=True,
            speech_gate_candidate_not_tts=True,
            action_safety_candidate_exists=True,
            observation_only_scope_preserved=True,
        )
    )


def build_safety_boundary_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionSafetyBoundaryClosure(
            closure_ref="rgb_vision_safety_boundary_closure_v1",
            rgb_first_hardware_baseline_preserved=(
                VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
            ),
            tof_stereo_depth_optional_auxiliary_only=(
                TOF_STEREO_DEPTH_ROLE == "optional_auxiliary_only"
            ),
            cognitive_world_reconstruction_objective_preserved=(
                SYSTEM_OBJECTIVE == "cognitive_world_reconstruction"
            ),
            ocr_output_not_fact=True,
            segmentation_output_not_route_activation=True,
            tracking_output_not_action_trigger=True,
            monocular_depth_vio_not_field_identity=True,
            scene_relation_not_final_interpretation=True,
            native_output_direct_to_field_blocked=True,
            no_live_camera_sensor_gps_map_api_ros=True,
            no_navigation_action_speech_fact_write=True,
        )
    )


def build_visual_symbol_evidence_extension_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        RGBVisionVisualSymbolEvidenceExtensionClosure(
            closure_ref="rgb_vision_visual_symbol_evidence_extension_closure_v1",
            color_evidence_candidate_covered=True,
            shape_evidence_candidate_covered=True,
            visual_symbol_candidate_covered=True,
            symbol_meaning_candidate_candidate_only=True,
            color_shape_symbol_not_fact=True,
            visual_symbol_not_direct_navigation=True,
            visual_symbol_not_direct_speech=True,
            visual_symbol_not_direct_fact_write=True,
            visual_symbol_requires_context_validation=True,
            symbol_meaning_refs=SYMBOL_MEANING_REFS,
            symbol_meaning_mappings=SYMBOL_MEANING_MAPPINGS,
        )
    )


def build_rgb_vision_evidence_chain_closure_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "closure_profile": build_closure_profile_v1(),
        "stage_refs": [candidate_to_dict(s) for s in _STAGES],
        "stage_ref_count": len(_STAGES),
        "source_coverage_closure": build_source_coverage_closure_v1(),
        "candidate_type_coverage_closure": build_candidate_type_coverage_closure_v1(),
        "dataset_test_source_closure": build_dataset_test_source_closure_v1(),
        "replay_path_closure": build_replay_path_closure_v1(),
        "safety_boundary_closure": build_safety_boundary_closure_v1(),
        "visual_symbol_evidence_extension_closure": (
            build_visual_symbol_evidence_extension_closure_v1()
        ),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_STAGES) != 5:
        issues.append("stage_ref_count_not_5")
    if len(SOURCE_COVERAGE_IDS) < 13:
        issues.append("source_coverage_count_lt_13")
    if len(CANDIDATE_TYPE_IDS) < 11:
        issues.append("candidate_type_coverage_count_lt_11")
    for required_candidate in (
        "color_evidence_candidate",
        "shape_evidence_candidate",
        "visual_symbol_candidate",
    ):
        if required_candidate not in CANDIDATE_TYPE_IDS:
            issues.append(f"visual_symbol_extension_candidate_missing:{required_candidate}")
    if len(SYMBOL_MEANING_REFS) < 5:
        issues.append("symbol_meaning_mapping_count_lt_5")

    seen = set()
    for s in _STAGES:
        if s.stage_ref in seen:
            issues.append(f"duplicate_stage_ref:{s.stage_ref}")
        seen.add(s.stage_ref)
        if not s.expected_final_decision:
            issues.append(f"stage_missing_expected_decision:{s.stage_ref}")
        if not s.coverage:
            issues.append(f"stage_missing_coverage:{s.stage_ref}")

    for expected in STAGE_REFS:
        if expected not in seen:
            issues.append(f"expected_stage_missing:{expected}")

    return len(issues) == 0, issues
