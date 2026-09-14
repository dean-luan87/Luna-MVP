# -*- coding: utf-8 -*-
"""SLAM Backend Evidence Chain Integrated Closure — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.slam_backend_evidence_chain_integrated_closure.slam_backend_evidence_chain_integrated_closure_types_v1 import (
    ADMISSION_PLANNING_REF,
    CANDIDATE_TYPE_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GENERIC_JSON_PARSER_PHASE_REF,
    GENERIC_JSON_PARSER_REF,
    GENERIC_TUM_DRYRUN_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_REF,
    SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
    SOURCE_FAMILY,
    SOURCE_FAMILY_IDS,
    STAGE_REFS,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    CLOSURE_GOVERNANCE_RULES,
    SLAMBackendCandidateTypeCoverageClosure,
    SLAMBackendEvidenceChainClosureProfile,
    SLAMBackendEvidenceChainStageRef,
    SLAMBackendLicenseBoundaryClosure,
    SLAMBackendReplayPathClosure,
    SLAMBackendSafetyBoundaryClosure,
    SLAMBackendSourceFamilyCoverageClosure,
    candidate_to_dict,
)

REGISTRY_ID = "slam_backend_evidence_chain_integrated_closure_registry_v1"
PROFILE_REF = "slam_backend_evidence_chain_integrated_closure_profile_v1"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
_STAGES: Tuple[SLAMBackendEvidenceChainStageRef, ...] = (
    SLAMBackendEvidenceChainStageRef(
        stage_ref="generic_tum_real_file_loader",
        phase_ref=GENERIC_TUM_DRYRUN_REF,
        expected_final_decision="GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO",
        coverage=("pose", "motion"),
    ),
    SLAMBackendEvidenceChainStageRef(
        stage_ref="rtab_real_file_loader_integrated",
        phase_ref=RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
        expected_final_decision="RTAB_MAP_REAL_FILE_LOADER_INTEGRATED_DRYRUN_GO",
        coverage=("pose", "motion", "health", "anchor", "relocalization", "drift"),
    ),
    SLAMBackendEvidenceChainStageRef(
        stage_ref="rtab_multi_export_spatial_evidence_replay",
        phase_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
        expected_final_decision=(
            "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_GO"
        ),
        coverage=(
            "spatial_evidence_candidate_bundle",
            "spatial_odometry_fusion_candidate",
            "field_task_guidance_replay_path",
        ),
    ),
    SLAMBackendEvidenceChainStageRef(
        stage_ref="slam_backend_admission_planning",
        phase_ref=ADMISSION_PLANNING_REF,
        expected_final_decision="SLAM_BACKEND_REAL_FILE_OUTPUT_INTEGRATED_ADMISSION_PLANNING_GO",
        coverage=(
            "multi_backend_admission",
            "license_boundary",
            "candidate_mapping",
            "replay_boundary",
        ),
    ),
    SLAMBackendEvidenceChainStageRef(
        stage_ref="slam_backend_integrated_output_replay_dryrun",
        phase_ref=SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_REF,
        expected_final_decision="SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_GO",
        coverage=(
            "openvins_like_output",
            "orb_slam3_like_output",
            "kimera_like_output",
            "hydra_like_output",
            "neural_gaussian_like_output",
        ),
    ),
)

# --------------------------------------------------------------------------- #
# Upstream sealed GO artifacts
# --------------------------------------------------------------------------- #
_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": GENERIC_TUM_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_tum_real_file_loader_dryrun_v1_smoke_v0/"
            "generic_tum_real_file_loader_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_real_file_loader_dryrun/"
            "generic_tum_real_file_loader_dryrun_types_v1.py"
        ),
        "verify_flag": "tum_real_file_loader_dryrun_go_verified",
    },
    {
        "phase_ref": RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_real_file_loader_integrated_dryrun_v1_smoke_v0/"
            "rtab_map_real_file_loader_integrated_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_REAL_FILE_LOADER_INTEGRATED_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_real_file_loader_integrated_dryrun/"
            "rtab_map_real_file_loader_integrated_dryrun_types_v1.py"
        ),
        "verify_flag": "rtab_real_file_loader_integrated_dryrun_go_verified",
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
        "phase_ref": ADMISSION_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_backend_real_file_output_integrated_admission_planning_v1_smoke_v0/"
            "slam_backend_real_file_output_integrated_admission_planning_review_v1.json"
        ),
        "expected_go": "SLAM_BACKEND_REAL_FILE_OUTPUT_INTEGRATED_ADMISSION_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_backend_real_file_output_integrated_admission_planning/"
            "slam_backend_real_file_output_integrated_admission_planning_types_v1.py"
        ),
        "verify_flag": "slam_backend_admission_planning_go_verified",
    },
    {
        "phase_ref": SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_backend_integrated_output_replay_dryrun_v1_smoke_v0/"
            "slam_backend_integrated_output_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_backend_integrated_output_replay_dryrun/"
            "slam_backend_integrated_output_replay_dryrun_types_v1.py"
        ),
        "verify_flag": "slam_backend_integrated_output_replay_dryrun_go_verified",
    },
    {
        "phase_ref": GENERIC_JSON_PARSER_PHASE_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_json_spatial_trace_parser_v1_smoke_v0/"
            "generic_json_spatial_trace_parser_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_parser/"
            "generic_json_spatial_trace_parser_types_v1.py"
        ),
        "verify_flag": "generic_json_spatial_trace_parser_go_verified",
    },
    {
        "phase_ref": SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
            "slam_spatial_evidence_chain_closure_review_v1.json"
        ),
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
            "slam_spatial_evidence_chain_closure_types_v1.py"
        ),
        "verify_flag": "slam_spatial_evidence_chain_field_alignment_closure_go_verified",
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
        SLAMBackendEvidenceChainClosureProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001",
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            slam_backend_integrated_output_replay_dryrun_ref=(
                SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_REF
            ),
            admission_planning_ref=ADMISSION_PLANNING_REF,
            generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            source_family=SOURCE_FAMILY,
            target_internal_format=TARGET_INTERNAL_FORMAT,
            target_entrypoint=TARGET_ENTRYPOINT,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            stage_refs=STAGE_REFS,
            source_family_ids=SOURCE_FAMILY_IDS,
            candidate_type_ids=CANDIDATE_TYPE_IDS,
            governance_rules=CLOSURE_GOVERNANCE_RULES,
        )
    )


def build_source_family_coverage_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendSourceFamilyCoverageClosure(
            closure_ref="slam_backend_source_family_coverage_closure_v1",
            source_family_ids=SOURCE_FAMILY_IDS,
            source_family_coverage_count=len(SOURCE_FAMILY_IDS),
            all_source_families_covered=len(SOURCE_FAMILY_IDS) >= 7,
        )
    )


def build_candidate_type_coverage_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendCandidateTypeCoverageClosure(
            closure_ref="slam_backend_candidate_type_coverage_closure_v1",
            candidate_type_ids=CANDIDATE_TYPE_IDS,
            candidate_type_coverage_count=len(CANDIDATE_TYPE_IDS),
            all_candidate_types_covered=len(CANDIDATE_TYPE_IDS) >= 12,
        )
    )


def build_replay_path_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendReplayPathClosure(
            closure_ref="slam_backend_replay_path_closure_v1",
            generic_json_parser_reused=True,
            spatial_evidence_candidate_bundle_path_closed=True,
            spatial_odometry_fusion_candidate_path_closed=True,
            field_candidate_path_closed=True,
            task_candidate_path_closed=True,
            guidance_candidate_path_closed=True,
            speech_gate_candidate_not_tts=True,
            action_safety_candidate_exists=True,
        )
    )


def build_safety_boundary_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendSafetyBoundaryClosure(
            closure_ref="slam_backend_safety_boundary_closure_v1",
            vio_slam_pose_not_field_identity=True,
            gps_does_not_override_field_identity=True,
            relocalization_does_not_restore_runtime_trust=True,
            drift_remains_uncertainty_evidence=True,
            health_candidate_only=True,
            semantic_label_not_fact=True,
            scene_graph_not_final_field_identity=True,
            backend_native_output_direct_to_field_blocked=True,
            no_live_sensor_ros_camera_imu_gps_map_api=True,
            no_navigation_action_speech_fact_write=True,
        )
    )


def build_license_boundary_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        SLAMBackendLicenseBoundaryClosure(
            closure_ref="slam_backend_license_boundary_closure_v1",
            no_slam_model_download=True,
            no_repo_clone=True,
            no_runtime_build=True,
            gpl_or_incompatible_backend_technical_reference_only=True,
            commercial_runtime_approved=False,
            heavy_neural_gaussian_runtime_not_admitted=True,
        )
    )


def build_slam_backend_evidence_chain_closure_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "closure_profile": build_closure_profile_v1(),
        "stage_refs": [candidate_to_dict(s) for s in _STAGES],
        "stage_ref_count": len(_STAGES),
        "source_family_coverage_closure": build_source_family_coverage_closure_v1(),
        "candidate_type_coverage_closure": build_candidate_type_coverage_closure_v1(),
        "replay_path_closure": build_replay_path_closure_v1(),
        "safety_boundary_closure": build_safety_boundary_closure_v1(),
        "license_boundary_closure": build_license_boundary_closure_v1(),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_STAGES) != 5:
        issues.append("stage_ref_count_not_5")
    if len(SOURCE_FAMILY_IDS) < 7:
        issues.append("source_family_coverage_count_lt_7")
    if len(CANDIDATE_TYPE_IDS) < 12:
        issues.append("candidate_type_coverage_count_lt_12")

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
