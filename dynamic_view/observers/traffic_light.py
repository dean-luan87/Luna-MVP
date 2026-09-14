import time
from typing import Optional

from .base import BaseObserver, Evidence


class TrafficLightObserver(BaseObserver):
    """
    Stub 红绿灯观察器：
    - 模拟颜色变化
    - 颜色存在即视为“可见”
    """

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self._color: Optional[str] = None

    def set_color(self, color: Optional[str]):
        self._color = color

    def poll(self) -> Optional[Evidence]:
        if self._color is None:
            return None
        return Evidence(
            entity_id=self.entity_id,
            timestamp=time.time(),
        )
