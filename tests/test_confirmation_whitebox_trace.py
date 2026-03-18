# -*- coding: utf-8 -*-
"""Confirmation Whitebox Trace M0 单测：容器/遮挡/取消/无输入等路径。"""

from types import SimpleNamespace

from decision_monitor.confirmation_input_bridge import build_confirmation_input_bridge
from decision_monitor.confirmation_whitebox_trace import build_confirmation_whitebox_trace


def _ns(**kwargs):
    return SimpleNamespace(**kwargs)


def _assert_common(out):
    assert out is not None
    assert len(out.reasoning_steps) == 4
    assert out.weight_allocation
    assert out.exclusion_log
    assert out.interaction_trace
    assert out.user_visible_explanation is not None
    uv = out.user_visible_explanation
    assert uv.user_visible_reason_mapping
    assert uv.user_visible_reason_next_effect
    assert uv.user_visible_changed_search_direction
    assert uv.user_visible_excluded_alternative


def test_confirmation_whitebox_container_opened_container():
    osi = _ns(interaction_flow_type="container_check_flow", search_subtask_state="waiting_user")
    cib = build_confirmation_input_bridge(
        osi, confirmation_input_type=None, confirmation_input_raw_text="打开了"
    )
    out = build_confirmation_whitebox_trace(
        confirmation_input_bridge=cib,
        object_search_interaction=osi,
        action_hint_copy=_ns(action_hint_primary="先看杯子里", action_hint_confirmation="打开后看看有没有"),
    )
    _assert_common(out)
    assert out.whitebox_applied is True
    assert cib.confirmation_input_type in ("opened_container",)
    assert cib.confirmation_bridge_next_effect == "advance_to_recheck"


def test_confirmation_whitebox_container_confirmed_no_reject_container():
    osi = _ns(interaction_flow_type="container_check_flow", search_subtask_state="waiting_user")
    cib = build_confirmation_input_bridge(
        osi, confirmation_input_type="confirmed_no", confirmation_input_raw_text="没有"
    )
    out = build_confirmation_whitebox_trace(
        confirmation_input_bridge=cib,
        object_search_interaction=osi,
        action_hint_copy=_ns(action_hint_primary="先看杯子里", action_hint_confirmation="确认一下杯子里有没有"),
    )
    _assert_common(out)
    assert cib.confirmation_bridge_next_effect == "mark_container_rejected"
    assert "取消" not in (out.user_visible_explanation.user_visible_reason_mapping or "")


def test_confirmation_whitebox_occlusion_cleared_marks_occlusion():
    osi = _ns(interaction_flow_type="occlusion_clear_flow", search_subtask_state="waiting_user")
    cib = build_confirmation_input_bridge(
        osi, confirmation_input_type=None, confirmation_input_raw_text="移开了"
    )
    out = build_confirmation_whitebox_trace(
        confirmation_input_bridge=cib,
        object_search_interaction=osi,
        action_hint_copy=_ns(action_hint_primary="先移开遮挡", action_hint_confirmation="移开后再确认"),
    )
    _assert_common(out)
    assert cib.confirmation_input_type == "occlusion_cleared"
    assert cib.confirmation_bridge_next_effect == "mark_occlusion_cleared"


def test_confirmation_whitebox_cancelled_cancels_search():
    osi = _ns(interaction_flow_type="general", search_subtask_state="waiting_user")
    cib = build_confirmation_input_bridge(
        osi, confirmation_input_type=None, confirmation_input_raw_text="取消"
    )
    out = build_confirmation_whitebox_trace(
        confirmation_input_bridge=cib,
        object_search_interaction=osi,
        action_hint_copy=_ns(action_hint_primary="继续找找", action_hint_confirmation="确认一下"),
    )
    _assert_common(out)
    assert cib.confirmation_input_type == "cancelled"
    assert cib.confirmation_bridge_next_effect == "cancel_search"
    assert "取消" in (out.user_visible_explanation.user_visible_changed_search_direction or "")


def test_confirmation_whitebox_no_input_records_no_confirmation_input():
    osi = _ns(interaction_flow_type="general", search_subtask_state="searching")
    cib = build_confirmation_input_bridge(osi, confirmation_input_type=None, confirmation_input_raw_text=None)
    out = build_confirmation_whitebox_trace(
        confirmation_input_bridge=cib,
        object_search_interaction=osi,
        action_hint_copy=None,
    )
    _assert_common(out)
    assert out.interaction_trace[0].interaction_effect_on_confirmation in (
        "no_confirmation_input_this_frame",
        "mapped=—;next=none",
    )

