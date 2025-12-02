# core/scene_graph.py
"""
SceneGraph 构建模块
负责把 YOLO / OCR 输出转换为 Luna 可理解的场景图结构

约定输入格式：
yolo_objects: List[Dict]
    [
      {
        "id": int / str,
        "cls": "person",
        "confidence": 0.92,
        "bbox": [x1_norm, y1_norm, x2_norm, y2_norm],   # 0-1 归一化
        "distance_m": 2.1 (可选)
      },
      ...
    ]

ocr_blocks: List[Dict]
    [
      {
        "text": "出口 Exit",
        "confidence": 0.88,
        "bbox": [x1_norm, y1_norm, x2_norm, y2_norm]
      },
      ...
    ]

返回：
scene_graph: Dict
    {
      "nodes": [ ... ],
      "relations": [ ... ]
    }
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple
import math


# --------- 数据结构 --------- #

@dataclass
class SGNode:
    id: str
    type: str          # "object" / "ocr" / "region" / "danger"
    cls: str = ""
    text: str = ""
    confidence: float = 1.0
    bbox: Tuple[float, float, float, float] | None = None
    extra: Dict[str, Any] | None = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # None 的字段不输出，减小体积
        return {k: v for k, v in d.items() if v is not None}


@dataclass
class SGRelation:
    source: str
    target: str
    type: str          # "in_region" / "near" / "front_of" / "attached_to" / ...

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SceneGraph:
    def __init__(self):
        self.nodes: List[SGNode] = []
        self.relations: List[SGRelation] = []

    def add_node(self, node: SGNode):
        self.nodes.append(node)

    def add_rel(self, rel: SGRelation):
        self.relations.append(rel)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "relations": [r.to_dict() for r in self.relations],
        }


# --------- 工具函数 --------- #

def _bbox_center(bbox: List[float]) -> Tuple[float, float]:
    x1, y1, x2, y2 = bbox
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0


def _bbox_area(bbox: List[float]) -> float:
    x1, y1, x2, y2 = bbox
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def _distance_2d(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


# --------- 主构建器 --------- #

class SceneGraphBuilder:
    """
    核心：从 yolo_objects / ocr_blocks 构建 SceneGraph
    """

    REGION_CONFIG = {
        "left":   (0.0, 0.0, 0.33, 1.0),
        "center": (0.33, 0.0, 0.66, 1.0),
        "right":  (0.66, 0.0, 1.0, 1.0),
        "near":   (0.0, 0.55, 1.0, 1.0),
        "mid":    (0.0, 0.3, 1.0, 0.7),
        "far":    (0.0, 0.0, 1.0, 0.45),
    }

    DANGER_CLASSES = {"car", "bus", "truck", "bicycle", "motorbike", "person", "stairs"}
    STEP_KEYWORDS = {"阶", "梯", "stairs"}

    @classmethod
    def build(
        cls,
        yolo_objects: List[Dict[str, Any]],
        ocr_blocks: List[Dict[str, Any]],
        frame_meta: Dict[str, Any] | None = None,
    ) -> SceneGraph:
        sg = SceneGraph()

        # 1. 区域节点
        region_nodes = {}
        for name, bbox in cls.REGION_CONFIG.items():
            nid = f"region_{name}"
            node = SGNode(id=nid, type="region", cls=name, bbox=bbox)
            sg.add_node(node)
            region_nodes[name] = node

        # 2. YOLO 物体节点
        obj_nodes: List[SGNode] = []
        for idx, obj in enumerate(yolo_objects):
            nid = f"obj_{obj.get('id', idx)}"
            node = SGNode(
                id=nid,
                type="object",
                cls=str(obj.get("cls", "")),
                confidence=float(obj.get("confidence", 1.0)),
                bbox=tuple(obj.get("bbox", (0, 0, 0, 0))),
                extra={
                    "distance_m": obj.get("distance_m"),
                },
            )
            sg.add_node(node)
            obj_nodes.append(node)

        # 3. OCR 节点
        ocr_nodes: List[SGNode] = []
        for i, blk in enumerate(ocr_blocks):
            nid = f"ocr_{i}"
            node = SGNode(
                id=nid,
                type="ocr",
                text=str(blk.get("text", "")),
                confidence=float(blk.get("confidence", 1.0)),
                bbox=tuple(blk.get("bbox", (0, 0, 0, 0))),
            )
            sg.add_node(node)
            ocr_nodes.append(node)

        # 4. 物体/文字 → 区域 关系
        for node in obj_nodes + ocr_nodes:
            if not node.bbox:
                continue
            cx, cy = _bbox_center(list(node.bbox))
            for rname, rnode in region_nodes.items():
                rx1, ry1, rx2, ry2 = rnode.bbox
                if rx1 <= cx <= rx2 and ry1 <= cy <= ry2:
                    sg.add_rel(SGRelation(source=node.id, target=rnode.id, type="in_region"))

        # 5. 物体之间"near"关系
        for i, a in enumerate(obj_nodes):
            if not a.bbox:
                continue
            ca = _bbox_center(list(a.bbox))
            for j in range(i + 1, len(obj_nodes)):
                b = obj_nodes[j]
                if not b.bbox:
                    continue
                cb = _bbox_center(list(b.bbox))
                d = _distance_2d(ca, cb)
                if d < 0.2:  # 归一化坐标下的"近"
                    sg.add_rel(SGRelation(source=a.id, target=b.id, type="near"))
                    sg.add_rel(SGRelation(source=b.id, target=a.id, type="near"))

        # 6. 基于类别构建 Danger 节点（抽象危险）
        #    如：前方有车辆、人、台阶 等
        danger_id = 0
        for obj in obj_nodes:
            if obj.cls in cls.DANGER_CLASSES:
                danger_type = "generic"

                if obj.cls == "person":
                    danger_type = "person"
                elif obj.cls in {"car", "bus", "truck", "bicycle", "motorbike"}:
                    danger_type = "vehicle"
                elif obj.cls == "stairs":
                    danger_type = "stairs"

                dnid = f"danger_{danger_id}"
                danger_id += 1
                dnode = SGNode(
                    id=dnid,
                    type="danger",
                    cls=danger_type,
                    confidence=obj.confidence,
                    bbox=obj.bbox,
                    extra={"source_obj": obj.id},
                )
                sg.add_node(dnode)
                sg.add_rel(SGRelation(source=obj.id, target=dnid, type="has_danger"))

        # 7. OCR 中与"出口/科室/区域"等相关的文字，建立语义结点
        for o in ocr_nodes:
            text = o.text
            if any(k in text for k in ("出口", "Exit", "exit")):
                # 出口
                sg.add_rel(SGRelation(source=o.id, target="semantic_exit", type="label"))
            if any(k in text for k in ("挂号", "门诊", "科室", "诊室")):
                sg.add_rel(SGRelation(source=o.id, target="semantic_hospital_area", type="label"))

        return sg

