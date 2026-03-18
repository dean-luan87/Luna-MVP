# -*- coding: utf-8 -*-
"""
主线 1.3B：短时预演容错（Predictive Hold）。

在视觉短时退化但运行域仍基本有效时，允许有限时间窗口内基于最近可信状态继续稳定解释；
超时或越界后必须进入恢复动作。规则型、保守、不做预测模型。
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from .schema import StateLayer, DecisionLayer

# 最大 hold 窗口（毫秒）
MAX_HOLD_MS = 1500.0
# 风险阈值：低于此才允许 hold
RISK_THRESHOLD = 0.5
# 默认恢复动作
DEFAULT_RECOVERY_ACTION = "recheck_environment"


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class PredictiveHold:
    """
    状态ful：记录是否在 hold 中及 hold 截止时间。
    仅当条件组 A/B/C 均满足时允许 hold；超时后强制恢复动作。
    """

    def __init__(self) -> None:
        self._hold_until_ts: Optional[float] = None  # 截止时间（unix s）
        self._in_hold: bool = False

    def evaluate(
        self,
        ctx: Dict[str, Any],
        state: StateLayer,
        decision: DecisionLayer,
    ) -> Dict[str, Any]:
        """
        在 state 连续化 + view_guard 之后调用；state 已含 view_misaligned、vision_degraded、vision_recovery_eta_ms、state_trend、risk_score 等。
        返回 7 个 predictive_hold 字段。
        """
        now = ctx.get("current_ts")
        if now is None:
            now = time.time()

        view_misaligned = _get(state, "view_misaligned")
        vision_degraded = _get(state, "vision_degraded")
        vision_recovery_eta_ms = _get(state, "vision_recovery_eta_ms")
        state_trend = _get(state, "state_trend")
        risk_score = _get(state, "risk_score")
        floor_forced = _get(decision, "floor_forced")
        escape_hatch = _get(decision, "escape_hatch_triggered")
        b2_applied = _get(decision, "b2_impact_applied")

        # 条件组 A：运行域基本正常
        if view_misaligned is True:
            self._exit_hold()
            return self._no_hold()
        if floor_forced is True or escape_hatch is True or b2_applied is True:
            self._exit_hold()
            return self._no_hold()

        # 条件组 B：视觉短时可恢复
        if vision_degraded is not True:
            self._exit_hold()
            return self._no_hold()
        eta_ms = float(vision_recovery_eta_ms) if vision_recovery_eta_ms is not None else 0.0
        if eta_ms <= 0 or eta_ms > MAX_HOLD_MS:
            self._exit_hold()
            return self._no_hold()

        # 条件组 C：最近状态稳定
        if state_trend != "stable":
            self._exit_hold()
            return self._no_hold()
        if risk_score is not None and float(risk_score) >= RISK_THRESHOLD:
            self._exit_hold()
            return self._no_hold()

        # 允许 hold
        allowed = True
        budget_ms = min(eta_ms, MAX_HOLD_MS)

        if not self._in_hold:
            self._in_hold = True
            self._hold_until_ts = now + budget_ms / 1000.0

        remaining_ms = (self._hold_until_ts - now) * 1000.0
        if remaining_ms <= 0:
            self._exit_hold()
            return {
                "predictive_hold_allowed": True,
                "predictive_hold_active": False,
                "predictive_hold_remaining_ms": 0.0,
                "predictive_hold_reason": "vision_short_degraded",
                "predictive_hold_confidence": 0.0,
                "predictive_hold_expired": True,
                "predictive_recovery_action": DEFAULT_RECOVERY_ACTION,
            }

        return {
            "predictive_hold_allowed": True,
            "predictive_hold_active": True,
            "predictive_hold_remaining_ms": round(remaining_ms, 1),
            "predictive_hold_reason": "vision_short_degraded",
            "predictive_hold_confidence": 0.8,
            "predictive_hold_expired": False,
            "predictive_recovery_action": DEFAULT_RECOVERY_ACTION,
        }

    def _exit_hold(self) -> None:
        self._in_hold = False
        self._hold_until_ts = None

    def _no_hold(self) -> Dict[str, Any]:
        return {
            "predictive_hold_allowed": False,
            "predictive_hold_active": False,
            "predictive_hold_remaining_ms": None,
            "predictive_hold_reason": None,
            "predictive_hold_confidence": None,
            "predictive_hold_expired": False,
            "predictive_recovery_action": None,
        }
