# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.run_summary_builder import (
    build_raw_trace_slice,
    build_run_summary_reference,
    build_structured_event_slice,
)


def _base_ctx():
    return {
        "frame_seq": 42,
        "current_ts": 99.0,
        "trace_anchor_id": "t_trace_summary_m02",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_run_summary_reference_built():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    rsr = frame.get("run_summary_reference")
    assert isinstance(rsr, dict)
    assert rsr.get("summary_reference_applied") is True
    assert rsr.get("summary_id") == "t_trace_summary_m02"
    assert (rsr.get("summary_brief") or "").strip()


def test_summary_derives_from_existing_trace_not_empty_hallucination():
    ctx = _base_ctx()
    full = DecisionMonitorBuilder().build(ctx).to_dict()
    r1 = build_run_summary_reference(full)
    assert r1.raw_trace_layer_snapshot.get("frame_seq") == 42
    assert r1.structured_event_layer_snapshot.get("layer") == "structured_event"
    assert isinstance(build_structured_event_slice(full).get("event_count"), int)

    stripped = dict(full)
    stripped["reasoning_timeline_view"] = None
    r2 = build_run_summary_reference(stripped)
    assert r2.structured_event_layer_snapshot.get("event_count", -1) == 0
    assert r1.structured_event_layer_snapshot.get("event_count", 0) >= 1


def test_builder_frame_includes_run_summary_reference():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx)
    assert frame.run_summary_reference is not None
    assert frame.run_summary_reference.summary_reference_applied is True


def test_aggregate_frame_reads_run_summary():
    from tools.reasoning_console_aggregator import aggregate_frame

    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    snap = aggregate_frame(frame)
    assert snap.run_summary_brief
    assert snap.run_summary_id == "t_trace_summary_m02"
    assert snap.raw_trace_layer_one_liner
    assert snap.structured_event_layer_one_liner
    assert snap.summary_reference_one_liner
    assert isinstance(snap.run_summary_reference, dict)


def test_three_layer_semantics_distinct():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    raw = build_raw_trace_slice(frame)
    ev = build_structured_event_slice(frame)
    rsr = build_run_summary_reference(frame).to_dict()
    assert raw.get("layer") == "raw_trace"
    assert ev.get("layer") == "structured_event"
    assert "summary_brief" in rsr and rsr.get("summary_feed_note")
    assert raw.get("action_summary") is not None or raw.get("goal_type") is not None
    assert "event_count" in ev
