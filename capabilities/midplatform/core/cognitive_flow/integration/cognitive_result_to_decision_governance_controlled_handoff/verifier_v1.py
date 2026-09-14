"""Fail-closed verifier for the controlled cognition-to-decision handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


PHASE = "Phase-P1-Luna-Cognitive-Result-To-Decision-Governance-Controlled-Handoff-Integration-v1-001"
COGNITION_OWNER = "Cognitive State Formation Governance"
DECISION_OWNER = "Decision Governance"
FLOW_OWNER = "Cognitive Flow Governance"
FPO_OWNER = "Field Perception Orchestrator"


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": passed, "observed": observed}


def _proofs(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("cognitive_case") or {}).get("cognitive_proofs") or [])


def _common_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    cognition = case.get("cognitive_case") or {}
    request = cognition.get("brain_request") or {}
    loop = cognition.get("loop_instance") or {}
    proofs = _proofs(case)
    handoff = case.get("decision_handoff") or {}
    decision = case.get("decision") or {}
    output = decision.get("output") or {}
    candidates = output.get("decision_candidates") or []
    checks = decision.get("checks") or {}
    final = proofs[-1] if proofs else {}
    trace = decision.get("decision_trace_causal_refs") or []
    evidence_trace = decision.get("decision_trace_evidence_refs") or []
    forbidden = case.get("forbidden_behaviors") or {}
    owner_boundaries = case.get("owner_boundaries") or {}
    traceability = case.get("traceability") or {}
    expected_forbidden = {
        "task_execution", "action_execution", "device_control", "model_invocation",
        "provider_invocation", "live_observation_execution", "field_mutation",
        "memory_mutation", "experience_mutation", "learning_mutation",
        "world_truth_declared",
    }
    return [
        _check("case_execution_mode", all(item.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME for item in proofs)),
        _check("cognition_executed", bool(proofs) and all(item.get("runtime_executed") is True for item in proofs)),
        _check("canonical_cognition_owner", bool(proofs) and all(item.get("owner_ref") == COGNITION_OWNER for item in proofs)),
        _check("flow_lifecycle_owner", loop.get("lifecycle_owner_ref") == FLOW_OWNER),
        _check("reobservation_owner_preserved", all(item.get("reobservation_owner_ref") == FPO_OWNER for item in proofs if item.get("reobservation_ref"))),
        _check("final_sufficiency", final.get("sufficiency_status") == "SUFFICIENT" and final.get("sufficiency_ref") == case.get("final_sufficiency_ref")),
        _check("final_stop", bool(final.get("stop_ref")) and final.get("stop_ref") == case.get("final_stop_ref")),
        _check("handoff_after_stop", bool(handoff) and handoff.get("stop_ref") == final.get("stop_ref")),
        _check("handoff_producer_cognition", handoff.get("producer_owner_ref") == COGNITION_OWNER),
        _check("handoff_consumer_decision", handoff.get("consumer_owner_ref") == DECISION_OWNER),
        _check("handoff_candidate_only", handoff.get("candidate_only") is True),
        _check("handoff_refs_match_final_cognition", handoff.get("a_route_execution_ref") == final.get("execution_ref") and handoff.get("sufficiency_ref") == final.get("sufficiency_ref") and handoff.get("stop_ref") == final.get("stop_ref")),
        _check("decision_governance_consumed", case.get("decision_governance_consumed") is True),
        _check("decision_candidate_present", bool(candidates)),
        _check("decision_candidate_owner", bool(candidates) and all(item.get("owner") == DECISION_OWNER for item in candidates)),
        _check("decision_candidate_candidate_only", bool(candidates) and all(item.get("action_authority") is False and item.get("task_authority") is False for item in candidates)),
        _check("decision_provenance_via_cognition", decision.get("decision_candidate_provenance_via_cognition") is True and all(ref in trace or ref in evidence_trace for ref in handoff.get("provenance_refs", []))),
        _check("decision_trace_ref_present", bool(decision.get("decision_trace_ref"))),
        _check("decision_input_validated", all(checks.get(key) is True for key in ("input_refs_read_only", "decision_candidates_valid", "trace_complete", "handoff_valid", "no_runtime_side_effects", "candidate_only", "decision_owner"))),
        _check("decision_no_runtime_side_effects", output.get("decision_output") is False and output.get("action_output") is False and output.get("task_output") is False and output.get("runtime_executed") is False),
        _check("owner_boundaries_preserved", owner_boundaries.get("cstate_owns_decision") is False and owner_boundaries.get("brain_owns_decision") is False and owner_boundaries.get("evaluation_owns_decision") is False and owner_boundaries.get("decision_governance_owns_decision_candidate") is True),
        _check("forbidden_behaviors_closed", set(forbidden) == expected_forbidden and all(value is False for value in forbidden.values()), forbidden),
        _check("integration_trace_complete", traceability.get("decision_handoff_ref") == case.get("decision_handoff_ref") and traceability.get("decision_trace_ref") == decision.get("decision_trace_ref") and traceability.get("decision_candidate_refs") == decision.get("decision_candidate_refs")),
        _check("validation_errors_empty", not case.get("validation_errors"), case.get("validation_errors")),
        _check("request_refs_present", all(request.get(key) for key in ("goal_ref", "intent_ref", "concern_ref", "context_ref"))),
    ]


def _case_a_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    attempts = case.get("handoff_attempts") or []
    return [
        _check("case_a_one_cycle", case.get("cognitive_cycle_count") == 1),
        _check("case_a_one_final_handoff", len(attempts) == 1 and attempts[0].get("status") == "ADMITTED"),
        _check("case_a_no_premature_handoff", all(item.get("cycle_index") != 0 for item in attempts)),
    ]


def _case_b_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    cognition = case.get("cognitive_case") or {}
    proofs = _proofs(case)
    attempts = case.get("handoff_attempts") or []
    first = proofs[0] if proofs else {}
    second = proofs[1] if len(proofs) > 1 else {}
    gateways = cognition.get("gateway_results") or []
    second_admission = (gateways[1].get("replay_admission") or {}) if len(gateways) > 1 else {}
    return [
        _check("case_b_two_cycles", case.get("cognitive_cycle_count") == 2 and len(proofs) == 2),
        _check("case_b_cycle_1_insufficient", first.get("sufficiency_status") == "INSUFFICIENT"),
        _check("case_b_cycle_1_no_handoff", len(attempts) >= 1 and attempts[0].get("status") == "ABSENT" and attempts[0].get("rejection_reason") == "decision_handoff_requires_sufficient_cognition"),
        _check("case_b_gap_present", bool(first.get("information_gap_ref"))),
        _check("case_b_reobservation_present", bool(first.get("reobservation_ref"))),
        _check("case_b_gap_reobservation_link", first.get("reobservation_information_gap_ref") == first.get("information_gap_ref")),
        _check("case_b_revision_linked", second.get("hypothesis_revision_information_gap_ref") == first.get("information_gap_ref") and second.get("hypothesis_revision_reobservation_ref") == first.get("reobservation_ref")),
        _check("case_b_final_handoff_only", len(attempts) == 2 and attempts[1].get("status") == "ADMITTED" and case.get("decision_handoff_ref") == attempts[1].get("handoff_ref")),
        _check("case_b_no_cycle_1_stop", not first.get("stop_ref")),
        _check("case_b_final_proof_is_cycle_2", case.get("final_cognition_execution_ref") == second.get("execution_ref")),
        _check("case_b_next_cycle_link", second_admission.get("prior_next_cycle_ingress_ref") == first.get("next_cycle_ingress_ref")),
    ]


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    checks = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("exactly_two_cases", set(cases) == {"CASE_A_SUFFICIENT_STOP", "CASE_B_GAP_REOBSERVE_REVISE_STOP"}),
        _check("premature_handoff_rejected", (summary.get("negative_test") or {}).get("rejected") is True and (summary.get("negative_test") or {}).get("decision_governance_called") is False),
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
        raise SystemExit("usage: python -m capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
