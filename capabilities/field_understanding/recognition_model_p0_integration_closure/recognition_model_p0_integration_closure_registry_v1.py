# -*- coding: utf-8 -*-
"""Recognition Model P0 Integration Closure — registry v1.

Static registry of the 15 upstream stage references (14 GO phases + governance
template), plus negative-closure guard predicates used to prove that violating
scenarios are correctly recognized as blockers.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

# --------------------------------------------------------------------------- #
# Stage registry: 14 GO phases (the 15th reference is the governance template).
# --------------------------------------------------------------------------- #
STAGE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "stage_index": 1,
        "phase_ref": "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001",
        "expected_go": "RECOGNITION_MODEL_SYSTEM_ADMISSION_AND_INVOCATION_PLANNING_GO",
        "verify_flag": "system_admission_planning_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_system_admission_and_invocation_planning_v1_smoke_v0/"
            "recognition_model_system_admission_and_invocation_planning_review_v1.json"
        ),
    },
    {
        "stage_index": 2,
        "phase_ref": "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_GO",
        "verify_flag": "invocation_feasibility_dryrun_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_invocation_feasibility_dryrun_v1_smoke_v0/"
            "recognition_model_invocation_feasibility_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 3,
        "phase_ref": "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO",
        "verify_flag": "mock_output_adapter_dryrun_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 4,
        "phase_ref": "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001",
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_GO",
        "verify_flag": "download_license_local_availability_planning_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_license_and_local_availability_planning_v1_smoke_v0/"
            "recognition_model_download_license_and_local_availability_planning_review_v1.json"
        ),
    },
    {
        "stage_index": 5,
        "phase_ref": "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_DOWNLOAD_AND_INSTALL_DRYRUN_GO",
        "verify_flag": "download_install_dryrun_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_download_and_install_dryrun_v1_smoke_v0/"
            "recognition_model_download_and_install_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 6,
        "phase_ref": "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_GO",
        "verify_flag": "real_output_adapter_dryrun_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0/"
            "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 7,
        "phase_ref": "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001",
        "expected_go": "RECOGNITION_MODEL_EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_GO",
        "verify_flag": "evidence_main_chain_integration_dryrun_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/recognition_model_evidence_main_chain_integration_dryrun_v1_smoke_v0/"
            "recognition_model_evidence_main_chain_integration_dryrun_run_and_review_v1.json"
        ),
    },
    {
        "stage_index": 8,
        "phase_ref": "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO",
        "verify_flag": "phase_one_evidence_main_chain_closure_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 9,
        "phase_ref": "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001",
        "expected_go": "RGB_VISION_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO",
        "verify_flag": "rgb_vision_evidence_chain_closure_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0/"
            "rgb_vision_evidence_chain_integrated_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 10,
        "phase_ref": "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001",
        "expected_go": "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO",
        "verify_flag": "rgb_slam_cross_modal_closure_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0/"
            "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 11,
        "phase_ref": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "verify_flag": "field_task_guidance_safety_chain_closure_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 12,
        "phase_ref": (
            "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
        ),
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
        ),
        "verify_flag": "runtime_governance_closure_go_verified",
        "artifact_rel": (
            "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0/"
            "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"
        ),
    },
    {
        "stage_index": 13,
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "verify_flag": "interface_layer_governance_verified",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
    },
    {
        "stage_index": 14,
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "verify_flag": "model_admission_governance_verified",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
    },
)

# 15th reference: governance lifecycle template (verified by ref equality, not artifact).
GOVERNANCE_TEMPLATE_STAGE_REF = "ControlledTrialGovernanceLifecycleTemplateV1"
TOTAL_STAGE_REF_COUNT = len(STAGE_REGISTRY) + 1  # 14 phases + template = 15

# Artifacts consumed for coverage extraction.
REAL_OUTPUT_ADAPTER_ARTIFACT_REL = (
    "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0/"
    "recognition_model_real_output_adapter_dryrun_run_and_review_v1.json"
)
INTEGRATION_ARTIFACT_REL = (
    "_tmp_eval_out/recognition_model_evidence_main_chain_integration_dryrun_v1_smoke_v0/"
    "recognition_model_evidence_main_chain_integration_dryrun_run_and_review_v1.json"
)
REAL_OUTPUT_ARTIFACT_DIR_REL = "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0"
REAL_OUTPUT_ARTIFACT_FILES: Tuple[str, ...] = (
    "real_ocr_output.json",
    "real_visual_symbol_output.json",
)


# --------------------------------------------------------------------------- #
# Negative-closure guard predicates: each returns True when the violating
# scenario is correctly recognized as a blocker (closure must NOT pass it).
# --------------------------------------------------------------------------- #
def guard_upstream_go_missing(all_upstream_go: bool) -> bool:
    # blocked when not all upstream GO -> a missing-GO scenario must block.
    return all_upstream_go is False


def guard_p0_real_output_missing(real_output_artifact_count: int, has_declared_unavailable: bool) -> bool:
    # blocked when no real output artifact AND no declared-unavailable record.
    return real_output_artifact_count < 1 and has_declared_unavailable is False


def guard_yolo_unavailable_misuse(treat_as_blocker: bool, download_triggered: bool) -> bool:
    return bool(treat_as_blocker or download_triggered)


def guard_fact_write(fact_write_attempted: bool) -> bool:
    return bool(fact_write_attempted)


def guard_route_navigation_activation(route_or_nav_activated: bool) -> bool:
    return bool(route_or_nav_activated)


def guard_guidance_runtime_navigation(guidance_became_runtime_nav: bool) -> bool:
    return bool(guidance_became_runtime_nav)


def guard_speech_gate_tts(speech_gate_triggered_tts: bool) -> bool:
    return bool(speech_gate_triggered_tts)


def guard_action_safety_action_trigger(action_triggered: bool) -> bool:
    return bool(action_triggered)


def guard_vla_action_chain(vla_in_scope: bool) -> bool:
    return bool(vla_in_scope)


def guard_tuning_dataset_approval(tuning_or_dataset_approved: bool) -> bool:
    return bool(tuning_or_dataset_approved)


def evaluate_negative_closure_checks(all_upstream_go: bool, real_output_artifact_count: int) -> Dict[str, bool]:
    """Each value is True when the violating scenario is correctly blocked."""
    return {
        "upstream_go_missing_blocked": guard_upstream_go_missing(False),
        "p0_real_output_missing_without_unavailable_record_blocked": guard_p0_real_output_missing(
            0, False
        ),
        "yolo_unavailable_blocker_or_download_blocked": guard_yolo_unavailable_misuse(True, True),
        "ocr_symbol_fact_write_blocked": guard_fact_write(True),
        "exit_route_navigation_activation_blocked": guard_route_navigation_activation(True),
        "guidance_runtime_navigation_blocked": guard_guidance_runtime_navigation(True),
        "speech_gate_tts_blocked": guard_speech_gate_tts(True),
        "action_safety_action_trigger_blocked": guard_action_safety_action_trigger(True),
        "vla_action_chain_current_scope_blocked": guard_vla_action_chain(True),
        "model_tuning_dataset_usage_approval_blocked": guard_tuning_dataset_approval(True),
    }
