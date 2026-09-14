# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_planning.phase_one_environment_cognition_runtime_trial_planning_registry_v1 import (
    REGISTRY_ID,
    build_phase_one_environment_cognition_runtime_trial_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_planning.phase_one_environment_cognition_runtime_trial_planning_types_v1 import (
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
    PLANNING_GOVERNANCE_RULES,
    PLANNING_OBJECT_TYPES,
    PLANNING_PRINCIPLE_ZH,
    PROHIBITED_ITEMS,
    RUNTIME_ADMISSION_LEVELS,
    RUNTIME_TRIAL_MODE,
    SCENARIO_POLICY_GO_KEYS,
    SCENARIO_POLICY_REFS,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_planning_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
    "phase_one_environment_cognition_runtime_trial_planning_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
    "phase_one_environment_cognition_runtime_trial_planning_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
    "review_phase_one_environment_cognition_runtime_trial_planning_v1.py",
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

    checks["sealed_phase_one_chain_verified"] = (
        checks.get(f"{PHASE_ONE_CHAIN_REF}.go_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.phase_one_chain_sealed", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.module_present", False)
        and checks.get(f"{PHASE_ONE_CHAIN_REF}.artifact_present", False)
    )
    if not checks["sealed_phase_one_chain_verified"]:
        issues.append("sealed_phase_one_chain_not_verified")

    return checks, issues


def validate_planning_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("controlled_runtime_trial_planning_profile") or {}
    if profile.get("phase_one_chain_ref") != PHASE_ONE_CHAIN_REF:
        issues.append("phase_one_chain_ref_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")
    if profile.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_mismatch")
    if profile.get("task_manager_entrypoint") != TASK_MANAGER_ENTRYPOINT:
        issues.append("task_manager_entrypoint_mismatch")
    if profile.get("guidance_entrypoint") != GUIDANCE_ENTRYPOINT:
        issues.append("guidance_entrypoint_mismatch")
    if profile.get("speech_gate_entrypoint") != SPEECH_GATE_ENTRYPOINT:
        issues.append("speech_gate_entrypoint_mismatch")
    if profile.get("action_safety_entrypoint") != ACTION_SAFETY_ENTRYPOINT:
        issues.append("action_safety_entrypoint_mismatch")
    if profile.get("candidate_only_source_chain_required") is not CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED:
        issues.append("candidate_only_source_chain_required_mismatch")

    policies = matrix.get("scenario_policies") or []
    if len(policies) != 6:
        issues.append(f"scenario_policy_count:{len(policies)}")

    policy_refs = {p.get("policy_ref") for p in policies}
    if policy_refs != set(SCENARIO_POLICY_REFS):
        issues.append(f"scenario_policy_refs_mismatch:{sorted(policy_refs)!r}")

    admission_levels = {p.get("admission_level") for p in policies}
    if not admission_levels.issubset(set(RUNTIME_ADMISSION_LEVELS)):
        issues.append(f"invalid_admission_levels:{sorted(admission_levels)!r}")

    for policy in policies:
        if not policy.get("admission_level"):
            issues.append(f"{policy.get('policy_ref')}.admission_level_missing")
        if not policy.get("rollback_policy_ref"):
            issues.append(f"{policy.get('policy_ref')}.rollback_policy_missing")
        if not policy.get("observation_log_policy_ref"):
            issues.append(f"{policy.get('policy_ref')}.observation_log_policy_missing")
        if policy.get("source_chain") != SOURCE_CHAIN:
            issues.append(f"{policy.get('policy_ref')}.source_chain_mismatch")
        if not policy.get("upstream_refs"):
            issues.append(f"{policy.get('policy_ref')}.upstream_refs_missing")

    shared = matrix.get("shared_requirements") or {}
    owner = shared.get("owner_approval_requirement") or {}
    if owner.get("owner_approval_required") is not True:
        issues.append("owner_approval_required_false")
    if owner.get("owner_approval_runtime_not_issued") is not True:
        issues.append("owner_approval_runtime_not_issued_false")

    rollback = shared.get("rollback_requirement") or {}
    if rollback.get("rollback_policy_required") is not True:
        issues.append("rollback_policy_required_false")

    obs = shared.get("observation_log_requirement") or {}
    if obs.get("observation_log_policy_required") is not True:
        issues.append("observation_log_policy_required_false")

    failure = shared.get("failure_handling_policy") or {}
    if failure.get("failure_handling_policy_required") is not True:
        issues.append("failure_handling_policy_required_false")

    safety = shared.get("safety_gate_requirement") or {}
    if safety.get("action_safety_candidate_required") is not True:
        issues.append("action_safety_candidate_required_false")
    if safety.get("speech_gate_candidate_required") is not True:
        issues.append("speech_gate_candidate_required_false")

    return len(issues) == 0 and registry_ok, issues


def _admission_level_support(
    policies: List[Dict[str, Any]],
) -> Dict[str, bool]:
    levels = {p.get("admission_level") for p in policies}
    return {
        "blocked_scenario_supported": "blocked" in levels,
        "observation_only_scenario_supported": "observation_only" in levels,
        "cautious_candidate_trial_supported": "cautious_candidate_trial" in levels,
        "low_risk_controlled_trial_candidate_supported": (
            "low_risk_controlled_trial_candidate" in levels
        ),
    }


def review_phase_one_environment_cognition_runtime_trial_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_planning_matrix_v1(matrix)
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

    profile = matrix.get("controlled_runtime_trial_planning_profile") or {}
    policies = matrix.get("scenario_policies") or []
    shared = matrix.get("shared_requirements") or {}
    scenario_go = matrix.get("scenario_policy_go_map") or {}
    admission_support = _admission_level_support(policies)

    owner = shared.get("owner_approval_requirement") or {}
    safety = shared.get("safety_gate_requirement") or {}
    rollback = shared.get("rollback_requirement") or {}
    obs = shared.get("observation_log_requirement") or {}
    failure = shared.get("failure_handling_policy") or {}

    admission_level_declared_for_all = all(p.get("admission_level") for p in policies)

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "scenario_policy_count": len(policies),
        "sealed_phase_one_chain_verified": upstream_checks.get("sealed_phase_one_chain_verified", False),
        **scenario_go,
        "admission_level_declared_for_all": admission_level_declared_for_all,
        **admission_support,
        "owner_approval_required": owner.get("owner_approval_required"),
        "owner_approval_runtime_not_issued": owner.get("owner_approval_runtime_not_issued"),
        "rollback_policy_required": rollback.get("rollback_policy_required"),
        "observation_log_policy_required": obs.get("observation_log_policy_required"),
        "failure_handling_policy_required": failure.get("failure_handling_policy_required"),
        "action_safety_candidate_required": safety.get("action_safety_candidate_required"),
        "speech_gate_candidate_required": safety.get("speech_gate_candidate_required"),
        "gps_slam_conflict_blocks_runtime_trial": any(
            p.get("policy_ref") == "gps_slam_conflict_runtime_blocker"
            and p.get("admission_level") == "blocked"
            for p in policies
        ),
        "crowd_high_risk_blocks_movement_guidance_trial": any(
            p.get("policy_ref") == "plaza_market_crowd_blocked_or_observation_only"
            and p.get("admission_level") == "observation_only"
            for p in policies
        ),
        "event_overlay_does_not_rewrite_map_place": any(
            "event_overlay_must_not_rewrite_map_place_ref" in (p.get("trial_conditions") or ())
            for p in policies
        ),
        "field_interaction_label_not_fact": True,
        "source_chain_required": all(p.get("source_chain") == SOURCE_CHAIN for p in policies),
        "upstream_refs_required": all(p.get("upstream_refs") for p in policies),
        "candidate_only_source_chain_required": profile.get("candidate_only_source_chain_required"),
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
        "guidance_entrypoint_locked": GUIDANCE_ENTRYPOINT,
        "speech_gate_entrypoint_locked": SPEECH_GATE_ENTRYPOINT,
        "action_safety_entrypoint_locked": ACTION_SAFETY_ENTRYPOINT,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "phase_one_chain_ref_locked": PHASE_ONE_CHAIN_REF,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "planning_profile_count_eq_1": review_checkpoints["planning_profile_count"] == 1,
        "scenario_policy_count_eq_6": review_checkpoints["scenario_policy_count"] == 6,
        "sealed_phase_one_chain_verified": review_checkpoints["sealed_phase_one_chain_verified"] is True,
        **{key: review_checkpoints.get(key) is True for key in SCENARIO_POLICY_GO_KEYS},
        "admission_level_declared_for_all": admission_level_declared_for_all is True,
        "blocked_scenario_supported": admission_support["blocked_scenario_supported"] is True,
        "observation_only_scenario_supported": admission_support["observation_only_scenario_supported"] is True,
        "cautious_candidate_trial_supported": admission_support["cautious_candidate_trial_supported"] is True,
        "low_risk_controlled_trial_candidate_supported": (
            admission_support["low_risk_controlled_trial_candidate_supported"] is True
        ),
        "owner_approval_required": review_checkpoints["owner_approval_required"] is True,
        "owner_approval_runtime_not_issued": review_checkpoints["owner_approval_runtime_not_issued"] is True,
        "rollback_policy_required": review_checkpoints["rollback_policy_required"] is True,
        "observation_log_policy_required": review_checkpoints["observation_log_policy_required"] is True,
        "failure_handling_policy_required": review_checkpoints["failure_handling_policy_required"] is True,
        "action_safety_candidate_required": review_checkpoints["action_safety_candidate_required"] is True,
        "speech_gate_candidate_required": review_checkpoints["speech_gate_candidate_required"] is True,
        "gps_slam_conflict_blocks_runtime_trial": review_checkpoints["gps_slam_conflict_blocks_runtime_trial"] is True,
        "crowd_high_risk_blocks_movement_guidance_trial": (
            review_checkpoints["crowd_high_risk_blocks_movement_guidance_trial"] is True
        ),
        "event_overlay_does_not_rewrite_map_place": (
            review_checkpoints["event_overlay_does_not_rewrite_map_place"] is True
        ),
        "field_interaction_label_not_fact": review_checkpoints["field_interaction_label_not_fact"] is True,
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "upstream_refs_required": review_checkpoints["upstream_refs_required"] is True,
        "candidate_only_source_chain_required": (
            review_checkpoints["candidate_only_source_chain_required"] is CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED
        ),
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Planning Matrix + Review",
        "lifecycle_variant": "compressed_runtime_trial_planning_review",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "planning_object_types": list(PLANNING_OBJECT_TYPES),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "phase_one_chain_ref": PHASE_ONE_CHAIN_REF,
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "prohibited_items": list(PROHIBITED_ITEMS),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "planning_matrix": matrix,
        "conclusions": {
            "runtime_trial_planning_status": "ready_for_owner_approval_request" if review_ok else "blocked",
            "runtime_activation_deferred": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
            "guidance_safety_entrypoints_locked": {
                "guidance": GUIDANCE_ENTRYPOINT,
                "speech_gate": SPEECH_GATE_ENTRYPOINT,
                "action_safety": ACTION_SAFETY_ENTRYPOINT,
            },
            "owner_approval_note": (
                "Owner approval runtime not issued; proceed to Owner Approval Request phase before trial issuance."
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
    result = review_phase_one_environment_cognition_runtime_trial_planning_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "planning_profile_count": checkpoints["planning_profile_count"],
                "scenario_policy_count": checkpoints["scenario_policy_count"],
                "sealed_phase_one_chain_verified": checkpoints["sealed_phase_one_chain_verified"],
                "mall_find_entrance_low_risk_trial_candidate": checkpoints.get(
                    "mall_find_entrance_low_risk_trial_candidate"
                ),
                "gps_slam_conflict_runtime_blocker": checkpoints.get("gps_slam_conflict_runtime_blocker"),
                "owner_approval_runtime_not_issued": checkpoints.get("owner_approval_runtime_not_issued"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
