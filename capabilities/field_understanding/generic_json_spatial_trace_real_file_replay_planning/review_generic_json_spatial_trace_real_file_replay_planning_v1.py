# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Controlled Replay Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.generic_json_spatial_trace_real_file_replay_planning.generic_json_spatial_trace_real_file_replay_planning_registry_v1 import (
    REGISTRY_ID,
    build_generic_json_spatial_trace_real_file_replay_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.generic_json_spatial_trace_real_file_replay_planning.generic_json_spatial_trace_real_file_replay_planning_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    INPUT_SOURCE_GO_KEYS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_STATUS,
    REPLAY_PLANNING_GOVERNANCE_RULES,
    REPLAY_PLANNING_PRINCIPLE_ZH,
    REPLAY_SCENARIO_GO_KEYS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
    UNIVERSAL_BLOCKED_OPERATIONS,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "generic_json_spatial_trace_real_file_replay_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "generic_json_spatial_trace_real_file_replay_planning_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_planning/"
    "generic_json_spatial_trace_real_file_replay_planning_types_v1.py",
    "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_planning/"
    "generic_json_spatial_trace_real_file_replay_planning_registry_v1.py",
    "capabilities/field_understanding/generic_json_spatial_trace_real_file_replay_planning/"
    "review_generic_json_spatial_trace_real_file_replay_planning_v1.py",
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

        if entry.get("require_parser_go"):
            checks["generic_json_spatial_trace_parser_go_verified"] = go_ok

        if entry.get("require_phase_one_chain_sealed") and artifact:
            sealed = (
                artifact.get("conclusions", {}).get("phase_one_environment_cognition_chain_status")
                == "sealed"
                or artifact.get("conclusions", {}).get("master_chain_sealed") is True
            )
            checks["phase_one_chain_sealed_verified"] = sealed
            if not sealed:
                issues.append("phase_one_chain_not_sealed")

        if entry.get("require_governance_sealed") and artifact:
            gov_sealed = (
                artifact.get("conclusions", {}).get("governance_closure_status") == "sealed"
                or artifact.get("final_decision")
                == "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
            )
            checks["controlled_runtime_trial_governance_sealed_verified"] = gov_sealed
            if not gov_sealed:
                issues.append("controlled_runtime_trial_governance_not_sealed")

    if not checks.get("generic_json_spatial_trace_parser_go_verified", False):
        issues.append("generic_json_spatial_trace_parser_go_not_verified")
    if not checks.get("phase_one_chain_sealed_verified", False):
        issues.append("phase_one_chain_sealed_not_verified")
    if not checks.get("controlled_runtime_trial_governance_sealed_verified", False):
        issues.append("controlled_runtime_trial_governance_sealed_not_verified")

    return checks, issues


def _policy_flags_ok(shared: Dict[str, Any]) -> Dict[str, bool]:
    admission = shared.get("format_admission_policy") or {}
    boundary = shared.get("replay_boundary_policy") or {}
    safety = shared.get("safety_policy") or {}
    return {
        "real_file_source_admission_required": admission.get("real_file_source_admission_required") is True,
        "file_origin_metadata_required": admission.get("file_origin_metadata_required") is True,
        "source_chain_required": admission.get("source_chain_required") is True,
        "unsupported_candidate_type_rejected": admission.get("unsupported_candidate_type_rejected") is True,
        "missing_source_chain_rejected": admission.get("missing_source_chain_rejected") is True,
        "generic_json_parser_reused": boundary.get("generic_json_parser_reused") is True,
        "backend_native_output_direct_to_field_blocked": (
            boundary.get("backend_native_output_direct_to_field_blocked") is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            safety.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "gps_does_not_override_field_identity": safety.get("gps_does_not_override_field_identity") is True,
        "candidate_only_replay_path_enforced": safety.get("candidate_only_replay_path_enforced") is True,
    }


def _input_sources_ok(policies: List[Dict[str, Any]]) -> Dict[str, bool]:
    checks = {
        "all_sources_require_parser_reuse": True,
        "all_sources_require_source_admission": True,
        "all_sources_require_file_origin_metadata": True,
    }
    for policy in policies:
        if not policy.get("requires_parser_reuse"):
            checks["all_sources_require_parser_reuse"] = False
        if not policy.get("requires_source_admission"):
            checks["all_sources_require_source_admission"] = False
        if not policy.get("requires_file_origin_metadata"):
            checks["all_sources_require_file_origin_metadata"] = False
    return checks


def validate_replay_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_generic_json_spatial_trace_real_file_replay_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("generic_json_spatial_trace_real_file_replay_planning_profile") or {}
    if profile.get("controlled_trial_governance_template_ref") != CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    if profile.get("generic_json_spatial_trace_parser_ref") != GENERIC_JSON_SPATIAL_TRACE_PARSER_REF:
        issues.append("generic_json_spatial_trace_parser_ref_mismatch")
    if profile.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("target_entrypoint_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    input_sources = matrix.get("real_file_input_source_policies") or []
    if len(input_sources) != 5:
        issues.append(f"real_file_input_source_policy_count:{len(input_sources)}")

    scenarios = matrix.get("replay_scenario_policies") or []
    if len(scenarios) != 6:
        issues.append(f"replay_scenario_count:{len(scenarios)}")

    blocked = next(
        (s for s in scenarios if s.get("scenario_ref") == "invalid_or_untrusted_file_blocked"),
        {},
    )
    if not blocked.get("blocked_scenario"):
        issues.append("invalid_or_untrusted_file_must_be_blocked_scenario")

    return len(issues) == 0 and registry_ok, issues


def review_generic_json_spatial_trace_real_file_replay_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_generic_json_spatial_trace_real_file_replay_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_replay_planning_matrix_v1(matrix)
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

    input_sources = matrix.get("real_file_input_source_policies") or []
    input_go = matrix.get("input_source_go_map") or {}
    scenario_go = matrix.get("replay_scenario_go_map") or {}
    shared = matrix.get("shared_replay_policies") or {}
    policy_flags = _policy_flags_ok(shared)
    input_checks = _input_sources_ok(input_sources)

    template_ok = (
        matrix.get("generic_json_spatial_trace_real_file_replay_planning_profile", {}).get(
            "controlled_trial_governance_template_ref"
        )
        == TEMPLATE_ID
    )

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "real_file_input_source_policy_count": len(input_sources),
        "replay_scenario_count": len(matrix.get("replay_scenario_policies") or []),
        "controlled_trial_governance_template_ref_ok": template_ok,
        "phase_one_chain_sealed_verified": upstream_checks.get("phase_one_chain_sealed_verified", False),
        "controlled_runtime_trial_governance_sealed_verified": upstream_checks.get(
            "controlled_runtime_trial_governance_sealed_verified", False
        ),
        "generic_json_spatial_trace_parser_go_verified": upstream_checks.get(
            "generic_json_spatial_trace_parser_go_verified", False
        ),
        **input_go,
        **scenario_go,
        **policy_flags,
        **input_checks,
        "candidate_only_enforced": CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        "controlled_runtime_trial_governance_status_locked": CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
        "target_entrypoint_locked": TARGET_ENTRYPOINT,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "planning_profile_count_eq_1": review_checkpoints["planning_profile_count"] == 1,
        "real_file_input_source_policy_count_eq_5": (
            review_checkpoints["real_file_input_source_policy_count"] == 5
        ),
        "replay_scenario_count_eq_6": review_checkpoints["replay_scenario_count"] == 6,
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        "phase_one_chain_sealed_verified": (
            review_checkpoints["phase_one_chain_sealed_verified"] is True
        ),
        "controlled_runtime_trial_governance_sealed_verified": (
            review_checkpoints["controlled_runtime_trial_governance_sealed_verified"] is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            review_checkpoints["generic_json_spatial_trace_parser_go_verified"] is True
        ),
        **{key: review_checkpoints.get(key) is True for key in INPUT_SOURCE_GO_KEYS},
        **{key: review_checkpoints.get(key) is True for key in REPLAY_SCENARIO_GO_KEYS},
        "real_file_source_admission_required": policy_flags["real_file_source_admission_required"] is True,
        "file_origin_metadata_required": policy_flags["file_origin_metadata_required"] is True,
        "source_chain_required": policy_flags["source_chain_required"] is True,
        "generic_json_parser_reused": policy_flags["generic_json_parser_reused"] is True,
        "backend_native_output_direct_to_field_blocked": (
            policy_flags["backend_native_output_direct_to_field_blocked"] is True
        ),
        "unsupported_candidate_type_rejected": (
            policy_flags["unsupported_candidate_type_rejected"] is True
        ),
        "missing_source_chain_rejected": policy_flags["missing_source_chain_rejected"] is True,
        "relocalization_does_not_restore_runtime_trust": (
            policy_flags["relocalization_does_not_restore_runtime_trust"] is True
        ),
        "gps_does_not_override_field_identity": (
            policy_flags["gps_does_not_override_field_identity"] is True
        ),
        "candidate_only_replay_path_enforced": (
            policy_flags["candidate_only_replay_path_enforced"] is True
        ),
        "real_file_replay_execution_allowed_false": (
            review_checkpoints["real_file_replay_execution_allowed"] is False
        ),
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "ros_connected_false": review_checkpoints["ros_connected"] is False,
        "camera_connected_false": review_checkpoints["camera_connected"] is False,
        "imu_connected_false": review_checkpoints["imu_connected"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
        "commercial_runtime_approved_false": review_checkpoints["commercial_runtime_approved"] is False,
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
        "step": "Generic JSON Spatial Trace Real File Controlled Replay Planning Review",
        "lifecycle_variant": "compressed_real_file_replay_planning_review",
        "replay_planning_principle_zh": REPLAY_PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "controlled_runtime_trial_governance_status": CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_STATUS,
        "replay_planning_governance_rules": list(REPLAY_PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "replay_planning_matrix": matrix,
        "conclusions": {
            "real_file_replay_planning_status": "ready_for_controlled_replay_dryrun" if review_ok else "blocked",
            "real_file_replay_planning_not_replay_execution": True,
            "real_file_replay_planning_not_runtime_activation": True,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "real_file_or_exported_trace",
                "parser": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "fusion": "spatial_odometry_fusion_candidate",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "Next: Real File Controlled Replay DryRun with local real sample files — "
                "still no live runtime."
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
    result = review_generic_json_spatial_trace_real_file_replay_planning_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "planning_profile_count": checkpoints["planning_profile_count"],
                "real_file_input_source_policy_count": checkpoints["real_file_input_source_policy_count"],
                "replay_scenario_count": checkpoints["replay_scenario_count"],
                "generic_json_spatial_trace_parser_go_verified": checkpoints.get(
                    "generic_json_spatial_trace_parser_go_verified"
                ),
                "invalid_or_untrusted_file_blocked": checkpoints.get("invalid_or_untrusted_file_blocked"),
                "real_file_replay_execution_allowed": checkpoints.get("real_file_replay_execution_allowed"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
