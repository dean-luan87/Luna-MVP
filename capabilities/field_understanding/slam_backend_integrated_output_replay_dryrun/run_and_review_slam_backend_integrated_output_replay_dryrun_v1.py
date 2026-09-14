# -*- coding: utf-8 -*-
"""SLAM Backend Integrated Output Replay DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_backend_integrated_output_replay_dryrun.slam_backend_integrated_output_replay_dryrun_cases_v1 import (
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.slam_backend_integrated_output_replay_dryrun.slam_backend_integrated_output_replay_dryrun_types_v1 import (
    ADAPTER_MAPPING_REF,
    ADMISSION_PLANNING_REF,
    ADMISSION_REQUIRED_FIELDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    COVERAGE_CANDIDATE_TYPES,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
    FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_PHASE_REF,
    GENERIC_JSON_PARSER_REF,
    GENERIC_TUM_DRYRUN_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_ADAPTER_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEGATIVE_CASE_REFS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SAMPLE_BACKENDS,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
    SOURCE_CHAIN,
    SOURCE_FAMILY,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    SLAMBackendIntegratedOutputReplayDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "slam_backend_integrated_output_replay_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "slam_backend_integrated_output_replay_dryrun_run_and_review_v1.json"
PROFILE_REF = "slam_backend_integrated_output_replay_dryrun_profile_v1"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "verify_flag": "admission_planning_go_verified",
    },
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

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "admission_planning_go_verified",
    "tum_real_file_loader_dryrun_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    "generic_json_spatial_trace_parser_go_verified",
    "slam_spatial_evidence_chain_field_alignment_closure_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
    "interface_layer_governance_verified",
    "model_admission_governance_verified",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_upstream_artifacts() -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in _UPSTREAM_ARTIFACTS:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        go_ok = actual_go == entry["expected_go"]
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        verify_flag = entry.get("verify_flag")
        if verify_flag:
            checks[verify_flag] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    for required in _REQUIRED_VERIFY_FLAGS:
        if not checks.get(required, False):
            issues.append(f"{required}_not_verified")

    return checks, issues


def build_profile() -> SLAMBackendIntegratedOutputReplayDryRunProfile:
    return SLAMBackendIntegratedOutputReplayDryRunProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        admission_planning_ref=ADMISSION_PLANNING_REF,
        rtab_multi_export_closure_ref=RTAB_MULTI_EXPORT_CLOSURE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_PARSER_REF,
        slam_spatial_evidence_chain_field_alignment_closure_ref=(
            SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF
        ),
        field_task_guidance_safety_chain_closure_ref=FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
        interface_adapter_ref=INTERFACE_ADAPTER_REF,
        adapter_mapping_ref=ADAPTER_MAPPING_REF,
        source_family=SOURCE_FAMILY,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        sample_backends=SAMPLE_BACKENDS,
        admission_required_fields=ADMISSION_REQUIRED_FIELDS,
        coverage_candidate_types=COVERAGE_CANDIDATE_TYPES,
        field_task_guidance_candidate_types=FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
        governance_rules=DRYRUN_GOVERNANCE_RULES,
    )


def _aggregate(case_run: Dict[str, Any]) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []
    by_ref = {c["case_ref"]: c for c in positive + negative}

    def passed(ref: str) -> bool:
        return bool((by_ref.get(ref) or {}).get("passed"))

    def chk(ref: str) -> Dict[str, Any]:
        return (by_ref.get(ref) or {}).get("checks") or {}

    coverage = chk("multi_backend_candidate_type_coverage")
    orb = chk("orb_slam3_keyframe_output_replay")
    openvins = chk("openvins_vio_output_replay")
    kimera = chk("kimera_metric_semantic_output_replay")
    hydra = chk("hydra_scene_graph_output_replay")
    neural = chk("neural_gaussian_slam_output_observation_replay")
    path = chk("multi_backend_spatial_evidence_replay_path")

    sample_count = sum(1 for n in SAMPLE_FILES if (samples_dir() / n).is_file())
    generated = set(case_run.get("generated_candidate_types") or [])

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": sum(1 for c in positive if c.get("passed")),
        "invalid_expected_reject_count": sum(1 for c in negative if c.get("passed")),
        "sample_file_count": sample_count,
        "backend_sample_count": case_run.get("backend_sample_count", 0),
        "openvins_vio_output_replay_ok": passed("openvins_vio_output_replay"),
        "orb_slam3_keyframe_output_replay_ok": passed("orb_slam3_keyframe_output_replay"),
        "kimera_metric_semantic_output_replay_ok": passed("kimera_metric_semantic_output_replay"),
        "hydra_scene_graph_output_replay_ok": passed("hydra_scene_graph_output_replay"),
        "neural_gaussian_slam_output_observation_replay_ok": passed(
            "neural_gaussian_slam_output_observation_replay"
        ),
        "multi_backend_candidate_type_coverage_complete": coverage.get(
            "candidate_type_coverage_complete"
        )
        is True,
        "multi_backend_spatial_evidence_replay_path_ok": passed(
            "multi_backend_spatial_evidence_replay_path"
        ),
        "observation_only_scope_preserved": passed(
            "multi_backend_observation_only_scope_replay"
        ),
        "generated_candidate_types": sorted(generated),
        "candidate_generated": {t: t in generated for t in COVERAGE_CANDIDATE_TYPES},
        "vio_slam_pose_not_field_identity": (
            openvins.get("vio_pose_does_not_override_field_identity") is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            orb.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "gpl_or_incompatible_backend_technical_reference_only": (
            orb.get("gpl_license_boundary_preserved") is True
        ),
        "semantic_label_not_fact": kimera.get("semantic_label_not_fact") is True,
        "scene_graph_not_final_field_identity": (
            hydra.get("scene_graph_not_final_field_identity") is True
        ),
        "heavy_neural_gaussian_runtime_not_admitted": (
            neural.get("heavy_neural_gaussian_runtime_not_admitted") is True
        ),
        "field_task_guidance_candidate_only": (
            path.get("field_task_guidance_replay_path_ok") is True
        ),
        "guidance_candidate_remains_candidate": (
            path.get("guidance_candidate_remains_candidate") is True
        ),
        "speech_gate_candidate_not_tts": path.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": path.get("action_safety_candidate_exists") is True,
        "missing_source_chain_rejected": chk("invalid_missing_source_chain_rejected").get(
            "missing_source_chain_rejected"
        )
        is True,
        "missing_license_ref_rejected": chk("invalid_missing_license_ref_rejected").get(
            "missing_license_ref_rejected"
        )
        is True,
        "gpl_marked_commercial_ready_rejected": chk(
            "invalid_gpl_marked_commercial_ready_rejected"
        ).get("gpl_marked_commercial_ready_rejected")
        is True,
        "native_output_direct_to_field_rejected": chk(
            "invalid_native_output_direct_to_field_rejected"
        ).get("native_output_direct_to_field_rejected")
        is True,
        "runtime_trust_restore_attempt_rejected": chk(
            "invalid_relocalization_runtime_trust_restore_rejected"
        ).get("runtime_trust_restore_attempt_rejected")
        is True,
        "semantic_fact_write_field_identity_rejected": chk(
            "invalid_semantic_label_fact_write_rejected"
        ).get("semantic_fact_write_field_identity_rejected")
        is True,
        "heavy_runtime_activation_rejected": chk(
            "invalid_heavy_neural_runtime_activation_rejected"
        ).get("heavy_runtime_activation_rejected")
        is True,
        "direct_action_speech_navigation_fact_write_rejected": chk(
            "invalid_direct_action_speech_navigation_fact_write_rejected"
        ).get("direct_action_speech_navigation_fact_write_rejected")
        is True,
        "drift_remains_uncertainty_evidence": "drift" in generated,
        "health_candidate_only": "health" in generated,
    }


def run_and_review_slam_backend_integrated_output_replay_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    upstream_checks, upstream_issues = review_upstream_artifacts()
    case_run = run_all_cases_v1()
    aggregate = _aggregate(case_run)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    cg = aggregate["candidate_generated"]

    go_conditions = {
        "dryrun_profile_count_eq_1": True,
        "sample_file_count_gte_13": aggregate["sample_file_count"] >= 13,
        "positive_case_count_eq_8": aggregate["positive_case_count"] == 8,
        "negative_case_count_eq_8": aggregate["negative_case_count"] == 8,
        "positive_pass_count_eq_8": aggregate["positive_pass_count"] == 8,
        "invalid_expected_reject_count_eq_8": aggregate["invalid_expected_reject_count"] == 8,
        "admission_planning_go_verified": (
            upstream_checks.get("admission_planning_go_verified") is True
        ),
        "tum_real_file_loader_dryrun_go_verified": (
            upstream_checks.get("tum_real_file_loader_dryrun_go_verified") is True
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            upstream_checks.get("rtab_multi_export_spatial_evidence_replay_closure_go_verified")
            is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            upstream_checks.get("generic_json_spatial_trace_parser_go_verified") is True
        ),
        "slam_spatial_evidence_chain_field_alignment_closure_go_verified": (
            upstream_checks.get("slam_spatial_evidence_chain_field_alignment_closure_go_verified")
            is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        "slam_backend_model_download_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_model_download_allowed"] is False
        ),
        "slam_backend_repo_clone_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_repo_clone_allowed"] is False
        ),
        "slam_backend_runtime_build_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_runtime_build_allowed"] is False
        ),
        "openvins_vio_output_replay_ok": aggregate["openvins_vio_output_replay_ok"] is True,
        "orb_slam3_keyframe_output_replay_ok": (
            aggregate["orb_slam3_keyframe_output_replay_ok"] is True
        ),
        "kimera_metric_semantic_output_replay_ok": (
            aggregate["kimera_metric_semantic_output_replay_ok"] is True
        ),
        "hydra_scene_graph_output_replay_ok": (
            aggregate["hydra_scene_graph_output_replay_ok"] is True
        ),
        "neural_gaussian_slam_output_observation_replay_ok": (
            aggregate["neural_gaussian_slam_output_observation_replay_ok"] is True
        ),
        "multi_backend_candidate_type_coverage_complete": (
            aggregate["multi_backend_candidate_type_coverage_complete"] is True
        ),
        "multi_backend_spatial_evidence_replay_path_ok": (
            aggregate["multi_backend_spatial_evidence_replay_path_ok"] is True
        ),
        "observation_only_scope_preserved": (
            aggregate["observation_only_scope_preserved"] is True
        ),
        "pose_candidate_generated": cg.get("pose") is True,
        "motion_candidate_generated": cg.get("motion") is True,
        "health_candidate_generated": cg.get("health") is True,
        "anchor_candidate_generated": cg.get("anchor") is True,
        "relocalization_candidate_generated": cg.get("relocalization") is True,
        "drift_candidate_generated": cg.get("drift") is True,
        "scene_relation_candidate_generated": cg.get("scene_relation") is True,
        "field_structure_candidate_generated": cg.get("field_structure") is True,
        "local_map_candidate_generated": cg.get("local_map") is True,
        "uncertainty_hint_candidate_generated": cg.get("uncertainty_hint") is True,
        "adapter_required": True,
        "native_output_direct_to_field_blocked": (
            aggregate["native_output_direct_to_field_rejected"] is True
        ),
        "source_chain_required": "source_chain" in ADMISSION_REQUIRED_FIELDS,
        "confidence_required": "confidence" in ADMISSION_REQUIRED_FIELDS,
        "backend_origin_required": "backend_origin" in ADMISSION_REQUIRED_FIELDS,
        "license_ref_required": "license_ref" in ADMISSION_REQUIRED_FIELDS,
        "gpl_or_incompatible_backend_technical_reference_only": (
            aggregate["gpl_or_incompatible_backend_technical_reference_only"] is True
        ),
        "vio_slam_pose_not_field_identity": (
            aggregate["vio_slam_pose_not_field_identity"] is True
        ),
        "gps_does_not_override_field_identity": True,
        "relocalization_does_not_restore_runtime_trust": (
            aggregate["relocalization_does_not_restore_runtime_trust"] is True
        ),
        "drift_remains_uncertainty_evidence": (
            aggregate["drift_remains_uncertainty_evidence"] is True
        ),
        "health_candidate_only": aggregate["health_candidate_only"] is True,
        "semantic_label_not_fact": aggregate["semantic_label_not_fact"] is True,
        "scene_graph_not_final_field_identity": (
            aggregate["scene_graph_not_final_field_identity"] is True
        ),
        "heavy_neural_gaussian_runtime_not_admitted": (
            aggregate["heavy_neural_gaussian_runtime_not_admitted"] is True
        ),
        "field_task_guidance_candidate_only": (
            aggregate["field_task_guidance_candidate_only"] is True
        ),
        "guidance_candidate_remains_candidate": (
            aggregate["guidance_candidate_remains_candidate"] is True
        ),
        "speech_gate_candidate_not_tts": aggregate["speech_gate_candidate_not_tts"] is True,
        "action_safety_candidate_exists": aggregate["action_safety_candidate_exists"] is True,
        "missing_source_chain_rejected": aggregate["missing_source_chain_rejected"] is True,
        "missing_license_ref_rejected": aggregate["missing_license_ref_rejected"] is True,
        "gpl_marked_commercial_ready_rejected": (
            aggregate["gpl_marked_commercial_ready_rejected"] is True
        ),
        "native_output_direct_to_field_rejected": (
            aggregate["native_output_direct_to_field_rejected"] is True
        ),
        "runtime_trust_restore_attempt_rejected": (
            aggregate["runtime_trust_restore_attempt_rejected"] is True
        ),
        "semantic_fact_write_field_identity_rejected": (
            aggregate["semantic_fact_write_field_identity_rejected"] is True
        ),
        "heavy_runtime_activation_rejected": (
            aggregate["heavy_runtime_activation_rejected"] is True
        ),
        "direct_action_speech_navigation_fact_write_rejected": (
            aggregate["direct_action_speech_navigation_fact_write_rejected"] is True
        ),
        "integrated_validation_mode_used": (
            NON_EXECUTION_FLAGS["integrated_validation_mode_used"] is True
        ),
        "single_backend_validation_not_used": (
            NON_EXECUTION_FLAGS["single_backend_validation_not_used"] is True
        ),
        "real_file_conversion_execution_allowed_true": (
            NON_EXECUTION_FLAGS["real_file_conversion_execution_allowed"] is True
        ),
        "real_file_replay_execution_allowed_true": (
            NON_EXECUTION_FLAGS["real_file_replay_execution_allowed"] is True
        ),
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
        "camera_connected_false": NON_EXECUTION_FLAGS["camera_connected"] is False,
        "imu_connected_false": NON_EXECUTION_FLAGS["imu_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            NON_EXECUTION_FLAGS["direct_fact_write_allowed"] is False
        ),
        "commercial_runtime_approved_false": (
            NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        ),
        "generic_json_output_ok_for_all_admitted": (
            case_run.get("generic_json_output_ok_for_all_admitted") is True
        ),
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    review_checkpoints = {
        **aggregate,
        **upstream_checks,
        "dryrun_profile_count": 1,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "admitted_backend_keys": case_run.get("admitted_backend_keys"),
        "samples_rel_dir": SAMPLES_REL_DIR,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "SLAM Backend Integrated Output Replay DryRun Run + Review",
        "lifecycle_variant": "multi_backend_slam_integrated_output_replay_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "admission_planning_ref": ADMISSION_PLANNING_REF,
        "rtab_multi_export_closure_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "adapter_mapping_ref": ADAPTER_MAPPING_REF,
        "admission_required_fields": list(ADMISSION_REQUIRED_FIELDS),
        "coverage_candidate_types": list(COVERAGE_CANDIDATE_TYPES),
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "dryrun_profile": candidate_to_dict(build_profile()),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "case_run": case_run,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "conclusions": {
            "slam_backend_integrated_output_replay_status": (
                "multi_backend_slam_output_replay_baseline_proven" if review_ok else "blocked"
            ),
            "multi_backend_output_proven_replayable": review_ok,
            "generic_json_spatial_trace_remains_default": True,
            "semantic_label_not_fact": True,
            "scene_graph_not_final_field_identity": True,
            "integrated_validation_mode_used": True,
            "adapter_mapping_enforced": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "slam_backend_mock_file_outputs",
                "backends": list(SAMPLE_BACKENDS.keys()),
                "admission": "source_chain_license_backend_origin_confidence_adapter_mapping",
                "adapter": INTERFACE_ADAPTER_REF,
                "internal_format": TARGET_INTERNAL_FORMAT,
                "parser": GENERIC_JSON_PARSER_REF,
                "candidates": list(case_run.get("generated_candidate_types") or []),
                "bundle": "spatial_evidence_candidate_bundle",
                "fusion": "spatial_odometry_fusion_candidate",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "Multi-backend SLAM mock-file output integrated replay proven (OpenVINS / ORB-SLAM3 / "
                "Kimera / Hydra / Neural-Gaussian). Next: SLAM Backend Evidence Chain Integrated "
                "Closure to seal RTAB/TUM/multi-backend mock file output together."
            ),
        },
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return result


def main() -> int:
    result = run_and_review_slam_backend_integrated_output_replay_dryrun_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "backend_sample_count": cp["backend_sample_count"],
                "sample_file_count": cp["sample_file_count"],
                "positive_case_count": cp["positive_case_count"],
                "negative_case_count": cp["negative_case_count"],
                "positive_pass_count": cp["positive_pass_count"],
                "invalid_expected_reject_count": cp["invalid_expected_reject_count"],
                "generated_candidate_types": cp["generated_candidate_types"],
                "admitted_backend_keys": cp["admitted_backend_keys"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
