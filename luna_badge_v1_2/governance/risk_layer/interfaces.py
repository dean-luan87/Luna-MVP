from dataclasses import dataclass
from typing import List, Optional, Literal


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float


@dataclass(frozen=True)
class Zone:
    zone_id: str
    center: Vec2
    radius: float


@dataclass(frozen=True)
class WorldObject:
    object_id: str
    position: Vec2
    velocity: Optional[Vec2]
    radius: float
    kind: str
    acceleration: Optional[Vec2] = None


@dataclass(frozen=True)
class WorldSnapshot:
    ts: float
    self_position: Vec2
    self_velocity: Vec2
    self_heading: float
    objects: List[WorldObject]
    restricted_zones: List[Zone]


@dataclass(frozen=True)
class RiskSignal:
    risk_present: bool
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "UNKNOWN"]
    risk_type: Literal[
        "STATIC_COLLISION",
        "DYNAMIC_COLLISION",
        "ZONE_VIOLATION",
        "RELATIVE_MOTION",
        "UNKNOWN",
    ]
    time_to_risk: Optional[float]
    confidence: Optional[float]
    reason_codes: List[str]
