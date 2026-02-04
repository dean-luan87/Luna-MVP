"""
Motion Corridor - 行进 Corridor（未来路径）

B2 v0.2: 未来路径表示

来源规则：
- 有导航 → 来自 NavigationExecutor
- 无导航 → ego heading + speed 构造直走 corridor
"""

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Any, Dict


@dataclass
class MotionCorridor:
    """
    行进 Corridor（未来路径）
    
    B2 v0.2: 未来 5~10 秒的占用区域
    """
    polygon: Any  # 未来 5~10 秒的占用区域（Polygon，简化用 List[List[float]]）
    horizon_sec: float  # 时间窗口（秒）
    source: Literal["NAV", "EGO"]  # 来源：导航 / 自运动
    width_m: float  # 走廊宽度（米）
    meta: Dict[str, Any] = field(default_factory=dict)  # 额外信息

