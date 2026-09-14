# -*- coding: utf-8 -*-
"""
v1.8.4: 动态区域评估器（DynamicEvaluator）

职责：
- 判断 RiskObject 当前是否激活（基于时间窗口或条件）
- 应用动态区域的 hazard 修正
- 只在 risk 模块内部使用，不影响主决策链
"""

from __future__ import annotations
from typing import Optional
import datetime
from .risk_object import RiskObject, DynamicProfile


def is_active(ro: RiskObject, now: datetime.datetime) -> bool:
    """
    判断风险对象当前是否激活
    
    Args:
        ro: 风险对象
        now: 当前时间（datetime 对象）
    
    Returns:
        bool: True 表示激活，False 表示未激活
    """
    dp = ro.dynamic_profile
    if not dp:
        return True  # 没有动态配置，永远激活
    
    if dp.mode == "ALWAYS":
        return True
    
    if dp.mode == "TIME_WINDOW":
        if not dp.active_windows:
            return False
        hour = now.hour
        for start, end in dp.active_windows:
            if start <= hour < end:
                return True
        return False
    
    if dp.mode == "CONDITION":
        # 1.8.4 先预留，后续接世界模型 / 外部信号
        # 可以通过 ro.meta 传递条件状态
        condition_active = ro.meta.get("dynamic_condition_active", False)
        return condition_active
    
    return False


def apply_hazard_modifier(ro: RiskObject) -> float:
    """
    应用动态区域的 hazard 修正
    
    Args:
        ro: 风险对象
    
    Returns:
        float: 修正后的 hazard_level
    """
    if not ro.dynamic_profile:
        return ro.hazard_level
    
    return ro.hazard_level * ro.dynamic_profile.hazard_multiplier


