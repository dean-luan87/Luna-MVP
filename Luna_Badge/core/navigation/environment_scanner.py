# core/navigation/environment_scanner.py
from __future__ import annotations

from typing import List, Dict, Any, Iterable, Optional
import logging
import time

from .scene_context import FrameContext
from .scene_node import SceneNode, SceneNodeType
from .scene_node_layer import SceneNodeLayer

logger = logging.getLogger(__name__)


class EnvironmentScanner:
    """
    E 模块：从 YOLO / OCR / 其它传感器结果中提取 SceneNode，
    再交给 SceneNodeLayer 做时序融合，最后提供给 DirectionEvaluator / 场景推理使用。

    注意：这里不做"危险级别判断"，只负责"识别场景元素"。
    真正危险等级可以在 DangerEnginePro / Scene Reasoning 中去计算。
    """

    def __init__(self, node_layer: Optional[SceneNodeLayer] = None):
        self.layer = node_layer or SceneNodeLayer()

    # --- 公共入口 ---

    def process(
        self,
        frame_ctx: FrameContext,
        yolo_results: Iterable[Dict[str, Any]],
        ocr_results: Iterable[Dict[str, Any]] = (),
    ):
        """
        处理一帧的检测结果：
        - 将 YOLO/ OCR 转为 SceneNode
        - 调用 SceneNodeLayer.update_from_detections 做多帧融合
        - 返回"稳定节点列表"
        """
        raw_nodes: List[SceneNode] = []
        raw_nodes.extend(self._from_yolo(frame_ctx, yolo_results))
        raw_nodes.extend(self._from_ocr(frame_ctx, ocr_results))

        stable_nodes = self.layer.update_from_detections(frame_ctx, raw_nodes)
        logger.debug("[EnvironmentScanner] frame=%s raw=%s stable=%s",
                     frame_ctx.frame_id, len(raw_nodes), len(stable_nodes))
        return stable_nodes

    # --- YOLO → SceneNode 的映射规则 ---

    def _from_yolo(
        self,
        frame_ctx: FrameContext,
        yolo_results: Iterable[Dict[str, Any]],
    ) -> List[SceneNode]:
        """
        将 YOLO 输出映射到统一的 SceneNode。
        典型 yolo_result 结构示例：
        {
            "label": "person",
            "confidence": 0.82,
            "bbox": [x1, y1, x2, y2],   # 归一化 [0,1]
            "distance_m": 3.2           # 可选
        }
        """
        nodes: List[SceneNode] = []
        ts = frame_ctx.timestamp

        for det in yolo_results:
            label: str = det.get("label", "").lower()
            conf: float = float(det.get("confidence", 0.0))
            bbox = det.get("bbox")
            distance_m = det.get("distance_m")

            node_type = self._map_label_to_type(label)
            if node_type is None:
                continue

            # 简单过滤：置信度太低、面积太小都先丢掉
            if conf < 0.4:
                continue
            if bbox and self._bbox_area(bbox) < 0.01:
                continue

            # 位置用 bbox 中心点
            if bbox:
                x1, y1, x2, y2 = bbox
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
            else:
                cx, cy = 0.5, 0.5

            node = SceneNode(
                node_id="tmp",  # 会在 SceneNodeLayer 中重写
                type=node_type,
                frame_id=frame_ctx.frame_id,
                created_at=ts,
                last_seen_at=ts,
                position_2d=(cx, cy),
                distance_m=distance_m,
                bbox=tuple(bbox) if bbox else None,
                confidence=conf,
                source="yolo",
                tags={"label": label},
                seen_count=1,
                frame_ids=[frame_ctx.frame_id],
            )
            nodes.append(node)

        return nodes

    # --- OCR → SceneNode（标识类信息） ---

    def _from_ocr(
        self,
        frame_ctx: FrameContext,
        ocr_results: Iterable[Dict[str, Any]],
    ) -> List[SceneNode]:
        """
        OCR 结构示例：
        {
            "text": "出口 Exit",
            "bbox": [x1, y1, x2, y2],
            "confidence": 0.85
        }
        """
        nodes: List[SceneNode] = []
        ts = frame_ctx.timestamp

        for det in ocr_results:
            text: str = det.get("text", "")
            conf: float = float(det.get("confidence", 0.0))
            bbox = det.get("bbox")

            if conf < 0.5 or not text.strip():
                continue

            node_type = self._classify_text(text)
            if node_type is None:
                continue

            if bbox:
                x1, y1, x2, y2 = bbox
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
            else:
                cx, cy = 0.5, 0.2

            node = SceneNode(
                node_id="tmp",
                type=node_type,
                frame_id=frame_ctx.frame_id,
                created_at=ts,
                last_seen_at=ts,
                position_2d=(cx, cy),
                distance_m=None,
                bbox=tuple(bbox) if bbox else None,
                confidence=conf,
                source="ocr",
                tags={"text": text},
                seen_count=1,
                frame_ids=[frame_ctx.frame_id],
            )
            nodes.append(node)

        return nodes

    # --- label → SceneNodeType 的映射逻辑 ---

    def _map_label_to_type(self, label: str) -> Optional[SceneNodeType]:
        """
        将 YOLO 类别统一映射到 SceneNodeType。
        这里只做一个比较粗的映射，后续可以扩展成外部配置表。
        """
        if label in {"person"}:
            return SceneNodeType.PERSON
        if label in {"wheelchair"}:
            return SceneNodeType.WHEELCHAIR
        if label in {"car", "truck", "bus"}:
            return SceneNodeType.CAR if label != "bus" else SceneNodeType.BUS
        if label in {"stairs", "stair", "staircase"}:
            return SceneNodeType.STAIR
        if label in {"ramp"}:
            return SceneNodeType.RAMP
        if label in {"door"}:
            return SceneNodeType.DOOR
        if label in {"elevator"}:
            return SceneNodeType.ELEVATOR
        if label in {"escalator"}:
            return SceneNodeType.ESCALATOR
        if label in {"crosswalk"}:
            return SceneNodeType.CROSSWALK
        if label in {"cone", "barrier", "bollard"}:
            return SceneNodeType.OBSTACLE

        # 避免把各种普通物体都当成 HAZARD，这里只映射小部分危险类
        if label in {"hole", "pit"}:
            return SceneNodeType.HOLE
        if label in {"river", "lake", "pool"}:
            return SceneNodeType.WATER

        # 其它不认识的先返回 None，交给更高层逻辑决定要不要用
        return None

    def _classify_text(self, text: str) -> Optional[SceneNodeType]:
        lower = text.lower()
        if "exit" in lower or "出口" in text:
            return SceneNodeType.SIGN
        if "toilet" in lower or "wc" in lower or "卫生间" in text or "洗手间" in text:
            return SceneNodeType.SIGN
        if "service" in lower or "服务台" in text or "咨询" in text:
            return SceneNodeType.SERVICE_DESK
        return SceneNodeType.SIGN  # 默认按指示牌处理

    @staticmethod
    def _bbox_area(bbox) -> float:
        x1, y1, x2, y2 = bbox
        return max(0.0, x2 - x1) * max(0.0, y2 - y1)

