# -*- coding: utf-8 -*-
"""
ENGAGED 介入强度 v0：在 ENGAGED 内细化为 L1/L2/L3

目标：把介入从「开/关」细化为强度等级，输出给下游做参数调制。
不决定说什么，只决定介入强度等级和频率预算。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class EngagementOutput:
    level: str = "L0"
    advice_scale: float = 0.0
    pal_lookahead_m: float = 0.0
    speak_cooldown_s: float = 0.0


class EngagementV0:
    """
    介入强度 v0：仅在 rhythm.state==ENGAGED 时计算 L1/L2/L3。
    升级立即生效，降级需连续 2 个窗口满足。
    """

    def __init__(self) -> None:
        self._level = "L0"
        self._down_counter = 0

    def _params(self, level: str) -> tuple[float, float, float]:
        return {
            "L1": (0.7, 8.0, 8.0),
            "L2": (0.85, 12.0, 6.0),
            "L3": (1.0, 18.0, 4.0),
        }.get(level, (0.0, 0.0, 0.0))

    def tick(
        self,
        *,
        rhythm_state: str,
        pal: float,
        complexity: float,
        vc: float,
        control_mode: str,
    ) -> EngagementOutput:
        # 非 ENGAGED
        if rhythm_state != "ENGAGED":
            self._level = "L0"
            self._down_counter = 0
            return EngagementOutput()

        # 目标级别计算（L1 默认，L2/L3 升级）
        target = "L1"
        if pal >= 0.35 or complexity >= 0.60:
            target = "L2"
        if (
            pal >= 0.50
            and complexity >= 0.75
            and vc >= 0.75
            and control_mode != "GUARDED"
        ):
            target = "L3"

        # 防抖：升级立即，降级需连续 2 个窗口
        if target > self._level:
            self._level = target
            self._down_counter = 0
        elif target < self._level:
            self._down_counter += 1
            if self._down_counter >= 2:
                self._level = target
                self._down_counter = 0
        else:
            self._down_counter = 0

        scale, look, cd = self._params(self._level)
        return EngagementOutput(
            level=self._level,
            advice_scale=scale,
            pal_lookahead_m=look,
            speak_cooldown_s=cd,
        )

    def reset(self) -> None:
        """重置状态（用于测试）"""
        self._level = "L0"
        self._down_counter = 0


_ENGAGEMENT: Optional[EngagementV0] = None


def get_engagement_v0() -> EngagementV0:
    global _ENGAGEMENT
    if _ENGAGEMENT is None:
        _ENGAGEMENT = EngagementV0()
    return _ENGAGEMENT


def reset_engagement_state() -> None:
    """重置介入强度状态（用于测试）"""
    global _ENGAGEMENT
    if _ENGAGEMENT is not None:
        _ENGAGEMENT.reset()
