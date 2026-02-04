"""
Task Corridor v0.2 - 任务走廊（导航 route 或 heading 兜底）

职责：
- 构建 B2 的"预演舞台"
- 有导航任务 → 用 route
- 无导航任务 → 用 heading 兜底
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskCorridor:
    """任务走廊"""
    mode: str  # "ROUTE" | "HEADING"
    points: List[List[float]] = field(default_factory=list)  # polyline, may be empty in HEADING mode
    width_m: float = 1.2
    horizon_sec: float = 8.0
    meta: Dict[str, Any] = field(default_factory=dict)

