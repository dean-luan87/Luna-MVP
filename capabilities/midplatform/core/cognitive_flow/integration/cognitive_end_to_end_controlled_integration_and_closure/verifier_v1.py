"""Fail-closed verifier for the end-to-end controlled cognition baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


PHASE = "Phase-P1-Luna-Cognitive-End-To-End-Controlled-Integration-And-Closure-v1-001"
COGNITION_OWNER = "Cognitive State Formation Governance"
FLOW_OWNER = "Cognitive Flow Governance"
FPO_OWNER = "Field Perception Orchestrator"
BRAIN_DOMAIN = "BRAIN"
UNRESOLVED = "OWNER_UNRESOLVED"
CASE_A = "CASE_A_SUFFICIENT_STOP"
CASE_B = "CASE_B_GAP_REOBSERVE_REVISE_STOP"


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": passed, "observed": observed}


def _raw(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("raw_case") or {}


def _proofs(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list(_raw(case).get("cognitive_proofs") or [])


def _all_false(values: Iterable[Any]) -> bool:
    return all(value is False for value in values)


def _common_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    raw = _raw(case)
    request = raw.get("brain_request") or {}
    proofs = _proofs(case)
    trace = case.get("traceability") or {}
    guards = case.get("negative_guards") or {}
    forbidden = case.get("forbidden_behaviors") or {}
    gateways = raw.get("gateway_results") or []
    expected_gateway_refs = [
        (item.get("replay_admission") or {}).get("gateway_admission_ref")
        for item in gateways
    ]
    expected_evidence_refs = [
        item.get("evidence_id")
        for gateway in gateways
        for item in gateway.get("evidence", [])
    ]
    expected_hypothesis_refs = [
        ref for proof in proofs for ref in proof.get("hypothesis_refs", [])
    ]
    expected_world_refs = [
        proof.get("current_world_ref") for proof in proofs if proof.get("current_world_ref")
    ]
    required_refs = (
        "goal_ref", "intent_ref", "concern_ref", "context_ref",
        "information_need_ref", "cognitive_loop_ref", "gateway_admission_refs",
        "a_route_execution_refs", "evidence_refs", "hypothesis_refs",
        "current_world_refs", "sufficiency_refs", "closure_candidate_ref",
        "assimilation_candidate_ref",
    )
    checks = [
        _check("case_execution_mode", case.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME),
        _check("case_cognition_execution", case.get("cognition_execution") is True),
        _check("case_runtime_executed", case.get("runtime_executed") is True),
        _check("brain_domain_preserved", case.get("brain_responsibility_domain") == BRAIN_DOMAIN),
        _check("brain_owner_unresolved", case.get("brain_canonical_owner_status") == UNRESOLVED),
        _check("information_need_owner_unresolved", case.get("information_need_canonical_owner_status") == UNRESOLVED),
        _check("flow_lifecycle_owner", case.get("lifecycle_owner_ref") == FLOW_OWNER),
        _check("proofs_present", bool(proofs)),
        _check("proofs_are_canonical", bool(proofs) and all(item.get("owner_ref") == COGNITION_OWNER for item in proofs)),
        _check("proofs_runtime_executed", bool(proofs) and all(item.get("runtime_executed") is True for item in proofs)),
        _check("proofs_candidate_only", bool(proofs) and all(item.get("candidate_only") is True for item in proofs)),
        _check("proofs_have_transitions", bool(proofs) and all(item.get("cognitive_transition_refs") for item in proofs)),
        _check("sufficient_proof_owner", all(
            item.get("sufficiency_owner_ref") == COGNITION_OWNER for item in proofs if item.get("sufficiency_ref")
        )),
        _check("reobservation_owner_preserved", all(
            item.get("reobservation_owner_ref") == FPO_OWNER for item in proofs if item.get("reobservation_ref")
        )),
        _check("stop_owner_preserved", all(
            item.get("stop_owner_ref") == COGNITION_OWNER for item in proofs if item.get("stop_ref")
        )),
        _check("closure_acceptance_unresolved", case.get("closure_acceptance_owner_ref") == UNRESOLVED),
        _check("closure_present", bool(case.get("closure_candidate_ref"))),
        _check("assimilation_present_candidate_only", bool(case.get("assimilation_candidate_ref")) and case.get("assimilation_candidate_only") is True),
        _check("request_capability_guards", _all_false(
            request.get(key) for key in (
                "model_invocation", "provider_invocation", "live_observation_execution",
                "action_execution", "task_execution",
            )
        )),
        _check("proof_capability_guards", _all_false(
            item.get(key) for item in proofs for key in (
                "model_invocation", "provider_invocation", "live_observation_execution",
                "action_execution", "field_mutation", "world_truth_declared",
            )
        )),
        _check("assimilation_mutation_guards", _all_false(
            (raw.get("assimilation_candidate") or {}).get(key) for key in (
                "world_truth_declared", "decision_created", "action_executed",
                "intent_mutation", "memory_mutation", "experience_mutation",
                "learning_executed", "automatic_loop_generation", "automatic_task_generation",
            )
        )),
        _check("negative_guards_closed", all(value is False for value in guards.values()), guards),
        _check("forbidden_behaviors_closed", set(forbidden) == {
            "model_invocation", "provider_invocation", "live_observation_execution",
            "field_mutation", "world_truth_declared", "memory_mutation",
            "experience_mutation", "learning_mutation", "decision_execution",
            "task_execution", "action_execution",
        } and all(value is True for value in forbidden.values()), forbidden),
        _check("validation_errors_empty", not case.get("validation_errors"), case.get("validation_errors")),
        _check("traceability_fields_present", all(trace.get(key) for key in required_refs), trace),
        _check("traceability_matches_request", all(
            trace.get(key) == request.get(key)
            for key in ("goal_ref", "intent_ref", "concern_ref", "context_ref")
        ) and trace.get("information_need_ref") == (raw.get("information_need") or {}).get("information_need_ref")
        and trace.get("cognitive_loop_ref") == (raw.get("loop_instance") or {}).get("cognitive_loop_ref")),
        _check("traceability_matches_gateway", trace.get("gateway_admission_refs") == expected_gateway_refs),
        _check("traceability_matches_evidence", trace.get("evidence_refs") == list(dict.fromkeys(expected_evidence_refs))),
        _check("traceability_matches_hypotheses", trace.get("hypothesis_refs") == list(dict.fromkeys(expected_hypothesis_refs))),
        _check("traceability_matches_current_world", trace.get("current_world_refs") == list(dict.fromkeys(expected_world_refs))),
        _check("traceability_matches_proofs", trace.get("a_route_execution_refs") == [item.get("execution_ref") for item in case.get("proofs", [])]),
    ]
    return checks


def _case_a_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    proofs = _proofs(case)
    proof = proofs[0] if proofs else {}
    trace = case.get("traceability") or {}
    return [
        _check("case_a_one_cycle", case.get("cognitive_cycle_count") == 1),
        _check("case_a_one_proof", len(proofs) == 1),
        _check("case_a_sufficient", proof.get("sufficiency_status") == "SUFFICIENT"),
        _check("case_a_stop_after_sufficiency", bool(proof.get("stop_ref")) and bool(proof.get("sufficiency_ref"))),
        _check("case_a_no_gap", not proof.get("information_gap_ref") and not trace.get("information_gap_ref")),
        _check("case_a_no_reobservation", not proof.get("reobservation_ref") and not proof.get("next_cycle_ingress_ref")),
        _check("case_a_closure_after_stop", bool(case.get("closure_candidate_ref")) and bool(proof.get("stop_ref"))),
        _check("case_a_assimilation_after_closure", bool(case.get("assimilation_candidate_ref")) and bool(case.get("closure_candidate_ref"))),
    ]


def _case_b_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    proofs = _proofs(case)
    first = proofs[0] if len(proofs) > 0 else {}
    second = proofs[1] if len(proofs) > 1 else {}
    raw = _raw(case)
    gateways = raw.get("gateway_results") or []
    second_admission = (gateways[1].get("replay_admission") or {}) if len(gateways) > 1 else {}
    trace = case.get("traceability") or {}
    first_evidence = tuple(item.get("evidence_id") for item in (gateways[0].get("evidence") or [])) if gateways else ()
    second_evidence = tuple(item.get("evidence_id") for item in (gateways[1].get("evidence") or [])) if len(gateways) > 1 else ()
    return [
        _check("case_b_two_cycles", case.get("cognitive_cycle_count") == 2 and len(proofs) == 2),
        _check("case_b_cycle_1_insufficient", first.get("sufficiency_status") == "INSUFFICIENT"),
        _check("case_b_cycle_1_gap", bool(first.get("information_gap_ref"))),
        _check("case_b_cycle_1_reobservation", bool(first.get("reobservation_ref"))),
        _check("case_b_gap_reobservation_link", first.get("reobservation_information_gap_ref") == first.get("information_gap_ref")),
        _check("case_b_next_cycle_ingress", bool(first.get("next_cycle_ingress_ref"))),
        _check("case_b_admission_gap_link", second_admission.get("prior_information_gap_ref") == first.get("information_gap_ref")),
        _check("case_b_admission_reobservation_link", second_admission.get("prior_reobservation_ref") == first.get("reobservation_ref")),
        _check("case_b_admission_next_cycle_link", second_admission.get("prior_next_cycle_ingress_ref") == first.get("next_cycle_ingress_ref")),
        _check("case_b_cycle_2_prior_ingress_link", second.get("prior_next_cycle_ingress_ref") == first.get("next_cycle_ingress_ref")),
        _check("case_b_new_evidence", bool(first_evidence) and bool(second_evidence) and set(first_evidence).isdisjoint(second_evidence)),
        _check("case_b_revision_present", bool(second.get("hypothesis_revision_ref"))),
        _check("case_b_revision_owner", second.get("hypothesis_revision_owner_ref") == COGNITION_OWNER),
        _check("case_b_revision_gap_link", second.get("hypothesis_revision_information_gap_ref") == first.get("information_gap_ref") == trace.get("information_gap_ref")),
        _check("case_b_revision_reobservation_link", second.get("hypothesis_revision_reobservation_ref") == first.get("reobservation_ref") == trace.get("reobservation_ref")),
        _check("case_b_final_sufficient", second.get("sufficiency_status") == "SUFFICIENT"),
        _check("case_b_final_stop", bool(second.get("stop_ref")) and second.get("stop_owner_ref") == COGNITION_OWNER),
        _check("case_b_no_cycle_1_stop", not first.get("stop_ref")),
        _check("case_b_closure_after_final_stop", bool(case.get("closure_candidate_ref")) and bool(second.get("stop_ref"))),
        _check("case_b_assimilation_after_closure", bool(case.get("assimilation_candidate_ref")) and bool(case.get("closure_candidate_ref"))),
    ]


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    checks: list[Dict[str, Any]] = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("source_integration_present", bool(summary.get("source_integration_phase"))),
        _check("brain_domain_preserved", summary.get("responsibility_domain") == BRAIN_DOMAIN),
        _check("brain_owner_unresolved", summary.get("canonical_owner_status") == UNRESOLVED),
        _check("exactly_two_cases", summary.get("case_count") == 2 and set(cases) == {CASE_A, CASE_B}),
        _check("negative_closure_fixture_rejected", (summary.get("negative_test") or {}).get("rejected") is True),
    ]
    for case_id in (CASE_A, CASE_B):
        case = cases.get(case_id, {})
        checks.extend(_common_checks(case))
        checks.extend(_case_a_checks(case) if case_id == CASE_A else _case_b_checks(case))
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
        raise SystemExit("usage: python -m capabilities.midplatform.core.cognitive_flow.integration.cognitive_end_to_end_controlled_integration_and_closure.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
