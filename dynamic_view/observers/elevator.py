import time
from typing import Optional

from .base import BaseObserver, Evidence


class ElevatorObserver(BaseObserver):
    """
    Stub 版电梯观察器：
    - 手动触发“看见 / 看不见”
    - 用于验证 Observation Engine 行为
    """

    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self._visible = False

    def set_visible(self, visible: bool):
        self._visible = visible

    def poll(self) -> Optional[Evidence]:
        if not self._visible:
            return None
        return Evidence(
            entity_id=self.entity_id,
            timestamp=time.time(),
        )
