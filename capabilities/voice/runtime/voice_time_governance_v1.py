# -*- coding: utf-8 -*-
"""
语音时间治理 v1：三套计时器分离 + 四态运行态。

- SilenceEndTimer：静默 ≥3s → 当前输入结束（与 30s 会话无关）
- SessionWindowTimer：由 VoiceWakeWindowManager 实现；capturing_input 时挂起
- InputCaptureTimer：单次接收最长 90s，80s 提示（可占位）

详见 docs/architecture/voice/LUNA_VOICE_TIME_GOVERNANCE_V1.md
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from capabilities.voice.runtime.voice_segment_timeout_policy import (
    DEFAULT_SEGMENT_END_SILENCE_SEC,
    VoiceSegmentTimeoutPolicy,
)
from capabilities.voice.runtime.voice_wake_window_manager import VoiceWakeWindowManager

# —— 固定口径（与产品一致）——
DEFAULT_SESSION_WINDOW_SEC = 30.0
DEFAULT_MAX_CAPTURE_SEC = 90.0
DEFAULT_WARN_CAPTURE_SEC = 80.0


class VoiceRuntimePhase(str, Enum):
    """语音输入运行态（可观察、可记录）。"""

    idle = "idle"
    session_open = "session_open"
    capturing_input = "capturing_input"
    processing_after_input = "processing_after_input"


class CutoffReason(str, Enum):
    """收口原因（字符串值写入事件/元数据）。"""

    none = ""
    max_capture_duration = "max_capture_duration"
    silence = "silence"


@dataclass
class GovernanceTickResult:
    """tick_capturing 的可观察输出。"""

    segment_end_silence: bool = False
    warn_capture_80: bool = False
    force_capture_90: bool = False


class SilenceEndTimer:
    """静默结束判定（委托 VoiceSegmentTimeoutPolicy，语义独立命名）。"""

    def __init__(self, silence_sec: float = DEFAULT_SEGMENT_END_SILENCE_SEC) -> None:
        self._policy = VoiceSegmentTimeoutPolicy(segment_end_silence_sec=silence_sec)

    @property
    def silence_sec(self) -> float:
        return self._policy.segment_end_silence_sec

    def is_segment_end(self, silence_duration_sec: float) -> bool:
        return self._policy.is_segment_end(silence_duration_sec)


class InputCaptureTimer:
    """单次长语音接收上限：80s 提示、90s 强切。"""

    def __init__(
        self,
        *,
        warn_sec: float = DEFAULT_WARN_CAPTURE_SEC,
        max_sec: float = DEFAULT_MAX_CAPTURE_SEC,
    ) -> None:
        self.warn_sec = float(warn_sec)
        self.max_sec = float(max_sec)

    def should_warn(self, capture_duration_sec: float, *, warn_emitted: bool) -> bool:
        return (
            not warn_emitted
            and capture_duration_sec >= self.warn_sec
            and capture_duration_sec < self.max_sec
        )

    def should_force_cutoff(self, capture_duration_sec: float) -> bool:
        return capture_duration_sec >= self.max_sec


class VoiceTimeGovernanceRuntime:
    """
    串联会话窗口与「输入态」四态；capturing_input 期间会话时钟挂起。

    ASR/采集层应调用：
    - on_capture_started：开始接收一段输入
    - tick_capturing：推进静默/长语音上限
    VoiceInputSessionManager 在 process_final_text 前后调用：
    - on_before_process_final_text / on_after_process_final_text
    """

    def __init__(
        self,
        *,
        window: Optional[VoiceWakeWindowManager] = None,
        silence_timer: Optional[SilenceEndTimer] = None,
        capture_timer: Optional[InputCaptureTimer] = None,
    ) -> None:
        self.window = window or VoiceWakeWindowManager(window_sec=DEFAULT_SESSION_WINDOW_SEC)
        self.silence_timer = silence_timer or SilenceEndTimer()
        self.capture_timer = capture_timer or InputCaptureTimer()
        self.phase: VoiceRuntimePhase = VoiceRuntimePhase.idle
        self._capture_start_ts: Optional[float] = None
        self._warn_80_emitted: bool = False

    @property
    def capture_started_ts(self) -> Optional[float]:
        return self._capture_start_ts

    @property
    def session_window_suspended(self) -> bool:
        return self.window.session_clock_suspended

    def is_window_active_for_routing(self, now: float) -> bool:
        """路由用：会话窗口是否仍有效；过期时同步 idle。"""
        active = self.window.is_window_active(now)
        if not active and self.phase == VoiceRuntimePhase.session_open:
            self.phase = VoiceRuntimePhase.idle
        return active

    # —— 会话与路由侧 —— #

    def on_wake_route_accept(self, now: float) -> None:
        self.window.open_or_refresh_on_wake(now)
        self.phase = VoiceRuntimePhase.session_open

    def on_valid_input_route_accept(self, now: float) -> None:
        self.window.refresh_on_valid_input(now)
        self.phase = VoiceRuntimePhase.session_open

    def on_session_end_clear(self) -> None:
        self.window.clear_session_end()
        self._reset_capture_state()
        self.phase = VoiceRuntimePhase.idle

    def on_shutdown(self) -> None:
        self.window.clear_shutdown_or_standby()
        self._reset_capture_state()
        self.phase = VoiceRuntimePhase.idle

    def on_capture_started(self, now: float) -> None:
        """进入 capturing_input：挂起 30s 会话时钟（不裁决）。"""
        if self.phase == VoiceRuntimePhase.idle and not self.window.is_window_active(now):
            return
        self.window.suspend_session_clock()
        self.phase = VoiceRuntimePhase.capturing_input
        self._capture_start_ts = now
        self._warn_80_emitted = False

    def tick_capturing(
        self,
        now: float,
        *,
        silence_duration_sec: float,
        capture_duration_sec: Optional[float] = None,
    ) -> GovernanceTickResult:
        """
        仅在 capturing_input 下由上游周期调用。
        capture_duration_sec 若省略，用 now - _capture_start_ts。
        """
        if self.phase != VoiceRuntimePhase.capturing_input:
            return GovernanceTickResult()
        cap = capture_duration_sec
        if cap is None and self._capture_start_ts is not None:
            cap = now - self._capture_start_ts
        elif cap is None:
            cap = 0.0

        if self.capture_timer.should_force_cutoff(cap):
            return GovernanceTickResult(force_capture_90=True)

        if self.silence_timer.is_segment_end(silence_duration_sec):
            return GovernanceTickResult(segment_end_silence=True)

        if self.capture_timer.should_warn(cap, warn_emitted=self._warn_80_emitted):
            self._warn_80_emitted = True
            return GovernanceTickResult(warn_capture_80=True)

        return GovernanceTickResult()

    def on_before_process_final_text(self, now: float) -> None:
        """一句将送入路由前：若仍在采集态，先收口并全量重置 30s 窗口。"""
        if self.phase != VoiceRuntimePhase.capturing_input:
            return
        self._finalize_capture_segment(now)

    def on_after_process_final_text(self, now: float) -> None:
        _ = now
        if self.phase == VoiceRuntimePhase.processing_after_input:
            self.phase = VoiceRuntimePhase.session_open

    def _finalize_capture_segment(self, now: float) -> None:
        self.window.resume_session_clock()
        self.window.reset_full_window_after_input(now)
        self._capture_start_ts = None
        self._warn_80_emitted = False
        self.phase = VoiceRuntimePhase.processing_after_input

    def _reset_capture_state(self) -> None:
        self._capture_start_ts = None
        self._warn_80_emitted = False
        self.window.resume_session_clock()
