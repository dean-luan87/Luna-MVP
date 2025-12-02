"""
Scene Output module.

将融合后的视觉结果 + 深度信息 + 原始帧
整理为统一场景状态对象 SceneState。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SceneState:
    timestamp: Optional[float]
    objects: List[Dict[str, Any]] = field(default_factory=list)
    depth_info: Optional[Any] = None
    walkable_zone: Optional[Any] = None
    raw_frame: Optional[Any] = None


def build_scene_state(fused_result: Dict[str, Any],
                      depth_result: Any,
                      raw_frame: Any) -> SceneState:
    """
    构建场景状态对象。
    """
    timestamp = None
    meta = fused_result.get("meta", {}) if fused_result else {}
    if isinstance(meta, dict):
        timestamp = meta.get("timestamp")

    objects = fused_result.get("detections", []) if fused_result else []
    return SceneState(
        timestamp=timestamp,
        objects=objects,
        depth_info=depth_result,
        walkable_zone=None,  # v1.2 先不计算可通行区域
        raw_frame=raw_frame,
    )










