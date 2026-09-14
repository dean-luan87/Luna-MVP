"""
Simulated State - 未来状态（模拟帧）

B2 v0.2: 未来时间点的状态快照
"""

from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class SimulatedState:
    """
    未来状态（模拟帧）
    
    B2 v0.2: 在时间 t 的状态快照
    """
    t: float  # 相对当前时间（秒）
    corridor: Any  # Polygon（简化用 List[List[float]]）
    object_boxes: List[Any] = field(default_factory=list)  # List[Polygon]

