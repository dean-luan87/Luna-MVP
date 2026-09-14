# -*- coding: utf-8 -*-
"""语音输入主线 v1：唤醒、窗口、白名单、路由、切段策略。"""

from __future__ import annotations

import pytest

from capabilities.voice.bridge.voice_input_router import WAKE_WORD, contains_wake_word
from capabilities.voice.providers.mock_asr_provider import MockASRProvider
from capabilities.voice.runtime.voice_input_session_manager import VoiceInputSessionManager
from capabilities.voice.runtime.voice_segment_timeout_policy import (
    DEFAULT_SEGMENT_END_SILENCE_SEC,
    VoiceSegmentTimeoutPolicy,
)
from capabilities.voice.runtime.voice_wake_window_manager import WakeWindowState


def test_scenario1_wake_opens_window() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("艾达", now=100.0, is_task_mode=False, session_id="s1")
    assert ev.router_decision == "accept"
    assert ev.wake_word_detected is True
    assert sm.window.state == WakeWindowState.active_window


def test_scenario2_wake_then_followup_no_wake() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达，开始导航去医院", now=0.0, is_task_mode=False, session_id="s1")
    ev2 = sm.process_final_text("现在到哪了", now=10.0, is_task_mode=True, session_id="s1")
    assert ev2.router_decision == "accept"
    assert ev2.wake_word_detected is False


def test_scenario3_segment_policy_3s() -> None:
    p = VoiceSegmentTimeoutPolicy()
    assert p.is_segment_end(2.9) is False
    assert p.is_segment_end(3.0) is True
    assert DEFAULT_SEGMENT_END_SILENCE_SEC == 3.0


def test_scenario4_window_expires_30s() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    assert sm.window.is_window_active(29.0) is True
    assert sm.window.is_window_active(31.0) is False
    ev = sm.process_final_text("随便说说", now=32.0, is_task_mode=False, session_id="s1")
    assert ev.router_decision == "reject"


def test_scenario5_task_mode_shortcut_without_wake() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("暂停", now=0.0, is_task_mode=True, session_id="s1")
    assert ev.router_decision == "accept"
    assert ev.shortcut_id == "task_pause"


@pytest.mark.parametrize(
    "phrase,expected_id",
    [
        ("暂停", "task_pause"),
        ("继续", "task_resume"),
        ("到哪了", "q_where"),
        ("当前状态", "q_status"),
        ("附近有什么", "q_nearby"),
    ],
)
def test_acceptance_item12_task_mode_shortcuts(phrase: str, expected_id: str) -> None:
    """验收项 12：任务态下暂停/继续/问询类可放行（白名单命中）。"""
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text(phrase, now=0.0, is_task_mode=True, session_id="s1")
    assert ev.router_decision == "accept"
    assert ev.shortcut_id == expected_id


def test_scenario6_normal_mode_no_wake_reject_long() -> None:
    sm = VoiceInputSessionManager()
    ev = sm.process_final_text("这是一段不在白名单里的很长的话", now=0.0, is_task_mode=False, session_id="s1")
    assert ev.router_decision == "reject"


def test_scenario7_shutdown_clears() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达", now=0.0, is_task_mode=False, session_id="s1")
    sm.on_shutdown_or_standby()
    assert sm.window.state == WakeWindowState.inactive


def test_scenario8_context_resume_hint() -> None:
    sm = VoiceInputSessionManager()
    sm.process_final_text("艾达，开始导航", now=0.0, is_task_mode=True, session_id="s1")
    ev2 = sm.process_final_text("那现在到哪了", now=5.0, is_task_mode=True, session_id="s1")
    assert ev2.router_decision == "accept"
    assert ev2.context_resume_hint is not None
    assert "prev=" in ev2.context_resume_hint or "now=" in ev2.context_resume_hint


def test_mock_asr_roundtrip() -> None:
    p = MockASRProvider()
    ev = p.transcribe(audio_bytes="艾达测试".encode("utf-8"))
    assert "艾达" in (ev.text or "")


def test_wake_word_constant() -> None:
    assert WAKE_WORD == "艾达"
    assert contains_wake_word("你好艾达") is True


def test_device_pause_resume_playback_phrases_in_task_mode() -> None:
    """显式设备短语「暂停播报」「继续播报」仍走 dev_pause / dev_resume。"""
    sm = VoiceInputSessionManager()
    ev1 = sm.process_final_text("暂停播报", now=0.0, is_task_mode=True, session_id="s1")
    assert ev1.shortcut_id == "dev_pause"
    ev2 = sm.process_final_text("继续播报", now=1.0, is_task_mode=True, session_id="s1")
    assert ev2.shortcut_id == "dev_resume"
