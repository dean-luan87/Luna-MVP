"""Fail-closed verifier for the final controlled-runtime closure audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.verifier_v1 import (
    _cognitive_checks,
)

from .contract_audit_v1 import run_static_contract_audit


PHASE = "Phase-P1-Luna-Controlled-Cognitive-Runtime-Final-Closure-Audit-v1-001"
CLOSURE_DECISION = "LUNA_CONTROLLED_COGNITIVE_RUNTIME_BASELINE_V1_CLOSED"


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": observed}


def _verify_operational(full: Dict[str, Any]) -> list[Dict[str, Any]]:
    checks = [_check("full_e2e_operational_result", full.get("operational_result") == "PASS", full.get("operational_result"))]
    cases = full.get("operational_source", {}).get("cases") or []
    checks.append(_check("operational_two_cases", len(cases) == 2, len(cases)))
    for case in cases:
        action = case.get("action_boundary") or {}
        checks.extend(
            [
                _check(f"task_admitted:{case.get('case_id')}", case.get("task_manager_admitted") is True),
                _check(f"action_admitted:{case.get('case_id')}", action.get("action_boundary_admitted") is True),
                _check(f"action_candidate:{case.get('case_id')}", bool(case.get("action_candidate_ref"))),
                _check(f"runtime_handoff_candidate:{case.get('case_id')}", bool(case.get("runtime_executor_handoff_ref"))),
                _check(f"runtime_not_invoked:{case.get('case_id')}", case.get("runtime_executor_invoked") is False),
                _check(f"case_validation:{case.get('case_id')}", not case.get("validation_errors"), case.get("validation_errors")),
            ]
        )
    return checks


def _verify_cognitive(full: Dict[str, Any]) -> list[Dict[str, Any]]:
    checks = [_check("full_e2e_cognitive_result", full.get("cognitive_logic_result") == "PASS", full.get("cognitive_logic_result"))]
    capability_gaps = full.get("capability_gaps") or []
    checks.append(_check("no_cognitive_capability_gaps", not capability_gaps, capability_gaps))
    checks.extend(_cognitive_checks(full))
    return checks


def _verify_governance(full: Dict[str, Any]) -> list[Dict[str, Any]]:
    checks: list[Dict[str, Any]] = []
    for result in full.get("contrast_results") or ():
        proof = result.get("execution_proof") or {}
        checks.append(_check(
            f"cognition_owner:{result.get('contrast_id')}",
            proof.get("owner_ref") == "Cognitive State Formation Governance",
            proof.get("owner_ref"),
        ))
    for case in full.get("operational_source", {}).get("cases") or ():
        action = case.get("action_boundary") or {}
        candidate = action.get("action_candidate") or {}
        source_case = case.get("source_case") or {}
        task = ((source_case.get("task_case") or {}).get("task_manager") or {})
        checks.extend([
            _check(f"action_owner:{case.get('case_id')}", candidate.get("owner") == "Action Governance", candidate.get("owner")),
            _check(f"task_owner:{case.get('case_id')}", task.get("task_manager_owner_ref") == "Task Manager", task.get("task_manager_owner_ref")),
            _check(f"runtime_not_invoked:{case.get('case_id')}", case.get("runtime_executor_invoked") is False, case.get("runtime_executor_invoked")),
        ])
    forbidden = full.get("forbidden_behaviors") or {}
    checks.append(_check("forbidden_behaviors_closed", all(value is False for value in forbidden.values()), forbidden))
    return checks


def _verify_traceability(full: Dict[str, Any]) -> list[Dict[str, Any]]:
    checks: list[Dict[str, Any]] = []
    for result in full.get("contrast_results") or ():
        semantics = result.get("input_semantics") or {}
        proof = result.get("execution_proof") or {}
        required = (
            result.get("gateway_admission_ref"),
            result.get("a_route_execution_ref"),
            proof.get("execution_ref"),
            proof.get("owner_ref"),
            result.get("hypothesis_refs"),
            result.get("current_world_ref"),
            result.get("sufficiency_ref"),
            semantics.get("role_ref"),
            semantics.get("task_ref"),
            semantics.get("goal_ref"),
        )
        checks.append(_check(f"contrast_trace:{result.get('contrast_id')}", all(bool(item) for item in required), required))
    for case in full.get("operational_source", {}).get("cases") or ():
        required = (
            (case.get("traceability") or {}).get("final_cognition_execution_ref"),
            (case.get("traceability") or {}).get("final_sufficiency_ref"),
            (case.get("traceability") or {}).get("final_stop_ref"),
            (case.get("traceability") or {}).get("decision_candidate_ref"),
            (case.get("traceability") or {}).get("decision_trace_ref"),
            (case.get("traceability") or {}).get("task_state_ref"),
            (case.get("traceability") or {}).get("task_trace_ref"),
            (case.get("traceability") or {}).get("action_candidate_ref"),
            (case.get("traceability") or {}).get("action_trace_ref"),
            (case.get("traceability") or {}).get("runtime_executor_handoff_ref"),
        )
        checks.append(_check(f"downstream_trace:{case.get('case_id')}", all(bool(item) for item in required), required))
    return checks


def verify_report_v1(report: Dict[str, Any]) -> Dict[str, Any]:
    full = report.get("full_e2e_summary") or {}
    static = run_static_contract_audit()
    checks = [
        _check("phase_present", report.get("phase") == PHASE),
        _check("current_session_evidence", (report.get("current_session_evidence") or {}).get("status") == "PRODUCED_BY_FINAL_AUDIT_RUNNER"),
        *_verify_operational(full),
        *_verify_cognitive(full),
        *_verify_governance(full),
        *_verify_traceability(full),
        _check("static_contract_integrity", static.get("passed") is True, static),
        _check("scenario_id_audit", (report.get("scenario_id_audit") or {}).get("passed") is True, report.get("scenario_id_audit")),
        _check("contract_integrity_result", report.get("contract_integrity_result") == "PASS", report.get("contract_integrity_result")),
        _check("no_blockers_declared", report.get("blocker_count") == 0, report.get("blocker_count")),
    ]
    failed = [item["check_id"] for item in checks if not item["passed"]]
    operational = "PASS" if all(item["passed"] for item in _verify_operational(full)) else "FAIL"
    cognitive = "PASS" if all(item["passed"] for item in _verify_cognitive(full)) else "FAIL"
    governance = "PASS" if all(item["passed"] for item in _verify_governance(full)) else "FAIL"
    traceability = "PASS" if all(item["passed"] for item in _verify_traceability(full)) else "FAIL"
    contract = "PASS" if static.get("passed") and (report.get("scenario_id_audit") or {}).get("passed") else "FAIL"
    all_passed = not failed and all(value == "PASS" for value in (operational, cognitive, governance, traceability, contract))
    return {
        "phase": PHASE,
        "all_checks_passed": all_passed,
        "operational_result": operational,
        "cognitive_logic_result": cognitive,
        "governance_result": governance,
        "traceability_result": traceability,
        "contract_integrity_result": contract,
        "blocker_count": len(failed),
        "non_blocking_debt_count": report.get("non_blocking_debt_count", 0),
        "deferred_runtime_count": report.get("deferred_runtime_count", 0),
        "failed_checks": failed,
        "checks": checks,
        "final_decision": CLOSURE_DECISION if all_passed else "NOT_GO",
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not all_passed else "GO_CANDIDATE_PENDING_USER_REVIEW",
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m capabilities.evaluation.luna_controlled_cognitive_runtime_final_closure_audit.verifier_v1 <audit_report_v1.json>")
    try:
        report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        result = {
            "phase": PHASE,
            "all_checks_passed": False,
            "failed_checks": [f"audit_report_read_failed:{type(exc).__name__}"],
            "final_decision": "NOT_GO",
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
        return 1
    result = verify_report_v1(report if isinstance(report, dict) else {})
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
