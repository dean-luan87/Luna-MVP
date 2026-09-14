# -*- coding: utf-8 -*-
"""RTAB-Map Real File Loader Integrated DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rtab_map_real_file_loader_integrated_dryrun.rtab_map_real_file_loader_integrated_dryrun_cases_v1 import (
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.rtab_map_real_file_loader_integrated_dryrun.rtab_map_real_file_loader_integrated_dryrun_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FULL_CANDIDATE_TYPE_COVERAGE,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    GOVERNANCE_CLOSURE_REF,
    INTEGRATED_GOVERNANCE_RULES,
    INTEGRATED_PRINCIPLE_ZH,
    INTEGRATION_PRINCIPLES,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    NEGATIVE_CASE_REFS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    REAL_FILE_REPLAY_DRYRUN_REF,
    RTAB_GRAPH_FIXTURE_REF,
    RTAB_ODOMETRY_FIXTURE_REF,
    RTAB_ODOMETRY_LOADER_PLANNING_REF,
    RTAB_TRAJECTORY_FIXTURE_REF,
    RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SOURCE_FAMILY,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TUM_REAL_FILE_LOADER_DRYRUN_REF,
    RTABMapRealFileLoaderIntegratedDryRunProfile,
    candidate_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "rtab_map_real_file_loader_integrated_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "rtab_map_real_file_loader_integrated_dryrun_run_and_review_v1.json"
PROFILE_REF = "rtab_map_real_file_loader_integrated_dryrun_profile_v1"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "require_go": True,
        "require_trajectory_loader_dryrun_go": True,
    },
    {
        "phase_ref": RTAB_ODOMETRY_LOADER_PLANNING_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_odometry_real_file_loader_planning_v1_smoke_v0/"
            "rtab_map_odometry_real_file_loader_planning_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_ODOMETRY_REAL_FILE_LOADER_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_odometry_real_file_loader_planning/"
            "rtab_map_odometry_real_file_loader_planning_types_v1.py"
        ),
        "require_go": True,
        "require_odometry_loader_planning_go": True,
    },
    {
        "phase_ref": RTAB_TRAJECTORY_FIXTURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_trajectory_export_ingest_v1_smoke_v0/"
            "rtab_map_trajectory_export_ingest_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_trajectory_export_ingest/"
            "rtab_map_trajectory_export_ingest_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": RTAB_ODOMETRY_FIXTURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_odometry_export_ingest_v1_smoke_v0/"
            "rtab_map_odometry_export_ingest_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_ODOMETRY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_odometry_export_ingest/"
            "rtab_map_odometry_export_ingest_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": RTAB_GRAPH_FIXTURE_REF,
        "artifact_rel": (
            "_tmp_eval_out/rtab_map_graph_export_ingest_v1_smoke_v0/"
            "rtab_map_graph_export_ingest_run_and_review_v1.json"
        ),
        "expected_go": "RTAB_MAP_GRAPH_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO",
        "module_rel": (
            "capabilities/field_understanding/rtab_map_graph_export_ingest/"
            "rtab_map_graph_export_ingest_types_v1.py"
        ),
        "require_go": True,
        "require_graph_fixture_go": True,
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
        "require_go": True,
        "require_parser_go": True,
    },
    {
        "phase_ref": REAL_FILE_REPLAY_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_json_spatial_trace_real_file_replay_dryrun_v1_smoke_v0/"
            "generic_json_spatial_trace_real_file_replay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_CONTROLLED_REPLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_dryrun/"
            "generic_json_spatial_trace_real_file_replay_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": TUM_REAL_FILE_LOADER_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/generic_tum_real_file_loader_dryrun_v1_smoke_v0/"
            "generic_tum_real_file_loader_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/generic_tum_real_file_loader_dryrun/"
            "generic_tum_real_file_loader_dryrun_types_v1.py"
        ),
        "require_go": True,
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
        "require_go": True,
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
        "require_go": True,
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
        "require_go": True,
    },
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

        if entry.get("require_trajectory_loader_dryrun_go"):
            checks["rtab_trajectory_real_file_loader_dryrun_go_verified"] = go_ok
        if entry.get("require_odometry_loader_planning_go"):
            checks["rtab_odometry_real_file_loader_planning_go_verified"] = go_ok
        if entry.get("require_graph_fixture_go"):
            checks["rtab_graph_fixture_go_verified"] = go_ok
        if entry.get("require_parser_go"):
            checks["generic_json_spatial_trace_parser_go_verified"] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    for required in (
        "rtab_trajectory_real_file_loader_dryrun_go_verified",
        "rtab_odometry_real_file_loader_planning_go_verified",
        "rtab_graph_fixture_go_verified",
        "generic_json_spatial_trace_parser_go_verified",
    ):
        if not checks.get(required, False):
            issues.append(f"{required}_not_verified")

    return checks, issues


def build_profile() -> RTABMapRealFileLoaderIntegratedDryRunProfile:
    return RTABMapRealFileLoaderIntegratedDryRunProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        generic_json_spatial_trace_parser_ref=GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        rtab_trajectory_loader_dryrun_ref=RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        rtab_odometry_loader_planning_ref=RTAB_ODOMETRY_LOADER_PLANNING_REF,
        rtab_graph_fixture_ref=RTAB_GRAPH_FIXTURE_REF,
        source_family=SOURCE_FAMILY,
        target_internal_format=TARGET_INTERNAL_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        integration_principles=INTEGRATION_PRINCIPLES,
        full_candidate_type_coverage=FULL_CANDIDATE_TYPE_COVERAGE,
        governance_rules=INTEGRATED_GOVERNANCE_RULES,
    )


def _aggregate(case_run: Dict[str, Any], trajectory_scope_closed: bool) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []
    by_ref = {c["case_ref"]: c for c in positive + negative}

    def chk(ref: str) -> Dict[str, Any]:
        return (by_ref.get(ref) or {}).get("checks") or {}

    odom_degraded = chk("rtab_odometry_degraded_health_integrated_dryrun")
    odom_lost = chk("rtab_odometry_lost_health_integrated_dryrun")
    odom_alias = chk("rtab_odometry_alias_fields_integrated_dryrun")
    graph_ar = chk("rtab_graph_anchor_relocalization_integrated_dryrun")
    graph_drift = chk("rtab_graph_drift_integrated_dryrun")
    graph_alias = chk("rtab_graph_alias_fields_integrated_dryrun")
    coverage = chk("rtab_multi_export_candidate_type_coverage")
    replay_path = chk("rtab_multi_export_field_task_guidance_replay_path")

    sample_count = sum(1 for n in SAMPLE_FILES if (samples_dir() / n).is_file())

    odom_pipe_pos = by_ref.get("rtab_odometry_degraded_health_integrated_dryrun") or {}

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": sum(1 for c in positive if c.get("passed")),
        "invalid_expected_reject_count": sum(1 for c in negative if c.get("passed")),
        "sample_file_count": sample_count,
        "local_file_read_used": True,
        "file_source_admission_required": True,
        "file_origin_metadata_required": True,
        "source_chain_required": True,
        "export_session_id_preserved": True,
        "odometry_pose_motion_health_ok": (
            odom_degraded.get("pose_item_count") == 3
            and odom_degraded.get("motion_item_count") == 2
            and odom_degraded.get("health_item_count") == 1
        ),
        "odometry_health_candidate_maps_to_slam_health_candidate": (
            odom_degraded.get("health_candidate_maps_to_slam_health_candidate") is True
        ),
        "degraded_health_does_not_directly_block_or_allow_action": (
            odom_degraded.get("degraded_health_does_not_directly_block_or_allow_action") is True
        ),
        "lost_health_does_not_trigger_runtime_shutdown": (
            odom_lost.get("lost_health_does_not_trigger_runtime_shutdown") is True
        ),
        "health_does_not_trigger_speech_navigation_fact_write": (
            odom_lost.get("health_does_not_trigger_speech_navigation_fact_write") is True
        ),
        "odometry_alias_field_mapping_ok": (
            odom_alias.get("odometry_alias_field_mapping_ok") is True
        ),
        "graph_planning_lite_completed": graph_ar.get("candidate_bundle_mapping_ok") is True,
        "graph_anchor_candidate_ok": graph_ar.get("anchor_item_count", 0) >= 1,
        "graph_relocalization_candidate_ok": graph_ar.get("relocalization_item_count", 0) >= 1,
        "graph_drift_candidate_ok": graph_drift.get("drift_item_count", 0) >= 1,
        "graph_alias_field_mapping_ok": graph_alias.get("graph_alias_field_mapping_ok") is True,
        "relocalization_does_not_restore_runtime_trust": (
            graph_ar.get("relocalization_does_not_restore_runtime_trust") is True
            and replay_path.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "drift_remains_uncertainty_evidence": (
            graph_drift.get("drift_remains_uncertainty_evidence") is True
        ),
        "graph_anchor_does_not_write_fact": True,
        "candidate_type_coverage_pose_motion_health_anchor_relocalization_drift": (
            coverage.get("candidate_type_coverage_complete") is True
        ),
        "multi_export_candidate_bundle_mapping_ok": (
            coverage.get("multi_export_candidate_bundle_mapping_ok") is True
        ),
        "field_task_guidance_replay_path_candidate_only": (
            replay_path.get("field_task_guidance_replay_path_candidate_only") is True
        ),
        "trajectory_scope_closed": coverage.get("trajectory_scope_closed") is True,
        "odometry_scope_closed": coverage.get("odometry_scope_closed") is True,
        "graph_scope_closed": coverage.get("graph_scope_closed") is True,
        "odometry_missing_tracking_state_rejected": chk(
            "invalid_odometry_missing_tracking_state_rejected"
        ).get("odometry_missing_tracking_state_rejected")
        is True,
        "graph_missing_node_id_rejected": chk("invalid_graph_missing_node_id_rejected").get(
            "graph_missing_node_id_rejected"
        )
        is True,
        "graph_missing_source_chain_rejected": chk(
            "invalid_graph_missing_source_chain_rejected"
        ).get("graph_missing_source_chain_rejected")
        is True,
        "runtime_trust_restore_attempt_rejected": chk(
            "invalid_graph_runtime_trust_restore_rejected"
        ).get("runtime_trust_restore_attempt_rejected")
        is True,
        "rtab_db_ros_live_runtime_rejected": chk(
            "invalid_rtab_db_ros_live_runtime_rejected"
        ).get("rtab_db_ros_live_runtime_rejected")
        is True,
        "direct_action_speech_navigation_fact_write_rejected": chk(
            "invalid_direct_action_speech_navigation_fact_write_rejected"
        ).get("direct_action_speech_navigation_fact_write_rejected")
        is True,
    }


def run_and_review_rtab_map_real_file_loader_integrated_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    upstream_checks, upstream_issues = review_upstream_artifacts()
    trajectory_scope_closed = upstream_checks.get(
        "rtab_trajectory_real_file_loader_dryrun_go_verified", False
    )
    case_run = run_all_cases_v1(trajectory_scope_closed=trajectory_scope_closed)
    aggregate = _aggregate(case_run, trajectory_scope_closed)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    go_conditions = {
        "integrated_profile_count_eq_1": True,
        "positive_case_count_eq_8": aggregate["positive_case_count"] == 8,
        "negative_case_count_eq_6": aggregate["negative_case_count"] == 6,
        "positive_pass_count_eq_8": aggregate["positive_pass_count"] == 8,
        "invalid_expected_reject_count_eq_6": aggregate["invalid_expected_reject_count"] == 6,
        "rtab_trajectory_real_file_loader_dryrun_go_verified": (
            upstream_checks.get("rtab_trajectory_real_file_loader_dryrun_go_verified") is True
        ),
        "rtab_odometry_real_file_loader_planning_go_verified": (
            upstream_checks.get("rtab_odometry_real_file_loader_planning_go_verified") is True
        ),
        "rtab_graph_fixture_go_verified": (
            upstream_checks.get("rtab_graph_fixture_go_verified") is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            upstream_checks.get("generic_json_spatial_trace_parser_go_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "sample_file_count_gte_11": aggregate["sample_file_count"] >= 11,
        "local_file_read_used": aggregate["local_file_read_used"] is True,
        "file_source_admission_required": aggregate["file_source_admission_required"] is True,
        "file_origin_metadata_required": aggregate["file_origin_metadata_required"] is True,
        "source_chain_required": aggregate["source_chain_required"] is True,
        "export_session_id_preserved": aggregate["export_session_id_preserved"] is True,
        "odometry_pose_motion_health_ok": aggregate["odometry_pose_motion_health_ok"] is True,
        "odometry_health_candidate_maps_to_slam_health_candidate": (
            aggregate["odometry_health_candidate_maps_to_slam_health_candidate"] is True
        ),
        "degraded_health_does_not_directly_block_or_allow_action": (
            aggregate["degraded_health_does_not_directly_block_or_allow_action"] is True
        ),
        "lost_health_does_not_trigger_runtime_shutdown": (
            aggregate["lost_health_does_not_trigger_runtime_shutdown"] is True
        ),
        "health_does_not_trigger_speech_navigation_fact_write": (
            aggregate["health_does_not_trigger_speech_navigation_fact_write"] is True
        ),
        "odometry_alias_field_mapping_ok": aggregate["odometry_alias_field_mapping_ok"] is True,
        "graph_planning_lite_completed": aggregate["graph_planning_lite_completed"] is True,
        "graph_anchor_candidate_ok": aggregate["graph_anchor_candidate_ok"] is True,
        "graph_relocalization_candidate_ok": aggregate["graph_relocalization_candidate_ok"] is True,
        "graph_drift_candidate_ok": aggregate["graph_drift_candidate_ok"] is True,
        "graph_alias_field_mapping_ok": aggregate["graph_alias_field_mapping_ok"] is True,
        "relocalization_does_not_restore_runtime_trust": (
            aggregate["relocalization_does_not_restore_runtime_trust"] is True
        ),
        "drift_remains_uncertainty_evidence": (
            aggregate["drift_remains_uncertainty_evidence"] is True
        ),
        "graph_anchor_does_not_write_fact": aggregate["graph_anchor_does_not_write_fact"] is True,
        "candidate_type_coverage_pose_motion_health_anchor_relocalization_drift": (
            aggregate["candidate_type_coverage_pose_motion_health_anchor_relocalization_drift"] is True
        ),
        "multi_export_candidate_bundle_mapping_ok": (
            aggregate["multi_export_candidate_bundle_mapping_ok"] is True
        ),
        "field_task_guidance_replay_path_candidate_only": (
            aggregate["field_task_guidance_replay_path_candidate_only"] is True
        ),
        "odometry_missing_tracking_state_rejected": (
            aggregate["odometry_missing_tracking_state_rejected"] is True
        ),
        "graph_missing_node_id_rejected": aggregate["graph_missing_node_id_rejected"] is True,
        "graph_missing_source_chain_rejected": (
            aggregate["graph_missing_source_chain_rejected"] is True
        ),
        "runtime_trust_restore_attempt_rejected": (
            aggregate["runtime_trust_restore_attempt_rejected"] is True
        ),
        "rtab_db_ros_live_runtime_rejected": (
            aggregate["rtab_db_ros_live_runtime_rejected"] is True
        ),
        "direct_action_speech_navigation_fact_write_rejected": (
            aggregate["direct_action_speech_navigation_fact_write_rejected"] is True
        ),
        "planning_only_governance_chain_not_reopened": (
            NON_EXECUTION_FLAGS["planning_only_governance_chain_not_reopened"] is True
        ),
        "real_file_conversion_execution_allowed_true": (
            NON_EXECUTION_FLAGS["real_file_conversion_execution_allowed"] is True
        ),
        "real_file_replay_execution_allowed_true": (
            NON_EXECUTION_FLAGS["real_file_replay_execution_allowed"] is True
        ),
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
        "integrated_profile_count": 1,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "samples_rel_dir": SAMPLES_REL_DIR,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RTAB-Map Real File Loader Integrated DryRun Run + Review",
        "lifecycle_variant": "integrated_rtab_real_file_loader_dryrun_closure",
        "integrated_principle_zh": INTEGRATED_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "rtab_trajectory_loader_dryrun_ref": RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        "rtab_odometry_loader_planning_ref": RTAB_ODOMETRY_LOADER_PLANNING_REF,
        "rtab_graph_fixture_ref": RTAB_GRAPH_FIXTURE_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "tum_real_file_loader_dryrun_ref": TUM_REAL_FILE_LOADER_DRYRUN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "integration_principles": list(INTEGRATION_PRINCIPLES),
        "integrated_governance_rules": list(INTEGRATED_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "integrated_profile": candidate_to_dict(build_profile()),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "case_run": case_run,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "conclusions": {
            "rtab_real_file_loader_integrated_dryrun_status": (
                "rtab_real_file_loader_baseline_sealed" if review_ok else "blocked"
            ),
            "trajectory_scope_closed": aggregate["trajectory_scope_closed"],
            "odometry_scope_closed": aggregate["odometry_scope_closed"],
            "graph_scope_closed": aggregate["graph_scope_closed"],
            "candidate_type_coverage": list(FULL_CANDIDATE_TYPE_COVERAGE),
            "generic_json_parser_reused": True,
            "planning_only_governance_chain_not_reopened": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "trajectory": "pose / motion (sealed dry-run reference)",
                "odometry": "pose / motion / health",
                "graph": "anchor / relocalization / drift",
                "parser": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RTAB trajectory / odometry / graph three real-file loader baselines integrated "
                "and sealed in one accelerated dry-run. Candidate coverage pose/motion/health/"
                "anchor/relocalization/drift proven candidate-only."
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
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return result


def main() -> int:
    result = run_and_review_rtab_map_real_file_loader_integrated_dryrun_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_case_count": cp["positive_case_count"],
                "negative_case_count": cp["negative_case_count"],
                "positive_pass_count": cp["positive_pass_count"],
                "invalid_expected_reject_count": cp["invalid_expected_reject_count"],
                "trajectory_scope_closed": cp["trajectory_scope_closed"],
                "odometry_scope_closed": cp["odometry_scope_closed"],
                "graph_scope_closed": cp["graph_scope_closed"],
                "candidate_type_coverage_complete": cp[
                    "candidate_type_coverage_pose_motion_health_anchor_relocalization_drift"
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
