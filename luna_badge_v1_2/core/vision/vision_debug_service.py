"""
VisionDebugService: 视觉健康调试服务

用于 Debug / Dashboard 的视觉健康服务。
上层通过本类获取 MultiModelEngine 的健康画像，不直接依赖多模型引擎内部结构。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional

from .multi_model_engine import MultiModelEngine


@dataclass
class VisionHealthSnapshot:
    """
    对外统一格式（比 MultiModelEngine 原始 snapshot 更适合可视化）：

    {
       "detect": {
          "yolo11n": {...},
          "yolo11s": {...}
       },
       "ocr": {...}
    }
    """
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return self.data


class VisionDebugService:
    """
    用于 Debug / Dashboard 的视觉健康服务。

    上层通过本类获取 MultiModelEngine 的健康画像，不直接依赖多模型引擎内部结构。
    """

    def __init__(self, engine: MultiModelEngine):
        """
        Args:
            engine: MultiModelEngine 实例
        """
        self._engine = engine

    def get_health(self) -> VisionHealthSnapshot:
        """
        获取完整的视觉健康快照。

        Returns:
            VisionHealthSnapshot: 健康快照
        """
        raw = self._engine.get_model_health_snapshot()

        # 可在此扩展更多字段：比如更新时间戳、版本号、模型 meta 等
        snapshot = {
            "engine_status": {
                "total_task_types": len(raw),
            },
            "models": raw,
        }

        return VisionHealthSnapshot(data=snapshot)

    def get_model_block(self, task_type: str) -> Optional[Dict[str, Any]]:
        """
        获取特定 task_type 的模型健康。

        Args:
            task_type: 任务类型（如 'detect', 'ocr'）

        Returns:
            Optional[Dict[str, Any]]: 该任务类型的模型健康信息，如果不存在则返回 None
        """
        snapshot = self.get_health().to_dict()
        return snapshot.get("models", {}).get(task_type)

