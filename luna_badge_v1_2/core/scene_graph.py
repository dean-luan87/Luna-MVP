"""
Scene Graph module.

根据多模态融合结果构建轻量级场景图：
- objects：稳定的目标列表
- relations：预留，用于未来表示"左/右/前方"等关系
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SceneGraph:
    objects: List[Dict[str, Any]] = field(default_factory=list)
    relations: List[Dict[str, Any]] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


def build_scene_graph(fused_result: Dict[str, Any]) -> SceneGraph:
    """
    从融合结果构建场景图。

    v1.3 占位实现：
    - 将 fused_result["objects"] 写入 SceneGraph.objects
    - relations 先留空
    """
    objects = fused_result.get("objects", []) if fused_result else []
    meta = fused_result.get("meta", {}) if fused_result else {}
    return SceneGraph(objects=objects, relations=[], meta=meta)














