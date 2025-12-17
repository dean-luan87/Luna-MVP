"""
TimeWindowGate 统一播报节流模块

用于安全播报 & 导航播报节流
v1.4.6d-TW
"""

# ======================================================================
# [v1.4.9 P0-1 FREEZE] Time window thresholds (behavior contract)
#
# These windows define user-perceived speaking frequency. Any change is a
# behavior change and requires a version bump.
#
# Frozen parameters:
# - safety_window:     0.8 seconds
# - navigation_window: 2.0 seconds
#
# Frozen semantics:
# - allow("SAFETY") updates last_safety_time on pass
# - allow("NAVIGATION") updates last_navigation_time on pass
# - unknown category -> allow (fallback)
# ======================================================================

import time
from dataclasses import dataclass, field
from typing import Callable


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
    # [v1.4.9 P0-2-B] 时间源注入点：默认仍为 wall clock，
    # Replay 模式下由 ReplayClock 绑定（不改语义、不改阈值）。
    now_fn: Callable[[], float] = field(default=time.time, repr=False, compare=False)

    def allow(self, category: str) -> bool:
        """
        检查该类型是否超过节流窗口
        """
        now = self.now_fn()

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

