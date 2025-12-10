from dataclasses import dataclass
from typing import Callable, List, Dict, Any
import time
from infra.logging_manager import get_logger

logger = get_logger("navigation")


@dataclass
class NavState:
    at_target: bool
    distance: float


class NavigationController:
    def __init__(self, tts_say: Callable[[str], None]) -> None:
        self._tts = tts_say
        self._active: bool = False
        self._target_name: str = ""
        self._distance: float = 10.0
        self._last_broadcast_ts = 0.0
        # 到达附近的语音提示冷却时间（在 Patch D 里会调大）
        self._broadcast_interval = 30.0  # 秒
        # 是否已经播报过"到达附近"
        self._arrival_announced = False

    def start(self, target) -> None:
        self._active = True
        self._target_name = target.name
        self._distance = 10.0
        self._tts(f"开始前往 {self._target_name}")

    def stop(self) -> None:
        if self._active:
            self._tts(f"已停止前往 {self._target_name}")
        self._active = False
        self._target_name = ""
        self._distance = 0.0

    def has_active_target(self) -> bool:
        return self._active

    def step(self, vision_objects: List[Dict[str, Any]]) -> NavState:
        if not self._active:
            return NavState(at_target=False, distance=0.0)

        # 这里只做一个非常简单的"距离递减"
        self._distance = max(0.0, self._distance - 0.5)
        now = time.time()
        
        # 统一"到达附近"的判定逻辑：<= 0.5m
        at_target = self._distance <= 0.5
        
        # 只在第一次进入 0.5m 区间时播报一次
        if at_target and not self._arrival_announced:
            # 冷却只是兜底保护，避免极短时间内逻辑抖动导致多次进出 0.5m
            if now - self._last_broadcast_ts > self._broadcast_interval:
                self._tts(f"已到达 {self._target_name} 附近。")
                self._last_broadcast_ts = now
                self._arrival_announced = True
        
        # 如果后续用户离开 1m 以外，再次允许"到达"提醒
        if not at_target and self._distance > 1.0:
            if self._arrival_announced:
                logger.info("[NAV] 离开目标区域，重置到达播报状态")
            self._arrival_announced = False
        
        # 低频播报（距离 < 3 米且超过播报间隔，但不在到达状态）
        if not at_target and self._distance < 3.0 and self._distance > 0:
            if now - self._last_broadcast_ts > self._broadcast_interval:
                logger.debug(f"[NAV] distance to {self._target_name}: {self._distance:.1f}")
                self._tts(f"距离 {self._target_name} 还有 {self._distance:.1f} 米。")
                self._last_broadcast_ts = now

        return NavState(at_target=at_target, distance=self._distance)

