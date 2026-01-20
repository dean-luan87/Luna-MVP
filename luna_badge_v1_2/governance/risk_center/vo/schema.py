from dataclasses import dataclass
from typing import Optional

from ...risk_layer.interfaces import Vec2


SCHEMA_VERSION = "risk.vo.v1"


@dataclass(frozen=True)
class RelativeState:
    self_position: Vec2
    self_velocity: Vec2
    other_position: Vec2
    other_velocity: Vec2


@dataclass(frozen=True)
class RiskProjectionVO:
    time_to_risk: Optional[float]
    min_distance: Optional[float]
    level: str
    schema_version: str = SCHEMA_VERSION
