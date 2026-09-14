# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.environment_task_context_reserve import build_environment_task_context_reserve


def test_environment_task_context_container_scene():
    frame = {
        "inputs": {"frame_seq": 1},
        "trace_anchor_id": "t_container",
        "object_search_interaction": {"interaction_flow_type": "container_check_flow", "search_terminal_status": "none"},
        "confirmation_input_bridge": {},
        "reasoning_tree_metrics": {},
    }
    out = build_environment_task_context_reserve(frame).to_dict()
    assert out["environment_context"]["environment_scene_type"] == "container"
    assert out["task_chain_context"]["task_chain_stage"] in ("search", "confirmation", "recheck", "fallback", "unresolved", "resolved")


def test_environment_task_context_occlusion_visibility():
    frame = {
        "inputs": {"frame_seq": 2},
        "trace_anchor_id": "t_occ",
        "object_search_interaction": {"interaction_flow_type": "occlusion_clear_flow", "search_terminal_status": "none"},
        "confirmation_input_bridge": {},
        "reasoning_tree_metrics": {},
    }
    out = build_environment_task_context_reserve(frame).to_dict()
    vis = out["environment_context"]["environment_visibility_state"]
    assert vis in ("occluded", "partial")


def test_environment_task_context_blocked_risk_and_stage():
    frame = {
        "inputs": {"frame_seq": 3},
        "trace_anchor_id": "t_blk",
        "object_search_interaction": {"interaction_flow_type": "container_check_flow", "search_terminal_status": "none"},
        "confirmation_input_bridge": {},
        "reasoning_tree_metrics": {
            "possible_tree_issue_type": "blocked_without_resolution",
            "possible_tree_issue_reason": "blocked",
            "blocked": True,
            "resolved": False,
        },
        "recheck_planner": {"recheck_blocked": True, "recheck_action": "hold_and_confirm"},
    }
    out = build_environment_task_context_reserve(frame).to_dict()
    assert out["environment_context"]["environment_scene_type"] == "blocked"
    risks = out["environment_context"]["environment_risk_factors"]
    assert "blocked_without_resolution" in risks
    assert out["task_chain_context"]["task_chain_stage"] in ("fallback", "unresolved")


def test_environment_task_context_user_feedback_effect_non_empty():
    frame = {
        "inputs": {"frame_seq": 4},
        "trace_anchor_id": "t_fb",
        "object_search_interaction": {"interaction_flow_type": "container_check_flow", "search_terminal_status": "none"},
        "confirmation_input_bridge": {
            "confirmation_input_raw_text": "我打开了",
            "confirmation_input_type": "opened_container",
            "confirmation_bridge_next_effect": "advance_to_recheck",
        },
        "reasoning_tree_metrics": {},
    }
    out = build_environment_task_context_reserve(frame).to_dict()
    u = out["task_chain_context"]["task_chain_user_action_effect"]
    assert u and str(u).strip() and u != "none"


def test_context_premise_summary_covers_env_and_task_chain():
    frame = {
        "inputs": {"frame_seq": 5},
        "trace_anchor_id": "t_sum",
        "object_search_interaction": {"interaction_flow_type": "container_check_flow", "search_terminal_status": "none"},
        "confirmation_input_bridge": {},
        "reasoning_tree_metrics": {},
    }
    out = build_environment_task_context_reserve(frame).to_dict()
    prem = out.get("context_premise_summary") or ""
    assert "场景" in prem
    assert "任务链" in prem


def test_builder_frame_has_environment_task_context_and_timeline_premise_event():
    ctx = {
        "frame_seq": 9,
        "trace_anchor_id": "bench_ctx_env",
        "current_ts": 0.0,
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 40, 80]}],
        "confirmation_input_raw_text": "我打开了",
        "confirmation_input_type": "opened_container",
    }
    d = DecisionMonitorBuilder().build(ctx).to_dict()
    etc = d.get("environment_task_context_reserve")
    assert isinstance(etc, dict)
    assert etc.get("context_premise_applied") is True
    assert etc.get("context_premise_summary")
    tv = d.get("reasoning_timeline_view") or {}
    evs = tv.get("events") or []
    types = [e.get("event_type") for e in evs if isinstance(e, dict)]
    assert "context_premise_recorded" in types
