# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Owner Approval Request — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_owner_approval_request.phase_one_environment_cognition_runtime_trial_owner_approval_request_registry_v1 import (
    OBSERVATION_LOG_POLICY_REF,
    REGISTRY_ID,
    ROLLBACK_POLICY_REF,
    _PLANNING_ARTIFACT_REL,
    build_phase_one_environment_cognition_runtime_trial_owner_approval_request_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_owner_approval_request.phase_one_environment_cognition_runtime_trial_owner_approval_request_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GUIDANCE_ENTRYPOINT,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    REQUEST_GOVERNANCE_RULES,
    REQUEST_ITEM_GO_KEYS,
    REQUEST_ITEM_REFS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_owner_approval_request_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_owner_approval_request_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_request/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_request_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_request/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_request_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_request/"
    "review_phase_one_environment_cognition_runtime_trial_owner_approval_request_v1.py",
)

_REQUESTABLE_STATUSES = frozenset(
    {"requestable", "requestable_with_constraints", "observation_only_requestable"}
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


def _planning_admission_levels() -> Dict[str, str]:
    planning = _load_json(_PLANNING_ARTIFACT_REL) or {}
    matrix = planning.get("planning_matrix") or {}
    levels: Dict[str, str] = {}
    for policy in matrix.get("scenario_policies") or []:
        ref = policy.get("policy_ref")
        level = policy.get("admission_level")
        if ref and level:
            levels[ref] = level
    return levels


def verify_admission_level_preserved(
    items: List[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    planning_levels = _planning_admission_levels()
    if not planning_levels:
        return False, ["planning_admission_levels_unavailable"]

    issues: List[str] = []
    for item in items:
        ref = item.get("planning_policy_ref")
        expected = planning_levels.get(ref or "")
        actual = item.get("admission_level")
        if expected != actual:
            issues.append(f"admission_level_mismatch:{ref}:{expected!r}!={actual!r}")

    return len(issues) == 0, issues


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

        skeleton_rel = entry.get("skeleton_module_rel")
        if skeleton_rel:
            checks[f"{phase_ref}.skeleton_present"] = (_REPO_ROOT / skeleton_rel).is_file()

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

    if not checks.get("planning_go_verified", False):
        issues.append("planning_go_not_verified")

    return checks, issues


def validate_request_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_owner_approval_request_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("owner_approval_request_profile") or {}
    if profile.get("planning_ref") != PLANNING_REF:
        issues.append("planning_ref_mismatch")
    if profile.get("phase_one_chain_ref") != PHASE_ONE_CHAIN_REF:
        issues.append("phase_one_chain_ref_mismatch")
    if profile.get("phase_one_chain_status") != PHASE_ONE_CHAIN_STATUS:
        issues.append("phase_one_chain_status_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")
    if profile.get("owner_approval_issued") is not False:
        issues.append("owner_approval_issued_must_be_false")
    if profile.get("trial_issuance_allowed") is not False:
        issues.append("trial_issuance_allowed_must_be_false")

    items = matrix.get("approval_request_items") or []
    if len(items) != 6:
        issues.append(f"approval_request_item_count:{len(items)}")

    item_refs = {i.get("item_ref") for i in items}
    if item_refs != set(REQUEST_ITEM_REFS):
        issues.append(f"request_item_refs_mismatch:{sorted(item_refs)!r}")

    preserved, preserve_issues = verify_admission_level_preserved(items)
    if not preserved:
        issues.extend(preserve_issues)

    for item in items:
        status = item.get("approval_request_status")
        level = item.get("admission_level")
        scope = item.get("request_scope")

        if level == "blocked" and status != "not_requestable":
            issues.append(f"{item.get('item_ref')}.blocked_must_be_not_requestable")
        if level == "observation_only" and scope != "observation_only":
            issues.append(f"{item.get('item_ref')}.observation_only_scope_mismatch")
        if status == "not_requestable" and scope != "blocked":
            issues.append(f"{item.get('item_ref')}.not_requestable_scope_mismatch")
        if status in _REQUESTABLE_STATUSES:
            if not item.get("rollback_policy_ref"):
                issues.append(f"{item.get('item_ref')}.rollback_policy_missing")
            if not item.get("observation_log_policy_ref"):
                issues.append(f"{item.get('item_ref')}.observation_log_policy_missing")
        if item.get("source_chain") != SOURCE_CHAIN:
            issues.append(f"{item.get('item_ref')}.source_chain_mismatch")
        if not item.get("upstream_refs"):
            issues.append(f"{item.get('item_ref')}.upstream_refs_missing")

    decision = matrix.get("request_decision") or {}
    if decision.get("requestable_item_count") != 2:
        issues.append(f"requestable_item_count:{decision.get('requestable_item_count')}")
    if decision.get("requestable_with_constraints_item_count") != 1:
        issues.append(
            f"requestable_with_constraints_item_count:"
            f"{decision.get('requestable_with_constraints_item_count')}"
        )
    if decision.get("observation_only_requestable_item_count") != 2:
        issues.append(
            f"observation_only_requestable_item_count:"
            f"{decision.get('observation_only_requestable_item_count')}"
        )
    if decision.get("not_requestable_item_count") != 1:
        issues.append(f"not_requestable_item_count:{decision.get('not_requestable_item_count')}")

    blocker = (matrix.get("shared_bindings") or {}).get("blocker_policy") or {}
    if blocker.get("blocked_scenario_not_requestable") is not True:
        issues.append("blocked_scenario_not_requestable_false")
    if blocker.get("observation_only_not_movement_trial") is not True:
        issues.append("observation_only_not_movement_trial_false")

    return len(issues) == 0 and registry_ok, issues


def _rollback_bound_for_requestable(items: List[Dict[str, Any]]) -> bool:
    for item in items:
        if item.get("approval_request_status") in _REQUESTABLE_STATUSES:
            if item.get("rollback_policy_ref") != ROLLBACK_POLICY_REF:
                return False
    return True


def _observation_log_bound_for_requestable(items: List[Dict[str, Any]]) -> bool:
    for item in items:
        if item.get("approval_request_status") in _REQUESTABLE_STATUSES:
            if item.get("observation_log_policy_ref") != OBSERVATION_LOG_POLICY_REF:
                return False
    return True


def review_phase_one_environment_cognition_runtime_trial_owner_approval_request_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_owner_approval_request_matrix_v1()
    matrix_ok, matrix_issues = validate_request_matrix_v1(matrix)
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

    profile = matrix.get("owner_approval_request_profile") or {}
    items = matrix.get("approval_request_items") or []
    decision = matrix.get("request_decision") or {}
    request_go = matrix.get("request_item_go_map") or {}
    shared = matrix.get("shared_bindings") or {}
    risk = shared.get("risk_summary") or {}
    blocker = shared.get("blocker_policy") or {}

    admission_preserved, _ = verify_admission_level_preserved(items)

    review_checkpoints: Dict[str, Any] = {
        "approval_request_profile_count": 1,
        "approval_request_item_count": len(items),
        "planning_go_verified": upstream_checks.get("planning_go_verified", False),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        "admission_level_preserved_for_all": admission_preserved,
        "requestable_item_count": decision.get("requestable_item_count"),
        "requestable_with_constraints_item_count": decision.get("requestable_with_constraints_item_count"),
        "observation_only_requestable_item_count": decision.get("observation_only_requestable_item_count"),
        "not_requestable_item_count": decision.get("not_requestable_item_count"),
        **request_go,
        "blocked_scenario_not_requestable": blocker.get("blocked_scenario_not_requestable"),
        "observation_only_not_movement_trial": blocker.get("observation_only_not_movement_trial"),
        "owner_approval_required": profile.get("owner_approval_required"),
        "owner_approval_issued": profile.get("owner_approval_issued"),
        "trial_issuance_allowed": profile.get("trial_issuance_allowed"),
        "rollback_policy_bound_for_requestable": _rollback_bound_for_requestable(items),
        "observation_log_policy_bound_for_requestable": _observation_log_bound_for_requestable(items),
        "source_chain_required": all(i.get("source_chain") == SOURCE_CHAIN for i in items),
        "upstream_refs_required": all(i.get("upstream_refs") for i in items),
        "gps_slam_conflict_blocks_runtime_trial": risk.get("gps_slam_conflict_blocks_runtime_trial"),
        "crowd_high_risk_blocks_movement_guidance_trial": risk.get(
            "crowd_high_risk_blocks_movement_guidance_trial"
        ),
        "candidate_only_source_chain_required": profile.get("candidate_only_source_chain_required"),
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "planning_ref_locked": PLANNING_REF,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "approval_request_profile_count_eq_1": review_checkpoints["approval_request_profile_count"] == 1,
        "approval_request_item_count_eq_6": review_checkpoints["approval_request_item_count"] == 6,
        "planning_go_verified": review_checkpoints["planning_go_verified"] is True,
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        "admission_level_preserved_for_all": admission_preserved is True,
        "requestable_item_count_eq_2": review_checkpoints["requestable_item_count"] == 2,
        "requestable_with_constraints_item_count_eq_1": (
            review_checkpoints["requestable_with_constraints_item_count"] == 1
        ),
        "observation_only_requestable_item_count_eq_2": (
            review_checkpoints["observation_only_requestable_item_count"] == 2
        ),
        "not_requestable_item_count_eq_1": review_checkpoints["not_requestable_item_count"] == 1,
        **{key: review_checkpoints.get(key) is True for key in REQUEST_ITEM_GO_KEYS},
        "blocked_scenario_not_requestable": review_checkpoints["blocked_scenario_not_requestable"] is True,
        "observation_only_not_movement_trial": review_checkpoints["observation_only_not_movement_trial"] is True,
        "owner_approval_required": review_checkpoints["owner_approval_required"] is True,
        "owner_approval_issued_false": review_checkpoints["owner_approval_issued"] is False,
        "trial_issuance_allowed_false": review_checkpoints["trial_issuance_allowed"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "rollback_policy_bound_for_requestable": (
            review_checkpoints["rollback_policy_bound_for_requestable"] is True
        ),
        "observation_log_policy_bound_for_requestable": (
            review_checkpoints["observation_log_policy_bound_for_requestable"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "gps_slam_conflict_blocks_runtime_trial": (
            review_checkpoints["gps_slam_conflict_blocks_runtime_trial"] is True
        ),
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Owner Approval Request Review",
        "lifecycle_variant": "compressed_runtime_trial_owner_approval_request_review",
        "request_principle_zh": (
            "将已 GO 的 controlled runtime trial planning 转为正式 Owner Approval Request；"
            "不签发 runtime trial，不启动真实 runtime。"
        ),
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "planning_ref": PLANNING_REF,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "request_governance_rules": list(REQUEST_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "approval_request_matrix": matrix,
        "conclusions": {
            "owner_approval_request_status": "ready_for_issuance_planning" if review_ok else "blocked",
            "owner_approval_issued": False,
            "trial_issuance_deferred": True,
            "runtime_activation_deferred": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "request_summary": {
                "requestable": ["mall_find_entrance", "home_return"],
                "requestable_with_constraints": ["subway_enter_station"],
                "observation_only_requestable": ["stadium_concert_ticket_gate", "plaza_market_crowd"],
                "not_requestable": ["gps_slam_conflict"],
            },
            "issuance_note": (
                "Owner Approval Issuance clarifies which trials may be authorized next; "
                "it still does not activate runtime."
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
    result = review_phase_one_environment_cognition_runtime_trial_owner_approval_request_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "approval_request_profile_count": checkpoints["approval_request_profile_count"],
                "approval_request_item_count": checkpoints["approval_request_item_count"],
                "planning_go_verified": checkpoints["planning_go_verified"],
                "mall_find_entrance_requestable": checkpoints.get("mall_find_entrance_requestable"),
                "gps_slam_conflict_not_requestable": checkpoints.get("gps_slam_conflict_not_requestable"),
                "owner_approval_issued": checkpoints.get("owner_approval_issued"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
