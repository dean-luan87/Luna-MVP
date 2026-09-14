# -*- coding: utf-8 -*-
"""
v1.8.4: 风险类型定义与参数表

职责：
- 定义风险类型枚举
- 提供风险类型到参数的映射（1.8.4 必须先固化的旋钮）
"""

from enum import Enum
from typing import Dict, Literal

class RiskType(str, Enum):
    """风险类型"""
    STAIRS = "STAIRS"
    WATER_EDGE = "WATER_EDGE"
    CLIFF_EDGE = "CLIFF_EDGE"
    FENCE = "FENCE"
    CONSTRUCTION = "CONSTRUCTION"
    CROWD = "CROWD"
    OBSTACLE = "OBSTACLE"  # 通用障碍物


# v1.8.4 参数表（必须先固化的旋钮）
# 参数定义：
#   - hazard_base: 世界模型未介入时的基础 Hazard（规则默认值）
#   - d0: 距离归一化基准（越大表示更早进入关注半径）
#   - delta_warn: ΔRisk 触发阈值（核心）
#   - cooldown_s: 触发后最短静默时间（防骚扰）
RISK_TYPE_CONFIG: Dict[str, Dict[str, float]] = {
    "STAIRS": {
        "hazard_base": 0.35,
        "d0": 8.0,
        "delta_warn": 0.18,
        "cooldown_s": 12.0,
    },
    "WATER_EDGE": {
        "hazard_base": 0.80,
        "d0": 20.0,
        "delta_warn": 0.12,
        "cooldown_s": 20.0,
    },
    "CLIFF_EDGE": {
        "hazard_base": 0.95,
        "d0": 25.0,
        "delta_warn": 0.10,
        "cooldown_s": 25.0,
    },
    "FENCE": {
        "hazard_base": 0.45,
        "d0": 10.0,
        "delta_warn": 0.16,
        "cooldown_s": 15.0,
    },
    "CONSTRUCTION": {
        "hazard_base": 0.70,
        "d0": 15.0,
        "delta_warn": 0.14,
        "cooldown_s": 18.0,
    },
    "CROWD": {
        "hazard_base": 0.40,
        "d0": 12.0,
        "delta_warn": 0.20,
        "cooldown_s": 10.0,
    },
    "OBSTACLE": {
        "hazard_base": 0.50,
        "d0": 10.0,
        "delta_warn": 0.15,
        "cooldown_s": 12.0,
    },
}


def get_risk_config(risk_type: str) -> Dict[str, float]:
    """
    获取风险类型配置
    
    Args:
        risk_type: 风险类型字符串
    
    Returns:
        Dict[str, float]: 风险配置参数
    """
    return RISK_TYPE_CONFIG.get(risk_type, {
        "hazard_base": 0.5,
        "d0": 10.0,
        "delta_warn": 0.15,
        "cooldown_s": 12.0,
    })


