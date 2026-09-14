from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any


@dataclass(frozen=True)
class MotionSample:
    ts: float
    position_xy: Tuple[float, float]
    heading_deg: Optional[float] = None
    speed_mps: Optional[float] = None
    source: str = "unknown"
    confidence: float = 0.5


@dataclass(frozen=True)
class NavigationGoal:
    goal_id: str
    goal_type: str
    target_xy: Optional[Tuple[float, float]] = None
    semantic: Optional[str] = None


class PathKind(str, Enum):
    MAIN = "main"
    BRANCH = "branch"


@dataclass
class PathSegment:
    segment_id: str
    kind: PathKind
    start_ts: float
    last_ts: float
    avg_heading_deg: Optional[float] = None
    avg_speed_mps: Optional[float] = None
    parent_main_id: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PathStackState:
    main: PathSegment
    active_branch: Optional[PathSegment] = None


class RoiKind(str, Enum):
    TRAFFIC_SIGNAL = "traffic_signal"
    CROSSWALK = "crosswalk"
    OBSTACLE = "obstacle"
    CONSTRUCTION = "construction"
    EXIT_AREA = "exit_area"
    ENTRANCE = "entrance"
    ELEVATOR = "elevator"
    STAIR = "stair"
    PATH_FORK = "path_fork"
    METRO_ARRIVAL = "metro_arrival"
    BUS_ARRIVAL = "bus_arrival"


class RoiPriority(int, Enum):
    SAFETY = 3
    ROUTE = 2
    CONTEXT = 1
    LOW = 0


@dataclass(frozen=True)
class AttentionHint:
    hint_id: str
    roi_kind: RoiKind
    priority: RoiPriority
    area_circle: Optional[Tuple[float, float, float]] = None
    area_rect_img: Optional[Tuple[int, int, int, int]] = None
    reason_codes: List[str] = field(default_factory=list)
    confidence: float = 0.5
    ttl_s: float = 3.0
    created_ts: float = 0.0
    meta: Dict[str, Any] = field(default_factory=dict)
