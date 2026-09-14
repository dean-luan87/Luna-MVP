# -*- coding: utf-8 -*-
"""语音主线：process_final_text → 长输入拆解 v1 分流集成（规则版）。"""

from __future__ import annotations

from capabilities.voice.bridge.route_types import BridgeRouteType
from capabilities.voice.runtime.voice_input_length_mode_classifier import classify_voice_input_length_mode
from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


def test_scenario1_short_whitelist_pause_task() -> None:
    sm = VoiceInputSessionManager()
    r = sm.process_final_text_with_dispatch("暂停任务", now=0.0, is_task_mode=True, session_id="s1")
    assert r.dispatch_type == "short_controlled_input"
    assert r.bridge_decision is not None
    assert r.bridge_decision.route == BridgeRouteType.TASK_LIFECYCLE
    assert r.long_input_parse_result is None


def test_scenario2_confirmation_yes_with_pending_context() -> None:
    sm = VoiceInputSessionManager()
    r = sm.process_final_text_with_dispatch(
        "是",
        now=0.0,
        is_task_mode=False,
        session_id="s1",
        pending_confirmation_context=True,
        pending_confirmation_id="pc-1",
    )
    assert r.dispatch_type == "short_controlled_input"
    assert r.bridge_decision is not None
    assert r.bridge_decision.route == BridgeRouteType.CONFIRMATION
    assert r.long_input_parse_result is None


def test_scenario3_long_natural_language_two_steps() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    r = sm.process_final_text_with_dispatch(
        "先去商场，再找便利店买点吃的",
        now=1.0,
        is_task_mode=False,
        session_id="s1",
    )
    assert r.dispatch_type == "long_task_planning_input"
    assert r.long_input_parse_result is not None
    assert r.long_input_parse_result.task_plan_v1 is not None
    assert len(r.long_input_parse_result.task_plan_v1.execution_order) == 2
    assert r.bridge_decision is None


def test_scenario4_accompanying_observation_long_chain() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    r = sm.process_final_text_with_dispatch(
        "去医院，路上顺便看看有没有便利店",
        now=2.0,
        is_task_mode=False,
        session_id="s1",
    )
    assert r.dispatch_type == "long_task_planning_input"
    assert r.long_input_parse_result is not None
    assert r.long_input_parse_result.task_plan_v1 is not None
    kinds = [t.system_mapping_candidate for t in r.long_input_parse_result.task_plan_v1.tasks]
    assert any(k.startswith("navigation.") for k in kinds)
    assert any(k.startswith("observation.") for k in kinds)


def test_scenario5_unsupported_long_parse_rejection_visible() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    r = sm.process_final_text_with_dispatch(
        "帮我自动挂号",
        now=3.0,
        is_task_mode=False,
        session_id="s1",
    )
    assert r.dispatch_type == "long_task_planning_input"
    assert r.long_input_parse_result is not None
    assert r.long_input_parse_result.rejection_needed is True
    assert r.long_input_parse_result.task_plan_v1 is None


def test_scenario6_long_nl_in_window_not_short_chain() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    r = sm.process_final_text_with_dispatch(
        "这是一段不在白名单里的很长的话我想描述一个复杂行程",
        now=4.0,
        is_task_mode=False,
        session_id="s1",
    )
    assert r.dispatch_type == "long_task_planning_input"
    assert r.bridge_decision is None
    assert r.long_input_parse_result is not None


def test_router_reject_is_structured_rejected_dispatch() -> None:
    sm = VoiceInputSessionManager()
    r = sm.process_final_text_with_dispatch(
        "随便说说没有唤醒也没有窗口",
        now=0.0,
        is_task_mode=False,
        session_id="s1",
    )
    assert r.dispatch_type == "rejected_input"
    assert r.rejection_result is not None
    assert r.rejection_result.reason_code == "no_wake_no_window"


def test_pending_confirmation_branch_without_shortcut_id() -> None:
    """待确认优先：无 shortcut_id 但 registry 命中 confirmation_feedback → 短链。"""
    ev = VoiceInputEvent(
        event_id="e1",
        request_id="r1",
        session_id="s1",
        router_decision="accept",
        raw_text="不是",
        normalized_text="不是",
        wake_word_stripped="不是",
        is_task_mode=True,
        shortcut_id=None,
        task_shortcut=False,
    )
    lm = classify_voice_input_length_mode(
        ev,
        pending_confirmation_context=True,
    )
    assert lm.mode == "short_controlled_input"
    assert lm.reason_code == "pending_confirmation_confirmation_feedback"


def test_dispatch_notes_explain_path() -> None:
    sm = VoiceInputSessionManager()
    r = sm.process_final_text_with_dispatch("暂停任务", now=0.0, is_task_mode=True, session_id="s1")
    assert "whitelist_shortcut" in r.dispatch_reason_code or r.notes
    assert r.metadata.get("length_mode_reason_code") == "whitelist_shortcut"
