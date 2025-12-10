"""
TimeWindowGate 统一播报节流模块

用于安全播报 & 导航播报节流
v1.4.6d-TW
"""

import time
from dataclasses import dataclass, field


@dataclass
class TimeWindowGate:
    """
    控制不同类别的播报最低时间间隔
    - SAFETY: 默认 0.8 秒
    - NAVIGATION: 默认 2.0 秒
    """

    safety_window: float = 0.8
    navigation_window: float = 2.0

    last_safety_time: float = field(default=0.0)
    last_navigation_time: float = field(default=0.0)

    def allow(self, category: str) -> bool:
        """
        检查该类型是否超过节流窗口
        """
        now = time.time()

        if category == "SAFETY":
            if now - self.last_safety_time >= self.safety_window:
                self.last_safety_time = now
                return True
            return False

        if category == "NAVIGATION":
            if now - self.last_navigation_time >= self.navigation_window:
                self.last_navigation_time = now
                return True
            return False

        # 默认允许
        return True

    def reset(self) -> None:
        """重置所有时间戳（用于测试）"""
        self.last_safety_time = 0.0
        self.last_navigation_time = 0.0

