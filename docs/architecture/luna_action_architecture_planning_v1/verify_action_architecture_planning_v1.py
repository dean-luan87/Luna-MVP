#!/usr/bin/env python3
"""
Verifier for Phase-Luna-Action-Architecture-Planning-v1-001.

This verifier is planning-only and performs static checks over artifacts.
It does not execute runtime, task scheduling, or device operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


PHASE_DIR = Path(__file__).resolve().parent


def _load_json(name: str) -> Dict[str, Any]:
    p = PHASE_DIR / name
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _check(
    condition: bool, code: str, message: str, findings: List[Dict[str, Any]]
) -> None:
    findings.append({"code": code, "passed": bool(condition), "message": message})


def _all_expected_present() -> Tuple[bool, List[str], List[str]]:
    contract = _load_json("phase_contract.json")
    expected = contract.get("expected_outputs", [])
    missing: List[str] = []
    for rel in expected:
        if not (PHASE_DIR / rel).exists():
            missing.append(rel)
    return (len(missing) == 0, expected, missing)


def run_verification() -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []

    ok_files, expected, missing = _all_expected_present()
    _check(
        ok_files, "FILES_COMPLETE", "All expected phase output files exist.", findings
    )

    owner = _load_json("action_owner_boundary_candidate_v1.json")
    _check(
        owner.get("canonical_owner") == "Action Governance",
        "OWNER_CANONICAL",
        "Canonical owner must be Action Governance.",
        findings,
    )
    _check(
        bool(owner.get("unique_owner")) is True,
        "OWNER_UNIQUE",
        "Owner must be unique.",
        findings,
    )
    aliases = owner.get("legacy_aliases", [])
    alias_safe = all(
        not a.get("creates_new_owner", True) and not a.get("mutation_authority", True)
        for a in aliases
    )
    _check(
        alias_safe,
        "OWNER_ALIAS_SAFE",
        "Legacy aliases must not create parallel ownership or mutation authority.",
        findings,
    )

    concept = _load_json("action_concept_boundary_matrix_v1.json")
    neq = concept.get("non_equivalence_guards", {})
    _check(
        bool(neq.get("decision_not_action")),
        "CONCEPT_DECISION_NEQ_ACTION",
        "Decision must not equal Action.",
        findings,
    )
    _check(
        bool(neq.get("selected_decision_not_action_execution")),
        "CONCEPT_SELECTED_NEQ_EXECUTED",
        "Selected decision must not equal action execution.",
        findings,
    )
    _check(
        bool(neq.get("action_candidate_not_runtime_command")),
        "CONCEPT_CANDIDATE_NEQ_RUNTIME_COMMAND",
        "Action candidate must not equal runtime command.",
        findings,
    )

    precondition = _load_json("action_precondition_model_candidate_v1.json")
    pre_rules = precondition.get("rules", {})
    _check(
        bool(pre_rules.get("unknown_not_satisfied")),
        "PRECONDITION_UNKNOWN_BLOCKS",
        "Unknown precondition must not be treated as satisfied.",
        findings,
    )

    perm = _load_json("action_permission_safety_boundary_candidate_v1.json")
    _check(
        bool(perm.get("permission_recheck", {}).get("required")),
        "PERMISSION_RECHECK_REQUIRED",
        "Permission re-check must be required.",
        findings,
    )
    _check(
        bool(perm.get("safety_recheck", {}).get("required")),
        "SAFETY_RECHECK_REQUIRED",
        "Safety re-check must be required.",
        findings,
    )
    _check(
        bool(
            perm.get("guards", {}).get(
                "permission_inheritance_without_validation_forbidden"
            )
        ),
        "PERMISSION_NO_INHERIT_BYPASS",
        "No permanent permission inheritance without re-validation.",
        findings,
    )
    _check(
        bool(
            perm.get("guards", {}).get(
                "safety_inheritance_without_validation_forbidden"
            )
        ),
        "SAFETY_NO_INHERIT_BYPASS",
        "No permanent safety inheritance without re-validation.",
        findings,
    )

    confirm = _load_json("action_human_confirmation_boundary_candidate_v1.json")
    c_rules = confirm.get("rules", {})
    _check(
        bool(c_rules.get("stale_confirmation_reuse_forbidden")),
        "CONFIRM_STALE_FORBIDDEN",
        "Stale confirmation reuse must be forbidden.",
        findings,
    )
    _check(
        bool(c_rules.get("fabricated_confirmation_forbidden")),
        "CONFIRM_FABRICATION_FORBIDDEN",
        "Fabricated confirmation must be forbidden.",
        findings,
    )

    reversibility = _load_json("action_reversibility_model_candidate_v1.json")
    i_rules = reversibility.get("irreversible_escalation_rules", {})
    _check(
        bool(i_rules.get("stronger_confirmation_requirement")),
        "IRREVERSIBLE_STRICTER_GATE",
        "Irreversible actions must use stricter gates.",
        findings,
    )

    readiness = _load_json("action_execution_readiness_model_candidate_v1.json")
    r_guards = readiness.get("guards", {})
    _check(
        bool(r_guards.get("ready_not_executed")),
        "READINESS_NOT_EXECUTION",
        "Ready candidate must not imply execution.",
        findings,
    )

    cancel_suspend = _load_json(
        "action_cancellation_suspension_model_candidate_v1.json"
    )
    _check(
        bool(cancel_suspend.get("guards", {}).get("cancelled_not_suspended")),
        "CANCEL_NOT_SUSPEND",
        "Cancelled and suspended must remain distinct semantics.",
        findings,
    )

    rollback = _load_json("action_rollback_boundary_candidate_v1.json")
    _check(
        bool(rollback.get("rules", {}).get("rollback_candidate_not_execution")),
        "ROLLBACK_BOUNDARY",
        "Rollback in this phase is boundary-only and non-executing.",
        findings,
    )

    failure = _load_json("action_failure_boundary_candidate_v1.json")
    d_contract = failure.get("downstream_result_contract", {})
    _check(
        bool(d_contract.get("execution_result_reference_required")),
        "FAILURE_RESULT_REF_REQUIRED",
        "Failure boundary requires execution result reference.",
        findings,
    )

    task = _load_json("action_task_manager_boundary_candidate_v1.json")
    _check(
        bool(
            task.get("task_relation", {}).get("action_governance_no_real_task_creation")
        ),
        "TASK_NO_REAL_CREATE",
        "Action governance must not create real task.",
        findings,
    )
    _check(
        bool(task.get("task_handoff", {}).get("reference_only")),
        "TASK_HANDOFF_REFERENCE_ONLY",
        "Task handoff must be reference-only.",
        findings,
    )

    executor = _load_json("action_runtime_executor_handoff_contract_candidate_v1.json")
    _check(
        executor.get("handoff_kind") == "candidate_only_reference_handoff",
        "EXECUTOR_HANDOFF_KIND",
        "Executor handoff must be candidate-only reference handoff.",
        findings,
    )

    scenarios = _load_json("action_minimum_scenario_suite_v1.json")
    scenario_ok = (
        scenarios.get("scenario_count") == 16
        and len(scenarios.get("scenarios", [])) == 16
    )
    _check(
        scenario_ok,
        "SCENARIO_COUNT_16",
        "Scenario suite must include exactly 16 scenarios.",
        findings,
    )

    manifest = _load_json("action_planning_change_manifest_v1.json")
    _check(
        bool(manifest.get("new_files_only")),
        "NEW_FILES_ONLY",
        "Planning phase must only add new files in target folder.",
        findings,
    )
    _check(
        len(manifest.get("modified_existing_assets", [])) == 0,
        "NO_EXISTING_ASSET_MODIFIED",
        "No existing upstream asset should be modified.",
        findings,
    )

    negative = _load_json("action_negative_guards_v1.json")
    forbidden_flags = negative.get("forbidden_flags", {})
    _check(
        bool(forbidden_flags.get("planning_only_false")),
        "FLAG_GUARD_PLANNING_ONLY",
        "planning_only=false must be forbidden.",
        findings,
    )
    _check(
        bool(forbidden_flags.get("runtime_executed_true")),
        "FLAG_GUARD_RUNTIME_EXECUTED",
        "runtime_executed=true must be forbidden.",
        findings,
    )
    _check(
        bool(forbidden_flags.get("action_execution_true")),
        "FLAG_GUARD_ACTION_EXECUTION",
        "action_execution=true must be forbidden.",
        findings,
    )
    _check(
        bool(forbidden_flags.get("task_created_true")),
        "FLAG_GUARD_TASK_CREATED",
        "task_created=true must be forbidden.",
        findings,
    )
    _check(
        bool(forbidden_flags.get("database_write_true")),
        "FLAG_GUARD_DATABASE_WRITE",
        "database_write=true must be forbidden.",
        findings,
    )
    _check(
        bool(forbidden_flags.get("device_control_true")),
        "FLAG_GUARD_DEVICE_CONTROL",
        "device_control=true must be forbidden.",
        findings,
    )
    _check(
        bool(forbidden_flags.get("scheduler_execution_true")),
        "FLAG_GUARD_SCHEDULER_EXEC",
        "scheduler_execution=true must be forbidden.",
        findings,
    )

    passed = all(item["passed"] for item in findings)

    return {
        "phase": "Phase-Luna-Action-Architecture-Planning-v1-001",
        "planning_only": True,
        "expected_file_count": len(expected),
        "missing_files": missing,
        "findings": findings,
        "all_passed": passed,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION"
        if passed
        else "VERIFICATION_FAILED",
    }


def main() -> int:
    result = run_verification()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("all_passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
