# -*- coding: utf-8 -*-
"""
v1.8.5: Position State（位置状态）

职责：
- PositionState 的定义
- 提供位置和稳定性评分

原则：
- position: (x, y) 米为单位
- stability_score: 0.0 ~ 1.0，用于稳定性闸门判断
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class PositionState:
    """
    位置状态
    
    字段说明：
    - position: 位置坐标 (x, y)，单位：米
    - stability_score: 稳定性评分 [0.0 ~ 1.0]
      - 用于稳定性闸门判断
      - < STABILITY_THRESHOLD 时冻结所有演化
    """
    position: Tuple[float, float]  # (x, y) meters
    stability_score: float  # 0.0 ~ 1.0


