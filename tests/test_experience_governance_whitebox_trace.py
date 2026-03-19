import pytest


from decision_monitor.confirmation_input_bridge import ConfirmationInputBridgeResult
from decision_monitor.experience_evolution import ExperienceCandidate, ExperienceEvolutionResult
from decision_monitor.experience_governance_whitebox_trace import build_experience_governance_whitebox_trace


def _cand(status: str, *, repeat: int = 1, support: int = 1, confirm: int = 0, fallback: int = 0, contradict: int = 0, scope: str = "local_only"):
    return ExperienceCandidate(
        experience_type="object_search_path_pattern",
        evolution_status=status,
        evolution_reason=f"status={status}",
        repeated_pattern_count=repeat,
        supporting_events_count=support,
        user_confirmed_count=confirm,
        fallback_count=fallback,
        contradiction_count=contradict,
        future_use_scope=scope,
        contradiction_sources=["user_denied"] if status == "rejected" else [],
    )


def test_watchlist_outcome_has_exclusion():
    evo = ExperienceEvolutionResult(candidates=[_cand("watchlist", repeat=1, support=1, confirm=1, fallback=0, contradict=0, scope="local_only")])
    out = build_experience_governance_whitebox_trace(experience_evolution=evo)
    assert out.whitebox_applied is True
    assert out.weight_allocation
    assert out.exclusion_log
    assert out.user_visible_explanation and out.user_visible_explanation.user_visible_reason_status


def test_promotable_outcome_present():
    evo = ExperienceEvolutionResult(candidates=[_cand("promotable", repeat=3, support=1, confirm=1, fallback=0, contradict=0, scope="same_flow_only")])
    out = build_experience_governance_whitebox_trace(experience_evolution=evo)
    assert out.weight_allocation
    # should rank promotable near top due to bias+bonuses
    assert out.weight_allocation[0].governance_outcome_id in ("promotable", "watchlist")


def test_blocked_outcome_present():
    evo = ExperienceEvolutionResult(candidates=[_cand("blocked", repeat=1, support=1, confirm=0, fallback=2, contradict=0, scope="review_required")])
    out = build_experience_governance_whitebox_trace(experience_evolution=evo)
    assert out.user_visible_explanation and out.user_visible_explanation.user_visible_reason_scope


def test_rejected_outcome_with_feedback():
    evo = ExperienceEvolutionResult(candidates=[_cand("rejected", repeat=1, support=0, confirm=0, fallback=0, contradict=1, scope="review_required")])
    cib = ConfirmationInputBridgeResult(confirmation_input_type="target_not_found", confirmation_input_raw_text="不是这个")
    out = build_experience_governance_whitebox_trace(experience_evolution=evo, confirmation_input_bridge=cib)
    assert out.interaction_trace
    assert out.interaction_trace[0].mapped_confirmation_type == "target_not_found"


def test_future_use_scope_is_exposed_in_user_visible_reason():
    evo = ExperienceEvolutionResult(candidates=[_cand("watchlist", scope="same_object_type_only")])
    out = build_experience_governance_whitebox_trace(experience_evolution=evo)
    assert "same_object_type_only" in (out.user_visible_explanation.user_visible_reason_scope or "")

