# -*- coding: utf-8 -*-
"""
N) 从 Shadow → Real 的「灰度切换规则」v0

目标：不是"功能开关"，而是"资格晋升"
Shadow 不是为了证明系统聪明，而是为了证明它"不会出事"。
切换规则不可自动触发，只能由开发者或受控策略明确记录。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# v0 三道门阈值（冻结）
GATE1_MIN_RUNTIME_HOURS = 24
GATE1_MAX_SWITCHES_PER_MIN = 3.0
GATE2_ENGAGED_RATIO_LO = 0.03
GATE2_ENGAGED_RATIO_HI = 0.15
GATE2_L3_RATIO_MAX = 0.05
GATE2_FAIL_LOW_CONFIDENCE_MAX = 0.30
GATE3_FAIRNESS_BOOST_RATE_MAX = 0.4

# 灰度阶段（v0）
STAGE_SHADOW = "Shadow"
STAGE_REAL_L1 = "Real-L1"
STAGE_REAL_L2 = "Real-L2"
STAGE_REAL_L3 = "Real-L3"


def evaluate_gate1_stability(
    intervention_stats: Dict[str, Any],
    runtime_hours: float,
    has_crash: bool = False,
) -> Tuple[bool, str]:
    """
    门 1：稳定性门（硬）
    - Shadow 连续运行 ≥ 24 小时
    - 无 crash / 无 runaway
    - avg_switches_per_min < 3
    """
    if has_crash:
        return False, "CRASH_DETECTED"
    if runtime_hours < GATE1_MIN_RUNTIME_HOURS:
        return False, f"RUNTIME_INSUFFICIENT_{runtime_hours:.1f}h"
    switches = intervention_stats.get("avg_switches_per_min", 0)
    if switches >= GATE1_MAX_SWITCHES_PER_MIN:
        return False, f"SWITCHES_TOO_HIGH_{switches:.1f}"
    return True, "OK"


def evaluate_gate2_conservative(
    intervention_stats: Dict[str, Any],
    failure_stats: Dict[str, float],
) -> Tuple[bool, str]:
    """
    门 2：保守性门（结构）
    - engaged_ratio 在 3%–15%
    - L3_ratio < 5%
    - FAIL_LOW_CONFIDENCE 不高于 30%
    """
    eng_ratio = intervention_stats.get("engaged_ratio", 0)
    if eng_ratio < GATE2_ENGAGED_RATIO_LO or eng_ratio > GATE2_ENGAGED_RATIO_HI:
        return False, f"ENGAGED_RATIO_OUT_OF_RANGE_{eng_ratio:.2f}"
    level_dist = intervention_stats.get("level_dist", {})
    total_eng = sum(level_dist.values())
    l3_ratio = level_dist.get("L3", 0) / max(total_eng, 1)
    if l3_ratio >= GATE2_L3_RATIO_MAX:
        return False, f"L3_RATIO_TOO_HIGH_{l3_ratio:.2f}"
    fail_low = failure_stats.get("FAIL_LOW_CONFIDENCE", 0)
    if fail_low > GATE2_FAIL_LOW_CONFIDENCE_MAX:
        return False, f"FAIL_LOW_CONFIDENCE_TOO_HIGH_{fail_low:.2f}"
    return True, "OK"


def evaluate_gate3_structural_health(
    arbitration_diagnosis: Optional[Dict[str, Any]],
    arbitration_stats: Dict[str, Any],
) -> Tuple[bool, str]:
    """
    门 3：结构健康门（最重要）
    - 无 STRUCTURAL_STARVATION
    - 无长期 TYPE_DOMINANCE
    - fairness_boost_rate < 0.4
    """
    tag = (arbitration_diagnosis or {}).get("tag", "ARBITRATION_OK")
    if tag == "STRUCTURAL_STARVATION":
        return False, "STRUCTURAL_STARVATION"
    if tag == "TYPE_DOMINANCE":
        return False, "TYPE_DOMINANCE"
    fb_rate = arbitration_stats.get("fairness_boost_rate", 0)
    if fb_rate >= GATE3_FAIRNESS_BOOST_RATE_MAX:
        return False, f"FAIRNESS_BOOST_RATE_TOO_HIGH_{fb_rate:.2f}"
    return True, "OK"


def evaluate_all_gates(
    intervention_stats: Dict[str, Any],
    arbitration_stats: Dict[str, Any],
    failure_stats: Dict[str, float],
    arbitration_diagnosis: Optional[Dict[str, Any]],
    runtime_hours: float,
    has_crash: bool = False,
) -> Dict[str, Any]:
    """
    评估三道门，返回结果（不自动触发切换）。
    """
    g1_ok, g1_reason = evaluate_gate1_stability(intervention_stats, runtime_hours, has_crash)
    g2_ok, g2_reason = evaluate_gate2_conservative(intervention_stats, failure_stats)
    g3_ok, g3_reason = evaluate_gate3_structural_health(arbitration_diagnosis, arbitration_stats)

    all_ok = g1_ok and g2_ok and g3_ok
    return {
        "gate1_stability": {"passed": g1_ok, "reason": g1_reason},
        "gate2_conservative": {"passed": g2_ok, "reason": g2_reason},
        "gate3_structural_health": {"passed": g3_ok, "reason": g3_reason},
        "all_passed": all_ok,
        "eligible_for_promotion": all_ok,
        "apply_now": False,  # 永不自动触发
    }


def get_stage_behavior(stage: str) -> str:
    """灰度阶段对应的行为描述"""
    return {
        STAGE_SHADOW: "全算不说",
        STAGE_REAL_L1: "只允许 L1",
        STAGE_REAL_L2: "允许 L1+L2",
        STAGE_REAL_L3: "全部",
    }.get(stage, "UNKNOWN")
