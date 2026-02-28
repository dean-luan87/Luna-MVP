# -*- coding: utf-8 -*-
"""
Phase4-MVP 调制器 v1：仅管 alpha。
极简窗口 risk_density_ema，输出 alpha_eff = clamp(alpha_base + lam * risk_density_ema, alpha_min, alpha_max)。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@dataclass
class ModulatorV1Params:
    lam: float = 0.10
    alpha_min: float = 0.55
    alpha_max: float = 0.80
    risk_density_alpha: float = 0.2  # EMA alpha for risk_density window


@dataclass
class ModulatorV1State:
    risk_density_ema: float = 0.0


class ModulatorV1:
    """单例状态：每 tick 更新 risk_density_ema，返回调制后 alpha_eff。"""

    def __init__(self, params: Optional[ModulatorV1Params] = None):
        self.params = params or ModulatorV1Params()
        self.state = ModulatorV1State()

    def get_alpha(
        self,
        alpha_base: float,
        signals: Any,
        state: Any = None,
        debug: Optional[Dict[str, Any]] = None,
    ) -> float:
        risk_raw = _clamp(getattr(signals, "risk_density", 0.0), 0.0, 1.0)
        a_ema = self.params.risk_density_alpha
        self.state.risk_density_ema = a_ema * risk_raw + (1.0 - a_ema) * self.state.risk_density_ema
        alpha_eff = _clamp(
            alpha_base + self.params.lam * self.state.risk_density_ema,
            self.params.alpha_min,
            self.params.alpha_max,
        )
        if isinstance(debug, dict):
            debug["mod.risk_density_ema"] = self.state.risk_density_ema
            debug["mod.alpha_eff"] = alpha_eff
        return alpha_eff

    def reset(self) -> None:
        self.state.risk_density_ema = 0.0
