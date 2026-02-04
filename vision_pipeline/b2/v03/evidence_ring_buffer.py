# vision_pipeline/b2/v03/evidence_ring_buffer.py
from __future__ import annotations
from collections import deque
from typing import Deque, List, Optional

from .evidence_types import EvidenceRecord


class EvidenceRingBuffer:
    """
    用于 Step 3 的实战级证据缓存：
    - 按时间连续写入 EvidenceRecord
    - 支持导出任意时间窗口
    """

    def __init__(self, max_seconds: float, fps: float):
        self.fps = fps
        self.max_seconds = max_seconds
        self.max_len = int(max_seconds * fps)

        self._buf: Deque[EvidenceRecord] = deque(maxlen=self.max_len)

    # ----------------------------
    # 写入
    # ----------------------------

    def push(self, record: EvidenceRecord) -> None:
        """
        每一帧 / 每一次 tick 调用
        """
        self._buf.append(record)

    # ----------------------------
    # 查询
    # ----------------------------

    def export_window(
        self,
        center_t: float,
        pre_sec: float,
        post_sec: float,
    ) -> List[EvidenceRecord]:
        """
        以某个 Anchor 时间为中心，导出证据窗口
        """
        start_t = center_t - pre_sec
        end_t = center_t + post_sec

        return [
            r for r in self._buf
            if start_t <= r.t_video <= end_t
        ]

    def export_range(
        self,
        start_t: float,
        end_t: float,
    ) -> List[EvidenceRecord]:
        """
        直接按时间范围导出
        """
        return [
            r for r in self._buf
            if start_t <= r.t_video <= end_t
        ]

    # ----------------------------
    # 状态辅助（调试用）
    # ----------------------------

    def size(self) -> int:
        return len(self._buf)

    def latest(self) -> Optional[EvidenceRecord]:
        if not self._buf:
            return None
        return self._buf[-1]

