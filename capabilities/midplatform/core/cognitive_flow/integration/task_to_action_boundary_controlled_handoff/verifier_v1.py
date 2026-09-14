"""Fail-closed verifier for the controlled Task-to-Action handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-Task-To-Action-Boundary-Controlled-Handoff-Integration-v1-001"
EXPECTED_CASES = {"CASE_A_SUFFICIENT_STOP", "CASE_B_GAP_REOBSERVE_REVISE_STOP"}
EXPECTED_FORBIDDEN = {
    "action_before_valid_task", "task_manager_executes_action", "decision_executes_action",
    "brain_executes_action", "cstate_executes_action", "real_action_execution",
    "device_control", "runtime_dispatch", "model_invocation", "provider_invocation",
    "live_observation_execution", "field_mutation", "memory_mutation",
    "experience_mutation", "learning_mutation", "world_truth_declared",
}


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": passed, "observed": observed}


def _ref_ids(items: Any) -> set[str]:
    return {
        str(item.get("ref_id"))
        for item in items or []
        if isinstance(item, dict) and item.get("ref_id")
    }


def _common_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    task_case = case.get("task_case") or {}
    task = task_case.get("task_manager") or {}
    decision_candidate_ref = case.get("task_case", {}).get("decision_candidate_ref")
    decision_trace_ref = case.get("task_case", {}).get("decision_trace_ref")
    task_handoff = case.get("task_to_action_handoff") or {}
    action = case.get("action_boundary") or {}
    candidate = action.get("action_candidate") or {}
    trace = action.get("action_trace") or {}
    transitions = action.get("action_transitions") or []
    request = action.get("request") or {}
    forbidden = case.get("forbidden_behaviors") or {}
    task_request = task.get("request") or {}
    final_proof = (((task_case.get("decision_case") or {}).get("cognitive_case") or {}).get("cognitive_proofs") or [])
    final_proof = final_proof[-1] if final_proof else {}
    expected_execution_ref = final_proof.get("execution_ref")
    return [
        _check("task_manager_admitted", task.get("task_manager_admitted") is True),
        _check("task_state_valid", task.get("task_state") in {"admitted", "planned", "ready"}),
        _check("task_trace_present", bool(task.get("task_trace_ref"))),
        _check("task_to_action_handoff_present", bool(task_handoff.get("handoff_ref"))),
        _check("task_to_action_owner_chain", task_handoff.get("producer_owner") == "Task Manager" and task_handoff.get("consumer_owner") == "Action Governance"),
        _check("task_to_action_task_link", task_handoff.get("task_state_ref") == task.get("controlled_task_state_ref") and task_handoff.get("task_trace_ref") == task.get("task_trace_ref")),
        _check("task_to_action_decision_link", task_handoff.get("decision_candidate_ref") == decision_candidate_ref and task_handoff.get("decision_trace_ref") == decision_trace_ref),
        _check("task_to_action_cognition_link", expected_execution_ref in (task_handoff.get("provenance_refs") or [])),
        _check("action_boundary_invoked", action.get("action_boundary_invoked") is True),
        _check("action_boundary_admitted", action.get("action_boundary_admitted") is True and action.get("action_boundary_admission_status") == "CANDIDATE_ADMITTED"),
        _check("action_candidate_present", bool(action.get("action_candidate_ref")) and action.get("action_candidate_ref") == candidate.get("action_candidate_id")),
        _check("action_candidate_owner", candidate.get("owner") == "Action Governance" and candidate.get("candidate_kind") == "ACTION_CANDIDATE"),
        _check("action_candidate_candidate_only", candidate.get("runtime_authority") is False and candidate.get("task_authority") is False),
        _check("action_trace_present", bool(action.get("action_trace_ref")) and action.get("action_trace_ref") == trace.get("trace_id") and trace.get("action_candidate_ref") == action.get("action_candidate_ref")),
        _check("action_trace_decision_link", decision_candidate_ref in (trace.get("decision_refs") or [])),
        _check("action_admission_transition_link", bool(action.get("action_boundary_admission_ref")) and transitions and action.get("action_boundary_admission_ref") == transitions[0].get("provenance_ref")),
        _check("action_task_provenance", task.get("task_trace_ref") in (task_handoff.get("provenance_refs") or []) and task.get("task_trace_ref") in _ref_ids(request.get("task_reference_context_refs"))),
        _check("action_input_decision_link", decision_candidate_ref in _ref_ids(request.get("selected_decision_refs"))),
        _check("action_no_runtime_side_effects", action.get("candidate_only") is True and action.get("real_action_execution") is False and action.get("device_control") is False and action.get("runtime_dispatch") is False),
        _check("forbidden_behaviors_closed", set(forbidden) == EXPECTED_FORBIDDEN and all(value is False for value in forbidden.values()), forbidden),
        _check("validation_errors_empty", not case.get("validation_errors"), case.get("validation_errors")),
    ]


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    checks = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("exactly_two_cases", set(cases) == EXPECTED_CASES),
        _check("negative_action_handoff_rejected", (summary.get("negative_test") or {}).get("rejected") is True and (summary.get("negative_test") or {}).get("action_boundary_invoked") is False),
    ]
    for case_id in sorted(EXPECTED_CASES):
        case = cases.get(case_id, {})
        checks.extend(_common_checks(case))
        attempts = case.get("cycle_action_handoff_attempts") or []
        if case_id == "CASE_A_SUFFICIENT_STOP":
            checks.extend([
                _check("case_a_one_cycle", case.get("cognitive_cycle_count") == 1),
                _check("case_a_one_action_handoff", len(attempts) == 1 and attempts[0].get("action_boundary_invoked") is True),
            ])
        else:
            checks.extend([
                _check("case_b_two_cycles", case.get("cognitive_cycle_count") == 2),
                _check("case_b_cycle_1_no_action", len(attempts) == 2 and attempts[0].get("status") == "ABSENT" and attempts[0].get("decision_present") is False and attempts[0].get("task_present") is False and attempts[0].get("action_boundary_invoked") is False),
                _check("case_b_cycle_2_one_action", len(attempts) == 2 and attempts[1].get("action_boundary_invoked") is True),
            ])
    failed = [item["check_id"] for item in checks if not item["passed"]]
    return {
        "phase": summary.get("phase"),
        "checks": checks,
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
