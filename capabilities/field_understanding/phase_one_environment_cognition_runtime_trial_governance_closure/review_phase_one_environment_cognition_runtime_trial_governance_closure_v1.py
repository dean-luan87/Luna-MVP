# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Runtime Trial Governance Closure — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_governance_closure.phase_one_environment_cognition_runtime_trial_governance_closure_registry_v1 import (
    REGISTRY_ID,
    _EXECUTION_PLANNING_ARTIFACT_REL,
    _GOVERNANCE_STAGE_SPECS,
    _MIDPLATFORM_UPSTREAM_SPECS,
    _SCENARIO_SPECS,
    build_phase_one_environment_cognition_runtime_trial_governance_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_governance_closure.phase_one_environment_cognition_runtime_trial_governance_closure_types_v1 import (
    _CANDIDATE_ONLY_ALLOWED_MARKERS,
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GOVERNANCE_CLOSURE_RULES,
    GOVERNANCE_CLOSURE_PRINCIPLE_ZH,
    GOVERNANCE_STAGE_GO_KEYS,
    GOVERNANCE_STAGE_REFS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_CHAIN_STATUS,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    RUNTIME_TRIAL_MODE,
    SCENARIO_COVERAGE_GO_KEYS,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_STAGES,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "phase_one_environment_cognition_runtime_trial_governance_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_runtime_trial_governance_closure_review_v1.json"

STEP_FILES = (
    "capabilities/midplatform/controlled_trial_governance/controlled_trial_governance_lifecycle_template_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
    "phase_one_environment_cognition_runtime_trial_governance_closure_types_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
    "phase_one_environment_cognition_runtime_trial_governance_closure_registry_v1.py",
    "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_governance_closure/"
    "review_phase_one_environment_cognition_runtime_trial_governance_closure_v1.py",
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


def verify_scenario_coverage_from_execution_planning(
    coverage: List[Dict[str, Any]],
) -> Tuple[bool, Dict[str, bool], List[str]]:
    execution_plans = _execution_plans_by_ref()
    if not execution_plans:
        return False, {}, ["execution_plans_unavailable"]

    go_map: Dict[str, bool] = {}
    issues: List[str] = []
    for spec in _SCENARIO_SPECS:
        plan = execution_plans.get(spec["plan_ref"], {})
        scope_ok = plan.get("execution_scope") == spec["expected_scope"]
        status_ok = plan.get("execution_plan_status") == spec["expected_execution_plan_status"]
        go_key = spec["go_key"]
        go_map[go_key] = scope_ok and status_ok
        if not scope_ok:
            issues.append(
                f"{spec['scenario_ref']}.scope_mismatch:"
                f"{plan.get('execution_scope')!r}!={spec['expected_scope']!r}"
            )
        if not status_ok:
            issues.append(
                f"{spec['scenario_ref']}.status_mismatch:"
                f"{plan.get('execution_plan_status')!r}!={spec['expected_execution_plan_status']!r}"
            )
    return len(issues) == 0, go_map, issues


def _allowed_plan_candidate_only(items: List[Dict[str, Any]]) -> bool:
    for item in items:
        for op in item.get("allowed_plan_operations") or ():
            if not any(marker in op for marker in _CANDIDATE_ONLY_ALLOWED_MARKERS):
                return False
    return True


def _live_sensor_trigger_blocked(items: List[Dict[str, Any]]) -> bool:
    for item in items:
        if "live_sensor_trigger" not in (item.get("blocked_operations") or ()):
            return False
    return True


def review_governance_stage_artifacts(
    matrix: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for spec in matrix.get("governance_stage_specs") or _GOVERNANCE_STAGE_SPECS:
        phase_ref = spec["phase_ref"]
        go_key = spec["go_key"]
        module_path = _REPO_ROOT / spec["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"governance_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(spec["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            issues.append(f"governance_artifact_missing:{phase_ref}")
            checks[go_key] = False
            continue

        actual_go = (artifact or {}).get("final_decision")
        expected_go = spec["expected_final_decision"]
        go_ok = actual_go == expected_go
        checks[go_key] = go_ok
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"governance_go_mismatch:{phase_ref}:{actual_go!r}")

        if spec.get("require_pre_package_sealed") and artifact:
            pre_sealed = (
                artifact.get("conclusions", {}).get("pre_runtime_trial_package_status") == "sealed"
                or artifact.get("conclusions", {}).get("runtime_trial_pre_package_sealed") is True
            )
            checks["pre_runtime_package_status_sealed"] = pre_sealed
            if not pre_sealed:
                issues.append("pre_runtime_trial_package_not_sealed")

    for spec in matrix.get("midplatform_upstream_specs") or _MIDPLATFORM_UPSTREAM_SPECS:
        phase_ref = spec["phase_ref"]
        module_path = _REPO_ROOT / spec["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"midplatform_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(spec["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            issues.append(f"midplatform_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        expected_go = spec["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"midplatform_go_mismatch:{phase_ref}:{actual_go!r}")

    checks["all_governance_stage_refs_verified"] = all(
        checks.get(spec["go_key"], False) for spec in _GOVERNANCE_STAGE_SPECS
    )
    if not checks["all_governance_stage_refs_verified"]:
        issues.append("all_governance_stage_refs_not_verified")

    if not checks.get("pre_runtime_package_status_sealed", False):
        if "pre_runtime_trial_package_not_sealed" not in issues:
            issues.append("pre_runtime_package_status_not_sealed")

    return checks, issues


def validate_governance_closure_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_phase_one_environment_cognition_runtime_trial_governance_closure_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    closure = matrix.get("phase_one_runtime_trial_governance_closure") or {}
    if closure.get("controlled_trial_governance_template_ref") != CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    if closure.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")
    if closure.get("pre_runtime_trial_package_status") != PRE_RUNTIME_TRIAL_PACKAGE_STATUS:
        issues.append("pre_runtime_trial_package_status_mismatch")

    stage_refs = matrix.get("governance_stage_refs") or []
    if len(stage_refs) != 8:
        issues.append(f"governance_stage_ref_count:{len(stage_refs)}")

    stage_ref_ids = {s.get("stage_ref") for s in stage_refs}
    if stage_ref_ids != set(GOVERNANCE_STAGE_REFS):
        issues.append(f"governance_stage_refs_mismatch:{sorted(stage_ref_ids)!r}")

    template_matrix = matrix.get("controlled_trial_governance_template_matrix") or {}
    if template_matrix.get("template_id") != TEMPLATE_ID:
        issues.append("template_id_mismatch")
    if template_matrix.get("template_stage_count") != 7:
        issues.append("template_stage_count_not_7")

    reuse = matrix.get("reuse_binding") or {}
    if not reuse.get("execution_planning_marked_terminal_for_planning_only_chain"):
        issues.append("execution_planning_not_marked_terminal")
    if not reuse.get("no_further_gate_package_issuance_split_required"):
        issues.append("no_further_split_not_declared")

    return len(issues) == 0 and registry_ok, issues


def review_phase_one_environment_cognition_runtime_trial_governance_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_phase_one_environment_cognition_runtime_trial_governance_closure_matrix_v1()
    matrix_ok, matrix_issues = validate_governance_closure_matrix_v1(matrix)
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

    governance_checks, governance_issues = review_governance_stage_artifacts(matrix)
    failed_checks.extend(governance_issues)

    execution_plans = list(_execution_plans_by_ref().values())
    scenario_ok, scenario_go_map, scenario_issues = verify_scenario_coverage_from_execution_planning(
        matrix.get("scenario_coverage") or []
    )
    failed_checks.extend(scenario_issues)

    candidate_only_ok = _allowed_plan_candidate_only(execution_plans) if execution_plans else False
    live_sensor_blocked = _live_sensor_trigger_blocked(execution_plans) if execution_plans else False

    reuse = matrix.get("reuse_binding") or {}
    template_matrix = matrix.get("controlled_trial_governance_template_matrix") or {}

    review_checkpoints: Dict[str, Any] = {
        "governance_closure_profile_count": 1,
        "controlled_trial_governance_template_created": template_matrix.get("template_id") == TEMPLATE_ID,
        "controlled_trial_governance_template_stage_count": len(TEMPLATE_STAGES),
        "governance_stage_ref_count": len(matrix.get("governance_stage_refs") or []),
        "all_governance_stage_refs_verified": governance_checks.get(
            "all_governance_stage_refs_verified", False
        ),
        **{key: governance_checks.get(key, False) for key in GOVERNANCE_STAGE_GO_KEYS},
        "pre_runtime_package_status_sealed": governance_checks.get(
            "pre_runtime_package_status_sealed", False
        ),
        "pre_runtime_package_sealed": governance_checks.get("pre_runtime_package_status_sealed", False),
        **scenario_go_map,
        "scenario_scope_preserved_for_all": scenario_ok,
        "execution_planning_marked_terminal_for_planning_only_chain": reuse.get(
            "execution_planning_marked_terminal_for_planning_only_chain"
        ),
        "no_further_gate_package_issuance_split_required": reuse.get(
            "no_further_gate_package_issuance_split_required"
        ),
        "future_governance_reuse_template_required": reuse.get(
            "future_governance_reuse_template_required"
        ),
        "template_supports_compressed_mode": reuse.get("template_supports_compressed_mode"),
        "candidate_only_enforced": CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
        "allowed_operations_candidate_only": candidate_only_ok,
        "live_sensor_trigger_blocked_for_all": live_sensor_blocked,
        "runtime_activation_deferred": NON_EXECUTION_FLAGS.get("runtime_activation_deferred"),
        "source_chain_required": all(
            (s.get("source_chain") == SOURCE_CHAIN)
            for s in (matrix.get("governance_stage_refs") or [])
        ),
        "upstream_refs_required": True,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "controlled_trial_governance_template_ref_locked": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "pre_runtime_trial_package_status_locked": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_status_locked": PHASE_ONE_CHAIN_STATUS,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "governance_closure_profile_count_eq_1": review_checkpoints["governance_closure_profile_count"] == 1,
        "controlled_trial_governance_template_created": (
            review_checkpoints["controlled_trial_governance_template_created"] is True
        ),
        "controlled_trial_governance_template_stage_count_eq_7": (
            review_checkpoints["controlled_trial_governance_template_stage_count"] == 7
        ),
        "governance_stage_ref_count_eq_8": review_checkpoints["governance_stage_ref_count"] == 8,
        "all_governance_stage_refs_verified": (
            review_checkpoints["all_governance_stage_refs_verified"] is True
        ),
        **{key: review_checkpoints.get(key) is True for key in GOVERNANCE_STAGE_GO_KEYS},
        "pre_runtime_package_status_sealed": (
            review_checkpoints["pre_runtime_package_status_sealed"] is True
        ),
        **{key: review_checkpoints.get(key) is True for key in SCENARIO_COVERAGE_GO_KEYS},
        "execution_planning_marked_terminal_for_planning_only_chain": (
            review_checkpoints["execution_planning_marked_terminal_for_planning_only_chain"] is True
        ),
        "no_further_gate_package_issuance_split_required": (
            review_checkpoints["no_further_gate_package_issuance_split_required"] is True
        ),
        "future_governance_reuse_template_required": (
            review_checkpoints["future_governance_reuse_template_required"] is True
        ),
        "template_supports_compressed_mode": (
            review_checkpoints["template_supports_compressed_mode"] is True
        ),
        "candidate_only_enforced": review_checkpoints["candidate_only_enforced"] is True,
        "allowed_operations_candidate_only": review_checkpoints["allowed_operations_candidate_only"] is True,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "trial_runtime_started_false": review_checkpoints["trial_runtime_started"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "live_sensor_trigger_blocked_for_all": review_checkpoints["live_sensor_trigger_blocked_for_all"] is True,
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
        "step": "Phase One Environment Cognition Controlled Runtime Trial Governance Closure Review",
        "lifecycle_variant": "compressed_runtime_trial_governance_closure_review",
        "governance_closure_principle_zh": GOVERNANCE_CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "pre_runtime_trial_package_status": PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        "phase_one_chain_status": PHASE_ONE_CHAIN_STATUS,
        "governance_closure_rules": list(GOVERNANCE_CLOSURE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "governance_stage_review": governance_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "governance_closure_matrix": matrix,
        "conclusions": {
            "governance_closure_status": "sealed" if review_ok else "blocked",
            "governance_closure_not_runtime_activation": True,
            "execution_planning_terminal_for_planning_only_chain": True,
            "no_further_gate_package_issuance_split": True,
            "runtime_activation_deferred": True,
            "trial_runtime_started": False,
            "next_phase_ref": NEXT_PHASE_REF,
            "governance_chain_summary": {
                "sealed_stages": list(GOVERNANCE_STAGE_REFS),
                "terminal_stage": "execution_planning",
                "template_ref": TEMPLATE_ID,
            },
            "transition_note": (
                "Governance chain closed. Next: real offline input replay planning — "
                "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-Planning-v1-001."
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
    result = review_phase_one_environment_cognition_runtime_trial_governance_closure_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "governance_closure_profile_count": checkpoints["governance_closure_profile_count"],
                "controlled_trial_governance_template_stage_count": checkpoints[
                    "controlled_trial_governance_template_stage_count"
                ],
                "governance_stage_ref_count": checkpoints["governance_stage_ref_count"],
                "execution_planning_go_verified": checkpoints.get("execution_planning_go_verified"),
                "gps_slam_conflict_blocked_preserved": checkpoints.get(
                    "gps_slam_conflict_blocked_preserved"
                ),
                "no_further_gate_package_issuance_split_required": checkpoints.get(
                    "no_further_gate_package_issuance_split_required"
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
