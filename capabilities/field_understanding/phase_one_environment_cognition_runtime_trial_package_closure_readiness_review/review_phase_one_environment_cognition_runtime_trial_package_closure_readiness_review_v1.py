# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Package Closure Readiness Review — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_package_closure_readiness_review.phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_registry_v1 import (
    FAILURE_HANDLING_POLICY_REF,
    OBSERVATION_LOG_POLICY_REF,
    REGISTRY_ID,
    ROLLBACK_POLICY_REF,
    _ISSUANCE_ARTIFACT_REL,
    _PACKAGE_BOUNDARY_ARTIFACT_REL,
    _PLANNING_ARTIFACT_REL,
    _REQUEST_ARTIFACT_REL,
    _STAGE_REQUIRED_CHECKS,
    build_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_package_closure_readiness_review.phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CLOSURE_STAGE_REFS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_BOUNDARY_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    RUNTIME_TRIAL_MODE,
    SCENARIO_READINESS_GO_KEYS,
    SCENARIO_READINESS_REFS,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review/"
    "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review/"
    "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review/"
    "review_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1.py",
)


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    path = _REPO_ROOT / rel
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _artifact_bool(artifact: Dict[str, Any], key: str) -> bool:
    go = artifact.get("go_conditions") or {}
    if key in go:
        return go[key] is True
    checkpoints = artifact.get("review_checkpoints") or {}
    if key in checkpoints:
        val = checkpoints[key]
        return val is True or val is False and key.endswith("_false") and val is False
    if key.endswith("_false"):
        base = key[: -len("_false")]
        return checkpoints.get(base) is False or go.get(key) is True
    return False


def _verify_planning_stage(artifact: Optional[Dict[str, Any]]) -> Tuple[bool, Dict[str, bool]]:
    checks: Dict[str, bool] = {}
    if not artifact:
        return False, checks
    checks["planning_go_verified"] = artifact.get("final_decision") == (
        "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_GO"
    )
    checks["admission_level_declared_for_all"] = _artifact_bool(
        artifact, "admission_level_declared_for_all"
    )
    checkpoints = artifact.get("review_checkpoints") or {}
    checks["rollback_policy_required"] = checkpoints.get("rollback_policy_required") is True
    checks["observation_log_policy_required"] = (
        checkpoints.get("observation_log_policy_required") is True
    )
    checks["owner_approval_required"] = checkpoints.get("owner_approval_required") is True
    checks["runtime_activation_allowed_false"] = checkpoints.get("runtime_activation_allowed") is False
    closed = all(checks.get(k, False) for k in _STAGE_REQUIRED_CHECKS["planning_stage_closed"])
    return closed, checks


def _verify_request_stage(artifact: Optional[Dict[str, Any]]) -> Tuple[bool, Dict[str, bool]]:
    checks: Dict[str, bool] = {}
    if not artifact:
        return False, checks
    checks["request_go_verified"] = artifact.get("final_decision") == (
        "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_REQUEST_GO"
    )
    checks["admission_level_preserved_for_all"] = _artifact_bool(
        artifact, "admission_level_preserved_for_all"
    )
    checkpoints = artifact.get("review_checkpoints") or {}
    checks["blocked_scenario_not_requestable"] = (
        checkpoints.get("blocked_scenario_not_requestable") is True
    )
    checks["observation_only_not_movement_trial"] = (
        checkpoints.get("observation_only_not_movement_trial") is True
    )
    checks["owner_approval_issued_false"] = checkpoints.get("owner_approval_issued") is False
    closed = all(checks.get(k, False) for k in _STAGE_REQUIRED_CHECKS["owner_approval_request_stage_closed"])
    return closed, checks


def _verify_issuance_stage(artifact: Optional[Dict[str, Any]]) -> Tuple[bool, Dict[str, bool]]:
    checks: Dict[str, bool] = {}
    if not artifact:
        return False, checks
    checks["issuance_go_verified"] = artifact.get("final_decision") == (
        "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_ISSUANCE_GO"
    )
    checks["request_scope_preserved_for_all"] = _artifact_bool(
        artifact, "request_scope_preserved_for_all"
    )
    checkpoints = artifact.get("review_checkpoints") or {}
    checks["blocked_scenario_not_issued"] = checkpoints.get("blocked_scenario_not_issued") is True
    checks["observation_only_not_upgraded"] = checkpoints.get("observation_only_not_upgraded") is True
    checks["issuance_not_runtime_activation"] = checkpoints.get("issuance_not_runtime_activation") is True
    closed = all(checks.get(k, False) for k in _STAGE_REQUIRED_CHECKS["owner_approval_issuance_stage_closed"])
    return closed, checks


def _verify_package_boundary_stage(artifact: Optional[Dict[str, Any]]) -> Tuple[bool, Dict[str, bool]]:
    checks: Dict[str, bool] = {}
    if not artifact:
        return False, checks
    checks["package_boundary_go_verified"] = artifact.get("final_decision") == (
        "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_BOUNDARY_PLANNING_GO"
    )
    checks["package_scope_preserved_for_all"] = _artifact_bool(
        artifact, "package_scope_preserved_for_all"
    )
    checks["issued_status_preserved_for_all"] = _artifact_bool(
        artifact, "issued_status_preserved_for_all"
    )
    checks["blocked_operations_declared_for_all"] = _artifact_bool(
        artifact, "blocked_operations_declared_for_all"
    )
    checks["allowed_operations_candidate_only"] = _artifact_bool(
        artifact, "allowed_operations_candidate_only"
    )
    checkpoints = artifact.get("review_checkpoints") or {}
    checks["trial_runtime_started_false"] = checkpoints.get("trial_runtime_started") is False
    closed = all(checks.get(k, False) for k in _STAGE_REQUIRED_CHECKS["package_boundary_stage_closed"])
    return closed, checks


def _package_items_from_boundary(artifact: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not artifact:
        return []
    matrix = artifact.get("package_boundary_matrix") or {}
    return list(matrix.get("trial_package_items") or [])


def _blocked_ops_from_packages(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    universal = set(UNIVERSAL_BLOCKED_OPERATIONS)
    all_declared = True
    result = {
        "direct_action_blocked_for_all": True,
        "direct_speech_blocked_for_all": True,
        "direct_fact_write_blocked_for_all": True,
        "real_navigation_blocked_for_all": True,
        "live_sensor_trigger_blocked_for_all": True,
        "blocked_operations_declared_for_all": True,
    }
    for item in items:
        blocked = set(item.get("blocked_operations") or ())
        if not blocked:
            all_declared = False
        for op in ("direct_action", "direct_speech_tts", "direct_fact_write", "real_navigation"):
            key = op.replace("_tts", "_blocked_for_all").replace("direct_", "direct_")
            if op == "direct_speech_tts":
                key = "direct_speech_blocked_for_all"
            elif op == "direct_action":
                key = "direct_action_blocked_for_all"
            elif op == "direct_fact_write":
                key = "direct_fact_write_blocked_for_all"
            elif op == "real_navigation":
                key = "real_navigation_blocked_for_all"
            if op not in blocked:
                result[key] = False
        if "live_sensor_trigger" not in blocked:
            result["live_sensor_trigger_blocked_for_all"] = False
        if not universal.issubset(blocked):
            all_declared = False
    result["blocked_operations_declared_for_all"] = all_declared
    return result


def _verify_scenario_scope_preserved(
    scenarios: List[Dict[str, Any]],
    package_items: List[Dict[str, Any]],
) -> bool:
    by_ref = {i.get("package_ref"): i for i in package_items}
    for scenario in scenarios:
        pkg = by_ref.get(scenario.get("package_ref"))
        if not pkg:
            return False
        if pkg.get("package_scope") != scenario.get("package_scope"):
            return False
    return True


def _bindings_ok_for_ready(scenarios: List[Dict[str, Any]]) -> Dict[str, bool]:
    rollback_ok = True
    obs_ok = True
    failure_ok = True
    for scenario in scenarios:
        if scenario.get("readiness_ok") is False:
            continue
        if scenario.get("rollback_policy_ref") != ROLLBACK_POLICY_REF:
            rollback_ok = False
        if scenario.get("observation_log_policy_ref") != OBSERVATION_LOG_POLICY_REF:
            obs_ok = False
        if scenario.get("failure_handling_policy_ref") != FAILURE_HANDLING_POLICY_REF:
            failure_ok = False
    return {
        "rollback_policy_bound_for_ready_scenarios": rollback_ok,
        "observation_log_policy_bound_for_ready_scenarios": obs_ok,
        "failure_handling_policy_bound_for_ready_scenarios": failure_ok,
    }


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

        artifact_rel = entry.get("artifact_rel")
        if not artifact_rel:
            continue

        artifact, exists = _load_upstream_artifact(artifact_rel)
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

        if entry.get("require_sealed") and artifact:
            sealed = (
                artifact.get("conclusions", {}).get("phase_one_environment_cognition_chain_status")
                == "sealed"
                or artifact.get("conclusions", {}).get("master_chain_sealed") is True
            )
            checks[f"{phase_ref}.phase_one_chain_sealed"] = sealed
            if not sealed:
                issues.append(f"phase_one_chain_not_sealed:{phase_ref}")

    checks["sealed_phase_one_chain_verified"] = (
        checks.get(f"{PHASE_ONE_CHAIN_REF}.go_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.phase_one_chain_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.module_present", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.artifact_present", False)
    )
    if not checks["sealed_phase_one_chain_verified"]:
        issues.append("sealed_phase_one_chain_not_verified")

    return checks, issues


def verify_closure_stages_from_artifacts() -> Tuple[Dict[str, bool], Dict[str, bool], List[str]]:
    issues: List[str] = []
    stage_closed: Dict[str, bool] = {}
    stage_checks: Dict[str, bool] = {}

    planning_art = _load_json(_PLANNING_ARTIFACT_REL)
    request_art = _load_json(_REQUEST_ARTIFACT_REL)
    issuance_art = _load_json(_ISSUANCE_ARTIFACT_REL)
    boundary_art = _load_json(_PACKAGE_BOUNDARY_ARTIFACT_REL)

    closed, checks = _verify_planning_stage(planning_art)
    stage_closed["planning_stage_closed"] = closed
    stage_checks.update({f"planning.{k}": v for k, v in checks.items()})
    if not closed:
        issues.append("planning_stage_not_closed")

    closed, checks = _verify_request_stage(request_art)
    stage_closed["owner_approval_request_stage_closed"] = closed
    stage_checks.update({f"request.{k}": v for k, v in checks.items()})
    if not closed:
        issues.append("owner_approval_request_stage_not_closed")

    closed, checks = _verify_issuance_stage(issuance_art)
    stage_closed["owner_approval_issuance_stage_closed"] = closed
    stage_checks.update({f"issuance.{k}": v for k, v in checks.items()})
    if not closed:
        issues.append("owner_approval_issuance_stage_not_closed")

    closed, checks = _verify_package_boundary_stage(boundary_art)
    stage_closed["package_boundary_stage_closed"] = closed
    stage_checks.update({f"package_boundary.{k}": v for k, v in checks.items()})
    if not closed:
        issues.append("package_boundary_stage_not_closed")

    stage_checks["planning_go_verified"] = stage_checks.get("planning.planning_go_verified", False)
    stage_checks["owner_approval_request_go_verified"] = stage_checks.get(
        "request.request_go_verified", False
    )
    stage_checks["owner_approval_issuance_go_verified"] = stage_checks.get(
        "issuance.issuance_go_verified", False
    )
    stage_checks["package_boundary_go_verified"] = stage_checks.get(
        "package_boundary.package_boundary_go_verified", False
    )

    return stage_closed, stage_checks, issues


def validate_closure_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    if len(matrix.get("closure_stages") or []) != 4:
        issues.append("closure_stage_count_not_4")
    if len(matrix.get("scenario_readiness") or []) != 6:
        issues.append("scenario_readiness_count_not_6")

    profile = matrix.get("closure_readiness_profile") or {}
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    return len(issues) == 0 and registry_ok, issues


def review_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_matrix_v1()
    matrix_ok, matrix_issues = validate_closure_matrix_v1(matrix)
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

    stage_closed, stage_checks, stage_issues = verify_closure_stages_from_artifacts()
    failed_checks.extend(stage_issues)

    boundary_art = _load_json(_PACKAGE_BOUNDARY_ARTIFACT_REL)
    package_items = _package_items_from_boundary(boundary_art)
    scenarios = matrix.get("scenario_readiness") or []
    governance = matrix.get("governance_readiness") or {}
    boundary = matrix.get("boundary_readiness") or {}
    scenario_go = matrix.get("scenario_readiness_go_map") or {}

    scope_preserved = _verify_scenario_scope_preserved(scenarios, package_items)
    blocked_ops = _blocked_ops_from_packages(package_items)
    binding_checks = _bindings_ok_for_ready(scenarios)

    subway = next((s for s in scenarios if s.get("scenario_ref") == "subway_enter_station_package"), {})
    gps = next((s for s in scenarios if s.get("scenario_ref") == "gps_slam_conflict_package"), {})

    review_checkpoints: Dict[str, Any] = {
        "closure_readiness_profile_count": 1,
        "closure_stage_count": len(matrix.get("closure_stages") or []),
        "scenario_readiness_count": len(scenarios),
        **stage_closed,
        "planning_go_verified": stage_checks.get("planning_go_verified", False),
        "owner_approval_request_go_verified": stage_checks.get("owner_approval_request_go_verified", False),
        "owner_approval_issuance_go_verified": stage_checks.get("owner_approval_issuance_go_verified", False),
        "package_boundary_go_verified": stage_checks.get("package_boundary_go_verified", False),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        **scenario_go,
        "scenario_scope_preserved_for_all": scope_preserved,
        "blocked_scenario_remains_blocked": (
            gps.get("package_scope") == "blocked" and gps.get("readiness_status") == "blocked_preserved"
        ),
        "observation_only_not_upgraded": governance.get("observation_only_not_upgraded"),
        "constrained_item_constraints_preserved": bool(subway.get("readiness_constraints")),
        "low_risk_candidates_do_not_start_runtime": governance.get("low_risk_candidates_do_not_start_runtime"),
        **binding_checks,
        "source_chain_required": all(s.get("source_chain") == SOURCE_CHAIN for s in scenarios),
        "upstream_refs_required": all(s.get("upstream_refs") for s in scenarios),
        "allowed_operations_candidate_only": _artifact_bool(boundary_art or {}, "allowed_operations_candidate_only"),
        **blocked_ops,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "closure_readiness_profile_count_eq_1": review_checkpoints["closure_readiness_profile_count"] == 1,
        "closure_stage_count_eq_4": review_checkpoints["closure_stage_count"] == 4,
        "scenario_readiness_count_eq_6": review_checkpoints["scenario_readiness_count"] == 6,
        "planning_stage_closed": review_checkpoints.get("planning_stage_closed") is True,
        "owner_approval_request_stage_closed": (
            review_checkpoints.get("owner_approval_request_stage_closed") is True
        ),
        "owner_approval_issuance_stage_closed": (
            review_checkpoints.get("owner_approval_issuance_stage_closed") is True
        ),
        "package_boundary_stage_closed": review_checkpoints.get("package_boundary_stage_closed") is True,
        "planning_go_verified": review_checkpoints["planning_go_verified"] is True,
        "owner_approval_request_go_verified": review_checkpoints["owner_approval_request_go_verified"] is True,
        "owner_approval_issuance_go_verified": review_checkpoints["owner_approval_issuance_go_verified"] is True,
        "package_boundary_go_verified": review_checkpoints["package_boundary_go_verified"] is True,
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        **{key: review_checkpoints.get(key) is True for key in SCENARIO_READINESS_GO_KEYS},
        "scenario_scope_preserved_for_all": scope_preserved is True,
        "blocked_scenario_remains_blocked": review_checkpoints["blocked_scenario_remains_blocked"] is True,
        "observation_only_not_upgraded": review_checkpoints["observation_only_not_upgraded"] is True,
        "constrained_item_constraints_preserved": (
            review_checkpoints["constrained_item_constraints_preserved"] is True
        ),
        "low_risk_candidates_do_not_start_runtime": (
            review_checkpoints["low_risk_candidates_do_not_start_runtime"] is True
        ),
        "rollback_policy_bound_for_ready_scenarios": (
            binding_checks["rollback_policy_bound_for_ready_scenarios"] is True
        ),
        "observation_log_policy_bound_for_ready_scenarios": (
            binding_checks["observation_log_policy_bound_for_ready_scenarios"] is True
        ),
        "failure_handling_policy_bound_for_ready_scenarios": (
            binding_checks["failure_handling_policy_bound_for_ready_scenarios"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "allowed_operations_candidate_only": review_checkpoints["allowed_operations_candidate_only"] is True,
        "blocked_operations_declared_for_all": blocked_ops["blocked_operations_declared_for_all"] is True,
        "direct_action_blocked_for_all": blocked_ops["direct_action_blocked_for_all"] is True,
        "direct_speech_blocked_for_all": blocked_ops["direct_speech_blocked_for_all"] is True,
        "direct_fact_write_blocked_for_all": blocked_ops["direct_fact_write_blocked_for_all"] is True,
        "real_navigation_blocked_for_all": blocked_ops["real_navigation_blocked_for_all"] is True,
        "live_sensor_trigger_blocked_for_all": blocked_ops["live_sensor_trigger_blocked_for_all"] is True,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "trial_runtime_started_false": review_checkpoints["trial_runtime_started"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Package Closure Readiness Review",
        "lifecycle_variant": "compressed_runtime_trial_pre_package_closure_readiness_review",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "pre_runtime_trial_chain_refs": [PLANNING_REF, OWNER_APPROVAL_REQUEST_REF, OWNER_APPROVAL_ISSUANCE_REF, PACKAGE_BOUNDARY_REF],
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "closure_stage_verification": stage_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "closure_readiness_matrix": matrix,
        "conclusions": {
            "pre_runtime_trial_package_status": "sealed" if review_ok else "blocked",
            "runtime_trial_pre_package_sealed": review_ok,
            "runtime_activation_deferred": True,
            "trial_runtime_started": False,
            "pre_package_summary": {
                "planning": PLANNING_REF,
                "request": OWNER_APPROVAL_REQUEST_REF,
                "issuance": OWNER_APPROVAL_ISSUANCE_REF,
                "package_boundary": PACKAGE_BOUNDARY_REF,
                "ready_for_pre_runtime_trial_review": [
                    "mall_find_entrance_package",
                    "home_return_package",
                ],
                "ready_with_constraints": ["subway_enter_station_package"],
                "observation_only_ready": [
                    "stadium_concert_ticket_gate_package",
                    "plaza_market_crowd_package",
                ],
                "blocked_preserved": ["gps_slam_conflict_package"],
            },
            "next_step_note": (
                "Pre-runtime trial package sealed. Next decision: whether to proceed with "
                "controlled trial issuance package — still not runtime activation."
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
    result = review_phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "closure_readiness_profile_count": checkpoints["closure_readiness_profile_count"],
                "closure_stage_count": checkpoints["closure_stage_count"],
                "planning_stage_closed": checkpoints.get("planning_stage_closed"),
                "mall_find_entrance_ready_for_pre_runtime_trial_review": checkpoints.get(
                    "mall_find_entrance_ready_for_pre_runtime_trial_review"
                ),
                "gps_slam_conflict_blocked_preserved": checkpoints.get("gps_slam_conflict_blocked_preserved"),
                "trial_runtime_started": checkpoints.get("trial_runtime_started"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
