# vision_pipeline/b2/v03/evidence_buffer.py
from __future__ import annotations
from collections import deque
from typing import Deque, List

from .evidence_types import EvidenceRecord


class EvidenceBuffer:
    """
    用于缓存最近 N 秒的 EvidenceRecord
    支持按时间窗口导出
    """

    def __init__(self, max_seconds: float, fps: float):
        self.max_len = int(max_seconds * fps)
        self.buffer: Deque[EvidenceRecord] = deque(maxlen=self.max_len)

    def append(self, record: EvidenceRecord) -> None:
        self.buffer.append(record)

    def export_window(self, start_t: float, end_t: float) -> List[EvidenceRecord]:
        """
        导出 [start_t, end_t] 内的所有证据记录
        """
        return [
            r for r in self.buffer
            if start_t <= r.t_video <= end_t
        ]

