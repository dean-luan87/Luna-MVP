"""
导航状态单独抽出来 (v1.2.0)
把「导航当前在干嘛」这件事变成一个干净的对象，方便 routes / 诊断 / 日志查询
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time


@dataclass
class NavStep:
    """单个导航步骤，比如：直行50米、左转、上楼梯"""
    index: int
    instruction: str
    distance_m: Optional[float] = None
    action: Optional[str] = None  # 'straight' | 'turn_left' | 'turn_right' | 'stairs' ...
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NavRoute:
    """路径整体信息（可接 path_planner 的输出）"""
    origin: str
    destination: str
    steps: List[NavStep] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NavigationStatus:
    """对外暴露的导航状态，方便 /api/navigation/status 直接返回"""
    state: str = "IDLE"  # IDLE / NAVIGATING / PAUSED / COMPLETED / CANCELED / ERROR
    destination: Optional[str] = None
    route: Optional[NavRoute] = None
    current_step_index: int = -1
    last_update_ts: float = field(default_factory=lambda: time.time())
    reason: Optional[str] = None  # 最近一次状态变化原因（暂停、取消、完成说明）
    hazards: List[Dict[str, Any]] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "state": self.state,
            "destination": self.destination,
            "current_step_index": self.current_step_index,
            "last_update_ts": self.last_update_ts,
            "reason": self.reason,
            "hazards": self.hazards,
            "extra": self.extra,
            "route": {
                "origin": self.route.origin,
                "destination": self.route.destination,
                "steps": [
                    {
                        "index": s.index,
                        "instruction": s.instruction,
                        "distance_m": s.distance_m,
                        "action": s.action,
                        "meta": s.meta,
                    }
                    for s in (self.route.steps if self.route else [])
                ],
                "raw_data": self.route.raw_data if self.route else {},
            }
            if self.route
            else None,
        }



