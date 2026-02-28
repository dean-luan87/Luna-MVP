# -*- coding: utf-8 -*-
"""
A3 Deterministic Decision v2 (Stage 2) - Fixed-point single source of truth.

All branch comparisons affecting safety_level, control_mode, advice_budget_scale,
allowed/QUOTA_EXCEEDED, record_spoken must be performed in integer domain.
Floating-point exists only as shadow for observability/debug.

Rounding: round half away from zero (symmetric rounding).
"""
from __future__ import annotations

import math
import os
from typing import Optional

# 3 decimals fixed-point
SCORE_SCALE = 1000
# Alpha for EMA: same scale (0.25 -> 250)
ALPHA_SCALE = 1000
# 抵消二进制浮点表示误差，避免 0.5000000000001 等边界抖动（跨平台一致性）
_Q_EPS = 1e-12


def _use_fixedpoint() -> bool:
    """Feature flag: A3_FIXEDPOINT=0/1 (default 1 for determinism)."""
    return os.environ.get("A3_FIXEDPOINT", "1") == "1"


def q(x: float, scale: int = SCORE_SCALE) -> int:
    """
    Quantize float to fixed-point int.
    Round half away from zero (e.g. 0.5 -> 1, -0.5 -> -1).
    使用 epsilon 消除浮点二进制表示误差，保证跨平台/跨机器一致性。
    """
    if not math.isfinite(x):
        return 0
    scaled = x * scale
    if scaled >= 0:
        return int(math.floor(scaled + 0.5 + _Q_EPS))
    return int(math.ceil(scaled - 0.5 - _Q_EPS))


def dq(i: int, scale: int = SCORE_SCALE) -> float:
    """Dequantize fixed-point int to float."""
    return i / scale


def clamp_i(v: int, lo: int, hi: int) -> int:
    """Clamp integer to [lo, hi]."""
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def ema_step_i(prev_q: int, x_q: int, alpha_q: int, scale: int = SCORE_SCALE) -> int:
    """
    EMA in integer domain: ema = prev + alpha*(x - prev).
    alpha_q in [0, scale] (e.g. 250 for 0.25).
    Returns new ema_q in [0, scale] (clamped).
    """
    # prev + (alpha_q * (x_q - prev)) / scale
    diff = x_q - prev_q
    delta = (alpha_q * diff) // scale
    out = prev_q + delta
    return clamp_i(out, 0, scale)


def view_conf_gate_q(view_conf_q: int, floor_q: int, k: float, scale: int = SCORE_SCALE) -> int:
    """
    B2 gate in fixed-point: floor + (1-floor)*view_conf^k.
    view_conf_q, floor_q in [0, scale]. Returns gate value in [0, scale].
    """
    if view_conf_q <= 0:
        return floor_q
    if view_conf_q >= scale:
        return scale
    vc = view_conf_q / scale
    gate_float = (floor_q / scale) + (1.0 - floor_q / scale) * (vc ** k)
    return clamp_i(q(gate_float, scale), 0, scale)
