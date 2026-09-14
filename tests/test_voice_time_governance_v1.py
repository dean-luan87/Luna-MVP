# -*- coding: utf-8 -*-
"""语音时间治理 v1：90s 长语音 vs 30s 会话窗口分离。"""

from __future__ import annotations

from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
from capabilities.voice.runtime.voice_time_governance_v1 import (
    GovernanceTickResult,
    VoiceRuntimePhase,
    VoiceTimeGovernanceRuntime,
)
from capabilities.voice.runtime.voice_wake_window_manager import WakeWindowState


def test_scenario1_long_capture_not_killed_by_30s_session_window() -> None:
    """长语音进行中，不应被 30 秒窗口打断（会话时钟挂起）。"""
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s")
    assert sm.governance.phase == VoiceRuntimePhase.session_open
    sm.on_capture_started(0.0)
    assert sm.governance.phase == VoiceRuntimePhase.capturing_input
    assert sm.governance.session_window_suspended is True
    assert sm.window.is_window_active(50.0) is True


def test_scenario2_silence_3s_ends_segment_via_tick() -> None:
    """静默 3 秒：tick 返回 segment_end（与 SessionWindowTimer 独立）。"""
    g = VoiceTimeGovernanceRuntime()
    g.on_wake_route_accept(0.0)
    g.on_capture_started(0.0)
    r = g.tick_capturing(10.0, silence_duration_sec=3.0, capture_duration_sec=5.0)
    assert r.segment_end_silence is True
    assert r.force_capture_90 is False


def test_scenario3_input_end_resets_full_30s_not_remainder() -> None:
    """输入结束后重新开满 30 秒窗口（从收口时刻起算）。"""
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s")
    sm.on_capture_started(0.0)
    sm.process_final_text("一句说完", now=5.0, is_task_mode=False, session_id="s")
    assert sm.window.is_window_active(34.0) is True
    assert sm.window.is_window_active(36.0) is False


def test_scenario4_forced_90s_cutoff_flags() -> None:
    """90 秒强切：事件字段与 tick 一致。"""
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s")
    sm.on_capture_started(0.0)
    ev = sm.process_final_text(
        "长内容",
        now=1.0,
        is_task_mode=True,
        session_id="s",
        is_forced_cutoff=True,
        cutoff_reason="max_capture_duration",
    )
    assert ev.is_forced_cutoff is True
    assert ev.cutoff_reason == "max_capture_duration"
    assert ev.continuation_allowed is True
    g = VoiceTimeGovernanceRuntime()
    g.on_wake_route_accept(0.0)
    g.on_capture_started(0.0)
    tr = g.tick_capturing(100.0, silence_duration_sec=0.0, capture_duration_sec=95.0)
    assert tr == GovernanceTickResult(force_capture_90=True)


def test_scenario5_forced_cutoff_then_followup_without_wake_in_window() -> None:
    """90 秒强切后在新窗口内可续接，不要求重新唤醒。"""
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s")
    sm.on_capture_started(0.0)
    sm.process_final_text(
        "第一段",
        now=1.0,
        is_task_mode=True,
        session_id="s",
        is_forced_cutoff=True,
        cutoff_reason="max_capture_duration",
    )
    ev2 = sm.process_final_text("到哪了", now=5.0, is_task_mode=True, session_id="s")
    assert ev2.router_decision == "accept"
    assert ev2.wake_word_detected is False
    assert ev2.shortcut_id == "q_where"


def test_warn_at_80_once() -> None:
    g = VoiceTimeGovernanceRuntime()
    g.on_wake_route_accept(0.0)
    g.on_capture_started(0.0)
    r1 = g.tick_capturing(80.0, silence_duration_sec=0.0, capture_duration_sec=80.0)
    assert r1.warn_capture_80 is True
    r2 = g.tick_capturing(81.0, silence_duration_sec=0.0, capture_duration_sec=81.0)
    assert r2.warn_capture_80 is False


def test_idle_session_open_observable_after_wake_without_capture() -> None:
    sm = VoiceInputSessionManager()
    assert sm.governance.phase == VoiceRuntimePhase.idle
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s")
    assert sm.governance.phase == VoiceRuntimePhase.session_open
    assert sm.window.state == WakeWindowState.active_window
