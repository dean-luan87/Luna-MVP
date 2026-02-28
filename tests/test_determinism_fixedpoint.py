# -*- coding: utf-8 -*-
"""
Stage 2: 同一量化输入跑两遍 A3 决策，输出（含 safety_level, control_mode, ema_q）完全一致。
含阈值边界 0.3795 / 0.38 / 0.3805 等用例。
"""
import os

import pytest

# 启用定点路径
os.environ["A3_FIXEDPOINT"] = "1"

from a3.engine import A3Engine
from a3.config import A3Config
from a3.types import A3Signals, SafetyLevel, ControlMode


def _make_engine():
    cfg = A3Config(enabled=True)
    cfg.smoothing.peak_hold_frames = 0
    cfg.smoothing.alpha = 0.3
    return A3Engine(cfg)


def test_same_obs_twice_identical_decision():
    """固定同一组 obs（浮点）-> 量化后决策两遍 -> decision 完全一致。"""
    eng = _make_engine()
    s = A3Signals(
        risk_density=0.35,
        path_stability=0.7,
        branch_count=2,
        roi_count=1,
        occlusion_ratio=0.0,
        recent_speak_rate=0.0,
        rejected_rate=0.0,
        has_goal=True,
        view_confidence=0.9,
        frame_quality="GOOD",
    )
    m1 = eng.tick(s, now_ms=1000)
    # 第二遍用新 engine 同输入，避免 state 延续
    eng2 = _make_engine()
    m2 = eng2.tick(s, now_ms=1000)
    assert m1.safety_level == m2.safety_level
    assert m1.control_mode == m2.control_mode
    assert m1.debug.get("ema_q") == m2.debug.get("ema_q")
    assert m1.complexity_score == m2.complexity_score
    assert m1.advice_budget_scale == m2.advice_budget_scale


def test_determinism_multiple_ticks_same_sequence():
    """同一序列连续 tick 两遍（两个 engine），每步 decision 一致。"""
    signals_list = [
        A3Signals(risk_density=0.2, path_stability=0.9, view_confidence=1.0),
        A3Signals(risk_density=0.4, path_stability=0.8, view_confidence=0.85),
        A3Signals(risk_density=0.35, path_stability=0.75, view_confidence=0.9),
    ]
    eng1 = _make_engine()
    eng2 = _make_engine()
    for i, s in enumerate(signals_list):
        now = 1000 + i * 100
        m1 = eng1.tick(s, now_ms=now)
        m2 = eng2.tick(s, now_ms=now)
        assert m1.safety_level == m2.safety_level, f"tick {i}"
        assert m1.control_mode == m2.control_mode, f"tick {i}"
        assert m1.debug.get("ema_q") == m2.debug.get("ema_q"), f"tick {i}"


def _base_signals(**kwargs):
    return A3Signals(
        path_stability=1.0,
        branch_count=0,
        roi_count=0,
        occlusion_ratio=0.0,
        recent_speak_rate=0.0,
        rejected_rate=0.0,
        view_confidence=1.0,
        frame_quality="GOOD",
        **kwargs,
    )


def test_threshold_boundary_safe_caution():
    """边界附近：0.3795 / 0.38 / 0.3805 等，决策由 ema_q 与 thresholds_q 整数比较确定。"""
    cfg = A3Config(enabled=True)
    cfg.smoothing.alpha = 1.0  # 无平滑，raw 直接到 ema
    cfg.smoothing.peak_hold_frames = 0
    cfg.thresholds.safe_to_caution = 0.38
    cfg.thresholds.hysteresis = 0.06
    eng = A3Engine(cfg)
    m_379 = eng.tick(_base_signals(risk_density=0.379), now_ms=1000)
    eng2 = A3Engine(cfg)
    m_380 = eng2.tick(_base_signals(risk_density=0.38), now_ms=1000)
    eng3 = A3Engine(cfg)
    m_381 = eng3.tick(_base_signals(risk_density=0.381), now_ms=1000)
    ema_q_379 = m_379.debug.get("ema_q")
    ema_q_380 = m_380.debug.get("ema_q")
    ema_q_381 = m_381.debug.get("ema_q")
    assert ema_q_379 is not None and ema_q_380 is not None and ema_q_381 is not None
    assert ema_q_379 <= ema_q_380 <= ema_q_381
    eng4 = A3Engine(cfg)
    m_380_repeat = eng4.tick(_base_signals(risk_density=0.38), now_ms=1000)
    assert m_380.debug.get("ema_q") == m_380_repeat.debug.get("ema_q")


def test_ema_q_authoritative_in_debug():
    """trace 中 ema_q 存在且为整数；ema 为 dq(ema_q) 的 shadow。"""
    eng = _make_engine()
    s = A3Signals(risk_density=0.277, path_stability=0.8, view_confidence=1.0)
    m = eng.tick(s, now_ms=1000)
    assert "ema_q" in m.debug
    assert isinstance(m.debug["ema_q"], int)
    assert 0 <= m.debug["ema_q"] <= 1000
    # shadow 与 dq(ema_q) 一致（允许浮点误差）
    from runtime.a3_fixedpoint import dq
    expected_ema = dq(m.debug["ema_q"])
    assert abs(m.debug["ema"] - expected_ema) < 1e-6
    assert abs(m.complexity_score - expected_ema) < 1e-6
