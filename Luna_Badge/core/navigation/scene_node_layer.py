# core/navigation/scene_node_layer.py
from __future__ import annotations

from typing import List, Dict, Optional, Iterable
from dataclasses import dataclass, field
import time
import logging
import uuid

from .scene_node import SceneNode, SceneNodeType
from .scene_context import FrameContext

logger = logging.getLogger(__name__)


@dataclass
class SceneNodeLayer:
    """
    场景节点层：负责维护多帧的节点集合，做简单的时序融合 / 去抖动。

    - YOLO、OCR、地图等都可以往这里"注册"节点
    - DirectionEvaluator & 高层 Scene Reasoning 只看这里的输出
    """
    nodes: Dict[str, SceneNode] = field(default_factory=dict)
    max_idle_seconds: float = 2.5   # 多久没看到就删掉
    min_seen_count: int = 2         # 至少出现几帧才认为是真实存在

    def _new_node_id(self) -> str:
        return uuid.uuid4().hex[:8]

    def update_from_detections(
        self,
        frame_ctx: FrameContext,
        raw_nodes: Iterable[SceneNode],
        iou_threshold: float = 0.5,
    ) -> List[SceneNode]:
        """
        用当前帧的"原始节点"（由 EnvironmentScanner 生成）更新内部状态，
        自动做多帧融合和去抖动，返回当前帧之后的"稳定节点列表"。

        raw_nodes: 同一帧上生成的 SceneNode（临时 ID 会被替换）
        """
        now = frame_ctx.timestamp
        logger.debug("[SceneNodeLayer] update_from_detections frame=%s raw_nodes=%s",
                     frame_ctx.frame_id, len(list(raw_nodes)))

        # 为了避免多次遍历，先转成 list
        raw_nodes = list(raw_nodes)

        # 逐个原始节点，尝试与已有节点匹配
        for rn in raw_nodes:
            best_node_id: Optional[str] = None
            best_iou = 0.0

            for node_id, node in self.nodes.items():
                if node.type != rn.type:
                    continue
                iou = node.iou(rn)
                if iou > best_iou:
                    best_iou = iou
                    best_node_id = node_id

            if best_node_id and best_iou >= iou_threshold:
                # 融合到已有节点
                node = self.nodes[best_node_id]
                node.position_2d = rn.position_2d
                node.bbox = rn.bbox or node.bbox
                node.distance_m = rn.distance_m or node.distance_m
                node.confidence = max(node.confidence, rn.confidence)
                node.tags.update(rn.tags)
                node.mark_seen(frame_ctx.frame_id, now)
            else:
                # 新建节点
                new_id = self._new_node_id()
                rn.node_id = new_id
                rn.frame_ids = [frame_ctx.frame_id]
                self.nodes[new_id] = rn

        # 清理过期节点
        self._prune(now)

        # 返回"稳定节点"：出现次数足够 & 信心足够
        stable_nodes = [n for n in self.nodes.values()
                        if n.seen_count >= self.min_seen_count and n.confidence >= 0.4]
        logger.debug("[SceneNodeLayer] stable_nodes=%s total_nodes=%s",
                     len(stable_nodes), len(self.nodes))
        return stable_nodes

    def _prune(self, now: Optional[float] = None) -> None:
        now = now or time.time()
        to_delete = [node_id for node_id, node in self.nodes.items()
                     if node.idle_time(now) > self.max_idle_seconds]
        for node_id in to_delete:
            logger.debug("[SceneNodeLayer] prune node_id=%s", node_id)
            self.nodes.pop(node_id, None)

    # 一些查询接口，给方向/场景推理用
    def query_by_type(self, node_type: SceneNodeType) -> List[SceneNode]:
        return [n for n in self.nodes.values() if n.type == node_type]

    def get_nearest(self, node_type: SceneNodeType) -> Optional[SceneNode]:
        candidates = self.query_by_type(node_type)
        if not candidates:
            return None
        candidates = sorted(
            candidates,
            key=lambda n: (n.distance_m if n.distance_m is not None else 9999.0)
        )
        return candidates[0]

    def to_list(self) -> List[SceneNode]:
        return list(self.nodes.values())

