# -*- coding: utf-8 -*-
"""Task Chain Position Explanation Enhancement M0.1 — 白盒 / 时间轴 / Summary / 聚合 对齐单测。"""

from __future__ import annotations

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree
from decision_monitor.reasoning_timeline_view import (
    append_task_chain_position_explanation_events,
    append_task_chain_snapshot_event,
)
from decision_monitor.run_summary_builder import build_run_summary_reference
from decision_monitor.task_chain_state_snapshot import (
    build_task_chain_state_snapshot,
    build_task_chain_progress_summary,
)
from tools.reasoning_console_aggregator import aggregate_frame


def _base_ctx():
    return {
        "frame_seq": 7,
        "current_ts": 2.0,
        "trace_anchor_id": "t_tc_pos_m01",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_snapshot_has_position_fields_and_stronger_progress_summary():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    tcs = frame.get("task_chain_state_snapshot")
    assert isinstance(tcs, dict)
    assert tcs.get("task_chain_state_snapshot_applied") is True
    assert tcs.get("task_position_reason_summary")
    assert isinstance(tcs.get("task_position_event_summaries"), list)
    assert tcs.get("task_position_warning_summary") is not None
    assert isinstance(tcs.get("task_position_timeline_events"), list)
    prog = build_task_chain_progress_summary(tcs)
    assert "main_push_hint=" in prog
    assert "local_only_risk=" in prog
    assert "warn=" in prog


def test_resume_target_yields_timeline_event():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    tcs = frame.get("task_chain_state_snapshot")
    tl = tcs.get("task_position_timeline_events") or []
    types = [x.get("event_type") for x in tl if isinstance(x, dict)]
    assert "task_chain_position_interpreted" in types
    assert len(types) >= 2


def test_timeline_includes_m01_explanation_events():
    """builder 主路径须在时间轴末尾注入 M0.1 位置解释事件。"""
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    tv = frame.get("reasoning_timeline_view")
    if hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    et = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    assert "task_chain_position_interpreted" in et
    assert "task_chain_state_snapshot_formed" in et


def test_append_helpers_chain_events():
    """显式调用 append_* 时仍能注入 M0.1 事件（与 builder 同源 API）。"""
    from decision_monitor.reasoning_timeline_view import ReasoningTimelineEvent, ReasoningTimelineViewResult

    tcs = build_task_chain_state_snapshot(
        {
            "trace_anchor_id": "x",
            "inputs": {"frame_seq": 1},
            "goal": {"goal_id": "g"},
            "task_chain_bridge": {"task_chain_state": "active", "task_chain_bundle_state": "none"},
        }
    ).to_dict()
    view = ReasoningTimelineViewResult(events=[], timeline_applied=True)
    v2 = append_task_chain_snapshot_event(view, tcs)
    v3 = append_task_chain_position_explanation_events(v2, tcs)
    et = [e.event_type for e in v3.events]
    assert "task_chain_position_interpreted" in et


def test_structure_tree_task_summary_enhanced():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    tree = build_reasoning_structure_tree(frame).to_dict()
    ts = tree.get("tree_summary") or ""
    assert "task_pos=" in ts
    assert "warn=" in ts


def test_run_summary_task_progress_enhanced():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    rsr = build_run_summary_reference(frame).to_dict()
    t = rsr.get("task_chain_progress_summary") or ""
    assert "main_push_hint=" in t
    brief = rsr.get("summary_brief") or ""
    assert "task=" in brief


def test_aggregator_reads_position_fields():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert snap.snapshot_task_position_reason_summary or snap.snapshot_task_position_warning_summary is not None
    assert (snap.snapshot_task_position_readable or "").strip()
    assert (snap.run_summary_task_chain_progress_summary or "").strip()


def test_manual_frame_local_success_warning():
    """构造子任务终端 found + 可恢复主链 → 局部成功风险与时间轴事件。"""
    frame = {
        "trace_anchor_id": "manual_tc",
        "inputs": {"frame_seq": 0, "current_ts": 0.0},
        "goal": {"goal_id": "g_main"},
        "task_chain_bridge": {
            "task_chain_state": "active",
            "task_chain_substate": None,
            "task_chain_bundle_state": "none",
        },
        "object_search_interaction": {
            "search_target_label": "cup",
            "search_subtask_state": "search_active",
            "search_terminal_status": "found",
            "search_can_resume_main_task": True,
            "search_result_level": "object",
        },
        "environment_task_context_reserve": {
            "task_chain_context": {
                "task_chain_id": "tc_x",
                "task_chain_stage": "search",
                "task_chain_context_summary": "ctx",
            },
            "context_premise_summary": "prem",
        },
    }
    snap = build_task_chain_state_snapshot(frame).to_dict()
    assert snap.get("task_mode") == "subtask"
    warn = snap.get("task_position_warning_summary") or ""
    assert "local_success" in warn
    tl = snap.get("task_position_timeline_events") or []
    et = [x.get("event_type") for x in tl if isinstance(x, dict)]
    assert "task_local_success_without_main_progress" in et
