"""
World Snapshot - 抽象输入（对接真实 pipeline 的"统一口径"）

职责：
- 将真实 pipeline 的输出（modeling_result / navigation_result / world_update）
  映射为 B2 能理解的统一格式
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorldObject:
    """世界对象"""
    obj_id: str
    cls: str
    bbox: Optional[List[float]] = None
    pos: Optional[List[float]] = None
    vel: Optional[List[float]] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EgoPose:
    """自位姿"""
    heading: float = 0.0
    speed: float = 0.0
    pos: Optional[List[float]] = None


@dataclass
class WorldSnapshot:
    """世界快照（B2 的输入）"""
    timestamp: float
    ego: EgoPose
    objects: List[WorldObject] = field(default_factory=list)
    texts: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

