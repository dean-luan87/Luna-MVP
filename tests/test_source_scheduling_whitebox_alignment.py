# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from tools.reasoning_console_aggregator import aggregate_frame


def _ctx():
    return {
        "frame_seq": 11,
        "current_ts": 0.0,
        "trace_anchor_id": "t_sched_align",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "不是这里",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 20, 100, 120], "conf": 0.7}],
    }


def test_dominant_source_has_reason_summary():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    sss = frame.get("scheduled_source_state")
    assert isinstance(sss, dict)
    assert (sss.get("dominant_source_reason_summary") or "").strip()


def test_conflict_or_override_events_exist():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    sss = frame.get("scheduled_source_state") or {}
    evs = sss.get("source_scheduling_event_summaries") or []
    assert any(("source_conflict_detected" in e) or ("priority_override_applied" in e) for e in evs)


def test_timeline_has_enhanced_source_scheduling_events():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    tv = frame.get("reasoning_timeline_view")
    assert isinstance(tv, dict)
    ev_types = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    assert "scheduled_source_state_formed" in ev_types
    assert "dominant_source_selected" in ev_types


def test_structure_tree_summary_has_source_dimensions():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    tree = frame.get("reasoning_structure_tree")
    if not isinstance(tree, dict):
        from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree

        tree = build_reasoning_structure_tree(frame).to_dict()
    ts = tree.get("tree_summary") or ""
    assert "source=" in ts
    assert "source_conflict=" in ts
    assert "source_override=" in ts


def test_aggregator_reads_enhanced_readable_summary():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert (snap.scheduled_source_readable_summary or "").strip()
    assert (snap.scheduled_source_state or {}).get("source_scheduling_event_summaries") is not None

