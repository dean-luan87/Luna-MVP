"""
Scene Types (C-2.2)

场景类型枚举

场景不是地点，是"认知负载模型"
"""

from enum import Enum


class SceneType(Enum):
    """
    SceneType Enum
    
    场景类型（一期就够用）：
    - NAVIGATION_SHORT: ≤50m 视角主导
    - NAVIGATION_LONG: >50m GPS参与
    - INDOOR: 室内
    - OUTDOOR: 室外
    - SAFE_MODE: 风险场景
    """
    NAVIGATION_SHORT = "navigation_short"     # ≤50m 视角主导
    NAVIGATION_LONG = "navigation_long"       # >50m GPS参与
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    SAFE_MODE = "safe_mode"                  # 风险场景
