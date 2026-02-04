# -*- coding: utf-8 -*-
"""
E) ACTIVE × Advice「内容类型节律」v0

把 Advice 看成"类别配额系统"，不是即时触发器。
ENGAGED ≠ 所有 Advice 都放行
ENGAGED = 在一个时间窗内，允许哪些类别出现、出现多少

不改 AdviceEngine，不反推文本，只是 允许/不允许这次说。
"""

from __future__ import annotations

import time
from collections import deque
from typing import Any, Dict, Literal, Optional, Tuple

# v0 固定集合（与 advice/schema 的 category 对应）
NAVIGATION_HINT = "NAVIGATION_HINT"
ENV_AWARENESS = "ENV_AWARENESS"
SAFETY_REMINDER = "SAFETY_REMINDER"
TASK_STATE = "TASK_STATE"

# v0 配额表：每 30s 最大次数
QUOTA: Dict[str, float] = {
    NAVIGATION_HINT: 2,
    ENV_AWARENESS: 2,
    TASK_STATE: 1,
    SAFETY_REMINDER: float("inf"),
}

WINDOW_SEC = 30.0

# 将 advice_category 映射到 v0 类型（兼容已有 AdviceEngine 输出）
CATEGORY_MAP: Dict[str, str] = {
    "TASK_STATE": TASK_STATE,
    "NAVIGATION_HINT": NAVIGATION_HINT,
    "ENV_AWARENESS": ENV_AWARENESS,
    "SAFETY_REMINDER": SAFETY_REMINDER,
    "REMINDER_FREQUENCY": ENV_AWARENESS,
}


def normalize_advice_type(advice_category: Optional[str], is_safety: bool = False) -> str:
    """将 advice_category 归一化为 v0 类型。"""
    if is_safety:
        return SAFETY_REMINDER
    if advice_category and advice_category in CATEGORY_MAP:
        return CATEGORY_MAP[advice_category]
    return TASK_STATE


def advice_type_gate(advice_type: str, window_stats: Dict[str, int]) -> Tuple[bool, str]:
    """
    放行规则（只读 gate）。

    Args:
        advice_type: 归一化后的 v0 类型
        window_stats: 滑窗内各类型已播报次数 {type: count}

    Returns:
        (allowed, reason)
    """
    if advice_type == SAFETY_REMINDER:
        return True, "OK"
    quota = QUOTA.get(advice_type, 1)
    count = window_stats.get(advice_type, 0)
    if count >= quota:
        return False, "QUOTA_EXCEEDED"
    return True, "OK"


class AdviceRhythmV0:
    """
    内容类型节律 v0：30s 滑窗 + 配额。
    """

    def __init__(self, window_sec: float = WINDOW_SEC):
        self.window_sec = window_sec
        self._events: deque = deque()  # (ts, advice_type)

    def _prune(self, now: float) -> None:
        cutoff = now - self.window_sec
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def window_stats(self, now: Optional[float] = None) -> Dict[str, int]:
        """滑窗内各类型已播报次数。"""
        now = now or time.time()
        self._prune(now)
        stats: Dict[str, int] = {}
        for _, t in self._events:
            stats[t] = stats.get(t, 0) + 1
        return stats

    def record_spoken(self, advice_type: str, now: Optional[float] = None) -> None:
        """记录一次已播报。"""
        now = now or time.time()
        self._prune(now)
        self._events.append((now, advice_type))

    def check(
        self,
        advice_category: Optional[str],
        is_safety: bool = False,
        now: Optional[float] = None,
    ) -> Tuple[bool, str, str, Dict[str, Any]]:
        """
        检查是否允许播报，并返回 trace 用的 advice_rhythm 结构。

        Returns:
            (allowed, reason, advice_type, advice_rhythm_dict)
        """
        now = now or time.time()
        advice_type = normalize_advice_type(advice_category, is_safety)
        stats = self.window_stats(now)
        allowed, reason = advice_type_gate(advice_type, stats)
        trace = {
            "allowed": allowed,
            "reason": reason,
            "type": advice_type,
        }
        return allowed, reason, advice_type, trace


_instance: Optional[AdviceRhythmV0] = None


def get_advice_rhythm_v0() -> AdviceRhythmV0:
    global _instance
    if _instance is None:
        _instance = AdviceRhythmV0()
    return _instance


def reset_advice_rhythm_state() -> None:
    global _instance
    _instance = None
