from __future__ import annotations

import copy

from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.runner_v1 import (
    build_runner_summary_v1,
)
from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.verifier_v1 import (
    verify_summary_v1,
)
from capabilities.evaluation.observation_capability_resolution_controlled.engine_v1 import (
    ObservationCapabilityResolutionEvaluationEngineV1,
)
from capabilities.evaluation.observation_capability_resolution_controlled.verifier_v1 import (
    verify as verify_capability,
)
from capabilities.evaluation.observation_demand_controlled.engine_v1 import (
    ObservationDemandEvaluationEngineV1,
)
from capabilities.evaluation.observation_demand_controlled.verifier_v1 import (
    verify as verify_demand,
)


def _capability_summary() -> dict:
    return ObservationCapabilityResolutionEvaluationEngineV1().run()


def _demand_summary() -> dict:
    return ObservationDemandEvaluationEngineV1().run()


def _e2e_summary() -> dict:
    return build_runner_summary_v1()


def _case(summary: dict, case_id: str) -> dict:
    return next(case for case in summary["cases"] if case["case_id"] == case_id)


def _contrast(summary: dict, contrast_id: str) -> dict:
    return next(case for case in summary["contrast_results"] if case["contrast_id"] == contrast_id)


def test_observation_capability_canonical_positive() -> None:
    assert verify_capability(_capability_summary())["all_checks_passed"] is True


def test_observation_capability_forged_selected_capability_is_rejected() -> None:
    summary = _capability_summary()
    _case(summary, "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH")["result"]["resolved_candidates"][0]["capability_candidate_ref"] = "forged"
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_missing_case_is_rejected() -> None:
    summary = _capability_summary()
    summary["cases"].pop()
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_duplicate_case_is_rejected() -> None:
    summary = _capability_summary()
    summary["cases"].append(copy.deepcopy(summary["cases"][0]))
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_extra_case_is_rejected() -> None:
    summary = _capability_summary()
    extra = copy.deepcopy(summary["cases"][0])
    extra["case_id"] = "FORGED_EXTRA_CASE"
    summary["cases"].append(extra)
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_duplicate_candidate_identity_is_rejected() -> None:
    summary = _capability_summary()
    case = _case(summary, "SINGLE_DEMAND_MULTIPLE_CAPABILITY_MATCHES")
    candidates = case["result"]["resolved_candidates"]
    candidates[1]["capability_candidate_ref"] = candidates[0]["capability_candidate_ref"]
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_unavailable_marked_available_is_rejected() -> None:
    summary = _capability_summary()
    case = _case(summary, "MATCHING_CAPABILITY_UNAVAILABLE")
    case["request"]["capability_inventory"][0]["availability_status"] = "AVAILABLE"
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_missing_governance_evidence_is_rejected() -> None:
    summary = _capability_summary()
    candidate = _case(summary, "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH")["result"]["resolved_candidates"][0]
    candidate["admission_status"] = "UNKNOWN"
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_capability_forged_aggregate_does_not_override_failure() -> None:
    summary = _capability_summary()
    _case(summary, "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH")["result"]["resolution_status"] = "CAPABILITY_CANDIDATES_RESOLVED"
    _case(summary, "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH")["result"]["resolved_candidates"][0]["capability_class_ref"] = "wrong"
    summary.update({"all_checks_passed": True, "passed_count": 9999, "final_decision": "GO"})
    assert verify_capability(summary)["all_checks_passed"] is False


def test_observation_demand_canonical_positive() -> None:
    assert verify_demand(_demand_summary())["all_checks_passed"] is True


def test_observation_demand_forged_replay_ref_is_rejected() -> None:
    summary = _demand_summary()
    _case(summary, "SINGLE_ADMITTED_PERCEPTION_STRATEGY")["deterministic_replay_demand_refs"] = ["forged"]
    assert verify_demand(summary)["all_checks_passed"] is False


def test_observation_demand_missing_demand_is_rejected() -> None:
    summary = _demand_summary()
    _case(summary, "SINGLE_ADMITTED_PERCEPTION_STRATEGY")["result"]["demands"] = []
    _case(summary, "SINGLE_ADMITTED_PERCEPTION_STRATEGY")["result"]["demand_refs"] = []
    assert verify_demand(summary)["all_checks_passed"] is False


def test_observation_demand_duplicate_demand_is_rejected() -> None:
    summary = _demand_summary()
    case = _case(summary, "SINGLE_ADMITTED_PERCEPTION_STRATEGY")
    case["result"]["demands"] = list(case["result"]["demands"]) + [copy.deepcopy(case["result"]["demands"][0])]
    case["result"]["demand_refs"] = list(case["result"]["demand_refs"]) + [case["result"]["demand_refs"][0]]
    assert verify_demand(summary)["all_checks_passed"] is False


def test_observation_demand_extra_case_is_rejected() -> None:
    summary = _demand_summary()
    extra = copy.deepcopy(summary["cases"][0])
    extra["case_id"] = "FORGED_EXTRA_CASE"
    summary["cases"].append(extra)
    assert verify_demand(summary)["all_checks_passed"] is False


def test_observation_demand_wrong_target_is_rejected() -> None:
    summary = _demand_summary()
    demand = _case(summary, "SINGLE_ADMITTED_PERCEPTION_STRATEGY")["result"]["demands"][0]
    demand["observation_target_refs"] = ["forged-target"]
    assert verify_demand(summary)["all_checks_passed"] is False


def test_full_e2e_canonical_positive() -> None:
    assert verify_summary_v1(_e2e_summary())["all_checks_passed"] is True


def test_full_e2e_missing_transition_is_rejected() -> None:
    summary = _e2e_summary()
    transitions = _contrast(summary, "role-owner")["execution_proof"]["cognitive_transition_refs"]
    transitions.pop(2)
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_full_e2e_reordered_transition_is_rejected() -> None:
    summary = _e2e_summary()
    transitions = _contrast(summary, "role-owner")["execution_proof"]["cognitive_transition_refs"]
    transitions[1], transitions[2] = transitions[2], transitions[1]
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_full_e2e_wrong_transition_owner_is_rejected() -> None:
    summary = _e2e_summary()
    _contrast(summary, "role-owner")["execution_proof"]["owner_ref"] = "forged-owner"
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_full_e2e_forged_terminal_status_is_rejected() -> None:
    summary = _e2e_summary()
    _contrast(summary, "role-owner")["semantic_snapshot"]["sufficiency_status"] = "INSUFFICIENT"
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_full_e2e_copied_contrast_snapshot_is_rejected() -> None:
    summary = _e2e_summary()
    source = _contrast(summary, "role-owner")["semantic_snapshot"]
    _contrast(summary, "role-visitor")["semantic_snapshot"] = copy.deepcopy(source)
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_full_e2e_forged_final_decision_does_not_override_failure() -> None:
    summary = _e2e_summary()
    _contrast(summary, "role-owner")["execution_proof"]["cognitive_transition_refs"].pop()
    summary["final_decision"] = "GO"
    summary["all_checks_passed"] = True
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_same_tampered_expected_and_result_are_rejected() -> None:
    summary = _capability_summary()
    case = _case(summary, "SINGLE_DEMAND_SINGLE_CAPABILITY_MATCH")
    case["expected_status"] = "WRONG"
    case["result"]["resolution_status"] = "WRONG"
    assert verify_capability(summary)["all_checks_passed"] is False


def test_full_e2e_forbidden_transition_is_rejected() -> None:
    summary = _e2e_summary()
    _contrast(summary, "role-owner")["execution_proof"]["cognitive_transition_refs"].append("forbidden-transition")
    assert verify_summary_v1(summary)["all_checks_passed"] is False


def test_full_e2e_runner_aggregate_fields_are_non_authoritative() -> None:
    summary = _e2e_summary()
    _contrast(summary, "role-owner")["execution_proof"]["cognitive_transition_refs"].append("forged-transition")
    summary.update({"final_decision": "GO", "operational_result": "PASS", "cognitive_logic_result": "PASS", "capability_gaps": ["forged-gap"]})
    assert verify_summary_v1(summary)["all_checks_passed"] is False
