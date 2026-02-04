"""
C1 状态机定义（C1 的骨架）
"""

from enum import Enum


class C1State(Enum):
    """
    C1 状态机定义
    
    最小可用版本，覆盖 90% 真实世界场景。
    """
    STABLE = "stable"
    TRANSITION = "transition"
    ALERT = "alert"
    SUSPENDED = "suspended"
