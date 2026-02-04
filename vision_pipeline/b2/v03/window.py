# vision_pipeline/b2/v03/window.py

import time
from typing import List, Dict, Any, Optional
from collections import deque


class FutureWindow:
    """
    B2 v0.3 时间窗：
    [now + 1s, now + 8s]
    """

    def __init__(self,
                 start_offset: float = 1.0,
                 duration: float = 8.0):
        self.start_offset = start_offset
        self.duration = duration
        self.buffer = deque()

    def push(self, state: Dict[str, Any]):
        """
        state 必须包含 ts
        """
        self.buffer.append(state)
        self._gc()

    def _gc(self):
        now = time.time()
        expire_before = now - 10.0
        while self.buffer and self.buffer[0]["ts"] < expire_before:
            self.buffer.popleft()

    def slice(self, now_ts: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        获取未来时间窗口内的状态
        now_ts: 当前时间戳，如果为 None 则使用 time.time()
        """
        if now_ts is None:
            now_ts = time.time()
        start = now_ts + self.start_offset
        end = start + self.duration

        return [
            s for s in self.buffer
            if start <= s["ts"] <= end
        ]

