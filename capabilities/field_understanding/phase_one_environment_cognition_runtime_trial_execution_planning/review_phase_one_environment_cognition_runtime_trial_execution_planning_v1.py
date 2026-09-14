# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Execution Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_execution_planning.phase_one_environment_cognition_runtime_trial_execution_planning_registry_v1 import (
    FAILURE_HANDLING_PLAN_REF,
    ISSUANCE_PACKAGE_REF_MAP,
    OBSERVATION_LOG_PLAN_REF,
    REGISTRY_ID,
    ROLLBACK_TRIGGER_POLICY_REF,
    _ISSUANCE_ARTIFACT_REL,
    build_phase_one_environment_cognition_runtime_trial_execution_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_execution_planning.phase_one_environment_cognition_runtime_trial_execution_planning_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    EXECUTION_PLAN_GO_KEYS,
    EXECUTION_PLAN_ITEM_REFS,
    EXECUTION_PLANNING_GOVERNANCE_RULES,
    EXECUTION_PLANNING_PRINCIPLE_ZH,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    ISSUANCE_PACKAGE_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_execution_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_execution_planning_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning/"
    "phase_one_environment_cognition_runtime_trial_execution_planning_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning/"
    "phase_one_environment_cognition_runtime_trial_execution_planning_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning/"
    "review_phase_one_environment_cognition_runtime_trial_execution_planning_v1.py",
)

_CANDIDATE_ONLY_ALLOWED_MARKERS = (
    "candidate_",
    "_replay",
    "_check",
    "conflict_record_",
    "conflict_resolution_planning_",
    "ocr_sign_evidence_request_placeholder",
    "event_overlay_validation_replay",
    "crowd_flow_risk_observation_replay",
    "crowd_queue_risk_observation_replay",
    "temporary_layout_uncertainty_logging_replay",
    "wait_observe_candidate_replay",
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


def _issuance_packages_by_ref() -> Dict[str, Dict[str, Any]]:
    issuance = _load_json(_ISSUANCE_ARTIFACT_REL) or {}
    matrix = issuance.get("issuance_package_matrix") or {}
    packages: Dict[str, Dict[str, Any]] = {}
    for entry in matrix.get("issuance_package_items") or []:
        ref = entry.get("package_ref")
        if ref:
            packages[ref] = entry
    return packages


def verify_scope_preserved_from_issuance(
    items: List[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    issuance_packages = _issuance_packages_by_ref()
    if not issuance_packages:
        return False, ["issuance_packages_unavailable"]

    issues: List[str] = []
    for item in items:
        pkg_ref = item.get("issuance_package_ref")
        issuance_pkg = issuance_packages.get(pkg_ref or "")
        if not issuance_pkg:
            issues.append(f"issuance_package_missing:{pkg_ref}")
            continue
        if issuance_pkg.get("package_scope") != item.get("execution_scope"):
            issues.append(
                f"execution_scope_mismatch:{item.get('plan_ref')}:"
                f"{issuance_pkg.get('package_scope')!r}!={item.get('execution_scope')!r}"
            )
        expected_status = issuance_pkg.get("issuance_package_status")
        actual_status = item.get("source_package_status")
        if expected_status != actual_status:
            issues.append(
                f"source_package_status_mismatch:{item.get('plan_ref')}:"
                f"{expected_status!r}!={actual_status!r}"
            )
    return len(issues) == 0, issues


def _allowed_plan_candidate_only(items: List[Dict[str, Any]]) -> bool:
    for item in items:
        for op in item.get("allowed_plan_operations") or ():
            if not any(marker in op for marker in _CANDIDATE_ONLY_ALLOWED_MARKERS):
                return False
    return True


def _blocked_ops_check(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    universal = set(UNIVERSAL_BLOCKED_OPERATIONS)
    result = {
        "blocked_operations_declared_for_all": True,
        "runtime_activation_blocked_for_all": True,
        "direct_action_blocked_for_all": True,
        "direct_speech_blocked_for_all": True,
        "direct_fact_write_blocked_for_all": True,
        "real_navigation_blocked_for_all": True,
        "live_sensor_trigger_blocked_for_all": True,
    }
    mapping = {
        "runtime_activation": "runtime_activation_blocked_for_all",
        "direct_action": "direct_action_blocked_for_all",
        "direct_speech_tts": "direct_speech_blocked_for_all",
        "direct_fact_write": "direct_fact_write_blocked_for_all",
        "real_navigation": "real_navigation_blocked_for_all",
        "live_sensor_trigger": "live_sensor_trigger_blocked_for_all",
    }
    for item in items:
        blocked = set(item.get("blocked_operations") or ())
        if not blocked:
            result["blocked_operations_declared_for_all"] = False
        if not universal.issubset(blocked):
            result["blocked_operations_declared_for_all"] = False
        for op, key in mapping.items():
            if op not in blocked:
                result[key] = False
    return result


def _bindings_ok_for_all(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    return {
        "rollback_trigger_policy_bound_for_all_execution_plans": all(
            i.get("rollback_trigger_policy_ref") == ROLLBACK_TRIGGER_POLICY_REF for i in items
        ),
        "observation_log_plan_bound_for_all_execution_plans": all(
            i.get("observation_log_plan_ref") == OBSERVATION_LOG_PLAN_REF for i in items
        ),
        "failure_handling_plan_bound_for_all_execution_plans": all(
            i.get("failure_handling_plan_ref") == FAILURE_HANDLING_PLAN_REF for i in items
        ),
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

        if entry.get("require_pre_package_sealed") and artifact:
            pre_sealed = (
                artifact.get("conclusions", {}).get("pre_runtime_trial_package_status") == "sealed"
                or artifact.get("conclusions", {}).get("runtime_trial_pre_package_sealed") is True
            )
            checks["pre_runtime_trial_package_status_sealed"] = pre_sealed
            if not pre_sealed:
                issues.append("pre_runtime_trial_package_not_sealed")

        if entry.get("require_issuance_package_go"):
            checks["issuance_package_go_verified"] = go_ok

    checks["sealed_phase_one_chain_verified"] = (
        checks.get(f"{PHASE_ONE_CHAIN_REF}.go_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.phase_one_chain_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.module_present", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.artifact_present", False)
    )
    if not checks["sealed_phase_one_chain_verified"]:
        issues.append("sealed_phase_one_chain_not_verified")
    if not checks.get("issuance_package_go_verified", False):
        issues.append("issuance_package_go_not_verified")
    if not checks.get("pre_runtime_trial_package_status_sealed", False):
        issues.append("pre_runtime_trial_package_status_not_sealed")

    return checks, issues


def validate_execution_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_execution_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("controlled_runtime_trial_execution_planning_profile") or {}
    if profile.get("issuance_package_ref") != ISSUANCE_PACKAGE_REF:
        issues.append("issuance_package_ref_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    items = matrix.get("execution_plan_items") or []
    if len(items) != 6:
        issues.append(f"execution_plan_item_count:{len(items)}")

    plan_refs = {i.get("plan_ref") for i in items}
    if plan_refs != set(EXECUTION_PLAN_ITEM_REFS):
        issues.append(f"execution_plan_item_refs_mismatch:{sorted(plan_refs)!r}")

    scope_ok, scope_issues = verify_scope_preserved_from_issuance(items)
    if not scope_ok:
        issues.extend(scope_issues)

    for item in items:
        ref = item.get("plan_ref")
        if item.get("issuance_package_ref") != ISSUANCE_PACKAGE_REF_MAP.get(ref or ""):
            issues.append(f"{ref}.issuance_package_ref_mismatch")
        if "runtime_activation" not in (item.get("blocked_operations") or ()):
            issues.append(f"{ref}.runtime_activation_not_blocked")

    gps = next((i for i in items if i.get("plan_ref") == "gps_slam_conflict_execution_plan"), {})
    if gps.get("execution_plan_status") != "blocked_no_execution_plan":
        issues.append("gps_slam_conflict_not_blocked_no_execution_plan")
    if gps.get("plan_ready") is not False:
        issues.append("gps_slam_conflict_plan_ready_must_be_false")

    subway = next((i for i in items if i.get("plan_ref") == "subway_enter_station_execution_plan"), {})
    if not subway.get("execution_constraints"):
        issues.append("subway_constraints_missing")

    if not _allowed_plan_candidate_only(items):
        issues.append("allowed_plan_operations_not_candidate_only")

    return len(issues) == 0 and registry_ok, issues


def review_phase_one_environment_cognition_runtime_trial_execution_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_execution_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_execution_planning_matrix_v1(matrix)
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

    items = matrix.get("execution_plan_items") or []
    plan_go = matrix.get("execution_plan_go_map") or {}

    scope_preserved, _ = verify_scope_preserved_from_issuance(items)
    binding_checks = _bindings_ok_for_all(items)
    blocked_checks = _blocked_ops_check(items)

    subway = next((i for i in items if i.get("plan_ref") == "subway_enter_station_execution_plan"), {})
    gps = next((i for i in items if i.get("plan_ref") == "gps_slam_conflict_execution_plan"), {})
    observation_items = [
        i
        for i in items
        if i.get("execution_scope") == "observation_only"
        and i.get("execution_plan_status") == "planned_observation_replay_only"
    ]

    review_checkpoints: Dict[str, Any] = {
        "execution_planning_profile_count": 1,
        "execution_plan_item_count": len(items),
        "issuance_package_go_verified": upstream_checks.get("issuance_package_go_verified", False),
        "pre_runtime_trial_package_status_sealed": upstream_checks.get(
            "pre_runtime_trial_package_status_sealed", False
        ),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        **plan_go,
        "scenario_scope_preserved_for_all": scope_preserved,
        "blocked_scenario_remains_blocked": (
            gps.get("execution_scope") == "blocked"
            and gps.get("execution_plan_status") == "blocked_no_execution_plan"
        ),
        "blocked_scenario_has_no_execution_plan": (
            gps.get("plan_ready") is False
            and gps.get("execution_plan_status") == "blocked_no_execution_plan"
        ),
        "observation_only_remains_observation_replay": len(observation_items) == 2,
        "constrained_item_constraints_preserved": bool(subway.get("execution_constraints")),
        "low_risk_candidates_candidate_replay_only": all(
            i.get("execution_plan_status") == "planned_candidate_replay_only"
            for i in items
            if i.get("execution_scope") == "low_risk_controlled_trial_candidate"
            and i.get("plan_ready") is not False
        ),
        **binding_checks,
        **blocked_checks,
        "source_chain_required": all(i.get("source_chain") == SOURCE_CHAIN for i in items),
        "upstream_refs_required": all(i.get("upstream_refs") for i in items),
        "allowed_plan_operations_candidate_only": _allowed_plan_candidate_only(items),
        "execution_planning_not_runtime_execution": NON_EXECUTION_FLAGS.get(
            "execution_planning_not_runtime_execution"
        ),
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "issuance_package_ref_locked": ISSUANCE_PACKAGE_REF,
        "pre_runtime_trial_package_status_locked": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "execution_planning_profile_count_eq_1": review_checkpoints["execution_planning_profile_count"] == 1,
        "execution_plan_item_count_eq_6": review_checkpoints["execution_plan_item_count"] == 6,
        "issuance_package_go_verified": review_checkpoints["issuance_package_go_verified"] is True,
        "pre_runtime_trial_package_status_sealed": (
            review_checkpoints["pre_runtime_trial_package_status_sealed"] is True
        ),
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        **{key: review_checkpoints.get(key) is True for key in EXECUTION_PLAN_GO_KEYS},
        "scenario_scope_preserved_for_all": scope_preserved is True,
        "blocked_scenario_remains_blocked": review_checkpoints["blocked_scenario_remains_blocked"] is True,
        "blocked_scenario_has_no_execution_plan": (
            review_checkpoints["blocked_scenario_has_no_execution_plan"] is True
        ),
        "observation_only_remains_observation_replay": (
            review_checkpoints["observation_only_remains_observation_replay"] is True
        ),
        "constrained_item_constraints_preserved": (
            review_checkpoints["constrained_item_constraints_preserved"] is True
        ),
        "low_risk_candidates_candidate_replay_only": (
            review_checkpoints["low_risk_candidates_candidate_replay_only"] is True
        ),
        "rollback_trigger_policy_bound_for_all_execution_plans": (
            binding_checks["rollback_trigger_policy_bound_for_all_execution_plans"] is True
        ),
        "observation_log_plan_bound_for_all_execution_plans": (
            binding_checks["observation_log_plan_bound_for_all_execution_plans"] is True
        ),
        "failure_handling_plan_bound_for_all_execution_plans": (
            binding_checks["failure_handling_plan_bound_for_all_execution_plans"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "allowed_plan_operations_candidate_only": (
            review_checkpoints["allowed_plan_operations_candidate_only"] is True
        ),
        "blocked_operations_declared_for_all": blocked_checks["blocked_operations_declared_for_all"] is True,
        "runtime_activation_blocked_for_all": blocked_checks["runtime_activation_blocked_for_all"] is True,
        "direct_action_blocked_for_all": blocked_checks["direct_action_blocked_for_all"] is True,
        "direct_speech_blocked_for_all": blocked_checks["direct_speech_blocked_for_all"] is True,
        "direct_fact_write_blocked_for_all": blocked_checks["direct_fact_write_blocked_for_all"] is True,
        "real_navigation_blocked_for_all": blocked_checks["real_navigation_blocked_for_all"] is True,
        "live_sensor_trigger_blocked_for_all": blocked_checks["live_sensor_trigger_blocked_for_all"] is True,
        "execution_planning_not_runtime_execution": (
            review_checkpoints["execution_planning_not_runtime_execution"] is True
        ),
        "trial_runtime_started_false": review_checkpoints["trial_runtime_started"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Execution Planning Review",
        "lifecycle_variant": "compressed_runtime_trial_execution_planning_review",
        "execution_planning_principle_zh": EXECUTION_PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "issuance_package_ref": ISSUANCE_PACKAGE_REF,
        "pre_runtime_trial_package_status": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "execution_planning_governance_rules": list(EXECUTION_PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "execution_planning_matrix": matrix,
        "conclusions": {
            "execution_planning_status": "ready_for_closure_trial_readiness_gate" if review_ok else "blocked",
            "execution_planning_not_runtime_execution": True,
            "runtime_activation_deferred": True,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "execution_plan_summary": {
                "planned_candidate_replay_only": [
                    "mall_find_entrance_execution_plan",
                    "home_return_execution_plan",
                ],
                "planned_constrained_candidate_replay_only": ["subway_enter_station_execution_plan"],
                "planned_observation_replay_only": [
                    "stadium_concert_ticket_gate_execution_plan",
                    "plaza_market_crowd_execution_plan",
                ],
                "blocked_no_execution_plan": ["gps_slam_conflict_execution_plan"],
            },
            "closure_gate_note": (
                "Next: Execution Planning Closure / Trial Readiness Gate — not direct execution."
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
    result = review_phase_one_environment_cognition_runtime_trial_execution_planning_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "execution_planning_profile_count": checkpoints["execution_planning_profile_count"],
                "execution_plan_item_count": checkpoints["execution_plan_item_count"],
                "issuance_package_go_verified": checkpoints["issuance_package_go_verified"],
                "mall_find_entrance_execution_plan_ready": checkpoints.get(
                    "mall_find_entrance_execution_plan_ready"
                ),
                "gps_slam_conflict_execution_plan_blocked": checkpoints.get(
                    "gps_slam_conflict_execution_plan_blocked"
                ),
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
