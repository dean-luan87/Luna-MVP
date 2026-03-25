# -*- coding: utf-8 -*-
"""Summary × Post-Processing Boundary Contract M0.5 单测。"""

from __future__ import annotations

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.post_processing_summary_contract import (
    PostProcessingSummaryEntry,
    build_post_processing_summary_entry,
)
from decision_monitor.run_summary_builder import build_run_summary_reference
from tools.reasoning_console_aggregator import aggregate_frame


def _ctx():
    return {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "t_pp_m05",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_build_entry_from_rsr():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    rsr = build_run_summary_reference(frame)
    assert rsr.summary_reference_applied
    pse = build_post_processing_summary_entry(frame)
    assert pse.post_processing_summary_entry_applied
    assert pse.entry_id.startswith("ppse_")
    assert pse.summary_brief_hint_only is True
    assert pse.memory_write_forbidden_from_summary_only is True
    assert "raw_trace_layer_snapshot" not in pse.to_dict()


def test_frame_has_post_processing_summary_entry():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    ppe = frame.get("post_processing_summary_entry")
    assert isinstance(ppe, dict)
    assert ppe.get("post_processing_summary_entry_applied") is True


def test_entry_has_backfill_flags():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    ppe = frame.get("post_processing_summary_entry") or {}
    assert "requires_trace_backfill" in ppe
    assert "requires_event_backfill" in ppe
    assert "requires_whitebox_backfill" in ppe
    assert "backfill_reason_summary" in ppe


def test_pp_reserve_has_entry_cross_ref():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    ppi = frame.get("post_processing_intelligence_reserve") or {}
    assert ppi.get("summary_post_processing_entry_id")


def test_aggregator_reads_entry():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert snap.post_processing_summary_entry
    assert snap.post_processing_entry_id


def test_entry_not_substitute_for_raw_trace_in_object():
    """契约对象不包含 raw/event 切片，仅承载 run_summary 侧摘要字段与边界标志。"""
    pse = PostProcessingSummaryEntry(
        post_processing_summary_entry_applied=True,
        entry_id="ppse_x",
    )
    d = pse.to_dict()
    assert "raw_trace_layer_snapshot" not in d
    assert "structured_event_layer_snapshot" not in d
