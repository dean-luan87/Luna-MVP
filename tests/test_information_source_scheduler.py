# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.information_source_scheduler import build_scheduled_source_state
from tools.reasoning_console_aggregator import aggregate_frame


def _base_ctx():
    return {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "t_sched",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_participating_sources_from_user_and_environment():
    ctx = _base_ctx()
    ctx["confirmation_input_raw_text"] = "不是这里"
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    sss = frame.get("scheduled_source_state")
    assert isinstance(sss, dict)
    ps = sss.get("participating_sources") or []
    assert "user_input" in ps
    assert "environment_observation" in ps or "task_state" in ps


def test_has_dominant_source():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    sss = frame.get("scheduled_source_state")
    assert isinstance(sss, dict)
    assert (sss.get("dominant_source") or "").strip()


def test_conflict_or_override_summary_exists():
    ctx = _base_ctx()
    ctx["confirmation_input_raw_text"] = "用户反馈"
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    sss = frame.get("scheduled_source_state")
    assert isinstance(sss, dict)
    assert (sss.get("source_conflict_summary") or "").strip()
    assert (sss.get("priority_override_summary") or "").strip()


def test_scheduled_source_state_applied_true():
    out = build_scheduled_source_state(DecisionMonitorBuilder().build(_base_ctx()).to_dict())
    assert out.scheduled_source_state_applied is True


def test_builder_frame_contains_scheduled_source_state():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    assert isinstance(frame.get("scheduled_source_state"), dict)


def test_timeline_has_scheduled_source_state_event():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    tv = frame.get("reasoning_timeline_view")
    assert isinstance(tv, dict)
    events = tv.get("events") or []
    assert any(e.get("event_type") == "scheduled_source_state_formed" for e in events if isinstance(e, dict))


def test_aggregator_can_read_scheduled_source_state_summary():
    frame = DecisionMonitorBuilder().build(_base_ctx()).to_dict()
    snap = aggregate_frame(frame)
    assert snap.scheduled_dominant_source
    assert snap.scheduled_source_state

