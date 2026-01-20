"""
Future Simulator Input - B2 v0.2 Part 1

输入（来自真实 pipeline）

核心原则：
- 不做理解
- 不做判断
- 只做几何 / 时序层面的预演
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict


@dataclass
class DynamicObject:
    """动态对象（来自 modeling）"""
    obj_id: str
    bbox: List[float]  # [x1, y1, x2, y2]
    velocity: List[float]  # [vx, vy]
    confidence: float
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StaticRegion:
    """静态区域（工地 / 事故 / 人群区域，粗粒度）"""
    region_id: str
    polygon: List[List[float]]  # 多边形顶点
    region_type: str  # "construction", "accident", "crowd", etc.
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FutureSimulatorInput:
    """
    B2 v0.2 Part 1: FutureSimulator 输入
    
    Task 1.2: 定义输入结构（FutureSimulatorInput）
    要求：100% 对齐真实 pipeline，不新增"想象字段"
    
    工程约束：
    - ❌ B2 不允许"补全""猜测""推理缺失字段"
    - ❌ 不允许引用图像帧
    - ✔ 只吃结构化结果
    """
    # 自身状态
    ego_position: tuple  # (x, y)
    ego_heading: tuple  # 单位向量 (dx, dy)
    ego_velocity: float  # m/s
    
    # 当前任务链（可为空）
    ego_path: Optional[List[tuple]] = None  # list[(x, y)] | None
    
    # 来自真实 pipeline
    dynamic_objects: List[dict] = field(default_factory=list)  # ModelingExecutor 输出
    static_regions: List[dict] = field(default_factory=list)  # Navigation / WorldModel
    
    timestamp: float = 0.0

