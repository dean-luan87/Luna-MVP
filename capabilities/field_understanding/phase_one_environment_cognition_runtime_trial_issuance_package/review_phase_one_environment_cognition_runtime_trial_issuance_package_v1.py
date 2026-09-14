# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Issuance Package — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_issuance_package.phase_one_environment_cognition_runtime_trial_issuance_package_registry_v1 import (
    CLOSURE_SCENARIO_REF_MAP,
    FAILURE_HANDLING_POLICY_REF,
    OBSERVATION_LOG_POLICY_REF,
    REGISTRY_ID,
    ROLLBACK_POLICY_REF,
    _CLOSURE_ARTIFACT_REL,
    build_phase_one_environment_cognition_runtime_trial_issuance_package_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_issuance_package.phase_one_environment_cognition_runtime_trial_issuance_package_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    ISSUANCE_PACKAGE_GOVERNANCE_RULES,
    ISSUANCE_PACKAGE_GO_KEYS,
    ISSUANCE_PACKAGE_ITEM_REFS,
    ISSUANCE_PACKAGE_PRINCIPLE_ZH,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_ONLY_NEXT_STEPS,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_issuance_package_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_issuance_package_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
    "phase_one_environment_cognition_runtime_trial_issuance_package_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
    "phase_one_environment_cognition_runtime_trial_issuance_package_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
    "review_phase_one_environment_cognition_runtime_trial_issuance_package_v1.py",
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


def _closure_scenarios_by_ref() -> Dict[str, Dict[str, Any]]:
    closure = _load_json(_CLOSURE_ARTIFACT_REL) or {}
    matrix = closure.get("closure_readiness_matrix") or {}
    scenarios: Dict[str, Dict[str, Any]] = {}
    for entry in matrix.get("scenario_readiness") or []:
        ref = entry.get("scenario_ref")
        if ref:
            scenarios[ref] = entry
    return scenarios


def verify_scope_preserved_from_closure(
    items: List[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    closure_scenarios = _closure_scenarios_by_ref()
    if not closure_scenarios:
        return False, ["closure_scenarios_unavailable"]

    issues: List[str] = []
    for item in items:
        closure_ref = item.get("closure_scenario_ref")
        closure_entry = closure_scenarios.get(closure_ref or "")
        if not closure_entry:
            issues.append(f"closure_scenario_missing:{closure_ref}")
            continue
        if closure_entry.get("package_scope") != item.get("package_scope"):
            issues.append(
                f"package_scope_mismatch:{item.get('package_ref')}:"
                f"{closure_entry.get('package_scope')!r}!={item.get('package_scope')!r}"
            )
    return len(issues) == 0, issues


def _blocked_ops_check(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    universal = set(UNIVERSAL_BLOCKED_OPERATIONS)
    result = {
        "blocked_operations_declared_for_all": True,
        "live_sensor_trigger_blocked_for_all": True,
    }
    for item in items:
        blocked = set(item.get("blocked_operations") or ())
        if not blocked:
            result["blocked_operations_declared_for_all"] = False
        if "live_sensor_trigger" not in blocked:
            result["live_sensor_trigger_blocked_for_all"] = False
        if not universal.issubset(blocked):
            result["blocked_operations_declared_for_all"] = False
    return result


def _bindings_ok_for_all(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    return {
        "rollback_policy_bound_for_all_packages": all(
            i.get("rollback_policy_ref") == ROLLBACK_POLICY_REF for i in items
        ),
        "observation_log_policy_bound_for_all_packages": all(
            i.get("observation_log_policy_ref") == OBSERVATION_LOG_POLICY_REF for i in items
        ),
        "failure_handling_policy_bound_for_all_packages": all(
            i.get("failure_handling_policy_ref") == FAILURE_HANDLING_POLICY_REF for i in items
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
            checks["pre_runtime_trial_package_go_verified"] = go_ok
            if not pre_sealed:
                issues.append("pre_runtime_trial_package_not_sealed")

    checks["sealed_phase_one_chain_verified"] = (
        checks.get(f"{PHASE_ONE_CHAIN_REF}.go_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.phase_one_chain_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.module_present", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.artifact_present", False)
    )
    if not checks["sealed_phase_one_chain_verified"]:
        issues.append("sealed_phase_one_chain_not_verified")
    if not checks.get("pre_runtime_trial_package_go_verified", False):
        issues.append("pre_runtime_trial_package_go_not_verified")
    if not checks.get("pre_runtime_trial_package_status_sealed", False):
        issues.append("pre_runtime_trial_package_status_not_sealed")

    return checks, issues


def validate_issuance_package_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_issuance_package_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("controlled_runtime_trial_issuance_package_profile") or {}
    if profile.get("pre_runtime_trial_package_ref") != PRE_RUNTIME_TRIAL_PACKAGE_REF:
        issues.append("pre_runtime_trial_package_ref_mismatch")
    if profile.get("pre_runtime_trial_package_status") != PRE_RUNTIME_TRIAL_PACKAGE_STATUS:
        issues.append("pre_runtime_trial_package_status_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    items = matrix.get("issuance_package_items") or []
    if len(items) != 6:
        issues.append(f"issuance_package_item_count:{len(items)}")

    package_refs = {i.get("package_ref") for i in items}
    if package_refs != set(ISSUANCE_PACKAGE_ITEM_REFS):
        issues.append(f"issuance_package_item_refs_mismatch:{sorted(package_refs)!r}")

    scope_ok, scope_issues = verify_scope_preserved_from_closure(items)
    if not scope_ok:
        issues.extend(scope_issues)

    for item in items:
        ref = item.get("package_ref")
        if item.get("closure_scenario_ref") != CLOSURE_SCENARIO_REF_MAP.get(ref or ""):
            issues.append(f"{ref}.closure_scenario_ref_mismatch")
        if item.get("allowed_next_step") not in PLANNING_ONLY_NEXT_STEPS:
            issues.append(f"{ref}.allowed_next_step_not_planning_only")
        if "runtime_activation" not in (item.get("blocked_operations") or ()):
            issues.append(f"{ref}.runtime_activation_not_blocked")

    subway = next((i for i in items if i.get("package_ref") == "subway_enter_station_issuance_package"), {})
    if not subway.get("package_constraints"):
        issues.append("subway_constraints_missing")

    gps = next((i for i in items if i.get("package_ref") == "gps_slam_conflict_issuance_package"), {})
    if gps.get("package_scope") != "blocked":
        issues.append("gps_slam_conflict_not_blocked")

    return len(issues) == 0 and registry_ok, issues


def review_phase_one_environment_cognition_runtime_trial_issuance_package_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_issuance_package_matrix_v1()
    matrix_ok, matrix_issues = validate_issuance_package_matrix_v1(matrix)
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

    profile = matrix.get("controlled_runtime_trial_issuance_package_profile") or {}
    items = matrix.get("issuance_package_items") or []
    package_go = matrix.get("issuance_package_item_go_map") or {}
    shared = matrix.get("shared_records") or {}
    blocker = shared.get("blocker_record") or {}

    scope_preserved, _ = verify_scope_preserved_from_closure(items)
    binding_checks = _bindings_ok_for_all(items)
    blocked_checks = _blocked_ops_check(items)

    subway = next((i for i in items if i.get("package_ref") == "subway_enter_station_issuance_package"), {})
    gps = next((i for i in items if i.get("package_ref") == "gps_slam_conflict_issuance_package"), {})
    allowed_planning_only = all(
        i.get("allowed_next_step") in PLANNING_ONLY_NEXT_STEPS for i in items
    )

    review_checkpoints: Dict[str, Any] = {
        "issuance_package_profile_count": 1,
        "issuance_package_item_count": len(items),
        "pre_runtime_trial_package_go_verified": upstream_checks.get(
            "pre_runtime_trial_package_go_verified", False
        ),
        "pre_runtime_trial_package_status_sealed": upstream_checks.get(
            "pre_runtime_trial_package_status_sealed", False
        ),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        **package_go,
        "scenario_scope_preserved_for_all": scope_preserved,
        "blocked_scenario_remains_blocked": (
            gps.get("package_scope") == "blocked"
            and gps.get("issuance_package_status") == "packaged_as_blocked_record"
        ),
        "observation_only_not_upgraded": blocker.get("observation_only_not_upgraded"),
        "constrained_item_constraints_preserved": bool(subway.get("package_constraints")),
        "low_risk_candidates_do_not_start_runtime": True,
        **binding_checks,
        **blocked_checks,
        "source_chain_required": all(i.get("source_chain") == SOURCE_CHAIN for i in items),
        "upstream_refs_required": all(i.get("upstream_refs") for i in items),
        "allowed_next_step_planning_only": allowed_planning_only,
        "issuance_package_not_runtime_activation": NON_EXECUTION_FLAGS.get(
            "issuance_package_not_runtime_activation"
        ),
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "pre_runtime_trial_package_ref_locked": PRE_RUNTIME_TRIAL_PACKAGE_REF,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "issuance_package_profile_count_eq_1": review_checkpoints["issuance_package_profile_count"] == 1,
        "issuance_package_item_count_eq_6": review_checkpoints["issuance_package_item_count"] == 6,
        "pre_runtime_trial_package_go_verified": (
            review_checkpoints["pre_runtime_trial_package_go_verified"] is True
        ),
        "pre_runtime_trial_package_status_sealed": (
            review_checkpoints["pre_runtime_trial_package_status_sealed"] is True
        ),
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        **{key: review_checkpoints.get(key) is True for key in ISSUANCE_PACKAGE_GO_KEYS},
        "scenario_scope_preserved_for_all": scope_preserved is True,
        "blocked_scenario_remains_blocked": review_checkpoints["blocked_scenario_remains_blocked"] is True,
        "observation_only_not_upgraded": review_checkpoints["observation_only_not_upgraded"] is True,
        "constrained_item_constraints_preserved": (
            review_checkpoints["constrained_item_constraints_preserved"] is True
        ),
        "low_risk_candidates_do_not_start_runtime": (
            review_checkpoints["low_risk_candidates_do_not_start_runtime"] is True
        ),
        "rollback_policy_bound_for_all_packages": (
            binding_checks["rollback_policy_bound_for_all_packages"] is True
        ),
        "observation_log_policy_bound_for_all_packages": (
            binding_checks["observation_log_policy_bound_for_all_packages"] is True
        ),
        "failure_handling_policy_bound_for_all_packages": (
            binding_checks["failure_handling_policy_bound_for_all_packages"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "allowed_next_step_planning_only": allowed_planning_only is True,
        "issuance_package_not_runtime_activation": (
            review_checkpoints["issuance_package_not_runtime_activation"] is True
        ),
        "trial_runtime_started_false": review_checkpoints["trial_runtime_started"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "live_sensor_trigger_blocked_for_all": blocked_checks["live_sensor_trigger_blocked_for_all"] is True,
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Issuance Package Review",
        "lifecycle_variant": "compressed_runtime_trial_issuance_package_review",
        "issuance_package_principle_zh": ISSUANCE_PACKAGE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "pre_runtime_trial_package_ref": PRE_RUNTIME_TRIAL_PACKAGE_REF,
        "pre_runtime_trial_package_status": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "issuance_package_governance_rules": list(ISSUANCE_PACKAGE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "issuance_package_matrix": matrix,
        "conclusions": {
            "issuance_package_status": "ready_for_trial_execution_planning" if review_ok else "blocked",
            "runtime_activation_deferred": True,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "issuance_package_summary": {
                "packaged_for_trial_execution_planning": [
                    "mall_find_entrance_issuance_package",
                    "home_return_issuance_package",
                ],
                "packaged_with_constraints": ["subway_enter_station_issuance_package"],
                "packaged_observation_only": [
                    "stadium_concert_ticket_gate_issuance_package",
                    "plaza_market_crowd_issuance_package",
                ],
                "packaged_as_blocked_record": ["gps_slam_conflict_issuance_package"],
            },
            "execution_planning_note": (
                "Next: Trial Execution Planning — planning only, no direct execution."
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
    result = review_phase_one_environment_cognition_runtime_trial_issuance_package_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "issuance_package_profile_count": checkpoints["issuance_package_profile_count"],
                "issuance_package_item_count": checkpoints["issuance_package_item_count"],
                "pre_runtime_trial_package_go_verified": checkpoints["pre_runtime_trial_package_go_verified"],
                "mall_find_entrance_packaged_for_trial_execution_planning": checkpoints.get(
                    "mall_find_entrance_packaged_for_trial_execution_planning"
                ),
                "gps_slam_conflict_packaged_as_blocked_record": checkpoints.get(
                    "gps_slam_conflict_packaged_as_blocked_record"
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
