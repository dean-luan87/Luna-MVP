# -*- coding: utf-8 -*-
"""Memory Invocation Explanation M0.3 — 主链 / 白盒 / Summary / 聚合 对齐。"""

from __future__ import annotations

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.memory_invocation_explanation import (
    build_memory_invocation_explanation,
    build_memory_usage_summary_line,
)
from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree
from decision_monitor.reasoning_timeline_view import append_memory_invocation_explanation_events
from decision_monitor.run_summary_builder import build_run_summary_reference
from tools.reasoning_console_aggregator import aggregate_frame


def _ctx():
    return {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "t_mem_m03",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_build_minimal_explanation():
    d = build_memory_invocation_explanation({}).to_dict()
    assert d.get("memory_invocation_explanation_applied") is True
    assert "memory_invocation_effect_summary" in d


def test_explanation_on_frame():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    mie = frame.get("memory_invocation_explanation")
    assert isinstance(mie, dict)
    assert mie.get("memory_invocation_explanation_applied") is True
    assert "memory_type_summary" in mie


def test_whitebox_tree_has_mem_tag():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    tree = build_reasoning_structure_tree(frame).to_dict()
    ts = tree.get("tree_summary") or ""
    assert "mem=inv=" in ts


def test_timeline_has_memory_events():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    tv = frame.get("reasoning_timeline_view")
    if hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    et = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    assert "memory_invocation_explained" in et


def test_run_summary_memory_line():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    rsr = build_run_summary_reference(frame).to_dict()
    assert rsr.get("memory_usage_summary")
    assert "invoked=" in (rsr.get("memory_usage_summary") or "")
    brief = rsr.get("summary_brief") or ""
    assert "; mem=" in brief


def test_append_memory_events_api():
    from decision_monitor.reasoning_timeline_view import ReasoningTimelineViewResult

    mie = build_memory_invocation_explanation(
        {
            "memory_novel_information_channel": {"memory_channel_count": 1, "channel_summary": "x"},
            "scheduled_source_state": {
                "dominant_source": "memory_recall",
                "source_conflict_summary": "none",
                "priority_override_summary": "none",
                "participating_sources": ["memory_recall", "environment_observation"],
                "scheduled_source_state_applied": True,
            },
        }
    ).to_dict()
    v0 = ReasoningTimelineViewResult(events=[], timeline_applied=True)
    v1 = append_memory_invocation_explanation_events(v0, mie)
    types = [e.event_type for e in v1.events]
    assert "memory_invocation_explained" in types


def test_aggregator_reads_memory_invocation():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert snap.memory_invocation_explanation
    assert (snap.memory_invocation_readable or "").strip()
    assert snap.run_summary_memory_usage_summary


def test_build_memory_usage_summary_line_merges():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    line = build_memory_usage_summary_line(frame)
    assert "effect=" in line
