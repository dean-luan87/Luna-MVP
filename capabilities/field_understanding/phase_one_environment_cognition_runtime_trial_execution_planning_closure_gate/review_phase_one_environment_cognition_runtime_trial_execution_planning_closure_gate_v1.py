# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Runtime Trial Execution Planning Closure Gate — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate.phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_registry_v1 import (
    FAILURE_HANDLING_PLAN_REF,
    OBSERVATION_LOG_PLAN_REF,
    REGISTRY_ID,
    ROLLBACK_TRIGGER_POLICY_REF,
    _EXECUTION_PLANNING_ARTIFACT_REL,
    build_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate.phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CLOSURE_GATE_GOVERNANCE_RULES,
    CLOSURE_GATE_PRINCIPLE_ZH,
    EXECUTION_PLANNING_REF,
    EXECUTION_PLAN_REF_MAP,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    ISSUANCE_PACKAGE_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_ONLY_NEXT_STEPS,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    READINESS_GATE_GO_KEYS,
    READINESS_GATE_ITEM_REFS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_v1_smoke_v0"
)
REVIEW_FILENAME = (
    "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_review_v1.json"
)

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate/"
    "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate/"
    "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate/"
    "review_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_v1.py",
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


def _execution_plans_by_ref() -> Dict[str, Dict[str, Any]]:
    planning = _load_json(_EXECUTION_PLANNING_ARTIFACT_REL) or {}
    matrix = planning.get("execution_planning_matrix") or {}
    plans: Dict[str, Dict[str, Any]] = {}
    for entry in matrix.get("execution_plan_items") or []:
        ref = entry.get("plan_ref")
        if ref:
            plans[ref] = entry
    return plans


def verify_scope_preserved_from_execution_planning(
    items: List[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    execution_plans = _execution_plans_by_ref()
    if not execution_plans:
        return False, ["execution_plans_unavailable"]

    issues: List[str] = []
    for item in items:
        plan_ref = item.get("execution_plan_ref")
        execution_plan = execution_plans.get(plan_ref or "")
        if not execution_plan:
            issues.append(f"execution_plan_missing:{plan_ref}")
            continue
        if execution_plan.get("execution_scope") != item.get("gate_scope"):
            issues.append(
                f"gate_scope_mismatch:{item.get('gate_ref')}:"
                f"{execution_plan.get('execution_scope')!r}!={item.get('gate_scope')!r}"
            )
        expected_status = execution_plan.get("execution_plan_status")
        actual_status = item.get("source_execution_plan_status")
        if expected_status != actual_status:
            issues.append(
                f"source_execution_plan_status_mismatch:{item.get('gate_ref')}:"
                f"{expected_status!r}!={actual_status!r}"
            )
    return len(issues) == 0, issues


def _blocked_ops_check(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    universal = set(UNIVERSAL_BLOCKED_OPERATIONS)
    result = {
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
        if not universal.issubset(blocked):
            for op, key in mapping.items():
                if op not in blocked:
                    result[key] = False
    return result


def _replay_capable_bindings_ok(items: List[Dict[str, Any]]) -> Dict[str, bool]:
    replay_items = [i for i in items if i.get("replay_capable") is True]
    return {
        "human_ack_declared_for_replay_capable_scenarios": all(
            "human_ack_before_replay_batch" in (i.get("gate_requirements") or ())
            for i in replay_items
        ),
        "rollback_readiness_bound_for_replay_capable_scenarios": all(
            i.get("rollback_trigger_policy_ref") == ROLLBACK_TRIGGER_POLICY_REF for i in replay_items
        ),
        "observation_log_readiness_bound_for_replay_capable_scenarios": all(
            i.get("observation_log_plan_ref") == OBSERVATION_LOG_PLAN_REF for i in replay_items
        ),
        "failure_handling_readiness_bound_for_replay_capable_scenarios": all(
            i.get("failure_handling_plan_ref") == FAILURE_HANDLING_PLAN_REF for i in replay_items
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

        if entry.get("require_execution_planning_go"):
            checks["execution_planning_go_verified"] = go_ok

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
    if not checks.get("execution_planning_go_verified", False):
        issues.append("execution_planning_go_not_verified")
    if not checks.get("pre_runtime_trial_package_status_sealed", False):
        issues.append("pre_runtime_trial_package_status_not_sealed")

    return checks, issues


def validate_closure_gate_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("execution_planning_closure_gate_profile") or {}
    if profile.get("execution_planning_ref") != EXECUTION_PLANNING_REF:
        issues.append("execution_planning_ref_mismatch")
    if profile.get("issuance_package_ref") != ISSUANCE_PACKAGE_REF:
        issues.append("issuance_package_ref_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")
    if profile.get("pre_runtime_trial_package_status") != PRE_RUNTIME_TRIAL_PACKAGE_STATUS:
        issues.append("pre_runtime_trial_package_status_mismatch")

    items = matrix.get("readiness_gate_items") or []
    if len(items) != 6:
        issues.append(f"readiness_gate_item_count:{len(items)}")

    gate_refs = {i.get("gate_ref") for i in items}
    if gate_refs != set(READINESS_GATE_ITEM_REFS):
        issues.append(f"readiness_gate_item_refs_mismatch:{sorted(gate_refs)!r}")

    scope_ok, scope_issues = verify_scope_preserved_from_execution_planning(items)
    if not scope_ok:
        issues.extend(scope_issues)

    for item in items:
        gate_ref = item.get("gate_ref")
        plan_ref = item.get("execution_plan_ref")
        if EXECUTION_PLAN_REF_MAP.get(gate_ref or "") != plan_ref:
            issues.append(f"{gate_ref}.execution_plan_ref_mismatch")
        if "runtime_activation" not in (item.get("blocked_operations") or ()):
            issues.append(f"{gate_ref}.runtime_activation_not_blocked")
        next_step = item.get("allowed_next_step")
        if next_step not in PLANNING_ONLY_NEXT_STEPS:
            issues.append(f"{gate_ref}.allowed_next_step_not_planning_only")

    gps = next((i for i in items if i.get("gate_ref") == "gps_slam_conflict_readiness_gate"), {})
    if gps.get("readiness_gate_status") != "blocked_preserved":
        issues.append("gps_slam_conflict_not_blocked_preserved")
    if gps.get("gate_passed") is not False:
        issues.append("gps_slam_conflict_gate_passed_must_be_false")

    subway = next((i for i in items if i.get("gate_ref") == "subway_enter_station_readiness_gate"), {})
    if not subway.get("gate_constraints"):
        issues.append("subway_gate_constraints_missing")

    return len(issues) == 0 and registry_ok, issues


def review_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_matrix_v1()
    matrix_ok, matrix_issues = validate_closure_gate_matrix_v1(matrix)
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

    items = matrix.get("readiness_gate_items") or []
    gate_go = matrix.get("readiness_gate_go_map") or {}

    scope_preserved, _ = verify_scope_preserved_from_execution_planning(items)
    replay_bindings = _replay_capable_bindings_ok(items)
    blocked_checks = _blocked_ops_check(items)

    gps = next((i for i in items if i.get("gate_ref") == "gps_slam_conflict_readiness_gate"), {})
    subway = next((i for i in items if i.get("gate_ref") == "subway_enter_station_readiness_gate"), {})
    observation_items = [
        i
        for i in items
        if i.get("gate_scope") == "observation_only"
        and i.get("readiness_gate_status") == "observation_only_ready_for_replay_planning"
    ]
    low_risk_items = [
        i
        for i in items
        if i.get("gate_scope") == "low_risk_controlled_trial_candidate"
        and i.get("gate_passed") is True
    ]

    review_checkpoints: Dict[str, Any] = {
        "closure_gate_profile_count": 1,
        "readiness_gate_item_count": len(items),
        "execution_planning_go_verified": upstream_checks.get("execution_planning_go_verified", False),
        "issuance_package_go_verified": upstream_checks.get("issuance_package_go_verified", False),
        "pre_runtime_trial_package_status_sealed": upstream_checks.get(
            "pre_runtime_trial_package_status_sealed", False
        ),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        **gate_go,
        "scenario_scope_preserved_for_all": scope_preserved,
        "blocked_scenario_remains_blocked": (
            gps.get("gate_scope") == "blocked"
            and gps.get("source_execution_plan_status") == "blocked_no_execution_plan"
            and gps.get("readiness_gate_status") == "blocked_preserved"
        ),
        "blocked_scenario_cannot_pass_readiness_gate": gps.get("gate_passed") is False,
        "observation_only_remains_observation_replay": len(observation_items) == 2,
        "constrained_item_constraints_preserved": bool(subway.get("gate_constraints")),
        "low_risk_candidates_do_not_start_runtime": all(
            i.get("readiness_gate_status") in (
                "ready_for_controlled_replay_trial_planning",
                "observation_only_ready_for_replay_planning",
            )
            for i in low_risk_items
        ),
        **replay_bindings,
        **blocked_checks,
        "source_chain_required": all(i.get("source_chain") == SOURCE_CHAIN for i in items),
        "upstream_refs_required": all(i.get("upstream_refs") for i in items),
        "allowed_next_step_planning_only": all(
            i.get("allowed_next_step") in PLANNING_ONLY_NEXT_STEPS for i in items
        ),
        "readiness_gate_not_runtime_execution": NON_EXECUTION_FLAGS.get(
            "readiness_gate_not_runtime_execution"
        ),
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "execution_planning_ref_locked": EXECUTION_PLANNING_REF,
        "issuance_package_ref_locked": ISSUANCE_PACKAGE_REF,
        "pre_runtime_trial_package_status_locked": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        "candidate_only_source_chain_required": CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "closure_gate_profile_count_eq_1": review_checkpoints["closure_gate_profile_count"] == 1,
        "readiness_gate_item_count_eq_6": review_checkpoints["readiness_gate_item_count"] == 6,
        "execution_planning_go_verified": review_checkpoints["execution_planning_go_verified"] is True,
        "issuance_package_go_verified": review_checkpoints["issuance_package_go_verified"] is True,
        "pre_runtime_trial_package_status_sealed": (
            review_checkpoints["pre_runtime_trial_package_status_sealed"] is True
        ),
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        **{key: review_checkpoints.get(key) is True for key in READINESS_GATE_GO_KEYS},
        "scenario_scope_preserved_for_all": scope_preserved is True,
        "blocked_scenario_remains_blocked": review_checkpoints["blocked_scenario_remains_blocked"] is True,
        "blocked_scenario_cannot_pass_readiness_gate": (
            review_checkpoints["blocked_scenario_cannot_pass_readiness_gate"] is True
        ),
        "observation_only_remains_observation_replay": (
            review_checkpoints["observation_only_remains_observation_replay"] is True
        ),
        "constrained_item_constraints_preserved": (
            review_checkpoints["constrained_item_constraints_preserved"] is True
        ),
        "low_risk_candidates_do_not_start_runtime": (
            review_checkpoints["low_risk_candidates_do_not_start_runtime"] is True
        ),
        "human_ack_declared_for_replay_capable_scenarios": (
            replay_bindings["human_ack_declared_for_replay_capable_scenarios"] is True
        ),
        "rollback_readiness_bound_for_replay_capable_scenarios": (
            replay_bindings["rollback_readiness_bound_for_replay_capable_scenarios"] is True
        ),
        "observation_log_readiness_bound_for_replay_capable_scenarios": (
            replay_bindings["observation_log_readiness_bound_for_replay_capable_scenarios"] is True
        ),
        "failure_handling_readiness_bound_for_replay_capable_scenarios": (
            replay_bindings["failure_handling_readiness_bound_for_replay_capable_scenarios"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "allowed_next_step_planning_only": review_checkpoints["allowed_next_step_planning_only"] is True,
        "readiness_gate_not_runtime_execution": (
            review_checkpoints["readiness_gate_not_runtime_execution"] is True
        ),
        "runtime_activation_blocked_for_all": blocked_checks["runtime_activation_blocked_for_all"] is True,
        "direct_action_blocked_for_all": blocked_checks["direct_action_blocked_for_all"] is True,
        "direct_speech_blocked_for_all": blocked_checks["direct_speech_blocked_for_all"] is True,
        "direct_fact_write_blocked_for_all": blocked_checks["direct_fact_write_blocked_for_all"] is True,
        "real_navigation_blocked_for_all": blocked_checks["real_navigation_blocked_for_all"] is True,
        "live_sensor_trigger_blocked_for_all": blocked_checks["live_sensor_trigger_blocked_for_all"] is True,
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Execution Planning Closure Trial Readiness Gate Review",
        "lifecycle_variant": "compressed_execution_planning_closure_trial_readiness_gate_review",
        "closure_gate_principle_zh": CLOSURE_GATE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "execution_planning_ref": EXECUTION_PLANNING_REF,
        "issuance_package_ref": ISSUANCE_PACKAGE_REF,
        "pre_runtime_trial_package_status": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "closure_gate_governance_rules": list(CLOSURE_GATE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "closure_gate_matrix": matrix,
        "conclusions": {
            "closure_gate_status": "ready_for_controlled_replay_trial_planning" if review_ok else "blocked",
            "readiness_gate_not_runtime_execution": True,
            "runtime_activation_deferred": True,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "readiness_gate_summary": {
                "ready_for_controlled_replay_trial_planning": [
                    "mall_find_entrance_readiness_gate",
                    "home_return_readiness_gate",
                ],
                "ready_with_constraints_for_controlled_replay_trial_planning": [
                    "subway_enter_station_readiness_gate",
                ],
                "observation_only_ready_for_replay_planning": [
                    "stadium_concert_ticket_gate_readiness_gate",
                    "plaza_market_crowd_readiness_gate",
                ],
                "blocked_preserved": ["gps_slam_conflict_readiness_gate"],
            },
            "controlled_replay_note": (
                "Next: Controlled Replay Trial Planning — still not live runtime."
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
    result = review_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "closure_gate_profile_count": checkpoints["closure_gate_profile_count"],
                "readiness_gate_item_count": checkpoints["readiness_gate_item_count"],
                "execution_planning_go_verified": checkpoints["execution_planning_go_verified"],
                "mall_find_entrance_ready_for_controlled_replay_trial_planning": checkpoints.get(
                    "mall_find_entrance_ready_for_controlled_replay_trial_planning"
                ),
                "gps_slam_conflict_blocked_preserved": checkpoints.get(
                    "gps_slam_conflict_blocked_preserved"
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
