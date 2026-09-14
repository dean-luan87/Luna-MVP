# -*- coding: utf-8 -*-
"""
唤醒与会话窗口管理：inactive / active_window / expired。

- 30s：会话窗口；有效输入刷新。
- 3s 切段由 VoiceSegmentTimeoutPolicy 单独描述，本类不计时音频静默。
"""

from __future__ import annotations

from enum import Enum
from typing import Optional


class WakeWindowState(str, Enum):
    inactive = "inactive"
    active_window = "active_window"
    expired = "expired"


DEFAULT_WINDOW_SEC = 30.0


class VoiceWakeWindowManager:
    """维护会话窗口状态与刷新时间。"""

    def __init__(self, window_sec: float = DEFAULT_WINDOW_SEC) -> None:
        self.window_sec = float(window_sec)
        self._state: WakeWindowState = WakeWindowState.inactive
        self._window_open_ts: float = 0.0
        self._last_refresh_ts: float = 0.0
        # capturing_input 期间挂起：不凭本计时器将窗口判过期（见 LUNA_VOICE_TIME_GOVERNANCE_V1）
        self._session_clock_suspended: bool = False

    @property
    def state(self) -> WakeWindowState:
        return self._state

    @property
    def session_clock_suspended(self) -> bool:
        return self._session_clock_suspended

    def is_window_active(self, now: float) -> bool:
        """当前时刻窗口是否仍有效（会按 30s 规则刷新过期）。"""
        self._reconcile(now)
        return self._state == WakeWindowState.active_window

    def suspend_session_clock(self) -> None:
        """正在接收一段输入时：会话窗口计时暂停裁决。"""
        self._session_clock_suspended = True

    def resume_session_clock(self) -> None:
        self._session_clock_suspended = False

    def reset_full_window_after_input(self, now: float) -> None:
        """
        一段输入结束后：全量重置为新的 window_sec（不续剩余时间）。
        inactive 时不强行开窗（无会话上下文）。
        """
        if self._state == WakeWindowState.inactive:
            return
        self._state = WakeWindowState.active_window
        self._window_open_ts = now
        self._last_refresh_ts = now

    def _reconcile(self, now: float) -> None:
        if self._session_clock_suspended:
            return
        if self._state != WakeWindowState.active_window:
            return
        if now - self._last_refresh_ts > self.window_sec:
            self._state = WakeWindowState.expired

    def open_or_refresh_on_wake(self, now: float) -> None:
        """唤醒成功：进入 active_window 并刷新计时。"""
        self._state = WakeWindowState.active_window
        self._window_open_ts = now
        self._last_refresh_ts = now

    def refresh_on_valid_input(self, now: float) -> None:
        """任意被路由接受的输入：刷新 30s。"""
        if self._state == WakeWindowState.active_window:
            self._last_refresh_ts = now

    def force_expire(self, now: float) -> None:
        """仅状态迁移（时间戳可选）。"""
        _ = now
        self._state = WakeWindowState.expired

    def clear_shutdown_or_standby(self) -> None:
        """关机 / 长待机 / 任务彻底结束等：清空窗口。"""
        self._state = WakeWindowState.inactive
        self._window_open_ts = 0.0
        self._last_refresh_ts = 0.0
        self._session_clock_suspended = False

    def clear_session_end(self) -> None:
        """用户显式结束对话：回到 inactive。"""
        self.clear_shutdown_or_standby()
