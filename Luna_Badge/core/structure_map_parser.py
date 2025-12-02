# core/structure_map_parser.py
"""
结构图（医院 / 商场 / 地铁 / 公共建筑）解析模块

输入：
- OCR blocks: [
    {"text": "...", "confidence": 0.9, "bbox": [x1,y1,x2,y2]}, ...
  ]

输出：
- floor_graph: SceneGraph
- map_kind: "hospital" / "mall" / "subway" / "generic"
"""

from __future__ import annotations

from typing import List, Dict, Any, Tuple
import math

from .scene_graph import SceneGraph, SGNode, SGRelation


class StructureMapClassifier:
    """根据文字关键词，大致判断结构图类型"""

    KEYWORDS = {
        "hospital": ["科室", "门诊", "挂号", "候诊", "住院部", "检查", "检验科", "急诊"],
        "mall": ["L1", "L2", "负一层", "店铺", "商场", "美食广场", "儿童区", "超市"],
        "subway": ["站台", "出入口", "出口", "闸机", "换乘", "地铁", "乘车", "安检"],
    }

    @classmethod
    def classify(cls, texts: List[str]) -> str:
        score = {k: 0 for k in cls.KEYWORDS.keys()}
        for t in texts:
            for kind, kws in cls.KEYWORDS.items():
                for kw in kws:
                    if kw in t:
                        score[kind] += 1

        # 选得分最高的
        best_kind = max(score, key=score.get)
        if score[best_kind] == 0:
            return "generic"
        return best_kind


class FloorPlanParser:
    """
    用 OCR 结果构造一个结构图 SceneGraph：
    - 房间/科室节点：room
    - 区域/功能区节点：zone
    - 出口/入口：exit
    - 电梯/楼梯：facility
    """

    @staticmethod
    def parse_floorplan(
        ocr_blocks: List[Dict[str, Any]],
        map_kind: str | None = None,
    ) -> Tuple[SceneGraph, str]:
        sg = SceneGraph()

        # 1. 判断 map 类型
        texts = [blk.get("text", "") for blk in ocr_blocks]
        detected_kind = StructureMapClassifier.classify(texts)
        if map_kind is None:
            map_kind = detected_kind

        # 2. 基于文字内容创建节点
        nodes: List[SGNode] = []
        for i, blk in enumerate(ocr_blocks):
            text = str(blk.get("text", "")).strip()
            if not text:
                continue

            bbox = blk.get("bbox", [0, 0, 0, 0])
            nid = f"fp_{i}"

            t = "label"
            cls = "label"

            if any(k in text for k in ("科", "诊室", "门诊", "病房", "室")):
                t = "room"
                cls = "room"
            elif any(k in text for k in ("区", "大厅", "广场", "Hall", "hall")):
                t = "zone"
                cls = "zone"
            elif any(k in text for k in ("出口", "出入口", "Exit", "EXIT", "出口A", "出口B")):
                t = "exit"
                cls = "exit"
            elif any(k in text for k in ("电梯", "扶梯", "梯", "stairs", "lift", "elevator")):
                t = "facility"
                cls = "stairs_or_elevator"

            node = SGNode(
                id=nid,
                type=t,
                cls=cls,
                text=text,
                confidence=float(blk.get("confidence", 1.0)),
                bbox=tuple(bbox) if isinstance(bbox, (list, tuple)) and len(bbox) == 4 else (0, 0, 0, 0),
                extra={"map_kind": map_kind},
            )
            nodes.append(node)
            sg.add_node(node)

        # 3. 建立相邻关系（利用 bbox 中心点距离）
        for i, a in enumerate(nodes):
            if not a.bbox:
                continue
            ca = FloorPlanParser._center(a.bbox)
            for j in range(i + 1, len(nodes)):
                b = nodes[j]
                if not b.bbox:
                    continue
                cb = FloorPlanParser._center(b.bbox)
                d = FloorPlanParser._dist(ca, cb)
                # 这个阈值可以后续调参
                if d < 0.2:
                    sg.add_rel(SGRelation(source=a.id, target=b.id, type="adjacent"))
                    sg.add_rel(SGRelation(source=b.id, target=a.id, type="adjacent"))

        # 4. 为出口、重点区域创建语义锚点
        for n in nodes:
            txt = n.text
            if "挂号" in txt:
                sg.add_rel(SGRelation(source=n.id, target="fp_semantic_registration", type="label"))
            if "急诊" in txt:
                sg.add_rel(SGRelation(source=n.id, target="fp_semantic_emergency", type="label"))
            if "候诊" in txt:
                sg.add_rel(SGRelation(source=n.id, target="fp_semantic_waiting", type="label"))

        return sg, map_kind

    @staticmethod
    def _center(bbox: Tuple[float, float, float, float]) -> Tuple[float, float]:
        x1, y1, x2, y2 = bbox
        return (x1 + x2) / 2.0, (y1 + y2) / 2.0

    @staticmethod
    def _dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])


class SceneGraphFusion:
    """
    负责把「真实场景 SceneGraph」和「结构图 SceneGraph」合并成一个大图
    """

    @staticmethod
    def merge(real_graph: SceneGraph, floor_graph: SceneGraph) -> SceneGraph:
        merged = SceneGraph()

        # 1. 直接合并节点/边，前缀区分来源
        for n in real_graph.nodes:
            merged.add_node(n)
        for n in floor_graph.nodes:
            merged.add_node(n)

        for r in real_graph.relations:
            merged.add_rel(r)
        for r in floor_graph.relations:
            merged.add_rel(r)

        # 2. TODO：这里可以加"对齐逻辑"，例如：
        #   - 当前摄像头看到的"门诊二部" 与 floor_graph 中同名节点建立 same_as
        #   - 通过 OCR 文本匹配
        # 先给一个非常简单的 same_text 连接

        real_label_nodes = [n for n in real_graph.nodes if n.type in ("ocr", "object")]
        floor_label_nodes = [n for n in floor_graph.nodes if n.type in ("room", "zone", "facility", "label")]

        for rn in real_label_nodes:
            txt_r = (rn.text or rn.cls or "").strip()
            if not txt_r:
                continue
            for fn in floor_label_nodes:
                txt_f = (fn.text or fn.cls or "").strip()
                if not txt_f:
                    continue
                # 非严格匹配：包含关系即可
                if txt_r in txt_f or txt_f in txt_r:
                    merged.add_rel(SGRelation(source=rn.id, target=fn.id, type="same_semantic"))
                    merged.add_rel(SGRelation(source=fn.id, target=rn.id, type="same_semantic"))

        return merged

