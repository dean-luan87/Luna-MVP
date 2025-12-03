"""
Speed Engine 共享上下文
1.4.1-speed.1: 线程基础框架
"""
from typing import Literal

SpeedMode = Literal["normal", "fast", "safe"]


class SpeedContext:
    """
    SpeedEngine 的共享上下文，包括线程运行状态、模式等。
    1.4.1-speed.1 仅作为占位，将在 speed.4 扩展。
    """
    
    speed_mode: SpeedMode = "normal"  # normal, fast, safe

    @staticmethod
    def set_mode(mode: SpeedMode):
        """
        设置速度模式
        
        Args:
            mode: 速度模式（normal, fast, safe）
        """
        SpeedContext.speed_mode = mode

    @staticmethod
    def get_mode() -> SpeedMode:
        """
        获取当前速度模式
        
        Returns:
            当前速度模式
        """
        return SpeedContext.speed_mode

