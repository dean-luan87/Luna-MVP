"""Fail-closed Verifier for the controlled Brain closure integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


COGNITION_OWNER = "Cognitive State Formation Governance"
BRAIN_RESPONSIBILITY_DOMAIN = "BRAIN"
BRAIN_CANONICAL_OWNER_STATUS = "OWNER_UNRESOLVED"
LOOP_OWNER = "Cognitive Flow Governance"
REOBSERVATION_OWNER = "Field Perception Orchestrator"


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": passed, "observed": observed}


def _proofs(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list(case.get("proofs") or [])


def _common_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    proofs = _proofs(case)
    guards = case.get("negative_guards") or {}
    checks = [
        _check("execution_mode_controlled_replay", case.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME),
        _check("brain_loop_lifecycle_owner", case.get("lifecycle_owner_ref") == LOOP_OWNER),
        _check("brain_responsibility_is_explicit", case.get("brain_responsibility_domain") == BRAIN_RESPONSIBILITY_DOMAIN),
        _check("brain_owner_is_unresolved", case.get("brain_canonical_owner_status") == BRAIN_CANONICAL_OWNER_STATUS),
        _check("information_need_owner_is_unresolved", case.get("information_need_canonical_owner_status") == BRAIN_CANONICAL_OWNER_STATUS),
        _check("cognition_proofs_present", bool(proofs)),
        _check("all_proofs_runtime_executed", bool(proofs) and all(item.get("runtime_executed") is True for item in proofs)),
        _check("all_proofs_canonical_owner", bool(proofs) and all(item.get("owner_ref") == COGNITION_OWNER for item in proofs)),
        _check("all_proofs_candidate_only", bool(proofs) and all(item.get("field_mutation") is False and item.get("world_truth_declared") is False for item in proofs)),
        _check("no_forbidden_runtime_capability", all(
            item.get(key) is False
            for item in proofs
            for key in ("model_invocation", "provider_invocation", "live_observation_execution", "action_execution")
        )),
        _check("negative_guards_closed", all(value is False for value in guards.values()), guards),
        _check("no_validation_errors", not case.get("validation_errors")),
        _check("closure_candidate_present", bool(case.get("closure_candidate_ref"))),
        _check("closure_acceptance_present", bool(case.get("closure_acceptance_ref"))),
        _check("closure_acceptance_owner_is_unresolved", case.get("closure_acceptance_owner_ref") == BRAIN_CANONICAL_OWNER_STATUS),
        _check("lifecycle_closure_present", bool(case.get("lifecycle_closure_ref"))),
        _check("assimilation_candidate_present", bool(case.get("assimilation_candidate_ref")) and case.get("assimilation_candidate_only") is True),
    ]
    return checks


def _case_a_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    proofs = _proofs(case)
    proof = proofs[0] if proofs else {}
    return [
        _check("case_a_one_cycle", case.get("cognitive_cycle_count") == 1),
        _check("case_a_sufficient", proof.get("sufficiency_status") == "SUFFICIENT"),
        _check("case_a_sufficiency_owner", proof.get("sufficiency_owner_ref") == COGNITION_OWNER),
        _check("case_a_stop_present", bool(proof.get("stop_ref"))),
        _check("case_a_stop_owner", proof.get("stop_owner_ref") == COGNITION_OWNER),
        _check("case_a_no_gap", not proof.get("information_gap_ref")),
        _check("case_a_no_reobservation", not proof.get("reobservation_ref") and not proof.get("next_cycle_ingress_ref")),
    ]


def _case_b_checks(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    proofs = _proofs(case)
    first = proofs[0] if len(proofs) > 0 else {}
    second = proofs[1] if len(proofs) > 1 else {}
    raw = case.get("raw_case") or {}
    gateways = raw.get("gateway_results") or []
    second_admission = (gateways[1].get("replay_admission") or {}) if len(gateways) > 1 else {}
    return [
        _check("case_b_two_cycles", case.get("cognitive_cycle_count") == 2 and len(proofs) == 2),
        _check("case_b_cycle_1_insufficient", first.get("sufficiency_status") == "INSUFFICIENT"),
        _check("case_b_cycle_1_gap", bool(first.get("information_gap_ref"))),
        _check("case_b_cycle_1_reobservation", bool(first.get("reobservation_ref"))),
        _check("case_b_reobservation_owner", first.get("reobservation_owner_ref") == REOBSERVATION_OWNER),
        _check("case_b_reobservation_gap_link", first.get("reobservation_information_gap_ref") == first.get("information_gap_ref")),
        _check("case_b_next_cycle_ingress", bool(first.get("next_cycle_ingress_ref"))),
        _check("case_b_admission_gap_link", second_admission.get("prior_information_gap_ref") == first.get("information_gap_ref")),
        _check("case_b_admission_reobservation_link", second_admission.get("prior_reobservation_ref") == first.get("reobservation_ref")),
        _check("case_b_admission_next_cycle_link", second_admission.get("prior_next_cycle_ingress_ref") == first.get("next_cycle_ingress_ref")),
        _check("case_b_revision_present", bool(second.get("hypothesis_revision_ref"))),
        _check("case_b_revision_owner", second.get("hypothesis_revision_owner_ref") == COGNITION_OWNER),
        _check("case_b_revision_gap_link", second.get("hypothesis_revision_information_gap_ref") == first.get("information_gap_ref")),
        _check("case_b_revision_reobservation_link", second.get("hypothesis_revision_reobservation_ref") == first.get("reobservation_ref")),
        _check("case_b_final_sufficient", second.get("sufficiency_status") == "SUFFICIENT"),
        _check("case_b_final_stop", bool(second.get("stop_ref")) and second.get("stop_owner_ref") == COGNITION_OWNER),
        _check("case_b_no_cycle_1_stop", not first.get("stop_ref")),
    ]


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    cases = {item.get("case_id"): item for item in summary.get("cases") or []}
    guard_coverage = summary.get("negative_guard_coverage") or {}
    expected_guards = {
        "evaluation_owns_cognition",
        "cstate_mutates_brain",
        "closure_without_sufficiency",
        "closure_before_stop",
        "assimilation_mutates_memory",
        "assimilation_mutates_experience",
        "assimilation_declares_world_truth",
        "decision_execution",
        "task_execution",
        "action_execution",
        "live_observation",
        "model_invocation",
        "provider_invocation",
    }
    checks: list[Dict[str, Any]] = [
        _check("phase_present", bool(summary.get("phase"))),
        _check("brain_responsibility_is_explicit", summary.get("responsibility_domain") == BRAIN_RESPONSIBILITY_DOMAIN),
        _check("brain_owner_is_unresolved", summary.get("canonical_owner_status") == BRAIN_CANONICAL_OWNER_STATUS),
        _check("exactly_two_cases", set(cases) == {"CASE_A_SUFFICIENT_STOP", "CASE_B_GAP_REOBSERVE_REVISE_STOP"}),
        _check("negative_closure_fixture_rejected", (summary.get("negative_test") or {}).get("rejected") is True),
        _check("negative_guard_inventory_complete", set(guard_coverage) == expected_guards),
        _check("closure_without_sufficiency_runtime_covered", guard_coverage.get("closure_without_sufficiency", {}).get("guard_runtime_covered") is True),
        _check("unexercised_guards_not_claimed_dynamic", all(
            item.get("guard_runtime_covered") is False and item.get("coverage_kind") == "STRUCTURAL_ONLY"
            for name, item in guard_coverage.items()
            if name != "closure_without_sufficiency"
        )),
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
        raise SystemExit("usage: python -m capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
