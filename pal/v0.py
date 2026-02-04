# -*- coding: utf-8 -*-
"""
PAL v0（Predictive Attention Lookahead）：只读前瞻

唯一使命：回答一个问题
「如果继续往前走，前方 3–5 秒的空间复杂度是否会显著上升？」

v0 只观测、不决策、不触发行为。
"""

from __future__ import annotations

from typing import Any


class EMA:
    """指数移动平均"""

    def __init__(self, alpha: float):
        self.alpha = alpha
        self.value: float | None = None

    def update(self, x: float) -> float:
        if self.value is None:
            self.value = x
        else:
            self.value = self.alpha * x + (1.0 - self.alpha) * self.value
        return self.value

    def reset(self) -> None:
        self.value = None


class PALv0:
    """PAL v0：只读前瞻，EMA 平滑 + 视角门禁"""

    def __init__(self, alpha: float = 0.4, vc_gate: float = 0.6):
        self.ema = EMA(alpha)
        self.vc_gate = vc_gate

    def compute(self, signals: Any, view_confidence: float) -> float:
        if view_confidence < self.vc_gate:
            return 0.0

        motion = max(0.0, min(1.0, getattr(signals, "motion_instability", 0.0)))
        path = max(0.0, min(1.0, getattr(signals, "path_instability", 0.0)))
        branch = max(0.0, min(1.0, getattr(signals, "branch_load", 0.0)))
        roi = max(0.0, min(1.0, getattr(signals, "roi_load", 0.0)))

        base = 0.4 * motion + 0.3 * path + 0.2 * branch + 0.1 * roi
        base = max(0.0, min(1.0, base))

        return max(0.0, min(1.0, self.ema.update(base)))

    def reset(self) -> None:
        self.ema.reset()


# 全局单例（跨 tick 持久化）
_PALv0: PALv0 | None = None


def get_pal_v0() -> PALv0:
    global _PALv0
    if _PALv0 is None:
        _PALv0 = PALv0(alpha=0.4, vc_gate=0.6)
    return _PALv0


def compute_pal_horizon_difficulty(
    motion: float,
    path: float,
    branch: float,
    roi: float,
    view_confidence: float,
) -> float:
    """
    计算 PAL 前瞻难度（v0）。兼容函数式调用。
    """
    from types import SimpleNamespace
    s = SimpleNamespace(
        motion_instability=motion,
        path_instability=path,
        branch_load=branch,
        roi_load=roi,
    )
    return get_pal_v0().compute(s, view_confidence)


def reset_pal_state() -> None:
    """重置 PAL 状态（用于测试或新会话）"""
    global _PALv0
    if _PALv0 is not None:
        _PALv0.reset()
