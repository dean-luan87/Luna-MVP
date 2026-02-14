# -*- coding: utf-8 -*-
"""
D1 可调参数范围表（仅 Layer0 weights）。
与 a3/config.py A3Weights 默认值对齐；范围 [0.5x_default, 2.0x_default]。
不可动：阈值、smoothing、hysteresis、lookahead policy。
"""
from typing import Dict, Tuple

# 默认值（与 a3.config.A3Weights 一致）
D1_WEIGHTS_DEFAULTS: Dict[str, float] = {
    "weights.risk_density": 0.30,
    "weights.redline_hit": 0.25,
    "weights.occlusion_ratio": 0.12,
    "weights.roi_load": 0.20,
    "weights.path_instability": 0.30,
    "weights.motion_instability": 0.30,
    "weights.branch_load": 0.20,
    "weights.speak_pressure": 0.05,
    "weights.reject_pressure": 0.03,
}

# (min, max) 绝对范围；第一版用 0.5x ~ 2.0x default
def _bounds(default: float) -> Tuple[float, float]:
    return (round(default * 0.5, 4), round(default * 2.0, 4))

D1_WEIGHTS_BOUNDS: Dict[str, Tuple[float, float]] = {
    k: _bounds(v) for k, v in D1_WEIGHTS_DEFAULTS.items()
}

# 用于 Candidate Generator 的键序（稳定 JSON 输出）
D1_WEIGHTS_KEYS = list(D1_WEIGHTS_DEFAULTS.keys())
