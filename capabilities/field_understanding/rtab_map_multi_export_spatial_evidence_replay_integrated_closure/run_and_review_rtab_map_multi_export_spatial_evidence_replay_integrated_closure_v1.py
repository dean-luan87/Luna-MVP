# -*- coding: utf-8 -*-
"""RTAB-Map Multi-Export Spatial Evidence Replay Integrated Closure — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rtab_map_multi_export_spatial_evidence_replay_integrated_closure.rtab_map_multi_export_spatial_evidence_replay_integrated_closure_cases_v1 import (
    run_all_cases_v1,
)
from capabilities.field_understanding.rtab_map_multi_export_spatial_evidence_replay_integrated_closure.rtab_map_multi_export_spatial_evidence_replay_integrated_closure_types_v1 import (
    CANDIDATE_TYPE_COVERAGE_REQUIRED,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FIELD_SYNTHESIS_MAP_PLACE_OVERLAY_DRYRUN_REF,
    FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    FIELD_TO_TASK_ALIGNMENT_DRYRUN_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEGATIVE_CASE_REFS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    REPLAY_PIPELINE,
    RTAB_ODOMETRY_LOADER_DRYRUN_REF,
    RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
    RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
    SOURCE_CHAIN,
    SOURCE_FAMILY,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_REF,
    RTABMultiExportSpatialEvidenceReplayClosureProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1_smoke_v0"
)
OUTPUT_FILENAME = (
    "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_run_and_review_v1.json"
)
PROFILE_REF = "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_profile_v1"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "phase_ref": RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_trajectory_real_file_loader_dryrun_v1_smoke_v0/"
            "rtab_map_trajectory_real_file_loader_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_TRAJECTORY_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_real_file_loader_dryrun/"
            "rtab_map_trajectory_real_file_loader_dryrun_types_v1.py"
        ),
        "verify_flag": "rtab_trajectory_loader_dryrun_go_verified",
    },
    {
        "phase_ref": RTAB_ODOMETRY_LOADER_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_odometry_real_file_loader_dryrun_v1_smoke_v0/"
            "rtab_map_odometry_real_file_loader_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_ODOMETRY_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_odometry_real_file_loader_dryrun/"
            "rtab_map_odometry_real_file_loader_dryrun_types_v1.py"
        ),
        "verify_flag": "rtab_odometry_loader_dryrun_go_verified",
    },
    {
        "phase_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
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
        "phase_ref": FIELD_SYNTHESIS_MAP_PLACE_OVERLAY_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_synthesis_map_place_event_overlay_dryrun_v1_smoke_v0/"
            "field_synthesis_map_place_event_overlay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "FIELD_SYNTHESIS_MAP_PLACE_REALTIME_EVENT_OVERLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/field_synthesis_map_place_event_overlay_dryrun/"
            "field_synthesis_map_place_event_overlay_dryrun_types_v1.py"
        ),
    },
    {
        "phase_ref": FIELD_TO_TASK_ALIGNMENT_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_to_task_alignment_dryrun_v1_smoke_v0/"
            "field_to_task_alignment_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "FIELD_TO_TASK_ALIGNMENT_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/field_to_task_alignment_dryrun/"
            "field_to_task_alignment_dryrun_types_v1.py"
        ),
    },
    {
        "phase_ref": TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/task_to_guidance_safety_gate_dryrun_v1_smoke_v0/"
            "task_to_guidance_safety_gate_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/task_to_guidance_safety_gate_dryrun/"
            "task_to_guidance_safety_gate_dryrun_types_v1.py"
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
    },
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rtab_real_file_loader_integrated_dryrun_go_verified",
    "rtab_trajectory_loader_dryrun_go_verified",
    "rtab_odometry_loader_dryrun_go_verified",
    "generic_json_spatial_trace_parser_go_verified",
    "slam_spatial_evidence_chain_field_alignment_closure_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
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


def build_profile() -> RTABMultiExportSpatialEvidenceReplayClosureProfile:
    return RTABMultiExportSpatialEvidenceReplayClosureProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        rtab_real_file_loader_integrated_dryrun_ref=RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
        source_family=SOURCE_FAMILY,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        candidate_type_coverage_required=CANDIDATE_TYPE_COVERAGE_REQUIRED,
        replay_pipeline=REPLAY_PIPELINE,
        field_task_guidance_candidate_types=FIELD_TASK_GUIDANCE_CANDIDATE_TYPES,
        governance_rules=CLOSURE_GOVERNANCE_RULES,
    )


def _aggregate(case_run: Dict[str, Any]) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []
    by_ref = {c["case_ref"]: c for c in positive + negative}

    def chk(ref: str) -> Dict[str, Any]:
        return (by_ref.get(ref) or {}).get("checks") or {}

    coverage = chk("rtab_multi_export_candidate_type_coverage")
    bundle = chk("rtab_multi_export_spatial_evidence_bundle_replay")
    fusion = chk("rtab_multi_export_spatial_odometry_fusion_replay")
    conflict = chk("rtab_multi_export_gps_slam_conflict_replay")
    ftg = chk("rtab_multi_export_field_task_guidance_replay")
    observation = chk("rtab_multi_export_observation_only_scenario_replay")

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": sum(1 for c in positive if c.get("passed")),
        "invalid_expected_reject_count": sum(1 for c in negative if c.get("passed")),
        "candidate_type_coverage_pose_motion_health_anchor_relocalization_drift": (
            coverage.get("candidate_type_coverage_complete") is True
        ),
        "spatial_evidence_candidate_bundle_generated": (
            bundle.get("spatial_evidence_candidate_bundle_generated") is True
        ),
        "candidate_bundle_mapping_ok": bundle.get("candidate_bundle_mapping_ok") is True,
        "source_chain_preserved": bundle.get("source_chain_preserved") is True,
        "file_origin_preserved": bundle.get("file_origin_preserved") is True,
        "export_session_id_preserved": bundle.get("export_session_id_preserved") is True,
        "spatial_odometry_fusion_candidate_generated": (
            fusion.get("spatial_odometry_fusion_candidate_generated") is True
        ),
        "gps_slam_conflict_candidate_generated": (
            conflict.get("gps_slam_conflict_candidate_generated") is True
        ),
        "gps_does_not_override_field_identity": (
            conflict.get("gps_does_not_override_field_identity") is True
        ),
        "field_identity_not_overwritten": conflict.get("field_identity_not_overwritten") is True,
        "relocalization_does_not_restore_runtime_trust": (
            fusion.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "drift_remains_uncertainty_evidence": (
            fusion.get("drift_remains_uncertainty_evidence") is True
        ),
        "health_can_only_influence_risk_as_evidence": (
            fusion.get("health_can_only_influence_risk_as_evidence") is True
        ),
        "field_task_guidance_replay_path_ok": (
            ftg.get("field_task_guidance_replay_path_ok") is True
        ),
        "task_risk_candidate_references_health_drift_conflict": (
            ftg.get("task_risk_candidate_references_health_drift_conflict") is True
        ),
        "guidance_candidate_remains_candidate": (
            ftg.get("guidance_candidate_remains_candidate") is True
        ),
        "speech_gate_candidate_not_tts": ftg.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": ftg.get("action_safety_candidate_exists") is True,
        "observation_only_scope_preserved": (
            observation.get("observation_only_scope_preserved") is True
        ),
        "missing_candidate_type_coverage_rejected": (
            chk("invalid_missing_candidate_type_coverage_rejected").get(
                "missing_candidate_type_coverage_rejected"
            )
            is True
        ),
        "missing_source_chain_or_file_origin_rejected": (
            chk("invalid_missing_source_chain_or_file_origin_rejected").get(
                "missing_source_chain_or_file_origin_rejected"
            )
            is True
        ),
        "runtime_trust_restore_attempt_rejected": (
            chk("invalid_runtime_trust_restore_attempt_rejected").get(
                "runtime_trust_restore_attempt_rejected"
            )
            is True
        ),
        "gps_field_identity_overwrite_rejected": (
            chk("invalid_gps_field_identity_overwrite_rejected").get(
                "gps_field_identity_overwrite_rejected"
            )
            is True
        ),
        "direct_action_speech_navigation_fact_write_rejected": (
            chk("invalid_direct_action_speech_navigation_fact_write_rejected").get(
                "direct_action_speech_navigation_fact_write_rejected"
            )
            is True
        ),
        "native_output_direct_to_field_rejected": (
            chk("invalid_native_output_direct_to_field_rejected").get(
                "native_output_direct_to_field_rejected"
            )
            is True
        ),
    }


def run_and_review_rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    upstream_checks, upstream_issues = review_upstream_artifacts()
    case_run = run_all_cases_v1()
    aggregate = _aggregate(case_run)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "positive_case_count_eq_6": aggregate["positive_case_count"] == 6,
        "negative_case_count_eq_6": aggregate["negative_case_count"] == 6,
        "positive_pass_count_eq_6": aggregate["positive_pass_count"] == 6,
        "invalid_expected_reject_count_eq_6": aggregate["invalid_expected_reject_count"] == 6,
        "rtab_real_file_loader_integrated_dryrun_go_verified": (
            upstream_checks.get("rtab_real_file_loader_integrated_dryrun_go_verified") is True
        ),
        "rtab_trajectory_loader_dryrun_go_verified": (
            upstream_checks.get("rtab_trajectory_loader_dryrun_go_verified") is True
        ),
        "rtab_odometry_loader_dryrun_go_verified": (
            upstream_checks.get("rtab_odometry_loader_dryrun_go_verified") is True
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
        "candidate_type_coverage_pose_motion_health_anchor_relocalization_drift": (
            aggregate["candidate_type_coverage_pose_motion_health_anchor_relocalization_drift"]
            is True
        ),
        "spatial_evidence_candidate_bundle_generated": (
            aggregate["spatial_evidence_candidate_bundle_generated"] is True
        ),
        "candidate_bundle_mapping_ok": aggregate["candidate_bundle_mapping_ok"] is True,
        "source_chain_preserved": aggregate["source_chain_preserved"] is True,
        "file_origin_preserved": aggregate["file_origin_preserved"] is True,
        "export_session_id_preserved": aggregate["export_session_id_preserved"] is True,
        "spatial_odometry_fusion_candidate_generated": (
            aggregate["spatial_odometry_fusion_candidate_generated"] is True
        ),
        "gps_slam_conflict_candidate_generated": (
            aggregate["gps_slam_conflict_candidate_generated"] is True
        ),
        "gps_does_not_override_field_identity": (
            aggregate["gps_does_not_override_field_identity"] is True
        ),
        "field_identity_not_overwritten": aggregate["field_identity_not_overwritten"] is True,
        "relocalization_does_not_restore_runtime_trust": (
            aggregate["relocalization_does_not_restore_runtime_trust"] is True
        ),
        "drift_remains_uncertainty_evidence": (
            aggregate["drift_remains_uncertainty_evidence"] is True
        ),
        "health_can_only_influence_risk_as_evidence": (
            aggregate["health_can_only_influence_risk_as_evidence"] is True
        ),
        "field_task_guidance_replay_path_ok": (
            aggregate["field_task_guidance_replay_path_ok"] is True
        ),
        "task_risk_candidate_references_health_drift_conflict": (
            aggregate["task_risk_candidate_references_health_drift_conflict"] is True
        ),
        "guidance_candidate_remains_candidate": (
            aggregate["guidance_candidate_remains_candidate"] is True
        ),
        "speech_gate_candidate_not_tts": aggregate["speech_gate_candidate_not_tts"] is True,
        "action_safety_candidate_exists": aggregate["action_safety_candidate_exists"] is True,
        "observation_only_scope_preserved": (
            aggregate["observation_only_scope_preserved"] is True
        ),
        "missing_candidate_type_coverage_rejected": (
            aggregate["missing_candidate_type_coverage_rejected"] is True
        ),
        "missing_source_chain_or_file_origin_rejected": (
            aggregate["missing_source_chain_or_file_origin_rejected"] is True
        ),
        "runtime_trust_restore_attempt_rejected": (
            aggregate["runtime_trust_restore_attempt_rejected"] is True
        ),
        "gps_field_identity_overwrite_rejected": (
            aggregate["gps_field_identity_overwrite_rejected"] is True
        ),
        "direct_action_speech_navigation_fact_write_rejected": (
            aggregate["direct_action_speech_navigation_fact_write_rejected"] is True
        ),
        "native_output_direct_to_field_rejected": (
            aggregate["native_output_direct_to_field_rejected"] is True
        ),
        "integrated_validation_mode_used": NON_EXECUTION_FLAGS["integrated_validation_mode_used"]
        is True,
        "single_loader_validation_not_used": NON_EXECUTION_FLAGS[
            "single_loader_validation_not_used"
        ]
        is True,
        "real_file_replay_execution_allowed_true": NON_EXECUTION_FLAGS[
            "real_file_replay_execution_allowed"
        ]
        is True,
        "runtime_activation_allowed_false": NON_EXECUTION_FLAGS["runtime_activation_allowed"]
        is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "rtab_database_read_allowed_false": NON_EXECUTION_FLAGS["rtab_database_read_allowed"]
        is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
        "live_rtab_runtime_started_false": NON_EXECUTION_FLAGS["live_rtab_runtime_started"]
        is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "camera_connected_false": NON_EXECUTION_FLAGS["camera_connected"] is False,
        "imu_connected_false": NON_EXECUTION_FLAGS["imu_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": NON_EXECUTION_FLAGS["direct_fact_write_allowed"]
        is False,
        "commercial_runtime_approved_false": NON_EXECUTION_FLAGS["commercial_runtime_approved"]
        is False,
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
        "closure_profile_count": 1,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "candidate_type_coverage": case_run.get("candidate_type_coverage"),
        "multi_export_json_trace_item_count": case_run.get("multi_export_json_trace_item_count"),
        "blocker_count": blocker_count,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RTAB-Map Multi-Export Spatial Evidence Replay Integrated Closure Run + Review",
        "lifecycle_variant": "integrated_rtab_multi_export_spatial_evidence_replay_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "rtab_real_file_loader_integrated_dryrun_ref": RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "replay_pipeline": list(REPLAY_PIPELINE),
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "closure_profile": candidate_to_dict(build_profile()),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "case_run": case_run,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "conclusions": {
            "rtab_multi_export_spatial_evidence_replay_status": (
                "rtab_multi_export_spatial_evidence_replay_baseline_sealed"
                if review_ok
                else "blocked"
            ),
            "candidate_type_coverage": list(CANDIDATE_TYPE_COVERAGE_REQUIRED),
            "generic_json_parser_reused": True,
            "integrated_validation_mode_used": True,
            "single_loader_validation_not_used": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "inputs": "rtab trajectory/odometry/graph real file outputs",
                "parser": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "fusion": "spatial_odometry_fusion_candidate",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RTAB real file outputs advanced from loader baseline to Luna spatial evidence "
                "chain usability layer. All replay outputs candidate-only. Next: external "
                "vision / OCR / segmentation outputs into the same integrated evidence replay."
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
    result = run_and_review_rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_case_count": cp["positive_case_count"],
                "negative_case_count": cp["negative_case_count"],
                "positive_pass_count": cp["positive_pass_count"],
                "invalid_expected_reject_count": cp["invalid_expected_reject_count"],
                "candidate_type_coverage_complete": cp[
                    "candidate_type_coverage_pose_motion_health_anchor_relocalization_drift"
                ],
                "spatial_odometry_fusion_candidate_generated": cp[
                    "spatial_odometry_fusion_candidate_generated"
                ],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
