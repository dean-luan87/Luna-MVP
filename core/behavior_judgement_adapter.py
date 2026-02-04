#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行为判断适配器 (v1.8.1)

功能：将导航判断结果映射为行为级建议
原则：不修改原导航判断逻辑，仅新增语义映射层
"""

from typing import Dict, Any, Optional
from enum import Enum


class BehaviorJudgementType(str, Enum):
    """行为判断类型"""
    BEHAVIOR_DIRECTION_ERROR = "BEHAVIOR_DIRECTION_ERROR"
    VIEW_NOT_PASSABLE = "VIEW_NOT_PASSABLE"
    SUGGEST_TURN_AROUND = "SUGGEST_TURN_AROUND"


# 导航状态到行为判断的映射
NAV_TO_BEHAVIOR_MAP = {
    "NAV_OFF_ROUTE": BehaviorJudgementType.BEHAVIOR_DIRECTION_ERROR,
    "PATH_BLOCKED": BehaviorJudgementType.VIEW_NOT_PASSABLE,
    "SUGGEST_REROUTE": BehaviorJudgementType.SUGGEST_TURN_AROUND,
}


def adapt_navigation_to_behavior(nav_result: Dict[str, Any]) -> Optional[BehaviorJudgementType]:
    """
    行为语义映射层
    
    将导航判断结果映射为行为级判断
    
    Args:
        nav_result: 导航判断结果，包含：
            - nav_status: 导航状态（如 "NAV_OFF_ROUTE"）
    
    Returns:
        Optional[BehaviorJudgementType]: 映射后的行为判断类型，如果无法映射则返回 None
    
    映射规则：
        - NAV_OFF_ROUTE → BEHAVIOR_DIRECTION_ERROR
        - PATH_BLOCKED → VIEW_NOT_PASSABLE
        - SUGGEST_REROUTE → SUGGEST_TURN_AROUND
    """
    nav_status = nav_result.get("nav_status", "")
    return NAV_TO_BEHAVIOR_MAP.get(nav_status)


def generate_behavior_suggestion(
    behavior_type: BehaviorJudgementType,
    observer_mode_active: bool = False
) -> Optional[str]:
    """
    动作级建议输出
    
    根据行为判断类型生成动作级建议文本
    
    Args:
        behavior_type: 行为判断类型
        observer_mode_active: Observer Mode 是否激活（仅在激活时生效）
    
    Returns:
        Optional[str]: 建议文本，如果 observer_mode 未激活则返回 None
    
    要求：
        - 不触发路径重规划
        - 仅在 observer_mode.active == True 时生效
        - v1.8 原导航输出保持不变
    """
    # 仅在 Observer Mode 激活时生效
    if not observer_mode_active:
        return None
    
    # 动作级建议模板
    suggestions = {
        BehaviorJudgementType.BEHAVIOR_DIRECTION_ERROR: "你现在面对的方向不对，建议原地转身。",
        BehaviorJudgementType.VIEW_NOT_PASSABLE: "前方通道不可通行，建议寻找其他路径。",
        BehaviorJudgementType.SUGGEST_TURN_AROUND: "建议你转身，换个方向试试。",
    }
    
    return suggestions.get(behavior_type)


