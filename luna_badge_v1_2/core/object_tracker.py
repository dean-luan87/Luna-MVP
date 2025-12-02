"""
Object Tracker module.

目标跟踪模块（占位）：
- 接收每帧检测结果，输出带 track_id 的目标列表
- 未来可接入 SORT / ByteTrack 等算法
"""

from typing import Any, Dict, List


class ObjectTracker:
    def __init__(self):
        self._next_track_id: int = 1

    def update(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        输入本帧的检测结果，输出带 track_id 的结果。

        v1.3 占位实现：简单给每个检测分配一个递增的 track_id。
        """
        tracked = []
        for det in detections:
            det_with_id = dict(det)
            det_with_id["track_id"] = self._next_track_id
            self._next_track_id += 1
            tracked.append(det_with_id)
        return tracked










