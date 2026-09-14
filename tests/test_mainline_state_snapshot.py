# -*- coding: utf-8 -*-
"""Mainline State / Phase Explicitness M0.4 对齐单测。"""

from __future__ import annotations

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.mainline_state_snapshot import (
    build_mainline_state_snapshot,
    build_mainline_state_summary_line,
)
from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree
from decision_monitor.reasoning_timeline_view import (
    ReasoningTimelineViewResult,
    append_mainline_state_snapshot_events,
)
from decision_monitor.run_summary_builder import build_run_summary_reference
from tools.reasoning_console_aggregator import aggregate_frame


def _ctx():
    return {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "t_mls_m04",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_build_snapshot_minimal():
    s = build_mainline_state_snapshot({}).to_dict()
    assert s.get("mainline_state_snapshot_applied") is True
    assert s.get("mainline_state") in ("candidate", "execution", "recovery", "pause", "unknown")
    assert s.get("mainline_phase") in (
        "contextualization",
        "candidate_formation",
        "path_selection",
        "recheck_or_repair",
        "closure",
        "result_feedback",
        "unknown",
    )


def test_snapshot_on_frame():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    mss = frame.get("mainline_state_snapshot")
    assert isinstance(mss, dict)
    assert mss.get("mainline_state_snapshot_applied") is True


def test_tree_summary_has_state_phase():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    tree = build_reasoning_structure_tree(frame).to_dict()
    ts = tree.get("tree_summary") or ""
    assert "state=" in ts
    assert "phase=" in ts


def test_timeline_has_mainline_events():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    tv = frame.get("reasoning_timeline_view")
    if hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    et = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    assert "mainline_state_snapshot_formed" in et


def test_run_summary_has_mainline_state_line():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    rsr = build_run_summary_reference(frame).to_dict()
    assert rsr.get("mainline_state_summary")
    assert "state=" in (rsr.get("mainline_state_summary") or "")
    brief = rsr.get("summary_brief") or ""
    assert "mainline=" in brief
    assert "ctx=" in brief


def test_append_mainline_events_api():
    mss = build_mainline_state_snapshot({"trace_anchor_id": "x", "inputs": {"frame_seq": 0}}).to_dict()
    v0 = ReasoningTimelineViewResult(events=[], timeline_applied=True)
    v1 = append_mainline_state_snapshot_events(v0, mss)
    assert any(e.event_type == "mainline_state_snapshot_formed" for e in v1.events)


def test_aggregator_reads_mainline():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert snap.mainline_state_snapshot
    assert snap.snapshot_mainline_state
    assert snap.run_summary_mainline_state_summary


def test_summary_line_helper():
    d = build_mainline_state_snapshot({}).to_dict()
    line = build_mainline_state_summary_line(d)
    assert "state=" in line
