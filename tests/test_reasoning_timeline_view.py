# -*- coding: utf-8 -*-

from decision_monitor.reasoning_timeline_view import build_reasoning_timeline_view


def test_flow_hypothesis_quality_events_present():
    frame = {
        "object_search_interaction": {"interaction_flow_type": "container_check_flow", "search_terminal_status": "none"},
        "hypothesis_layer": {"hypotheses": [{"hypothesis_type": "container_candidate", "hypothesis_summary": "目标可能在容器内"}]},
        "reasoning_tree_quality_overlay": {"quality_grade": "acceptable", "quality_summary": "ok"},
    }
    out = build_reasoning_timeline_view(frame).to_dict()
    types = [e["event_type"] for e in out["events"]]
    assert "flow_entered" in types
    assert "hypothesis_selected" in types
    assert "quality_changed" in types


def test_feedback_and_path_switched():
    frame = {
        "confirmation_input_bridge": {"confirmation_input_raw_text": "我打开了", "confirmation_input_type": "opened_container"},
        "spatiotemporal_continuity_reserve": {"continuity_support_level": "broken", "continuity_broken": True, "continuity_influence_reason": "user feedback changed path"},
        "reasoning_tree_quality_overlay": {"quality_grade": "acceptable"},
    }
    out = build_reasoning_timeline_view(frame).to_dict()
    types = [e["event_type"] for e in out["events"]]
    assert "feedback_received" in types
    assert "path_switched" in types
    assert "continuity_changed" in types


def test_blocked_to_fallback_issue_present():
    frame = {
        "reasoning_tree_metrics": {"possible_tree_issue_type": "blocked_without_resolution", "possible_tree_issue_reason": "blocked=true", "blocked": True, "resolved": False},
        "recheck_planner": {"recheck_action": "hold_and_confirm", "recheck_reason": "blocked_fallback"},
        "reasoning_tree_quality_overlay": {"quality_grade": "poor"},
    }
    out = build_reasoning_timeline_view(frame).to_dict()
    types = [e["event_type"] for e in out["events"]]
    assert "issue_detected" in types
    assert "fallback_triggered" in types
    assert "resolution_updated" in types


def test_optimization_and_validation_events():
    frame = {
        "optimization_hint": {"optimization_hint_type": "reduce_dead_branches", "suggested_optimization_module": "hypothesis_layer"},
        "optimization_feedback_loop": {"validation_result": "improved"},
        "reasoning_tree_quality_overlay": {"quality_grade": "acceptable"},
    }
    out = build_reasoning_timeline_view(frame).to_dict()
    types = [e["event_type"] for e in out["events"]]
    assert "optimization_hint_generated" in types
    assert "validation_result_changed" in types


def test_key_transition_summary_non_empty_when_high_events():
    frame = {
        "reasoning_tree_metrics": {"possible_tree_issue_type": "high_dead_branch_ratio", "possible_tree_issue_reason": "prune_rate=0.7", "blocked": False, "resolved": False},
        "recheck_planner": {"recheck_action": "ask_user_for_clarification"},
        "reasoning_tree_quality_overlay": {"quality_grade": "acceptable"},
    }
    out = build_reasoning_timeline_view(frame).to_dict()
    assert out["key_transition_summary"]
    assert out["key_transition_count"] >= 1

