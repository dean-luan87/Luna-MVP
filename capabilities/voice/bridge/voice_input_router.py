# -*- coding: utf-8 -*-
"""
语音输入路由（v1）：三入口 — 唤醒词 / 会话窗口内 / 任务态白名单。

不裁决主链；只产出路由决策，供会话协调器组装 VoiceInputEvent。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutEntry, VoiceShortcutRegistry

# v1 固定唤醒词（中文）
WAKE_WORD = "艾达"


def normalize_for_match(text: str) -> str:
    return (text or "").strip()


def contains_wake_word(text: str) -> bool:
    return WAKE_WORD in normalize_for_match(text)


def strip_wake_word(text: str) -> str:
    t = normalize_for_match(text)
    if WAKE_WORD in t:
        t = t.replace(WAKE_WORD, "", 1).strip()
        # 去掉常见逗号
        if t.startswith("，"):
            t = t[1:].strip()
        if t.startswith(","):
            t = t[1:].strip()
    return t


@dataclass(frozen=True)
class VoiceInputRouteDecision:
    """路由结果。"""

    decision: str  # accept | reject
    reject_reason: Optional[str] = None
    wake_word_detected: bool = False
    wake_word_stripped: str = ""
    shortcut: Optional[VoiceShortcutEntry] = None
    # 细分 reject
    reason_code: str = ""  # no_wake_no_window | not_whitelisted_normal | empty


def route_voice_text(
    raw_text: str,
    *,
    now: float,
    window_active: bool,
    is_task_mode: bool,
    registry: VoiceShortcutRegistry,
) -> VoiceInputRouteDecision:
    """
    三入口规则：
    1) 含「艾达」→ accept（唤醒词入口），并 strip
    2) 任务态 + 白名单命中 → accept（任务短指令入口），无需唤醒
    3) 会话窗口 active → accept（窗口内连续输入）
    否则 → reject
    """
    _ = now
    t = normalize_for_match(raw_text)
    if not t:
        return VoiceInputRouteDecision("reject", reject_reason="empty", reason_code="empty")

    if contains_wake_word(t):
        stripped = strip_wake_word(t)
        # 唤醒后正文仍可命中白名单（如「艾达，开始导航去医院」→ task_start_nav）
        sc_wake = registry.match(stripped, is_task_mode=is_task_mode) if stripped else None
        return VoiceInputRouteDecision(
            "accept",
            wake_word_detected=True,
            wake_word_stripped=stripped,
            shortcut=sc_wake,
            reason_code="wake_word",
        )

    sc = registry.match(t, is_task_mode=is_task_mode)
    if is_task_mode and sc is not None:
        return VoiceInputRouteDecision(
            "accept",
            shortcut=sc,
            reason_code="task_shortcut",
        )

    if window_active:
        return VoiceInputRouteDecision("accept", reason_code="active_window")

    # 普通态未唤醒：仅允许已在白名单且 allowed_in_normal_mode 的短语（由 registry.match 在 is_task_mode=False 时过滤）
    sc2 = registry.match(t, is_task_mode=False)
    if sc2 is not None:
        return VoiceInputRouteDecision("accept", shortcut=sc2, reason_code="normal_whitelist")

    return VoiceInputRouteDecision(
        "reject",
        reject_reason="需要唤醒词「艾达」或任务态白名单短指令",
        reason_code="no_wake_no_window",
    )
