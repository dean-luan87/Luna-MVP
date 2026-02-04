"""
PriorityBand: 优先级分段定义

将数值 priority 划分为几个等级，便于调度。

Step 12: 统一优先级调度器
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Priority band thresholds (behavior contract)
#
# These thresholds define cross-module ordering. Any change alters which
# messages the user hears first and is therefore a contract change.
#
# Frozen mapping:
# - priority >= 90  -> P0_SAFETY
# - priority >= 70  -> P1_NAV
# - priority >= 40  -> P2_TASK
# - else            -> P3_CHAT
# ======================================================================

from __future__ import annotations

from enum import Enum


class PriorityBand(Enum):
    """将数值 priority 划分为几个等级，便于调度."""

    P0_SAFETY = 0   # 安全
    P1_NAV = 1      # 导航
    P2_TASK = 2     # 任务 / 系统
    P3_CHAT = 3     # 闲聊 / 低优先级

    @classmethod
    def from_priority(cls, priority: int) -> "PriorityBand":
        """
        根据数值 priority 映射到优先级段.

        Args:
            priority: 优先级数值（0-100）

        Returns:
            PriorityBand: 对应的优先级段
        """
        if priority >= 90:
            return cls.P0_SAFETY
        if priority >= 70:
            return cls.P1_NAV
        if priority >= 40:
            return cls.P2_TASK
        return cls.P3_CHAT

    def is_higher_than(self, other: "PriorityBand") -> bool:
        """
        判断当前优先级段是否高于另一个优先级段.

        Args:
            other: 另一个 PriorityBand

        Returns:
            bool: True 表示当前优先级更高（value 更小）
        """
        return self.value < other.value






