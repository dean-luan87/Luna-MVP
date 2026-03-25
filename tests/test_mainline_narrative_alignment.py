# -*- coding: utf-8 -*-
"""Mainline Narrative Alignment M0.6 单测。"""

from __future__ import annotations

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.mainline_narrative_alignment import build_mainline_narrative_alignment
from tools.reasoning_console_aggregator import aggregate_frame


def _ctx():
    return {
        "frame_seq": 2,
        "current_ts": 0.1,
        "trace_anchor_id": "t_nar_m06",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_narrative_alignment_constructed():
    d = build_mainline_narrative_alignment({}).to_dict()
    assert "narrative_brief" in d


def test_frame_has_narrative_alignment():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    nar = frame.get("mainline_narrative_alignment")
    assert isinstance(nar, dict)
    assert nar.get("mainline_narrative_alignment_applied") is True


def test_narrative_has_multi_segments():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    nar = frame.get("mainline_narrative_alignment") or {}
    filled = [
        bool(nar.get("source_summary")),
        bool(nar.get("task_summary")),
        bool(nar.get("memory_summary")),
        bool(nar.get("mainline_state_summary")),
        bool(nar.get("risk_summary")),
    ]
    assert sum(1 for x in filled if x) >= 4


def test_summary_brief_aligned_with_narrative_order():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    rsr = frame.get("run_summary_reference") or {}
    brief = rsr.get("summary_brief") or ""
    assert "ctx=" in brief
    assert "source=" in brief
    assert "task=" in brief
    assert "mem=" in brief
    assert "mainline=" in brief
    assert "closure=" in brief
    assert "risk=" in brief


def test_post_processing_entry_has_narrative_readable():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    ppe = frame.get("post_processing_summary_entry") or {}
    assert ppe.get("narrative_readable")
    assert ppe.get("summary_brief_hint_only") is True


def test_aggregator_reads_narrative():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert snap.mainline_narrative_readable
    assert snap.post_processing_summary_entry
