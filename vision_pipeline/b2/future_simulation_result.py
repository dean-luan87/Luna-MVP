"""
Future Simulation Result - B2 v0.2 Part 1

输出（不判断，只标记）

⚠️ 注意：
这里不叫 risk，不叫 danger，只叫 overlap / enter / collide
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class CollisionEvent:
    """可能发生空间重叠的事件"""
    obj_id: str
    t_sec: float  # 发生时间（秒）
    overlap_ratio: float  # 重叠比例
    distance: float  # 距离（米）
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegionEnterEvent:
    """是否会进入风险区域"""
    region_id: str
    region_type: str
    t_sec: float  # 进入时间（秒）
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FutureSimulationResult:
    """
    B2 v0.2 Part 1: FutureSimulation 输出
    
    Task 1.3: 定义 FutureSimulationResult（禁止语义）
    
    ⚠️ 强约束：
    - 不允许出现 risk / safe / warn
    - 不允许做策略判断
    - 这是"事实缓存"，不是"判断"
    """
    horizon_sec: float  # 预演到多少秒
    collisions: List[dict] = field(default_factory=list)  # [{object_id, t, distance}]
    path_overlap: bool = False  # 是否有物体与未来路径重叠
    region_enter: List[dict] = field(default_factory=list)  # [{region_id, t}]
    timestamp: float = 0.0

