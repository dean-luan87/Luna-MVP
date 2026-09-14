# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Owner Approval Issuance — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_owner_approval_issuance.phase_one_environment_cognition_runtime_trial_owner_approval_issuance_registry_v1 import (
    OBSERVATION_LOG_POLICY_REF,
    REGISTRY_ID,
    ROLLBACK_POLICY_REF,
    _PLANNING_ARTIFACT_REL,
    _REQUEST_ARTIFACT_REL,
    build_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_owner_approval_issuance.phase_one_environment_cognition_runtime_trial_owner_approval_issuance_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    ISSUANCE_GOVERNANCE_RULES,
    ISSUANCE_ITEM_GO_KEYS,
    ISSUANCE_ITEM_REFS,
    ISSUANCE_PRINCIPLE_ZH,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    OWNER_APPROVAL_REQUEST_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    REQUEST_ITEM_REF_MAP,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_issuance/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_issuance/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_issuance/"
    "review_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1.py",
)

_ISSUED_STATUSES = frozenset(
    {
        "issued_for_next_stage_planning",
        "issued_with_constraints_for_next_stage_planning",
        "issued_observation_only",
    }
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


def _request_items_by_ref() -> Dict[str, Dict[str, Any]]:
    request = _load_json(_REQUEST_ARTIFACT_REL) or {}
    matrix = request.get("approval_request_matrix") or {}
    items: Dict[str, Dict[str, Any]] = {}
    for item in matrix.get("approval_request_items") or []:
        ref = item.get("item_ref")
        if ref:
            items[ref] = item
    return items


def verify_preserved_from_request(
    items: List[Dict[str, Any]],
) -> Tuple[bool, bool, List[str]]:
    request_items = _request_items_by_ref()
    if not request_items:
        return False, False, ["request_items_unavailable"]

    issues: List[str] = []
    admission_ok = True
    scope_ok = True

    for item in items:
        req_ref = item.get("request_item_ref")
        request_item = request_items.get(req_ref or "")
        if not request_item:
            issues.append(f"request_item_missing:{req_ref}")
            admission_ok = False
            scope_ok = False
            continue

        expected_level = request_item.get("admission_level")
        actual_level = item.get("admission_level")
        if expected_level != actual_level:
            issues.append(f"admission_level_mismatch:{req_ref}:{expected_level!r}!={actual_level!r}")
            admission_ok = False

        expected_scope = request_item.get("request_scope")
        actual_scope = item.get("request_scope")
        if expected_scope != actual_scope:
            issues.append(f"request_scope_mismatch:{req_ref}:{expected_scope!r}!={actual_scope!r}")
            scope_ok = False

        expected_status = request_item.get("approval_request_status")
        actual_status = item.get("request_status")
        if expected_status != actual_status:
            issues.append(f"request_status_mismatch:{req_ref}:{expected_status!r}!={actual_status!r}")

        if item.get("issued_scope") != actual_level:
            issues.append(f"issued_scope_must_match_admission_level:{req_ref}")

    return admission_ok, scope_ok, issues


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

        if not entry.get("require_go", True):
            checks[f"{phase_ref}.binding_ok"] = checks[f"{phase_ref}.module_present"]
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
    if not checks.get("owner_approval_request_go_verified", False):
        issues.append("owner_approval_request_go_not_verified")
    if not checks.get("planning_go_verified", False):
        issues.append("planning_go_not_verified")

    return checks, issues


def validate_issuance_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("owner_approval_issuance_profile") or {}
    if profile.get("owner_approval_request_ref") != OWNER_APPROVAL_REQUEST_REF:
        issues.append("owner_approval_request_ref_mismatch")
    if profile.get("planning_ref") != PLANNING_REF:
        issues.append("planning_ref_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    items = matrix.get("issuance_items") or []
    if len(items) != 6:
        issues.append(f"issuance_item_count:{len(items)}")

    item_refs = {i.get("item_ref") for i in items}
    if item_refs != set(ISSUANCE_ITEM_REFS):
        issues.append(f"issuance_item_refs_mismatch:{sorted(item_refs)!r}")

    admission_ok, scope_ok, preserve_issues = verify_preserved_from_request(items)
    if not admission_ok:
        issues.extend(preserve_issues)
    if not scope_ok:
        issues.extend(preserve_issues)

    for item in items:
        ref = item.get("item_ref")
        if item.get("request_item_ref") != REQUEST_ITEM_REF_MAP.get(ref or ""):
            issues.append(f"{ref}.request_item_ref_mismatch")
        if item.get("issued_status") == "not_issued_blocked" and item.get("issued_scope") != "blocked":
            issues.append(f"{ref}.blocked_issued_scope_mismatch")
        if item.get("issued_status") in _ISSUED_STATUSES:
            if item.get("rollback_policy_ref") != ROLLBACK_POLICY_REF:
                issues.append(f"{ref}.rollback_policy_not_bound")
            if item.get("observation_log_policy_ref") != OBSERVATION_LOG_POLICY_REF:
                issues.append(f"{ref}.observation_log_policy_not_bound")
            if "no_runtime_activation" not in (item.get("required_controls") or ()):
                issues.append(f"{ref}.no_runtime_activation_control_missing")

    decision = matrix.get("issuance_decision") or {}
    if decision.get("issued_for_next_stage_planning_count") != 2:
        issues.append(f"issued_for_next_stage_planning_count:{decision.get('issued_for_next_stage_planning_count')}")
    if decision.get("issued_with_constraints_count") != 1:
        issues.append(f"issued_with_constraints_count:{decision.get('issued_with_constraints_count')}")
    if decision.get("issued_observation_only_count") != 2:
        issues.append(f"issued_observation_only_count:{decision.get('issued_observation_only_count')}")
    if decision.get("not_issued_blocked_count") != 1:
        issues.append(f"not_issued_blocked_count:{decision.get('not_issued_blocked_count')}")

    blocker = (matrix.get("shared_records") or {}).get("blocker_record") or {}
    if blocker.get("blocked_scenario_not_issued") is not True:
        issues.append("blocked_scenario_not_issued_false")
    if blocker.get("observation_only_not_upgraded") is not True:
        issues.append("observation_only_not_upgraded_false")
    if blocker.get("constrained_item_not_unconstrained") is not True:
        issues.append("constrained_item_not_unconstrained_false")

    return len(issues) == 0 and registry_ok, issues


def _bindings_ok_for_issued(items: List[Dict[str, Any]]) -> Tuple[bool, bool]:
    rollback_ok = True
    obs_ok = True
    for item in items:
        if item.get("issued_status") not in _ISSUED_STATUSES:
            continue
        if item.get("rollback_policy_ref") != ROLLBACK_POLICY_REF:
            rollback_ok = False
        if item.get("observation_log_policy_ref") != OBSERVATION_LOG_POLICY_REF:
            obs_ok = False
    return rollback_ok, obs_ok


def review_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_matrix_v1()
    matrix_ok, matrix_issues = validate_issuance_matrix_v1(matrix)
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

    profile = matrix.get("owner_approval_issuance_profile") or {}
    items = matrix.get("issuance_items") or []
    decision = matrix.get("issuance_decision") or {}
    issuance_go = matrix.get("issuance_item_go_map") or {}
    shared = matrix.get("shared_records") or {}
    blocker = shared.get("blocker_record") or {}

    admission_preserved, scope_preserved, _ = verify_preserved_from_request(items)
    rollback_bound, obs_bound = _bindings_ok_for_issued(items)

    review_checkpoints: Dict[str, Any] = {
        "issuance_profile_count": 1,
        "issuance_item_count": len(items),
        "owner_approval_request_go_verified": upstream_checks.get("owner_approval_request_go_verified", False),
        "planning_go_verified": upstream_checks.get("planning_go_verified", False),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        "admission_level_preserved_for_all": admission_preserved,
        "request_scope_preserved_for_all": scope_preserved,
        "issued_for_next_stage_planning_count": decision.get("issued_for_next_stage_planning_count"),
        "issued_with_constraints_count": decision.get("issued_with_constraints_count"),
        "issued_observation_only_count": decision.get("issued_observation_only_count"),
        "not_issued_blocked_count": decision.get("not_issued_blocked_count"),
        **issuance_go,
        "blocked_scenario_not_issued": blocker.get("blocked_scenario_not_issued"),
        "observation_only_not_upgraded": blocker.get("observation_only_not_upgraded"),
        "constrained_item_not_unconstrained": blocker.get("constrained_item_not_unconstrained"),
        "issuance_not_runtime_activation": NON_EXECUTION_FLAGS.get("issuance_not_runtime_activation"),
        "trial_runtime_started": NON_EXECUTION_FLAGS.get("trial_runtime_started"),
        "rollback_policy_bound_for_issued": rollback_bound,
        "observation_log_policy_bound_for_issued": obs_bound,
        "source_chain_required": all(i.get("source_chain") == SOURCE_CHAIN for i in items),
        "upstream_refs_required": all(i.get("upstream_refs") for i in items),
        "gps_slam_conflict_blocks_issuance": blocker.get("gps_slam_conflict_blocks_issuance"),
        "crowd_high_risk_blocks_movement_guidance_trial": blocker.get(
            "crowd_high_risk_blocks_movement_guidance_trial"
        ),
        "candidate_only_source_chain_required": profile.get("candidate_only_source_chain_required"),
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "owner_approval_request_ref_locked": OWNER_APPROVAL_REQUEST_REF,
        "planning_ref_locked": PLANNING_REF,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "issuance_profile_count_eq_1": review_checkpoints["issuance_profile_count"] == 1,
        "issuance_item_count_eq_6": review_checkpoints["issuance_item_count"] == 6,
        "owner_approval_request_go_verified": review_checkpoints["owner_approval_request_go_verified"] is True,
        "planning_go_verified": review_checkpoints["planning_go_verified"] is True,
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        "admission_level_preserved_for_all": admission_preserved is True,
        "request_scope_preserved_for_all": scope_preserved is True,
        "issued_for_next_stage_planning_count_eq_2": (
            review_checkpoints["issued_for_next_stage_planning_count"] == 2
        ),
        "issued_with_constraints_count_eq_1": review_checkpoints["issued_with_constraints_count"] == 1,
        "issued_observation_only_count_eq_2": review_checkpoints["issued_observation_only_count"] == 2,
        "not_issued_blocked_count_eq_1": review_checkpoints["not_issued_blocked_count"] == 1,
        **{key: review_checkpoints.get(key) is True for key in ISSUANCE_ITEM_GO_KEYS},
        "blocked_scenario_not_issued": review_checkpoints["blocked_scenario_not_issued"] is True,
        "observation_only_not_upgraded": review_checkpoints["observation_only_not_upgraded"] is True,
        "constrained_item_not_unconstrained": review_checkpoints["constrained_item_not_unconstrained"] is True,
        "issuance_not_runtime_activation": review_checkpoints["issuance_not_runtime_activation"] is True,
        "trial_runtime_started_false": review_checkpoints["trial_runtime_started"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "rollback_policy_bound_for_issued": rollback_bound is True,
        "observation_log_policy_bound_for_issued": obs_bound is True,
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "gps_slam_conflict_blocks_issuance": review_checkpoints["gps_slam_conflict_blocks_issuance"] is True,
        "crowd_high_risk_blocks_movement_guidance_trial": (
            review_checkpoints["crowd_high_risk_blocks_movement_guidance_trial"] is True
        ),
        "candidate_only_source_chain_required": (
            review_checkpoints["candidate_only_source_chain_required"] is CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED
        ),
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Owner Approval Issuance Review",
        "lifecycle_variant": "compressed_runtime_trial_owner_approval_issuance_review",
        "issuance_principle_zh": ISSUANCE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "owner_approval_request_ref": OWNER_APPROVAL_REQUEST_REF,
        "planning_ref": PLANNING_REF,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "issuance_governance_rules": list(ISSUANCE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "issuance_matrix": matrix,
        "conclusions": {
            "owner_approval_issuance_status": "ready_for_trial_package_planning" if review_ok else "blocked",
            "trial_runtime_started": False,
            "runtime_activation_deferred": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "issuance_summary": {
                "issued_for_next_stage_planning": ["mall_find_entrance", "home_return"],
                "issued_with_constraints": ["subway_enter_station"],
                "issued_observation_only": ["stadium_concert_ticket_gate", "plaza_market_crowd"],
                "not_issued_blocked": ["gps_slam_conflict"],
            },
            "trial_package_note": (
                "Next: Trial Package / Trial Boundary Planning to encapsulate "
                "2 low-risk, 1 constrained, 2 observation-only, 1 blocked scenarios."
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
    result = review_phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "issuance_profile_count": checkpoints["issuance_profile_count"],
                "issuance_item_count": checkpoints["issuance_item_count"],
                "owner_approval_request_go_verified": checkpoints["owner_approval_request_go_verified"],
                "mall_find_entrance_issued_for_next_stage_planning": checkpoints.get(
                    "mall_find_entrance_issued_for_next_stage_planning"
                ),
                "gps_slam_conflict_not_issued_blocked": checkpoints.get("gps_slam_conflict_not_issued_blocked"),
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
