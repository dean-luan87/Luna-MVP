# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Package Boundary Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_package_boundary_planning.phase_one_environment_cognition_runtime_trial_package_boundary_planning_registry_v1 import (
    FAILURE_HANDLING_POLICY_REF,
    OBSERVATION_LOG_POLICY_REF,
    REGISTRY_ID,
    ROLLBACK_POLICY_REF,
    _ISSUANCE_ARTIFACT_REL,
    build_phase_one_environment_cognition_runtime_trial_package_boundary_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_package_boundary_planning.phase_one_environment_cognition_runtime_trial_package_boundary_planning_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    ISSUANCE_ITEM_REF_MAP,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_GOVERNANCE_RULES,
    PACKAGE_ITEM_GO_KEYS,
    PACKAGE_ITEM_REFS,
    PACKAGE_PRINCIPLE_ZH,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_package_boundary_planning_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_boundary_planning/"
    "phase_one_environment_cognition_runtime_trial_package_boundary_planning_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_boundary_planning/"
    "phase_one_environment_cognition_runtime_trial_package_boundary_planning_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_boundary_planning/"
    "review_phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1.py",
)

_CANDIDATE_ONLY_ALLOWED_PREFIXES = (
    "candidate_",
    "guidance_candidate_",
    "evidence_request_candidate_",
    "observation_candidate_",
    "crowd_flow_risk_candidate_",
    "crowd_queue_risk_",
    "temporary_layout_uncertainty_",
    "wait_observe_candidate_",
    "conflict_record_",
    "conflict_resolution_planning_",
    "coarse_map_route_candidate_",
    "local_spatial_check_candidate_",
    "event_overlay_label_validation",
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


def _issuance_items_by_ref() -> Dict[str, Dict[str, Any]]:
    issuance = _load_json(_ISSUANCE_ARTIFACT_REL) or {}
    matrix = issuance.get("issuance_matrix") or {}
    items: Dict[str, Dict[str, Any]] = {}
    for item in matrix.get("issuance_items") or []:
        ref = item.get("item_ref")
        if ref:
            items[ref] = item
    return items


def verify_preserved_from_issuance(
    items: List[Dict[str, Any]],
) -> Tuple[bool, bool, List[str]]:
    issuance_items = _issuance_items_by_ref()
    if not issuance_items:
        return False, False, ["issuance_items_unavailable"]

    issues: List[str] = []
    scope_ok = True
    status_ok = True

    for item in items:
        iss_ref = item.get("issuance_item_ref")
        issuance_item = issuance_items.get(iss_ref or "")
        if not issuance_item:
            issues.append(f"issuance_item_missing:{iss_ref}")
            scope_ok = False
            status_ok = False
            continue

        expected_scope = issuance_item.get("issued_scope")
        actual_scope = item.get("package_scope")
        if expected_scope != actual_scope:
            issues.append(f"package_scope_mismatch:{iss_ref}:{expected_scope!r}!={actual_scope!r}")
            scope_ok = False

        expected_status = issuance_item.get("issued_status")
        actual_status = item.get("issued_status")
        if expected_status != actual_status:
            issues.append(f"issued_status_mismatch:{iss_ref}:{expected_status!r}!={actual_status!r}")
            status_ok = False

    return scope_ok, status_ok, issues


def _allowed_operations_candidate_only(items: List[Dict[str, Any]]) -> bool:
    for item in items:
        for op in item.get("allowed_operations") or ():
            if not any(op.startswith(p) or op == p for p in _CANDIDATE_ONLY_ALLOWED_PREFIXES):
                return False
    return True


def _blocked_ops_check(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    universal = set(UNIVERSAL_BLOCKED_OPERATIONS)
    all_declared = True
    action_blocked = True
    speech_blocked = True
    fact_write_blocked = True
    nav_blocked = True

    for item in items:
        blocked = set(item.get("blocked_operations") or ())
        if not blocked:
            all_declared = False
        if "direct_action" not in blocked:
            action_blocked = False
        if "direct_speech_tts" not in blocked:
            speech_blocked = False
        if "direct_fact_write" not in blocked:
            fact_write_blocked = False
        if "real_navigation" not in blocked:
            nav_blocked = False
        if not universal.issubset(blocked):
            all_declared = False

    return {
        "blocked_operations_declared_for_all": all_declared,
        "direct_action_blocked_for_all": action_blocked,
        "direct_speech_blocked_for_all": speech_blocked,
        "direct_fact_write_blocked_for_all": fact_write_blocked,
        "real_navigation_blocked_for_all": nav_blocked,
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

        if entry.get("require_issuance_go"):
            checks["owner_approval_issuance_go_verified"] = go_ok
        if entry.get("require_request_go"):
            checks["owner_approval_request_go_verified"] = go_ok
        if entry.get("require_planning_go"):
            checks["planning_go_verified"] = go_ok

    checks["sealed_phase_one_chain_verified"] = (
        checks.get(f"{PHASE_ONE_CHAIN_REF}.go_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.phase_one_chain_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.module_present", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.artifact_present", False)
    )
    if not checks["sealed_phase_one_chain_verified"]:
        issues.append("sealed_phase_one_chain_not_verified")
    if not checks.get("owner_approval_issuance_go_verified", False):
        issues.append("owner_approval_issuance_go_not_verified")
    if not checks.get("owner_approval_request_go_verified", False):
        issues.append("owner_approval_request_go_not_verified")
    if not checks.get("planning_go_verified", False):
        issues.append("planning_go_not_verified")

    return checks, issues


def validate_package_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_package_boundary_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("controlled_runtime_trial_package_profile") or {}
    if profile.get("owner_approval_issuance_ref") != OWNER_APPROVAL_ISSUANCE_REF:
        issues.append("owner_approval_issuance_ref_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    items = matrix.get("trial_package_items") or []
    if len(items) != 6:
        issues.append(f"trial_package_item_count:{len(items)}")

    package_refs = {i.get("package_ref") for i in items}
    if package_refs != set(PACKAGE_ITEM_REFS):
        issues.append(f"package_item_refs_mismatch:{sorted(package_refs)!r}")

    scope_ok, status_ok, preserve_issues = verify_preserved_from_issuance(items)
    if not scope_ok or not status_ok:
        issues.extend(preserve_issues)

    for item in items:
        ref = item.get("package_ref")
        if item.get("issuance_item_ref") != ISSUANCE_ITEM_REF_MAP.get(ref or ""):
            issues.append(f"{ref}.issuance_item_ref_mismatch")
        if item.get("rollback_policy_ref") != ROLLBACK_POLICY_REF:
            issues.append(f"{ref}.rollback_policy_not_bound")
        if item.get("observation_log_policy_ref") != OBSERVATION_LOG_POLICY_REF:
            issues.append(f"{ref}.observation_log_policy_not_bound")
        if item.get("failure_handling_policy_ref") != FAILURE_HANDLING_POLICY_REF:
            issues.append(f"{ref}.failure_handling_policy_not_bound")
        if item.get("source_chain") != SOURCE_CHAIN:
            issues.append(f"{ref}.source_chain_mismatch")
        if not item.get("upstream_refs"):
            issues.append(f"{ref}.upstream_refs_missing")

    blocked_checks = _blocked_ops_check(items)
    if not blocked_checks["blocked_operations_declared_for_all"]:
        issues.append("blocked_operations_not_declared_for_all")

    if not _allowed_operations_candidate_only(items):
        issues.append("allowed_operations_not_candidate_only")

    gps = next((i for i in items if i.get("package_ref") == "gps_slam_conflict_package"), None)
    if gps:
        blocked = set(gps.get("blocked_operations") or ())
        if "route_hint_activation" not in blocked and "route_activation" not in blocked:
            issues.append("gps_slam_conflict_route_activation_not_blocked")

    plaza = next((i for i in items if i.get("package_ref") == "plaza_market_crowd_package"), None)
    if plaza and "movement_guidance_trial" not in (plaza.get("blocked_operations") or ()):
        issues.append("plaza_movement_guidance_trial_not_blocked")

    subway = next((i for i in items if i.get("package_ref") == "subway_enter_station_package"), None)
    if subway and not subway.get("package_constraints"):
        issues.append("subway_constraints_missing")

    return len(issues) == 0 and registry_ok, issues


def review_phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_package_boundary_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_package_matrix_v1(matrix)
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

    profile = matrix.get("controlled_runtime_trial_package_profile") or {}
    items = matrix.get("trial_package_items") or []
    package_go = matrix.get("package_item_go_map") or {}
    shared = matrix.get("shared_bindings") or {}

    scope_preserved, status_preserved, _ = verify_preserved_from_issuance(items)
    blocked_checks = _blocked_ops_check(items)

    gps_item = next((i for i in items if i.get("package_ref") == "gps_slam_conflict_package"), {})
    plaza_item = next((i for i in items if i.get("package_ref") == "plaza_market_crowd_package"), {})
    subway_item = next((i for i in items if i.get("package_ref") == "subway_enter_station_package"), {})

    review_checkpoints: Dict[str, Any] = {
        "trial_package_profile_count": 1,
        "trial_package_item_count": len(items),
        "owner_approval_issuance_go_verified": upstream_checks.get("owner_approval_issuance_go_verified", False),
        "owner_approval_request_go_verified": upstream_checks.get("owner_approval_request_go_verified", False),
        "planning_go_verified": upstream_checks.get("planning_go_verified", False),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        "package_scope_preserved_for_all": scope_preserved,
        "issued_status_preserved_for_all": status_preserved,
        "blocked_scenario_remains_blocked": (
            gps_item.get("package_scope") == "blocked"
            and gps_item.get("issued_status") == "not_issued_blocked"
        ),
        "observation_only_not_upgraded": all(
            i.get("package_scope") == "observation_only"
            for i in items
            if i.get("issued_status") == "issued_observation_only"
        ),
        "constrained_item_constraints_preserved": bool(subway_item.get("package_constraints")),
        **package_go,
        "rollback_policy_bound_for_all_packages": all(
            i.get("rollback_policy_ref") == ROLLBACK_POLICY_REF for i in items
        ),
        "observation_log_policy_bound_for_all_packages": all(
            i.get("observation_log_policy_ref") == OBSERVATION_LOG_POLICY_REF for i in items
        ),
        "failure_handling_policy_bound_for_all_packages": all(
            i.get("failure_handling_policy_ref") == FAILURE_HANDLING_POLICY_REF for i in items
        ),
        "source_chain_required": all(i.get("source_chain") == SOURCE_CHAIN for i in items),
        "upstream_refs_required": all(i.get("upstream_refs") for i in items),
        "allowed_operations_candidate_only": _allowed_operations_candidate_only(items),
        **blocked_checks,
        "gps_slam_conflict_blocks_route_activation": (
            "route_hint_activation" in (gps_item.get("blocked_operations") or ())
            or "route_activation" in (gps_item.get("blocked_operations") or ())
        ),
        "crowd_high_risk_blocks_movement_guidance_trial": (
            "movement_guidance_trial" in (plaza_item.get("blocked_operations") or ())
        ),
        "candidate_only_source_chain_required": profile.get("candidate_only_source_chain_required"),
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "owner_approval_issuance_ref_locked": OWNER_APPROVAL_ISSUANCE_REF,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "trial_package_profile_count_eq_1": review_checkpoints["trial_package_profile_count"] == 1,
        "trial_package_item_count_eq_6": review_checkpoints["trial_package_item_count"] == 6,
        "owner_approval_issuance_go_verified": review_checkpoints["owner_approval_issuance_go_verified"] is True,
        "owner_approval_request_go_verified": review_checkpoints["owner_approval_request_go_verified"] is True,
        "planning_go_verified": review_checkpoints["planning_go_verified"] is True,
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        "package_scope_preserved_for_all": scope_preserved is True,
        "issued_status_preserved_for_all": status_preserved is True,
        "blocked_scenario_remains_blocked": review_checkpoints["blocked_scenario_remains_blocked"] is True,
        "observation_only_not_upgraded": review_checkpoints["observation_only_not_upgraded"] is True,
        "constrained_item_constraints_preserved": (
            review_checkpoints["constrained_item_constraints_preserved"] is True
        ),
        **{key: review_checkpoints.get(key) is True for key in PACKAGE_ITEM_GO_KEYS},
        "rollback_policy_bound_for_all_packages": (
            review_checkpoints["rollback_policy_bound_for_all_packages"] is True
        ),
        "observation_log_policy_bound_for_all_packages": (
            review_checkpoints["observation_log_policy_bound_for_all_packages"] is True
        ),
        "failure_handling_policy_bound_for_all_packages": (
            review_checkpoints["failure_handling_policy_bound_for_all_packages"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "allowed_operations_candidate_only": review_checkpoints["allowed_operations_candidate_only"] is True,
        "blocked_operations_declared_for_all": (
            review_checkpoints["blocked_operations_declared_for_all"] is True
        ),
        "direct_action_blocked_for_all": review_checkpoints["direct_action_blocked_for_all"] is True,
        "direct_speech_blocked_for_all": review_checkpoints["direct_speech_blocked_for_all"] is True,
        "direct_fact_write_blocked_for_all": review_checkpoints["direct_fact_write_blocked_for_all"] is True,
        "real_navigation_blocked_for_all": review_checkpoints["real_navigation_blocked_for_all"] is True,
        "gps_slam_conflict_blocks_route_activation": (
            review_checkpoints["gps_slam_conflict_blocks_route_activation"] is True
        ),
        "crowd_high_risk_blocks_movement_guidance_trial": (
            review_checkpoints["crowd_high_risk_blocks_movement_guidance_trial"] is True
        ),
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Package Boundary Planning Review",
        "lifecycle_variant": "compressed_runtime_trial_package_boundary_planning_review",
        "package_principle_zh": PACKAGE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "owner_approval_issuance_ref": OWNER_APPROVAL_ISSUANCE_REF,
        "owner_approval_request_ref": OWNER_APPROVAL_REQUEST_REF,
        "planning_ref": PLANNING_REF,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "package_governance_rules": list(PACKAGE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "package_boundary_matrix": matrix,
        "conclusions": {
            "trial_package_boundary_planning_status": (
                "ready_for_closure_readiness_review" if review_ok else "blocked"
            ),
            "trial_runtime_started": False,
            "runtime_activation_deferred": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "package_summary": {
                "low_risk_controlled_trial_candidate": ["mall_find_entrance_package", "home_return_package"],
                "cautious_candidate_trial": ["subway_enter_station_package"],
                "observation_only": [
                    "stadium_concert_ticket_gate_package",
                    "plaza_market_crowd_package",
                ],
                "blocked": ["gps_slam_conflict_package"],
            },
            "closure_note": (
                "Next: Trial Package Closure / Readiness Review to seal planning, request, "
                "issuance, and package boundary as runtime trial pre-package."
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
    result = review_phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "trial_package_profile_count": checkpoints["trial_package_profile_count"],
                "trial_package_item_count": checkpoints["trial_package_item_count"],
                "owner_approval_issuance_go_verified": checkpoints["owner_approval_issuance_go_verified"],
                "mall_find_entrance_package_ready": checkpoints.get("mall_find_entrance_package_ready"),
                "gps_slam_conflict_package_blocked": checkpoints.get("gps_slam_conflict_package_blocked"),
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
