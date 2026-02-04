from dataclasses import dataclass
from typing import List, Optional


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


@dataclass(frozen=True)
class WorldSnapshot:
    ts: float
    self_position: Vec2
    self_velocity: Vec2
    self_heading: float
    objects: List[WorldObject]
    restricted_zones: List[Zone]
