"""
Dynamic Object - 可移动对象（最小化）

B2 v0.2: 不需要类别，不需要"是人还是车"
只关心：位置、速度、置信度
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict


@dataclass
class BoundingBox:
    """边界框（简化）"""
    x1: float
    y1: float
    x2: float
    y2: float
    
    def translate(self, dx: float, dy: float) -> 'BoundingBox':
        """平移"""
        return BoundingBox(
            x1=self.x1 + dx,
            y1=self.y1 + dy,
            x2=self.x2 + dx,
            y2=self.y2 + dy,
        )
    
    def to_polygon(self) -> List[List[float]]:
        """转换为多边形（4 个点）"""
        return [
            [self.x1, self.y1],
            [self.x2, self.y1],
            [self.x2, self.y2],
            [self.x1, self.y2],
        ]


@dataclass
class Vector2D:
    """2D 向量（速度）"""
    x: float = 0.0
    y: float = 0.0


@dataclass
class DynamicObject:
    """
    可移动对象（最小化）
    
    ⚠️ 不需要类别
    ⚠️ 不需要"是人还是车"
    """
    obj_id: str
    bbox: BoundingBox
    velocity: Vector2D  # 可为空（默认 0）
    confidence: float  # 对象置信度
    meta: Dict[str, Any] = field(default_factory=dict)  # 额外信息

