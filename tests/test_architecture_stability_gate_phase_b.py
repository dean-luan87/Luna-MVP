"""Phase B controlled temporal authority sandbox acceptance tests."""

from capabilities.evaluation.architecture_stability_gate_phase_b.engine_v1 import (
    run_phase_b_scenarios,
)
from capabilities.evaluation.architecture_stability_gate_phase_b.verifier_v1 import (
    verify_phase_b_results,
)


def test_phase_b_minimum_temporal_authority_scenarios() -> None:
    results = run_phase_b_scenarios()
    report = verify_phase_b_results(results)

    assert all(report["structural_checks"].values()), report
    assert report["stale_authority_consumption"] == "NOT_CONFIRMED"
    assert report["dynamic_finding_is_not_a_phase_decision"] is True


def test_phase_b_preserves_real_owner_transition_and_auth_reuse() -> None:
    results = run_phase_b_scenarios()
    for scenario_id in (
        "B02_ACTION_REVOKED_AFTER_AUTHORIZATION",
        "B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION",
        "B04_COGNITIVE_GRANT_REVOKED_AFTER_AUTHORIZATION",
        "B05_CONCERN_SUPERSEDED_AFTER_AUTHORIZATION",
        "B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION",
    ):
        result = results[scenario_id]
        assert result["real_owner_transition_used"] is True
        assert result["owner_requery_after_transition"] == "NOT_CURRENT"
        assert result["runtime_authorization_object_reused"] is True


def test_phase_b_explicit_runtime_authorization_invalidation_denies() -> None:
    result = run_phase_b_scenarios()["B07_RUNTIME_AUTHORIZATION_INVALIDATED"]
    assert result["upstream_owner_transition"] == "INVALIDATE_RUNTIME_AUTHORIZATION"
    assert result["owner_requery_after_transition"] == "NOT_CURRENT"
    assert result["runtime_authorization_state_after"] == "NOT_CURRENT"
    assert result["final_boundary_result"] == "DENY"


def test_phase_b_post_remediation_temporal_semantics() -> None:
    results = run_phase_b_scenarios()
    assert results["B01_STABLE_AUTHORIZED_EFFECT"]["final_boundary_result"] == "ALLOW"
    assert results["B02_ACTION_REVOKED_AFTER_AUTHORIZATION"]["final_boundary_result"] == "DENY"
    assert results["B02_ACTION_REVOKED_AFTER_AUTHORIZATION"]["adapter_error_code"] == "ADMITTED_ACTION_NOT_CURRENT"
    assert results["B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION"]["final_boundary_result"] == "DENY"
    assert results["B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION"]["adapter_error_code"] == "ADMITTED_ACTION_NOT_CURRENT"
    assert results["B04_COGNITIVE_GRANT_REVOKED_AFTER_AUTHORIZATION"]["final_boundary_result"] == "DENY"
    assert results["B04_COGNITIVE_GRANT_REVOKED_AFTER_AUTHORIZATION"]["adapter_error_code"] == "ADMITTED_ACTION_NOT_CURRENT"
    assert results["B05_CONCERN_SUPERSEDED_AFTER_AUTHORIZATION"]["final_boundary_result"] == "DENY"
    assert results["B05_CONCERN_SUPERSEDED_AFTER_AUTHORIZATION"]["adapter_error_code"] == "ADMITTED_ACTION_NOT_CURRENT"
    assert results["B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION"]["final_boundary_result"] == "DENY"
    assert results["B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION"]["adapter_error_code"] == "RUNTIME_SAFETY_PREREQUISITE_NOT_CURRENT"
    assert results["B07_RUNTIME_AUTHORIZATION_INVALIDATED"]["final_boundary_result"] == "DENY"
    assert results["B07_RUNTIME_AUTHORIZATION_INVALIDATED"]["adapter_error_code"] == "RUNTIME_AUTHORIZATION_NOT_CURRENT"


def test_phase_b_owner_transition_finding_excludes_non_effect_time_cognition() -> None:
    report = verify_phase_b_results(run_phase_b_scenarios())
    assert report["stale_authority_consumption"] == "NOT_CONFIRMED"
    assert report["allowed_after_authoritative_owner_transition"] == ()
