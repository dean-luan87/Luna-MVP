"""
Navigation State (v1.3.0)

导航任务状态枚举

定义导航任务的所有可能状态
"""

from enum import Enum


class NavigationState(Enum):
    """
    导航任务状态

    状态流转：
    IDLE → ACTIVE → PAUSED ↔ ACTIVE → ARRIVED / STOPPED
    """

    IDLE = "idle"          # 未开始
    ACTIVE = "active"      # 正在导航（实时处理视觉 + 决策 + 语音）
    PAUSED = "paused"      # 临时中断（如如厕、询问、停下来查东西）
    STOPPED = "stopped"    # 用户主动或被动终止
    ARRIVED = "arrived"    # 到达目标

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, state_str: str):
        """
        从字符串转换为状态枚举

        Args:
            state_str: 状态字符串

        Returns:
            NavigationState: 状态枚举
        """
        try:
            return cls(state_str.lower())
        except ValueError:
            return cls.IDLE

    def can_transition_to(self, target_state: 'NavigationState') -> bool:
        """
        判断是否可以转换到目标状态

        Args:
            target_state: 目标状态

        Returns:
            bool: 是否可以转换
        """
        transitions = {
            NavigationState.IDLE: [NavigationState.ACTIVE],
            NavigationState.ACTIVE: [
                NavigationState.PAUSED,
                NavigationState.STOPPED,
                NavigationState.ARRIVED,
            ],
            NavigationState.PAUSED: [
                NavigationState.ACTIVE,
                NavigationState.STOPPED,
            ],
            NavigationState.STOPPED: [],  # 终止状态，不能转换
            NavigationState.ARRIVED: [],  # 终止状态，不能转换
        }

        return target_state in transitions.get(self, [])













