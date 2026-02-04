# -*- coding: utf-8 -*-
"""
ENGAGED 介入强度 → AdviceBudget 只读调制

原则：不改 AdviceBudget 决策逻辑，只在预算计算处乘系数。
ENGAGED 之外无影响（engagement 为空或 L0 时行为不变）。
"""

from __future__ import annotations

from typing import Any, Dict, Optional


def get_effective_advice_scale(base_scale: float, engagement: Optional[Dict[str, Any]]) -> float:
    """
    非 ENGAGED（L0 或空）：返回 base_scale，行为不变。
    ENGAGED：返回 base_scale * engagement.advice_scale
    """
    if not engagement or engagement.get("level", "L0") == "L0":
        return base_scale
    scale = engagement.get("advice_scale", 1.0)
    return base_scale * scale


def get_effective_speak_cooldown_s(
    base_cooldown_s: float, engagement: Optional[Dict[str, Any]]
) -> float:
    """
    非 ENGAGED（L0 或空）：返回 base_cooldown_s，行为不变。
    ENGAGED：返回 engagement.speak_cooldown_s（覆盖 base）
    """
    if not engagement or engagement.get("level", "L0") == "L0":
        return base_cooldown_s
    cd = engagement.get("speak_cooldown_s")
    if cd is not None:
        return float(cd)
    return base_cooldown_s


def apply_engagement_to_score(score: float, engagement: Optional[Dict[str, Any]]) -> float:
    """
    在 evaluate_advice 的 score 上乘 engagement.advice_scale。
    非 ENGAGED：返回 score 不变。
    """
    if not engagement or engagement.get("level", "L0") == "L0":
        return score
    scale = engagement.get("advice_scale", 1.0)
    return score * scale
