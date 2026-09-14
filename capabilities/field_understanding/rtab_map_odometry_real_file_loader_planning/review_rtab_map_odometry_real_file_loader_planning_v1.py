# -*- coding: utf-8 -*-
"""RTAB-Map Odometry Real File Loader Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rtab_map_odometry_real_file_loader_planning.rtab_map_odometry_real_file_loader_planning_registry_v1 import (
    REGISTRY_ID,
    build_rtab_map_odometry_real_file_loader_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.rtab_map_odometry_real_file_loader_planning.rtab_map_odometry_real_file_loader_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXPORT_LOADER_PLANNING_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    LOADER_PLANNING_GOVERNANCE_RULES,
    LOADER_PLANNING_PRINCIPLE_ZH,
    LOADER_SCENARIO_GO_KEYS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    RTAB_ODOMETRY_FIXTURE_REF,
    RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SOURCE_FORMAT,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    UNIVERSAL_BLOCKED_OPERATIONS,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rtab_map_odometry_real_file_loader_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "rtab_map_odometry_real_file_loader_planning_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/rtab_map_odometry_real_file_loader_planning/"
    "rtab_map_odometry_real_file_loader_planning_types_v1.py",
    "capabilities/field_understanding/rtab_map_odometry_real_file_loader_planning/"
    "rtab_map_odometry_real_file_loader_planning_registry_v1.py",
    "capabilities/field_understanding/rtab_map_odometry_real_file_loader_planning/"
    "review_rtab_map_odometry_real_file_loader_planning_v1.py",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_sealed_upstream_artifacts(
    matrix: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in matrix.get("sealed_upstream_go_artifacts") or []:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            if entry.get("require_go", True):
                issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        expected_go = entry["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        if entry.get("require_odometry_fixture_go"):
            checks["rtab_odometry_fixture_go_verified"] = go_ok
        if entry.get("require_trajectory_loader_dryrun_go"):
            checks["rtab_trajectory_real_file_loader_dryrun_go_verified"] = go_ok
        if entry.get("require_parser_go"):
            checks["generic_json_spatial_trace_parser_go_verified"] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    if not checks.get("rtab_odometry_fixture_go_verified", False):
        issues.append("rtab_odometry_fixture_go_not_verified")
    if not checks.get("rtab_trajectory_real_file_loader_dryrun_go_verified", False):
        issues.append("rtab_trajectory_real_file_loader_dryrun_go_not_verified")
    if not checks.get("generic_json_spatial_trace_parser_go_verified", False):
        issues.append("generic_json_spatial_trace_parser_go_not_verified")

    return checks, issues


def _policy_flags_ok(shared: Dict[str, Any]) -> Dict[str, bool]:
    admission = shared.get("format_admission_policy") or {}
    mapping = shared.get("mapping_policy") or {}
    health = shared.get("health_mapping_policy") or {}
    boundary = shared.get("boundary_policy") or {}
    safety = shared.get("safety_policy") or {}
    return {
        "format_admission_required": admission.get("format_admission_required") is True,
        "node_id_required": admission.get("node_id_required") is True,
        "timestamp_required": admission.get("timestamp_required") is True,
        "pose_required": admission.get("pose_required") is True,
        "confidence_required": admission.get("confidence_required") is True,
        "tracking_state_required": admission.get("tracking_state_required") is True,
        "source_chain_required": admission.get("source_chain_required") is True,
        "file_origin_metadata_required": admission.get("file_origin_metadata_required") is True,
        "quaternion_validation_required": admission.get("quaternion_validation_required") is True,
        "rtab_database_read_blocked": admission.get("rtab_database_read_blocked") is True,
        "ros_topic_blocked": admission.get("ros_topic_blocked") is True,
        "live_rtab_runtime_blocked": admission.get("live_rtab_runtime_blocked") is True,
        "generic_json_output_required": mapping.get("generic_json_output_required") is True,
        "generic_json_parser_required": mapping.get("generic_json_parser_required") is True,
        "motion_generated_only_from_consecutive_records": (
            mapping.get("motion_generated_only_from_consecutive_records") is True
        ),
        "health_candidate_mapping_required": (
            health.get("health_candidate_mapping_required") is True
        ),
        "health_candidate_candidate_only": health.get("health_candidate_candidate_only") is True,
        "degraded_health_does_not_directly_block_or_allow_action": (
            health.get("degraded_health_does_not_directly_block_or_allow_action") is True
        ),
        "lost_health_does_not_trigger_runtime_shutdown": (
            health.get("lost_health_does_not_trigger_runtime_shutdown") is True
        ),
        "health_does_not_trigger_speech_navigation_fact_write": (
            health.get("health_does_not_trigger_speech_navigation_fact_write") is True
        ),
        "backend_native_output_direct_to_field_blocked": (
            boundary.get("backend_native_output_direct_to_field_blocked") is True
        ),
        "field_task_guidance_replay_path_candidate_only": (
            safety.get("field_task_guidance_replay_candidate_only") is True
        ),
    }


def validate_loader_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_rtab_map_odometry_real_file_loader_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("rtab_map_odometry_real_file_loader_planning_profile") or {}
    if profile.get("controlled_trial_governance_template_ref") != CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    if profile.get("generic_json_spatial_trace_parser_ref") != GENERIC_JSON_SPATIAL_TRACE_PARSER_REF:
        issues.append("generic_json_spatial_trace_parser_ref_mismatch")
    if profile.get("rtab_trajectory_real_file_loader_dryrun_ref") != RTAB_TRAJECTORY_LOADER_DRYRUN_REF:
        issues.append("rtab_trajectory_real_file_loader_dryrun_ref_mismatch")
    if profile.get("rtab_odometry_fixture_ref") != RTAB_ODOMETRY_FIXTURE_REF:
        issues.append("rtab_odometry_fixture_ref_mismatch")
    if profile.get("source_format") != SOURCE_FORMAT:
        issues.append("source_format_mismatch")
    if profile.get("target_internal_format") != TARGET_INTERNAL_FORMAT:
        issues.append("target_internal_format_mismatch")
    if profile.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("target_entrypoint_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    if not matrix.get("rtab_odometry_export_file_policy"):
        issues.append("rtab_odometry_export_file_policy_missing")

    health_policy = (matrix.get("shared_loader_policies") or {}).get("health_mapping_policy")
    if not health_policy:
        issues.append("health_mapping_policy_missing")

    scenarios = matrix.get("loader_scenario_policies") or []
    if len(scenarios) != 6:
        issues.append(f"loader_scenario_count:{len(scenarios)}")

    blocked = next(
        (
            s
            for s in scenarios
            if s.get("scenario_ref") == "invalid_or_unsafe_rtab_odometry_export_blocked"
        ),
        {},
    )
    if not blocked.get("blocked_scenario"):
        issues.append("invalid_or_unsafe_rtab_odometry_export_must_be_blocked_scenario")

    return len(issues) == 0 and registry_ok, issues


def review_rtab_map_odometry_real_file_loader_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_rtab_map_odometry_real_file_loader_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_loader_planning_matrix_v1(matrix)
    registry_ok, registry_issues = validate_registry()

    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    if matrix_ok:
        passed_checks.append("matrix_validation_ok=true")
    else:
        failed_checks.extend(matrix_issues)

    if registry_ok:
        passed_checks.append("registry_validation_ok=true")
    else:
        failed_checks.extend(registry_issues)

    upstream_checks, upstream_issues = review_sealed_upstream_artifacts(matrix)
    failed_checks.extend(upstream_issues)

    scenario_go = matrix.get("loader_scenario_go_map") or {}
    shared = matrix.get("shared_loader_policies") or {}
    policy_flags = _policy_flags_ok(shared)

    template_ok = (
        matrix.get("rtab_map_odometry_real_file_loader_planning_profile", {}).get(
            "controlled_trial_governance_template_ref"
        )
        == TEMPLATE_ID
    )

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "rtab_odometry_export_file_policy_count": 1
        if matrix.get("rtab_odometry_export_file_policy")
        else 0,
        "health_mapping_policy_count": 1 if shared.get("health_mapping_policy") else 0,
        "loader_scenario_count": len(matrix.get("loader_scenario_policies") or []),
        "rtab_trajectory_real_file_loader_dryrun_go_verified": upstream_checks.get(
            "rtab_trajectory_real_file_loader_dryrun_go_verified", False
        ),
        "rtab_odometry_fixture_go_verified": upstream_checks.get(
            "rtab_odometry_fixture_go_verified", False
        ),
        "generic_json_spatial_trace_parser_go_verified": upstream_checks.get(
            "generic_json_spatial_trace_parser_go_verified", False
        ),
        "controlled_trial_governance_template_ref_ok": template_ok,
        **scenario_go,
        **policy_flags,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "source_format_locked": SOURCE_FORMAT,
        "target_internal_format_locked": TARGET_INTERNAL_FORMAT,
        "target_entrypoint_locked": TARGET_ENTRYPOINT,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "planning_profile_count_eq_1": review_checkpoints["planning_profile_count"] == 1,
        "rtab_odometry_export_file_policy_count_eq_1": (
            review_checkpoints["rtab_odometry_export_file_policy_count"] == 1
        ),
        "health_mapping_policy_count_eq_1": (
            review_checkpoints["health_mapping_policy_count"] == 1
        ),
        "loader_scenario_count_eq_6": review_checkpoints["loader_scenario_count"] == 6,
        "rtab_trajectory_real_file_loader_dryrun_go_verified": (
            review_checkpoints["rtab_trajectory_real_file_loader_dryrun_go_verified"] is True
        ),
        "rtab_odometry_fixture_go_verified": (
            review_checkpoints["rtab_odometry_fixture_go_verified"] is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            review_checkpoints["generic_json_spatial_trace_parser_go_verified"] is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        **{key: review_checkpoints.get(key) is True for key in LOADER_SCENARIO_GO_KEYS},
        "format_admission_required": policy_flags["format_admission_required"] is True,
        "node_id_required": policy_flags["node_id_required"] is True,
        "timestamp_required": policy_flags["timestamp_required"] is True,
        "pose_required": policy_flags["pose_required"] is True,
        "confidence_required": policy_flags["confidence_required"] is True,
        "tracking_state_required": policy_flags["tracking_state_required"] is True,
        "source_chain_required": policy_flags["source_chain_required"] is True,
        "file_origin_metadata_required": policy_flags["file_origin_metadata_required"] is True,
        "quaternion_validation_required": policy_flags["quaternion_validation_required"] is True,
        "generic_json_output_required": policy_flags["generic_json_output_required"] is True,
        "generic_json_parser_required": policy_flags["generic_json_parser_required"] is True,
        "backend_native_output_direct_to_field_blocked": (
            policy_flags["backend_native_output_direct_to_field_blocked"] is True
        ),
        "rtab_database_read_blocked": policy_flags["rtab_database_read_blocked"] is True,
        "ros_topic_blocked": policy_flags["ros_topic_blocked"] is True,
        "live_rtab_runtime_blocked": policy_flags["live_rtab_runtime_blocked"] is True,
        "motion_generated_only_from_consecutive_records": (
            policy_flags["motion_generated_only_from_consecutive_records"] is True
        ),
        "health_candidate_mapping_required": (
            policy_flags["health_candidate_mapping_required"] is True
        ),
        "health_candidate_candidate_only": (
            policy_flags["health_candidate_candidate_only"] is True
        ),
        "degraded_health_does_not_directly_block_or_allow_action": (
            policy_flags["degraded_health_does_not_directly_block_or_allow_action"] is True
        ),
        "lost_health_does_not_trigger_runtime_shutdown": (
            policy_flags["lost_health_does_not_trigger_runtime_shutdown"] is True
        ),
        "health_does_not_trigger_speech_navigation_fact_write": (
            policy_flags["health_does_not_trigger_speech_navigation_fact_write"] is True
        ),
        "field_task_guidance_replay_path_candidate_only": (
            policy_flags["field_task_guidance_replay_path_candidate_only"] is True
        ),
        "real_file_conversion_execution_allowed_false": (
            review_checkpoints["real_file_conversion_execution_allowed"] is False
        ),
        "real_file_replay_execution_allowed_false": (
            review_checkpoints["real_file_replay_execution_allowed"] is False
        ),
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"]
        is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "ros_connected_false": review_checkpoints["ros_connected"] is False,
        "camera_connected_false": review_checkpoints["camera_connected"] is False,
        "imu_connected_false": review_checkpoints["imu_connected"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"]
        is False,
        "commercial_runtime_approved_false": review_checkpoints["commercial_runtime_approved"]
        is False,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = matrix_ok and registry_ok and blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RTAB-Map Odometry Real File Loader Planning Review",
        "lifecycle_variant": "compressed_rtab_odometry_real_file_loader_planning_review",
        "loader_planning_principle_zh": LOADER_PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_format": SOURCE_FORMAT,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "export_loader_planning_ref": EXPORT_LOADER_PLANNING_REF,
        "rtab_odometry_fixture_ref": RTAB_ODOMETRY_FIXTURE_REF,
        "rtab_trajectory_real_file_loader_dryrun_ref": RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "loader_planning_governance_rules": list(LOADER_PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "rtab_odometry_loader_planning_matrix": matrix,
        "conclusions": {
            "rtab_odometry_loader_planning_status": (
                "ready_for_rtab_odometry_real_file_loader_dryrun" if review_ok else "blocked"
            ),
            "rtab_odometry_loader_planning_not_conversion_execution": True,
            "rtab_odometry_loader_planning_not_live_runtime": True,
            "rtab_database_read_blocked": True,
            "ros_topic_blocked": True,
            "health_candidate_candidate_only": True,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "rtab_map_odometry_export_file",
                "admission": "format_admission",
                "converter": "rtab_odometry_to_json_trace_converter_planning",
                "candidates": "pose_motion_health",
                "output": TARGET_INTERNAL_FORMAT,
                "parser": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RTAB odometry loader planning baseline locked with health mapping. Next: RTAB "
                "odometry real file loader dry-run — validate pose/motion/health into parser replay."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_rtab_map_odometry_real_file_loader_planning_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "planning_profile_count": checkpoints["planning_profile_count"],
                "rtab_odometry_export_file_policy_count": checkpoints[
                    "rtab_odometry_export_file_policy_count"
                ],
                "health_mapping_policy_count": checkpoints["health_mapping_policy_count"],
                "loader_scenario_count": checkpoints["loader_scenario_count"],
                "rtab_odometry_fixture_go_verified": checkpoints.get(
                    "rtab_odometry_fixture_go_verified"
                ),
                "rtab_trajectory_real_file_loader_dryrun_go_verified": checkpoints.get(
                    "rtab_trajectory_real_file_loader_dryrun_go_verified"
                ),
                "health_candidate_mapping_required": checkpoints.get(
                    "health_candidate_mapping_required"
                ),
                "invalid_or_unsafe_rtab_odometry_export_blocked": checkpoints.get(
                    "invalid_or_unsafe_rtab_odometry_export_blocked"
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
