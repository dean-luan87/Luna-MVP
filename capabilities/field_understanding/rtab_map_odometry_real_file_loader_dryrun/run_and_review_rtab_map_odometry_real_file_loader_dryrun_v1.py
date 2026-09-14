# -*- coding: utf-8 -*-
"""RTAB-Map Odometry Real File Loader DryRun — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rtab_map_odometry_real_file_loader_dryrun.rtab_map_odometry_real_file_loader_dryrun_cases_v1 import (
    build_negative_cases_v1,
    build_positive_cases_v1,
    run_all_cases_v1,
    samples_dir,
)
from capabilities.field_understanding.rtab_map_odometry_real_file_loader_dryrun.rtab_map_odometry_real_file_loader_dryrun_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DRYRUN_GOVERNANCE_RULES,
    DRYRUN_PRINCIPLE_ZH,
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
    REAL_FILE_REPLAY_DRYRUN_REF,
    RTAB_ODOMETRY_FIXTURE_REF,
    RTAB_ODOMETRY_LOADER_PLANNING_REF,
    RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SOURCE_FORMAT,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TUM_REAL_FILE_LOADER_DRYRUN_REF,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "rtab_map_odometry_real_file_loader_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "rtab_map_odometry_real_file_loader_dryrun_run_and_review_v1.json"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
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
        "require_loader_planning_go": True,
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
        "require_fixture_go": True,
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
        "require_go": True,
        "require_trajectory_loader_dryrun_go": True,
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
        expected_go = entry["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        if entry.get("require_loader_planning_go"):
            checks["rtab_odometry_loader_planning_go_verified"] = go_ok
        if entry.get("require_fixture_go"):
            checks["rtab_odometry_fixture_go_verified"] = go_ok
        if entry.get("require_trajectory_loader_dryrun_go"):
            checks["rtab_trajectory_real_file_loader_dryrun_go_verified"] = go_ok
        if entry.get("require_parser_go"):
            checks["generic_json_spatial_trace_parser_go_verified"] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    if not checks.get("rtab_odometry_loader_planning_go_verified", False):
        issues.append("rtab_odometry_loader_planning_go_not_verified")
    if not checks.get("rtab_odometry_fixture_go_verified", False):
        issues.append("rtab_odometry_fixture_go_not_verified")
    if not checks.get("rtab_trajectory_real_file_loader_dryrun_go_verified", False):
        issues.append("rtab_trajectory_real_file_loader_dryrun_go_not_verified")
    if not checks.get("generic_json_spatial_trace_parser_go_verified", False):
        issues.append("parser_go_not_verified")

    return checks, issues


def _aggregate_case_results(case_run: Dict[str, Any]) -> Dict[str, Any]:
    positive = case_run.get("positive_cases") or []
    negative = case_run.get("negative_cases") or []

    positive_pass = sum(1 for c in positive if c.get("passed"))
    negative_pass = sum(1 for c in negative if c.get("passed"))

    by_ref = {c["case_ref"]: c for c in positive + negative}

    valid = by_ref.get("rtab_odometry_valid_file_to_pose_motion_health_json_trace", {})
    alias = by_ref.get("rtab_odometry_alias_fields_to_standard_trace", {})
    meta = by_ref.get("rtab_odometry_metadata_and_source_chain_preserved", {})
    guidance = by_ref.get("rtab_odometry_to_field_task_guidance_replay_path", {})
    lost = by_ref.get("rtab_odometry_lost_tracking_to_critical_health", {})
    lowq = by_ref.get("rtab_odometry_low_quality_degrades_health", {})
    missing_ts = by_ref.get("invalid_missing_tracking_state_rejected", {})
    zero_quat = by_ref.get("invalid_zero_quaternion_rejected", {})
    missing_chain = by_ref.get("invalid_missing_source_chain_rejected", {})
    direct_write = by_ref.get("invalid_direct_field_synthesis_write_rejected", {})
    db_ros = by_ref.get("invalid_rtab_db_ros_live_runtime_rejected", {})

    valid_checks = valid.get("checks") or {}
    alias_checks = alias.get("checks") or {}
    meta_checks = meta.get("checks") or {}
    guidance_checks = guidance.get("checks") or {}
    lost_checks = lost.get("checks") or {}
    lowq_checks = lowq.get("checks") or {}

    sample_count = sum(1 for name in SAMPLE_FILES if (samples_dir() / name).is_file())

    metadata_positive = (valid, alias, meta)
    file_origin_required = all(
        (c.get("admission") or {}).get("file_origin_metadata_present") is True
        for c in metadata_positive
        if c.get("admission")
    )
    source_chain_required = all(
        (c.get("admission") or {}).get("source_chain_present") is True
        for c in metadata_positive
        if c.get("admission")
    )
    admission_required = all(
        (c.get("admission") or {}).get("file_source_admitted") is True
        for c in metadata_positive
        if c.get("admission")
    )

    return {
        "positive_case_count": len(positive),
        "negative_case_count": len(negative),
        "positive_pass_count": positive_pass,
        "invalid_expected_reject_count": negative_pass,
        "sample_file_count": sample_count,
        "local_file_read_used": valid_checks.get("local_file_read_used") is True,
        "file_source_admission_required": admission_required,
        "file_origin_metadata_required": file_origin_required,
        "source_chain_required": source_chain_required,
        "export_session_id_preserved": meta_checks.get("export_session_id_preserved") is True,
        "rtab_odometry_valid_file_loaded": valid.get("passed") is True,
        "rtab_odometry_alias_field_mapping_ok": alias_checks.get(
            "rtab_odometry_alias_field_mapping_ok"
        )
        is True,
        "rtab_record_count": valid_checks.get("rtab_record_count"),
        "json_trace_item_count": valid_checks.get("json_trace_item_count"),
        "pose_item_count": valid_checks.get("pose_item_count"),
        "motion_item_count": valid_checks.get("motion_item_count"),
        "health_item_count": valid_checks.get("health_item_count"),
        "rtab_odometry_to_json_trace_conversion_ok": valid_checks.get(
            "rtab_odometry_to_json_trace_conversion_ok"
        )
        is True,
        "generic_json_parser_reused": valid_checks.get("generic_json_parser_reused") is True,
        "candidate_bundle_mapping_ok": valid_checks.get("candidate_bundle_mapping_ok") is True,
        "health_candidate_maps_to_slam_health_candidate": valid_checks.get(
            "health_candidate_maps_to_slam_health_candidate"
        )
        is True,
        "field_task_guidance_replay_path_candidate_only": (
            (guidance.get("path_trace") or {}).get("candidate_only") is True
            and guidance.get("passed") is True
        ),
        "health_can_only_influence_risk_as_evidence": (
            guidance_checks.get("health_can_only_influence_risk_as_evidence") is True
            and guidance.get("passed") is True
        ),
        "motion_generated_only_from_consecutive_records": valid_checks.get("motion_item_count") == 2,
        "degraded_health_does_not_directly_block_or_allow_action": (
            lowq_checks.get("degraded_health_does_not_directly_block_or_allow_action") is True
            and lowq.get("passed") is True
        ),
        "lost_health_does_not_trigger_runtime_shutdown": (
            lost_checks.get("lost_health_does_not_trigger_runtime_shutdown") is True
            and lost.get("passed") is True
        ),
        "health_does_not_trigger_speech_navigation_fact_write": (
            lost_checks.get("health_does_not_trigger_speech_navigation_fact_write") is True
            and lost.get("passed") is True
        ),
        "low_quality_degrades_health": lowq.get("passed") is True,
        "missing_tracking_state_rejected": (missing_ts.get("checks") or {}).get(
            "missing_tracking_state_rejected"
        )
        is True,
        "zero_quaternion_rejected": (zero_quat.get("checks") or {}).get("zero_quaternion_rejected")
        is True,
        "missing_source_chain_rejected": (missing_chain.get("checks") or {}).get(
            "missing_source_chain_rejected"
        )
        is True,
        "direct_field_synthesis_write_rejected": (direct_write.get("checks") or {}).get(
            "direct_field_synthesis_write_rejected"
        )
        is True,
        "rtab_db_ros_live_runtime_rejected": (db_ros.get("checks") or {}).get(
            "rtab_db_ros_live_runtime_rejected"
        )
        is True,
    }


def run_and_review_rtab_map_odometry_real_file_loader_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    case_run = run_all_cases_v1()
    upstream_checks, upstream_issues = review_upstream_artifacts()
    aggregate = _aggregate_case_results(case_run)

    failed_checks: List[str] = list(upstream_issues)
    passed_checks: List[str] = []

    go_conditions = {
        "positive_case_count_eq_6": aggregate["positive_case_count"] == 6,
        "negative_case_count_eq_5": aggregate["negative_case_count"] == 5,
        "positive_pass_count_eq_6": aggregate["positive_pass_count"] == 6,
        "invalid_expected_reject_count_eq_5": aggregate["invalid_expected_reject_count"] == 5,
        "rtab_odometry_loader_planning_go_verified": (
            upstream_checks.get("rtab_odometry_loader_planning_go_verified") is True
        ),
        "rtab_odometry_fixture_go_verified": (
            upstream_checks.get("rtab_odometry_fixture_go_verified") is True
        ),
        "rtab_trajectory_real_file_loader_dryrun_go_verified": (
            upstream_checks.get("rtab_trajectory_real_file_loader_dryrun_go_verified") is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            upstream_checks.get("generic_json_spatial_trace_parser_go_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": (
            upstream_checks.get("controlled_trial_governance_template_ref_ok") is True
        ),
        "sample_file_count_gte_8": aggregate["sample_file_count"] >= 8,
        "local_file_read_used": aggregate["local_file_read_used"] is True,
        "file_source_admission_required": aggregate["file_source_admission_required"] is True,
        "file_origin_metadata_required": aggregate["file_origin_metadata_required"] is True,
        "source_chain_required": aggregate["source_chain_required"] is True,
        "export_session_id_preserved": aggregate["export_session_id_preserved"] is True,
        "rtab_odometry_valid_file_loaded": aggregate["rtab_odometry_valid_file_loaded"] is True,
        "rtab_odometry_alias_field_mapping_ok": (
            aggregate["rtab_odometry_alias_field_mapping_ok"] is True
        ),
        "rtab_record_count_eq_3": aggregate["rtab_record_count"] == 3,
        "json_trace_item_count_eq_6": aggregate["json_trace_item_count"] == 6,
        "pose_item_count_eq_3": aggregate["pose_item_count"] == 3,
        "motion_item_count_eq_2": aggregate["motion_item_count"] == 2,
        "health_item_count_eq_1": aggregate["health_item_count"] == 1,
        "rtab_odometry_to_json_trace_conversion_ok": (
            aggregate["rtab_odometry_to_json_trace_conversion_ok"] is True
        ),
        "generic_json_parser_reused": aggregate["generic_json_parser_reused"] is True,
        "candidate_bundle_mapping_ok": aggregate["candidate_bundle_mapping_ok"] is True,
        "health_candidate_maps_to_slam_health_candidate": (
            aggregate["health_candidate_maps_to_slam_health_candidate"] is True
        ),
        "field_task_guidance_replay_path_candidate_only": (
            aggregate["field_task_guidance_replay_path_candidate_only"] is True
        ),
        "health_can_only_influence_risk_as_evidence": (
            aggregate["health_can_only_influence_risk_as_evidence"] is True
        ),
        "motion_generated_only_from_consecutive_records": (
            aggregate["motion_generated_only_from_consecutive_records"] is True
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
        "low_quality_degrades_health": aggregate["low_quality_degrades_health"] is True,
        "missing_tracking_state_rejected": aggregate["missing_tracking_state_rejected"] is True,
        "zero_quaternion_rejected": aggregate["zero_quaternion_rejected"] is True,
        "missing_source_chain_rejected": aggregate["missing_source_chain_rejected"] is True,
        "direct_field_synthesis_write_rejected": (
            aggregate["direct_field_synthesis_write_rejected"] is True
        ),
        "rtab_db_ros_live_runtime_rejected": aggregate["rtab_db_ros_live_runtime_rejected"]
        is True,
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
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_format": SOURCE_FORMAT,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "rtab_odometry_loader_planning_ref": RTAB_ODOMETRY_LOADER_PLANNING_REF,
        "rtab_odometry_fixture_ref": RTAB_ODOMETRY_FIXTURE_REF,
        "rtab_trajectory_real_file_loader_dryrun_ref": RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "samples_rel_dir": SAMPLES_REL_DIR,
        **NON_EXECUTION_FLAGS,
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RTAB-Map Odometry Real File Loader DryRun Run + Review",
        "lifecycle_variant": "compressed_rtab_odometry_real_file_loader_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_format": SOURCE_FORMAT,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "rtab_odometry_loader_planning_ref": RTAB_ODOMETRY_LOADER_PLANNING_REF,
        "rtab_odometry_fixture_ref": RTAB_ODOMETRY_FIXTURE_REF,
        "rtab_trajectory_real_file_loader_dryrun_ref": RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "tum_real_file_loader_dryrun_ref": TUM_REAL_FILE_LOADER_DRYRUN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "dryrun_governance_rules": list(DRYRUN_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "positive_cases": [
            {
                "case_ref": c.case_ref,
                "case_kind": c.case_kind,
                "sample_file": c.sample_file,
                "expected_outcome": c.expected_outcome,
                "source_chain": c.source_chain,
            }
            for c in build_positive_cases_v1()
        ],
        "negative_cases": [
            {
                "case_ref": c.case_ref,
                "case_kind": c.case_kind,
                "sample_file": c.sample_file,
                "expected_outcome": c.expected_outcome,
                "source_chain": c.source_chain,
            }
            for c in build_negative_cases_v1()
        ],
        "case_run": case_run,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "conclusions": {
            "rtab_odometry_real_file_loader_dryrun_status": (
                "ready_for_rtab_graph_real_file_loader_planning" if review_ok else "blocked"
            ),
            "rtab_odometry_real_file_loader_dryrun_not_live_runtime": True,
            "local_file_read_used": aggregate["local_file_read_used"],
            "generic_json_parser_reused": True,
            "health_candidate_maps_to_slam_health_candidate": aggregate[
                "health_candidate_maps_to_slam_health_candidate"
            ],
            "rtab_database_read_allowed": False,
            "ros_connected": False,
            "live_rtab_runtime_started": False,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "local_real_rtab_odometry_export_file",
                "admission": "rtab_odometry_file_source_admission",
                "alias_normalization": "node_id_timestamp_translation_tracking_state_aliases",
                "health_mapping": "tracking_state_odometry_quality_to_slam_health_candidate",
                "converter": "rtab_odometry_records_to_generic_json_spatial_trace",
                "output": TARGET_INTERNAL_FORMAT,
                "parser": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "candidates": "pose_motion_health",
            },
            "transition_note": (
                "RTAB odometry pose/motion/health closed loop proven from real export file. Next: "
                "RTAB graph real file loader planning — anchor / relocalization / drift."
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
    result = run_and_review_rtab_map_odometry_real_file_loader_dryrun_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_case_count": checkpoints["positive_case_count"],
                "negative_case_count": checkpoints["negative_case_count"],
                "positive_pass_count": checkpoints["positive_pass_count"],
                "invalid_expected_reject_count": checkpoints["invalid_expected_reject_count"],
                "rtab_record_count": checkpoints["rtab_record_count"],
                "json_trace_item_count": checkpoints["json_trace_item_count"],
                "pose_item_count": checkpoints["pose_item_count"],
                "motion_item_count": checkpoints["motion_item_count"],
                "health_item_count": checkpoints["health_item_count"],
                "health_candidate_maps_to_slam_health_candidate": checkpoints.get(
                    "health_candidate_maps_to_slam_health_candidate"
                ),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
