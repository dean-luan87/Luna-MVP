from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass(frozen=True)
class AttentionWindow:
    area_type: str
    hint: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    ttl_frames: int = 30
    source: str = "map_candidate"


class AttentionManager:
    """
    只读关注窗口管理：
    - 有 TTL
    - 可被完全忽略
    """

    def __init__(self):
        self._windows: List[AttentionWindow] = []
        self._ttl: Dict[int, int] = {}

    def set(self, windows: List[AttentionWindow]):
        self._windows = list(windows)
        self._ttl = {i: w.ttl_frames for i, w in enumerate(self._windows)}

    def tick(self):
        expired = []
        for i in list(self._ttl.keys()):
            self._ttl[i] -= 1
            if self._ttl[i] <= 0:
                expired.append(i)
        for i in sorted(expired, reverse=True):
            self._ttl.pop(i, None)
            self._windows.pop(i)

    def get(self) -> List[AttentionWindow]:
        return list(self._windows)
