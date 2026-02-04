from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from .schema import MotionSample, NavigationGoal


@dataclass
class PalContext:
    now_ts: float
    motion_window: List[MotionSample] = field(default_factory=list)
    goal: Optional[NavigationGoal] = None
    b_readonly: Dict[str, Any] = field(default_factory=dict)
    attention_preferences: Dict[str, float] = field(default_factory=dict)
    roi_recent_hits: Dict[str, Any] = field(default_factory=dict)
