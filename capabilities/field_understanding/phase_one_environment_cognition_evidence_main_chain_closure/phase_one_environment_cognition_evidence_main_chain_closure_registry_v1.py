# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Evidence Main Chain Closure — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_evidence_main_chain_closure.phase_one_environment_cognition_evidence_main_chain_closure_types_v1 import (
    CANDIDATE_LAYER_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEFERRED_EXPANSION_IDS,
    EVIDENCE_SOURCE_IDS,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    PHASE_ONE_SCOPE,
    RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
    RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
    SLAM_ROLE,
    STAGE_REFS,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    VISION_HARDWARE_BASELINE,
    CLOSURE_GOVERNANCE_RULES,
    PhaseOneCandidateLayerCoverageClosure,
    PhaseOneCrossModalPathClosure,
    PhaseOneDeferredExpansionRecord,
    PhaseOneEnvironmentCognitionEvidenceMainChainClosureProfile,
    PhaseOneEvidenceMainChainStageRef,
    PhaseOneEvidenceSourceCoverageClosure,
    PhaseOneFieldTaskGuidancePathClosure,
    PhaseOneGovernanceBoundaryClosure,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_evidence_main_chain_closure_registry_v1"
PROFILE_REF = "phase_one_environment_cognition_evidence_main_chain_closure_profile_v1"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
_STAGES: Tuple[PhaseOneEvidenceMainChainStageRef, ...] = (
    PhaseOneEvidenceMainChainStageRef(
        stage_ref="rgb_vision_evidence_chain_closure",
        phase_ref=RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF,
        expected_final_decision="RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        coverage=(
            "RGB-first vision / OCR / segmentation / tracking / visual symbol / "
            "test source evidence chain"
        ),
    ),
    PhaseOneEvidenceMainChainStageRef(
        stage_ref="slam_backend_evidence_chain_closure",
        phase_ref=SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF,
        expected_final_decision="SLAM_BACKEND_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        coverage="TUM / RTAB / multi-backend SLAM spatial evidence chain",
    ),
    PhaseOneEvidenceMainChainStageRef(
        stage_ref="rgb_vision_slam_cross_modal_closure",
        phase_ref=RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF,
        expected_final_decision=(
            "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO"
        ),
        coverage="RGB semantic evidence + SLAM spatial evidence unified candidate layer",
    ),
    PhaseOneEvidenceMainChainStageRef(
        stage_ref="field_task_guidance_safety_chain_closure",
        phase_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        expected_final_decision="FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        coverage="Field / Task / Guidance candidate-only safety path",
    ),
    PhaseOneEvidenceMainChainStageRef(
        stage_ref="runtime_governance_closure",
        phase_ref=GOVERNANCE_CLOSURE_REF,
        expected_final_decision=(
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        coverage="controlled runtime governance sealed",
    ),
    PhaseOneEvidenceMainChainStageRef(
        stage_ref="interface_and_model_admission_governance",
        phase_ref=f"{INTERFACE_LAYER_GOVERNANCE_REF} + {MODEL_ADMISSION_GOVERNANCE_REF}",
        expected_final_decision="INTERFACE_AND_MODEL_ADMISSION_GOVERNANCE_VERIFIED",
        coverage="external output admission / adapter governance / model output governance",
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
        "verify_flag": "rgb_vision_slam_cross_modal_closure_go_verified",
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


def build_closure_profile_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneEnvironmentCognitionEvidenceMainChainClosureProfile(
            profile_ref=PROFILE_REF,
            phase_id="Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
            phase_one_scope=PHASE_ONE_SCOPE,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            vision_hardware_baseline=VISION_HARDWARE_BASELINE,
            slam_role=SLAM_ROLE,
            system_objective=SYSTEM_OBJECTIVE,
            target_entrypoint=TARGET_ENTRYPOINT,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            stage_refs=STAGE_REFS,
            evidence_source_ids=EVIDENCE_SOURCE_IDS,
            candidate_layer_ids=CANDIDATE_LAYER_IDS,
            deferred_expansion_ids=DEFERRED_EXPANSION_IDS,
            governance_rules=CLOSURE_GOVERNANCE_RULES,
        )
    )


def build_evidence_source_coverage_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneEvidenceSourceCoverageClosure(
            closure_ref="phase_one_evidence_source_coverage_closure_v1",
            evidence_source_ids=EVIDENCE_SOURCE_IDS,
            evidence_source_coverage_count=len(EVIDENCE_SOURCE_IDS),
        )
    )


def build_candidate_layer_coverage_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneCandidateLayerCoverageClosure(
            closure_ref="phase_one_candidate_layer_coverage_closure_v1",
            candidate_layer_ids=CANDIDATE_LAYER_IDS,
            candidate_layer_coverage_count=len(CANDIDATE_LAYER_IDS),
        )
    )


def build_cross_modal_path_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneCrossModalPathClosure(
            closure_ref="phase_one_cross_modal_path_closure_v1",
            rgb_evidence_path_closed=True,
            slam_spatial_evidence_path_closed=True,
            rgb_slam_cross_modal_path_closed=True,
            generic_json_spatial_trace_parser_reused=True,
            interface_adapter_required=True,
            source_admission_required=True,
            source_chain_preserved=True,
            confidence_preserved=True,
            origin_metadata_preserved=True,
            spatial_evidence_candidate_bundle_path_closed=True,
            spatial_odometry_fusion_candidate_path_closed=True,
        )
    )


def build_field_task_guidance_path_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneFieldTaskGuidancePathClosure(
            closure_ref="phase_one_field_task_guidance_path_closure_v1",
            field_candidate_path_closed=True,
            task_candidate_path_closed=True,
            guidance_candidate_path_closed=True,
            guidance_candidate_remains_candidate=True,
            speech_gate_candidate_not_tts=True,
            action_safety_candidate_exists=True,
            observation_only_scope_preserved=True,
            all_evidence_candidate_only=True,
            field_task_guidance_candidate_only=True,
        )
    )


def build_governance_boundary_closure_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneGovernanceBoundaryClosure(
            closure_ref="phase_one_governance_boundary_closure_v1",
            rgb_first_hardware_baseline_preserved=(
                VISION_HARDWARE_BASELINE == "rgb_first_first_person_camera"
            ),
            slam_role_spatial_evidence_provider=(SLAM_ROLE == "spatial_evidence_provider"),
            cognitive_world_reconstruction_objective_preserved=(
                SYSTEM_OBJECTIVE == "cognitive_world_reconstruction"
            ),
            object_identity_not_fact=True,
            ocr_text_not_fact=True,
            color_shape_symbol_not_fact=True,
            visual_symbol_requires_context_validation=True,
            segmentation_not_route_activation=True,
            tracking_not_action_trigger=True,
            monocular_depth_vio_slam_pose_not_field_identity=True,
            relocalization_does_not_restore_runtime_trust=True,
            drift_remains_uncertainty_evidence=True,
            health_candidate_only=True,
            gps_does_not_override_field_identity=True,
            conflict_not_direct_fact_write=True,
            conflict_not_direct_action_speech_navigation=True,
        )
    )


def build_deferred_expansion_record_v1() -> Dict[str, Any]:
    return candidate_to_dict(
        PhaseOneDeferredExpansionRecord(
            record_ref="phase_one_deferred_expansion_record_v1",
            deferred_expansion_ids=DEFERRED_EXPANSION_IDS,
            future_information_source_expansion_deferred=True,
            latent_relation_mechanism_deferred=True,
            hidden_object_relation_mechanism_deferred=True,
            deferred_expansion_not_part_of_current_closure=True,
            current_closure_does_not_expand_new_sources=True,
        )
    )


def build_main_chain_closure_matrix_v1() -> Dict[str, Any]:
    return {
        "registry_id": REGISTRY_ID,
        "closure_profile": build_closure_profile_v1(),
        "stage_refs": [candidate_to_dict(s) for s in _STAGES],
        "stage_ref_count": len(_STAGES),
        "evidence_source_coverage_closure": build_evidence_source_coverage_closure_v1(),
        "candidate_layer_coverage_closure": build_candidate_layer_coverage_closure_v1(),
        "cross_modal_path_closure": build_cross_modal_path_closure_v1(),
        "field_task_guidance_path_closure": build_field_task_guidance_path_closure_v1(),
        "governance_boundary_closure": build_governance_boundary_closure_v1(),
        "deferred_expansion_record": build_deferred_expansion_record_v1(),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if len(_STAGES) < 6:
        issues.append("stage_ref_count_lt_6")
    if len(EVIDENCE_SOURCE_IDS) < 10:
        issues.append("evidence_source_coverage_count_lt_10")
    if len(CANDIDATE_LAYER_IDS) < 34:
        issues.append("candidate_layer_coverage_count_lt_34")
    if len(DEFERRED_EXPANSION_IDS) == 0:
        issues.append("deferred_expansion_record_empty")

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

    if len(set(EVIDENCE_SOURCE_IDS)) != len(EVIDENCE_SOURCE_IDS):
        issues.append("duplicate_evidence_source_id")
    if len(set(CANDIDATE_LAYER_IDS)) != len(CANDIDATE_LAYER_IDS):
        issues.append("duplicate_candidate_layer_id")

    return len(issues) == 0, issues
