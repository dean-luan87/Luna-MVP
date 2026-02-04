"""
Landmark Observation (v1.4.8 StepB-3)

视觉侧地标观测结构
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class LandmarkType(Enum):
    """地标类型"""
    CROSSWALK = "crosswalk"
    INTERSECTION = "intersection"
    TURN_CORNER = "turn_corner"
    ENTRANCE = "entrance"
    EXIT = "exit"
    STAIRS = "stairs"
    ELEVATOR = "elevator"
    SERVICE_DESK = "service_desk"
    SIGN = "sign"


@dataclass
class LandmarkObservation:
    """
    视觉观测数据结构
    """
    landmark_type: LandmarkType
    confidence: float            # 0~1，来自视觉模型
    direction_hint: Optional[str]  # "left" / "right" / "forward" / "unknown"
    frame_id: str
    timestamp: float
    extra: Dict[str, Any]






