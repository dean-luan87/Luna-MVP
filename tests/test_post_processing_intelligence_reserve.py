# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.post_processing_intelligence_reserve import build_post_processing_intelligence_reserve


def _base_ctx():
    return {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "t_pp_base",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_record_candidate_from_reasoning_and_whitebox():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    pp = frame.get("post_processing_intelligence_reserve")
    assert isinstance(pp, dict)
    rc = pp.get("record_candidates") or []
    types = [r.get("record_source_type") for r in rc if isinstance(r, dict)]
    assert "reasoning_trace" in types
    assert "whitebox_summary" in types


def test_failure_mode_reserve_for_benchmark_and_real_case_hints():
    ctx = _base_ctx()
    ctx["trace_anchor_id"] = "benchmark_smoke_R1_case"
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    pp = frame.get("post_processing_intelligence_reserve")
    ar = pp.get("analysis_reserve") or []
    atypes = [a.get("analysis_type") for a in ar if isinstance(a, dict)]
    assert "failure_mode_analysis" in atypes


def test_strategy_effectiveness_reserve_for_optimization_feedback():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    pp = frame.get("post_processing_intelligence_reserve")
    ar = pp.get("analysis_reserve") or []
    atypes = [a.get("analysis_type") for a in ar if isinstance(a, dict)]
    assert "strategy_effectiveness_analysis" in atypes


def test_routing_reserve_nonempty():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    pp = frame.get("post_processing_intelligence_reserve")
    rr = pp.get("routing_reserve") or []
    assert len(rr) >= 1


def test_post_processing_summary_nonempty():
    ctx = _base_ctx()
    out = build_post_processing_intelligence_reserve(DecisionMonitorBuilder().build(ctx).to_dict())
    assert out.post_processing_summary and str(out.post_processing_summary).strip()


def test_timeline_has_post_processing_event():
    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    tv = frame.get("reasoning_timeline_view")
    assert isinstance(tv, dict)
    evs = tv.get("events") or []
    assert any(e.get("event_type") == "post_processing_reserved" for e in evs if isinstance(e, dict))


def test_aggregate_frame_exposes_post_processing():
    from tools.reasoning_console_aggregator import aggregate_frame

    ctx = _base_ctx()
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    snap = aggregate_frame(frame)
    assert snap.post_processing_summary
    assert snap.post_processing_intelligence_reserve
