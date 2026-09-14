# -*- coding: utf-8 -*-
"""PAL v0 单元测试：视角门禁、EMA 平滑"""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from pal.v0 import compute_pal_horizon_difficulty, reset_pal_state


def test_view_gate_low_confidence():
    """视角门禁：view_confidence < 0.6 → 返回 0"""
    reset_pal_state()
    out = compute_pal_horizon_difficulty(
        motion=0.8, path=0.8, branch=0.8, roi=0.8,
        view_confidence=0.5,
    )
    assert out == 0.0


def test_view_gate_at_threshold():
    """view_confidence = 0.6 时通过门禁"""
    reset_pal_state()
    out = compute_pal_horizon_difficulty(
        motion=0.5, path=0.5, branch=0.5, roi=0.5,
        view_confidence=0.6,
    )
    assert 0 < out <= 1.0


def test_ema_smoothing():
    """EMA 平滑：高复杂后接低复杂，PAL 应平滑下降"""
    reset_pal_state()
    # 先喂高复杂
    for _ in range(5):
        compute_pal_horizon_difficulty(
            motion=0.9, path=0.9, branch=0.9, roi=0.9,
            view_confidence=0.9,
        )
    high = compute_pal_horizon_difficulty(
        motion=0.9, path=0.9, branch=0.9, roi=0.9,
        view_confidence=0.9,
    )
    # 再喂低复杂
    low = compute_pal_horizon_difficulty(
        motion=0.1, path=0.1, branch=0.1, roi=0.1,
        view_confidence=0.9,
    )
    assert high > low
    assert low > 0.1  # EMA 不会立刻掉到 0.1


def test_output_range():
    """输出始终在 [0, 1]"""
    reset_pal_state()
    for vc in [0.6, 0.8, 1.0]:
        out = compute_pal_horizon_difficulty(
            motion=0.5, path=0.5, branch=0.5, roi=0.5,
            view_confidence=vc,
        )
        assert 0 <= out <= 1.0
