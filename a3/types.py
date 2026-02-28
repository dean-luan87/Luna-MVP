from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class SafetyLevel(str, Enum):
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    DANGER = "DANGER"


class ControlMode(str, Enum):
    ASSISTED = "ASSISTED"
    SHARED = "SHARED"
    GUARDED = "GUARDED"


class PerceptionState(str, Enum):
    NORMAL = "NORMAL"
    DEGRADED = "DEGRADED"


@dataclass
class A3Signals:
    risk_density: float = 0.0
    redline_hit: bool = False
    path_stability: float = 1.0
    branch_count: int = 0
    roi_count: int = 0
    roi_type_entropy: float = 0.0
    occlusion_ratio: float = 0.0
    recent_speak_rate: float = 0.0
    rejected_rate: float = 0.0
    has_goal: bool = False
    explore_mode: bool = False
    ocr_explain_stability: Optional[float] = None
    perception_state: PerceptionState = PerceptionState.NORMAL
    view_confidence: float = 1.0
    frame_quality: str = "GOOD"
    motion_instability: float = 0.0
    path_instability: Optional[float] = None  # Path v0：vision 光流方向一致性，None 时用 1-path_stability
    branch_load: Optional[float] = None  # Branch v0：vision 有效运动方向数量密度，None 时用 branch_count 归一化


@dataclass
class EnvironmentMode:
    complexity_score: float
    safety_level: SafetyLevel
    control_mode: ControlMode
    allowed_errors: bool
    advice_budget_scale: float
    pal_lookahead_m: float
    updated_at_ms: int
    debug: Dict[str, Any] = field(default_factory=dict)  # Stage 2: 含 int 权威字段如 ema_q
