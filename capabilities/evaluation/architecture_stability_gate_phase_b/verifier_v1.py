"""Component-level result checks for the Phase B controlled sandbox.

This verifier classifies dynamic evidence; it does not grant a phase decision.
"""

from __future__ import annotations

from typing import Any, Mapping

from .engine_v1 import SCENARIO_IDS


def verify_phase_b_results(results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    missing = tuple(scenario_id for scenario_id in SCENARIO_IDS if scenario_id not in results)
    stable = results.get("B01_STABLE_AUTHORIZED_EFFECT", {})
    runtime_auth_invalidated = results.get("B07_RUNTIME_AUTHORIZATION_INVALIDATED", {})
    trigger_ids = tuple(
        scenario_id
        for scenario_id in SCENARIO_IDS[1:6]
        if results.get(scenario_id, {}).get("owner_requery_after_transition") == "NOT_CURRENT"
        and results.get(scenario_id, {}).get("runtime_authorization_state_after") == "AUTHORIZED"
        and results.get(scenario_id, {}).get("runtime_authorization_object_reused") is True
    )
    allowed_after_owner_transition = tuple(
        scenario_id
        for scenario_id in (
            "B02_ACTION_REVOKED_AFTER_AUTHORIZATION",
            "B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION",
            "B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION",
        )
        if results[scenario_id].get("final_boundary_result") == "ALLOW"
    )
    structural_checks = {
        "all_required_scenarios_present": not missing,
        "stable_control_allows": stable.get("final_boundary_result") == "ALLOW",
        "runtime_authorization_invalidation_denies": runtime_auth_invalidated.get(
            "final_boundary_result"
        ) == "DENY",
        "trigger_owner_requeries_are_not_current": len(trigger_ids) == 5,
        "real_final_authorization_query_used": all(
            results.get(scenario_id, {}).get("real_final_authorization_query_used") is True
            for scenario_id in SCENARIO_IDS
        ),
        "no_real_effect_executed": all(
            results.get(scenario_id, {}).get("real_effect_executed") is False
            for scenario_id in SCENARIO_IDS
        ),
    }
    finding = "CONFIRMED" if allowed_after_owner_transition else "NOT_CONFIRMED"
    return {
        "structural_checks": structural_checks,
        "missing_scenarios": missing,
        "trigger_variant_ids": trigger_ids,
        "effect_time_trigger_variant_ids": (
            "B02_ACTION_REVOKED_AFTER_AUTHORIZATION",
            "B03_WORKING_ENVELOPE_INVALIDATED_AFTER_AUTHORIZATION",
            "B06_SAFETY_INVALIDATED_AFTER_AUTHORIZATION",
        ),
        "allowed_after_authoritative_owner_transition": allowed_after_owner_transition,
        "stale_authority_consumption": finding,
        "dynamic_finding_is_not_a_phase_decision": True,
    }


__all__ = ["verify_phase_b_results"]
