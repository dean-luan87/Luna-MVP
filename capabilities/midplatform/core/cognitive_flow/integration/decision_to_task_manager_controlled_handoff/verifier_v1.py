"""Fail-closed verifier for the controlled Decision-to-Task handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


PHASE = "Phase-P1-Luna-Decision-To-Task-Manager-Controlled-Handoff-Integration-v1-001"
DECISION_OWNER = "Decision Governance"
TASK_MANAGER_OWNER = "Task Manager"
EXPECTED_FORBIDDEN = {
    "task_before_valid_decision", "decision_executes_task", "brain_owns_task",
    "cstate_owns_task", "task_manager_owns_decision", "action_execution",
    "device_control", "model_invocation", "provider_invocation",
    "live_observation_execution", "field_mutation", "memory_mutation",
    "experience_mutation", "learning_mutation", "world_truth_declared",
}


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": passed, "observed": observed}


def _common_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    decision_case = case.get("decision_case") or {}
    cognitive_case = decision_case.get("cognitive_case") or {}
    proofs = cognitive_case.get("cognitive_proofs") or []
    decision = decision_case.get("decision") or {}
    decision_output = decision.get("output") or {}
    selection = decision_output.get("selection_candidate") or {}
    candidates = decision_output.get("decision_candidates") or []
    selected = next((item for item in candidates if item.get("decision_candidate_id") == selection.get("selected_candidate_ref")), {})
    handoff = case.get("task_handoff") or {}
    task = case.get("task_manager") or {}
    task_output = task.get("task_manager_output") or {}
    forbidden = case.get("forbidden_behaviors") or {}
    owners = case.get("owner_boundaries") or {}
    provenance = handoff.get("provenance_refs") or []
    task_request = task.get("request") or {}
    steps = (task_output.get("diagnostics") or {}).get("step_results") or []
    admission = next((item for item in steps if item.get("step") == "admission"), {})
    return [
        _check("controlled_replay_cognition", bool(proofs) and all(item.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME for item in proofs)),
        _check("decision_owner", selected.get("owner") == DECISION_OWNER),
        _check("decision_selected_eligible", selection.get("execution_eligibility_candidate") is True and selected.get("eligibility_candidate") is True),
        _check("decision_candidate_only", decision_output.get("candidate_only") is True and decision_output.get("decision_output") is False),
        _check("task_handoff_present", bool(handoff.get("handoff_ref"))),
        _check("task_handoff_producer", handoff.get("producer_owner_ref") == DECISION_OWNER),
        _check("task_handoff_consumer", handoff.get("consumer_owner_ref") == TASK_MANAGER_OWNER),
        _check("task_handoff_candidate_only", handoff.get("candidate_only") is True and handoff.get("task_execution") is False and handoff.get("action_execution") is False),
        _check("task_handoff_decision_link", handoff.get("decision_candidate_ref") == selection.get("selected_candidate_ref") and handoff.get("selected_candidate_ref") == selection.get("selected_candidate_ref")),
        _check("task_handoff_trace_link", handoff.get("decision_trace_ref") == decision.get("decision_trace_ref") and handoff.get("source_decision_handoff_ref") == (decision_output.get("handoff_candidate") or {}).get("handoff_id")),
        _check("task_handoff_cognition_provenance", bool(provenance) and case.get("decision_candidate_ref") in provenance and case.get("final_cognition_execution_ref", ((proofs[-1] if proofs else {}).get("execution_ref"))) in provenance),
        _check("task_manager_invoked", task.get("task_manager_invoked") is True),
        _check("task_manager_owner", task.get("task_manager_owner_ref") == TASK_MANAGER_OWNER),
        _check("task_manager_admitted", task.get("task_manager_admitted") is True and admission.get("ok") is True),
        _check("controlled_task_state_present", bool(task.get("controlled_task_state_ref")) and task.get("controlled_task_state_ref") == task.get("task_state_ref") and task.get("task_state") in {"admitted", "planned", "ready"}),
        _check("task_manager_trace_present", bool(task.get("task_trace_ref")) and task.get("task_trace_ref") == task_output.get("trace_ref")),
        _check("task_input_decision_link", selection.get("selected_candidate_ref") in task_request.get("decision_refs", [])),
        _check("task_provenance_resolves_decision", task_request.get("requester_ref") == handoff.get("handoff_ref") and task_request.get("permission_snapshot", {}).get("governance_ref") == handoff.get("source_decision_handoff_ref")),
        _check("task_no_runtime_side_effects", task.get("task_execution") is False and task_output.get("action_execution_executed") is False and task_output.get("model_call_executed") is False and task_output.get("state_mutation_executed") is False and task_output.get("fact_promotion_executed") is False and task_output.get("runtime_dispatch_executed") is False),
        _check("owner_boundaries", owners.get("decision_owns_decision_candidate") is True and owners.get("task_manager_owns_task_state") is True and owners.get("task_manager_owns_decision") is False and owners.get("brain_owns_task") is False and owners.get("cstate_owns_task") is False and owners.get("decision_executes_task") is False),
        _check("forbidden_behaviors_closed", set(forbidden) == EXPECTED_FORBIDDEN and all(value is False for value in forbidden.values()), forbidden),
        _check("validation_errors_empty", not case.get("validation_errors"), case.get("validation_errors")),
    ]


def _case_a_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    attempts = case.get("cycle_task_handoff_attempts") or []
    return [
        _check("case_a_one_cycle", case.get("cognitive_cycle_count") == 1),
        _check("case_a_one_task_handoff", len(attempts) == 1 and attempts[0].get("status") == "ADMITTED"),
        _check("case_a_one_task_manager_invocation", case.get("task_manager_invocation_count") == 1),
    ]


def _case_b_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    attempts = case.get("cycle_task_handoff_attempts") or []
    return [
        _check("case_b_two_cycles", case.get("cognitive_cycle_count") == 2),
        _check("case_b_cycle_1_no_task", len(attempts) == 2 and attempts[0].get("status") == "ABSENT" and attempts[0].get("task_manager_invoked") is False),
        _check("case_b_cycle_2_one_task", len(attempts) == 2 and attempts[1].get("status") == "ADMITTED" and attempts[1].get("task_manager_invoked") is True),
        _check("case_b_one_task_manager_invocation", case.get("task_manager_invocation_count") == 1),
    ]


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    checks = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("exactly_two_cases", set(cases) == {"CASE_A_SUFFICIENT_STOP", "CASE_B_GAP_REOBSERVE_REVISE_STOP"}),
        _check("negative_task_handoff_rejected", (summary.get("negative_test") or {}).get("rejected") is True and (summary.get("negative_test") or {}).get("task_manager_invoked") is False),
    ]
    for case_id in ("CASE_A_SUFFICIENT_STOP", "CASE_B_GAP_REOBSERVE_REVISE_STOP"):
        case = cases.get(case_id, {})
        checks.extend(_common_checks(case))
        checks.extend(_case_a_checks(case) if case_id == "CASE_A_SUFFICIENT_STOP" else _case_b_checks(case))
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
        raise SystemExit("usage: python -m capabilities.midplatform.core.cognitive_flow.integration.decision_to_task_manager_controlled_handoff.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
