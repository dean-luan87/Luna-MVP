"""
Fusion Engine module (v1.3).

多模态多帧融合：
- 根据时间窗口融合 detections / tracked_objects 等
- v1.3 仍用简化逻辑：当前先直接使用最近一帧的 tracked_objects
"""

from collections import deque
from typing import Any, Deque, Dict


class FusionEngine:
    def __init__(self, window_size: int = 10):
        self.window_size: int = window_size
        self._results: Deque[Dict[str, Any]] = deque(maxlen=window_size)

    def add_result(self, result: Dict[str, Any]) -> None:
        """
        添加单帧推理结果。
        """
        self._results.append(result)

    def get_fused_result(self) -> Dict[str, Any]:
        """
        返回融合后的结果。

        v1.3 简化实现：
        - 若存在结果，则：
          - objects = 最近一帧的 tracked_objects
        - 未来可在此实现：
          - 多帧投票稳定 ID
          - 去除短暂出现的目标
        """
        if not self._results:
            return {"objects": [], "meta": {}}

        latest = self._results[-1]
        objects = latest.get("tracked_objects") or latest.get("detections") or []
        meta = latest.get("meta", {})
        result = {
            "objects": objects,
            "meta": meta,
        }
        # 兼容旧测试：过去版本使用 "detections" 字段，现在统一返回 "objects"。
        # 为了不破坏现有调用方，这里增加一个别名字段。
        # 对业务逻辑无影响，但可以让 test_fusion 中对 "detections" 的断言通过。
        if "detections" not in result:
            result["detections"] = objects
        return result

