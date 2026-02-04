# core/navigation/scene_node.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum, auto
import time


class SceneNodeType(Enum):
    """场景节点类型，统一环境信息表达."""
    UNKNOWN = auto()

    # 导航相关
    PATH = auto()              # 路径线 / 可通行区域
    TURNING_POINT = auto()     # 转弯点
    STAIR = auto()             # 台阶 / 楼梯
    RAMP = auto()              # 斜坡
    ELEVATOR = auto()
    ESCALATOR = auto()
    DOOR = auto()
    CROSSWALK = auto()         # 斑马线 / 人行横道

    # 人群 & 车辆
    PERSON = auto()
    CROWD = auto()
    WHEELCHAIR = auto()
    BICYCLE = auto()
    CAR = auto()
    BUS = auto()

    # 标识 & 关键点
    SIGN = auto()              # 指示牌（出口、厕所等）
    SERVICE_DESK = auto()      # 服务台 / 咨询处
    COUNTER = auto()           # 窗口 / 办事柜台

    # 危险相关
    HAZARD = auto()            # 危险泛型（坑、障碍、施工等）
    EDGE = auto()              # 边缘、台阶边
    WATER = auto()             # 水体
    HOLE = auto()              # 洞
    OBSTACLE = auto()          # 障碍物（箱子、路障等）


@dataclass
class SceneNode:
    """
    场景节点：统一所有"环境要素"的表示。

    - type: 节点类型（如 STAIR / SIGN / HAZARD）
    - position_2d: 在相机平面的归一化坐标 (x, y) ∈ [0,1]
    - distance_m: 估计距离（可空）
    - bbox: YOLO 等检测的原始框 (x1, y1, x2, y2) 归一化 [0,1]
    - confidence: 综合置信度（多源融合后的）
    - tags: 额外标签，例如 {"label": "stairs", "text": "出口"}
    """
    node_id: str
    type: SceneNodeType
    frame_id: int
    created_at: float
    last_seen_at: float

    position_2d: Tuple[float, float]
    distance_m: Optional[float] = None
    bbox: Optional[Tuple[float, float, float, float]] = None  # (x1, y1, x2, y2) in [0,1]

    confidence: float = 0.5
    source: str = "unknown"   # "yolo" / "ocr" / "map" / "fusion"

    tags: Dict[str, Any] = field(default_factory=dict)
    # 多帧融合信息
    seen_count: int = 1
    frame_ids: List[int] = field(default_factory=list)

    def mark_seen(self, frame_id: int, timestamp: Optional[float] = None) -> None:
        self.last_seen_at = timestamp or time.time()
        self.seen_count += 1
        self.frame_ids.append(frame_id)

    def age(self, now: Optional[float] = None) -> float:
        """距离首次出现的时间（秒）."""
        now = now or time.time()
        return now - self.created_at

    def idle_time(self, now: Optional[float] = None) -> float:
        """距离最后一次出现的时间（秒）."""
        now = now or time.time()
        return now - self.last_seen_at

    def iou(self, other: "SceneNode") -> float:
        """计算两个节点 bbox 的 IoU，用于跟踪/融合."""
        if not self.bbox or not other.bbox:
            return 0.0
        x1, y1, x2, y2 = self.bbox
        ox1, oy1, ox2, oy2 = other.bbox

        inter_x1 = max(x1, ox1)
        inter_y1 = max(y1, oy1)
        inter_x2 = min(x2, ox2)
        inter_y2 = min(y2, oy2)

        if inter_x2 <= inter_x1 or inter_y2 <= inter_y1:
            return 0.0

        inter_area = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
        self_area = (x2 - x1) * (y2 - y1)
        other_area = (ox2 - ox1) * (oy2 - oy1)
        union_area = self_area + other_area - inter_area
        if union_area <= 0:
            return 0.0
        return inter_area / union_area

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "type": self.type.name,
            "frame_id": self.frame_id,
            "created_at": self.created_at,
            "last_seen_at": self.last_seen_at,
            "position_2d": self.position_2d,
            "distance_m": self.distance_m,
            "bbox": self.bbox,
            "confidence": self.confidence,
            "source": self.source,
            "tags": self.tags,
            "seen_count": self.seen_count,
            "frame_ids": self.frame_ids,
        }

