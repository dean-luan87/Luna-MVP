from dataclasses import dataclass

from ..interfaces import Vec2


@dataclass(frozen=True)
class RelativeState:
    rel_pos: Vec2
    rel_vel: Vec2
    distance: float
    closing_speed: float
