# -*- coding: utf-8 -*-
"""N) Shadow → Real 灰度切换规则 v0 单元测试"""

import pytest

from intervention.shadow_to_real_v0 import (
    evaluate_gate1_stability,
    evaluate_gate2_conservative,
    evaluate_gate3_structural_health,
    evaluate_all_gates,
    get_stage_behavior,
    STAGE_SHADOW,
    STAGE_REAL_L1,
    STAGE_REAL_L2,
    STAGE_REAL_L3,
)


def test_gate1_stability_pass():
    stats = {"avg_switches_per_min": 1.5}
    ok, reason = evaluate_gate1_stability(stats, runtime_hours=25, has_crash=False)
    assert ok is True
    assert reason == "OK"


def test_gate1_stability_fail_runtime():
    stats = {"avg_switches_per_min": 1.0}
    ok, reason = evaluate_gate1_stability(stats, runtime_hours=10, has_crash=False)
    assert ok is False
    assert "RUNTIME" in reason


def test_gate1_stability_fail_switches():
    stats = {"avg_switches_per_min": 5.0}
    ok, reason = evaluate_gate1_stability(stats, runtime_hours=25, has_crash=False)
    assert ok is False
    assert "SWITCHES" in reason


def test_gate2_conservative_pass():
    int_stats = {"engaged_ratio": 0.08, "level_dist": {"L1": 50, "L2": 30, "L3": 2}}
    fail_stats = {"FAIL_LOW_CONFIDENCE": 0.15}
    ok, reason = evaluate_gate2_conservative(int_stats, fail_stats)
    assert ok is True
    assert reason == "OK"


def test_gate2_conservative_fail_engaged_ratio():
    int_stats = {"engaged_ratio": 0.25, "level_dist": {"L1": 10, "L2": 5, "L3": 0}}
    fail_stats = {}
    ok, reason = evaluate_gate2_conservative(int_stats, fail_stats)
    assert ok is False
    assert "ENGAGED_RATIO" in reason


def test_gate3_structural_health_pass():
    arb_diag = {"tag": "ARBITRATION_OK"}
    arb_stats = {"fairness_boost_rate": 0.2}
    ok, reason = evaluate_gate3_structural_health(arb_diag, arb_stats)
    assert ok is True
    assert reason == "OK"


def test_gate3_structural_health_fail_starvation():
    arb_diag = {"tag": "STRUCTURAL_STARVATION"}
    arb_stats = {"fairness_boost_rate": 0.1}
    ok, reason = evaluate_gate3_structural_health(arb_diag, arb_stats)
    assert ok is False
    assert reason == "STRUCTURAL_STARVATION"


def test_evaluate_all_gates():
    int_stats = {"engaged_ratio": 0.08, "level_dist": {"L1": 50, "L2": 30, "L3": 2}, "avg_switches_per_min": 1.5}
    arb_stats = {"fairness_boost_rate": 0.2, "winner_type_dist": {}}
    fail_stats = {"FAIL_LOW_CONFIDENCE": 0.15}
    arb_diag = {"tag": "ARBITRATION_OK"}
    result = evaluate_all_gates(int_stats, arb_stats, fail_stats, arb_diag, runtime_hours=25, has_crash=False)
    assert result["all_passed"] is True
    assert result["eligible_for_promotion"] is True
    assert result["apply_now"] is False


def test_get_stage_behavior():
    assert get_stage_behavior(STAGE_SHADOW) == "全算不说"
    assert get_stage_behavior(STAGE_REAL_L1) == "只允许 L1"
    assert get_stage_behavior(STAGE_REAL_L2) == "允许 L1+L2"
    assert get_stage_behavior("UNKNOWN") == "UNKNOWN"
