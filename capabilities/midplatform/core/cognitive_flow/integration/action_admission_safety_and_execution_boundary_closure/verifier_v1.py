"""Fail-closed verifier for Action admission/safety boundary closure."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable


PHASE = "Phase-P1-Luna-Action-Admission-Safety-And-Execution-Boundary-Closure-v1-001"
EXPECTED_CASES = {
    "CASE_A_SUFFICIENT_STOP",
    "CASE_B_GAP_REOBSERVE_REVISE_STOP",
}
EXPECTED_NEGATIVES = {"action_without_permission", "action_fails_safety"}


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": observed}


def _all_false(values: Dict[str, Any]) -> bool:
    return all(value is False for value in values.values())


def _positive_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    action = case.get("action_boundary") or {}
    candidate = action.get("action_candidate") or {}
    trace = action.get("action_trace") or {}
    runtime_handoff = case.get("runtime_executor_handoff") or {}
    task_case = case.get("source_case") or {}
    task = task_case.get("task_manager") or {}
    task_attempts = task_case.get("cycle_action_handoff_attempts") or []
    eligibility = case.get("execution_eligibility") or {}
    forbidden = case.get("forbidden_behaviors") or {}
    request = action.get("request") or {}
    checks = [
        _check("task_manager_admitted", case.get("task_manager_admitted") is True),
        _check("task_state_eligible", case.get("task_status") in {"admitted", "planned", "ready"}),
        _check("task_trace_present", bool(case.get("task_trace_ref"))),
        _check("task_to_action_handoff_present", bool(case.get("action_handoff_ref")) and case.get("action_handoff_ref") == case.get("task_to_action_handoff_ref")),
        _check("action_boundary_invoked", action.get("action_boundary_invoked") is True),
        _check("action_boundary_admitted", action.get("action_boundary_admitted") is True and case.get("action_boundary_admission_status") == "CANDIDATE_ADMITTED" and bool(case.get("action_boundary_admission_ref"))),
        _check("action_candidate_present", bool(case.get("action_candidate_ref")) and candidate.get("action_candidate_id") == case.get("action_candidate_ref")),
        _check("action_owner", candidate.get("owner") == "Action Governance" and candidate.get("candidate_kind") == "ACTION_CANDIDATE"),
        _check("action_candidate_only", action.get("candidate_only") is True and candidate.get("runtime_authority") is False and candidate.get("task_authority") is False),
        _check("permission_validation_passed", (case.get("permission_validation") or {}).get("valid") is True and bool(request.get("permission_refs"))),
        _check("safety_validation_passed", (case.get("safety_validation") or {}).get("valid") is True and bool(request.get("safety_refs"))),
        _check("constraint_resource_validation_passed", (case.get("constraint_validation") or {}).get("status") == "VALIDATED" and (case.get("constraint_validation") or {}).get("resource_state") == "available"),
        _check("candidate_readiness", action.get("action_state") == "READY_CANDIDATE" and action.get("action_readiness") == "candidate_ready"),
        _check("execution_eligibility_formed", eligibility.get("status") == "ELIGIBLE_CANDIDATE" and bool(eligibility.get("ref")) and eligibility.get("candidate_only") is True and eligibility.get("executed") is False),
        _check("eligibility_ref_is_canonical_handoff", eligibility.get("ref") == case.get("runtime_executor_handoff_ref") and case.get("execution_eligibility_ref") == case.get("runtime_executor_handoff_ref") and eligibility.get("ref_source") == "canonical_action_runtime_handoff_id"),
        _check("runtime_handoff_owner_chain", runtime_handoff.get("producer_owner") == "Action Governance" and runtime_handoff.get("consumer_owner") == "Runtime Executor"),
        _check("runtime_handoff_candidate_only", runtime_handoff.get("candidate_only") is True and runtime_handoff.get("action_executed") is False and runtime_handoff.get("device_control_executed") is False),
        _check("runtime_handoff_eligibility", runtime_handoff.get("execution_readiness") == "candidate_ready"),
        _check("runtime_executor_not_invoked", case.get("runtime_executor_invoked") is False),
        _check("action_trace_link", bool(case.get("action_trace_ref")) and trace.get("trace_id") == case.get("action_trace_ref") and trace.get("action_candidate_ref") == case.get("action_candidate_ref")),
        _check("action_trace_decision_link", bool((case.get("traceability") or {}).get("decision_candidate_ref")) and (case.get("traceability") or {}).get("decision_candidate_ref") in (trace.get("decision_refs") or [])),
        _check("action_request_task_link", case.get("task_state_ref") in [item.get("ref_id") for item in request.get("task_reference_context_refs") or []] and case.get("task_trace_ref") in [item.get("ref_id") for item in request.get("task_reference_context_refs") or []]),
        _check("runtime_handoff_action_link", runtime_handoff.get("action_candidate_ref") == case.get("action_candidate_ref")),
        _check("task_provenance_link", bool(case.get("task_trace_ref")) and case.get("task_trace_ref") in (case.get("task_to_action_handoff") or {}).get("provenance_refs", ())),
        _check("cognition_provenance_link", bool((case.get("traceability") or {}).get("final_cognition_execution_ref")) and (case.get("traceability") or {}).get("final_cognition_execution_ref") in (case.get("task_to_action_handoff") or {}).get("provenance_refs", ())),
        _check("case_b_cycle_1_no_action", case.get("case_id") != "CASE_B_GAP_REOBSERVE_REVISE_STOP" or (task_attempts and task_attempts[0].get("action_boundary_invoked") is False)),
        _check("case_final_action_once", len(task_attempts) == (1 if case.get("case_id") == "CASE_A_SUFFICIENT_STOP" else 2) and sum(1 for item in task_attempts if item.get("action_boundary_invoked") is True) == 1),
        _check("forbidden_behaviors_closed", _all_false(forbidden), forbidden),
        _check("validation_errors_empty", not case.get("validation_errors"), case.get("validation_errors")),
    ]
    return checks


def _negative_checks(item: Dict[str, Any]) -> list[Dict[str, Any]]:
    forbidden = item.get("forbidden_behaviors") or {}
    return [
        _check("negative_rejected", item.get("rejected") is True),
        _check("negative_action_boundary_not_admitted", item.get("action_boundary_admitted") is False),
        _check("negative_permission_or_safety_failed", item.get("permission_validation", {}).get("valid") is False or item.get("safety_validation", {}).get("valid") is False),
        _check("negative_not_execution_eligible", (item.get("execution_eligibility") or {}).get("status") == "NOT_EXECUTION_ELIGIBLE"),
        _check("negative_runtime_executor_not_invoked", item.get("runtime_executor_invoked") is False),
        _check("negative_handoff_candidate_only", (item.get("runtime_executor_handoff") or {}).get("candidate_only") is True),
        _check("negative_forbidden_behaviors_closed", _all_false(forbidden), forbidden),
        _check("negative_validation_errors_empty", not item.get("validation_errors"), item.get("validation_errors")),
    ]


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    negatives = {item.get("fixture"): item for item in summary.get("negative_cases") or []}
    checks = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("exactly_two_positive_cases", len(summary.get("cases") or []) == 2 and set(cases) == EXPECTED_CASES),
        _check("negative_cases_present", len(summary.get("negative_cases") or []) == 2 and set(negatives) == EXPECTED_NEGATIVES),
    ]
    per_case: Dict[str, Any] = {}
    for case_id in sorted(EXPECTED_CASES):
        case_checks = _positive_checks(cases.get(case_id, {}))
        per_case[case_id] = case_checks
        checks.extend(case_checks)
    for negative_id in sorted(EXPECTED_NEGATIVES):
        negative_checks = _negative_checks(negatives.get(negative_id, {}))
        per_case[negative_id] = negative_checks
        checks.extend(negative_checks)

    operational_pass = all(item["passed"] for item in checks)
    return {
        "phase": PHASE,
        "operational_result": "PASS" if operational_pass else "FAIL",
        "cognitive_logic_result": "NOT_INDEPENDENTLY_EXERCISED",
        "final_decision": "NOT_GO",
        "phase_result": "ACTION_BOUNDARY_CONTROLLED_CLOSURE_PASS" if operational_pass else "FAIL",
        "checks": checks,
        "per_case": per_case,
        "all_checks_passed": operational_pass,
        "note": "Cognitive Logic Conformance is intentionally not independently exercised by this narrow Action safety phase.",
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m capabilities.midplatform.core.cognitive_flow.integration.action_admission_safety_and_execution_boundary_closure.verifier_v1 <runner_summary.json>")
    path = Path(sys.argv[1])
    summary = json.loads(path.read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
