# -*- coding: utf-8 -*-
"""
ConversationWindowState (Stage-1 placeholder).

规则：首次唤醒建立窗口；有效交互刷新；超时/长待机/关机失效。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConversationWindowState:
    window_sec: float = 30.0
    active: bool = False
    window_start_ts: float = 0.0
    last_refresh_ts: float = 0.0

