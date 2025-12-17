"""
Embodiment Profiles (C-2)

我是谁/身体形态/单位体系（米 vs 步）
"""

from dataclasses import dataclass
from enum import Enum


class DistanceUnit(Enum):
    """距离单位"""
    METER = "meter"
    STEP = "step"


class DirectionReference(Enum):
    """方向参考系"""
    BODY_RELATIVE = "body_relative"  # 身体相对
    WORLD_RELATIVE = "world_relative"  # 世界相对


class Precision(Enum):
    """精度级别"""
    COARSE = "coarse"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class EmbodimentProfile:
    """
    EmbodimentProfile 数据类
    
    至少包含：
    - name：blind / toy / default
    - distance_unit：meter / step
    - direction_reference：body_relative / world_relative
    - precision：coarse/medium/high
    """
    name: str
    distance_unit: DistanceUnit
    direction_reference: DirectionReference
    precision: Precision
    
    # 可选扩展字段
    extra: dict = None
    
    def __post_init__(self):
        if self.extra is None:
            self.extra = {}
