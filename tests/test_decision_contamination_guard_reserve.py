# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.decision_contamination_guard_reserve import build_decision_contamination_guard_reserve


def test_user_input_entry_from_confirmation():
    ctx = {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "t_dc",
        "focus_object_label": "bottle",
        "confirmation_input_type": "confirmed_no",
        "confirmation_input_raw_text": "不是这个",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    dcg = frame.get("decision_contamination_guard_reserve")
    assert isinstance(dcg, dict)
    eps = dcg.get("potential_entry_points") or []
    types = [e.get("entry_point_type") for e in eps if isinstance(e, dict)]
    assert "user_input" in types


def test_memory_and_novel_entries():
    ctx = {
        "frame_seq": 2,
        "current_ts": 0.0,
        "trace_anchor_id": "t_dc2",
        "focus_object_label": "bottle",
        "memory_hint_present": True,
        "novel_candidate_present": True,
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    dcg = frame.get("decision_contamination_guard_reserve")
    assert isinstance(dcg, dict)
    eps = dcg.get("potential_entry_points") or []
    types = [e.get("entry_point_type") for e in eps if isinstance(e, dict)]
    assert "memory_recall" in types or "novel_information" in types


def test_strategy_shadow_entry():
    ctx = {
        "frame_seq": 3,
        "current_ts": 0.0,
        "trace_anchor_id": "t_dc3",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    dcg = frame.get("decision_contamination_guard_reserve")
    assert isinstance(dcg, dict)
    eps = dcg.get("potential_entry_points") or []
    types = [e.get("entry_point_type") for e in eps if isinstance(e, dict)]
    assert "strategy_injection" in types


def test_mitigation_reserve_list():
    ctx = {
        "frame_seq": 4,
        "current_ts": 0.0,
        "trace_anchor_id": "t_dc4",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "测",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    dcg = frame.get("decision_contamination_guard_reserve")
    mits = dcg.get("potential_mitigation_points") or []
    assert len(mits) >= 1
    mtypes = [m.get("mitigation_type") for m in mits if isinstance(m, dict)]
    assert "shadow_validation" in mtypes


def test_contamination_summary_nonempty():
    ctx = {
        "frame_seq": 5,
        "current_ts": 0.0,
        "trace_anchor_id": "t_dc5",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }
    out = build_decision_contamination_guard_reserve(DecisionMonitorBuilder().build(ctx).to_dict())
    assert out.contamination_observation_summary and str(out.contamination_observation_summary).strip()


def test_timeline_has_contamination_event():
    ctx = {
        "frame_seq": 6,
        "current_ts": 0.0,
        "trace_anchor_id": "t_dc6",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "x",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    tv = frame.get("reasoning_timeline_view")
    assert isinstance(tv, dict)
    evs = tv.get("events") or []
    assert any(e.get("event_type") == "contamination_guard_reserved" for e in evs if isinstance(e, dict))
