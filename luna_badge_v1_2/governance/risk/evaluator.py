from dataclasses import dataclass
from typing import Optional

from .risk_signal import RiskSignal
from .world_snapshot import Vec2, WorldObject, WorldSnapshot, Zone


def _distance(a: Vec2, b: Vec2) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return (dx * dx + dy * dy) ** 0.5


def _project_position(pos: Vec2, vel: Vec2, dt: float) -> Vec2:
    return Vec2(pos.x + vel.x * dt, pos.y + vel.y * dt)


def _time_to_collision(
    self_pos: Vec2,
    self_vel: Vec2,
    obj: WorldObject,
    horizon_sec: float,
) -> Optional[float]:
    if obj.velocity is None:
        return None
    rel_pos = Vec2(obj.position.x - self_pos.x, obj.position.y - self_pos.y)
    rel_vel = Vec2(obj.velocity.x - self_vel.x, obj.velocity.y - self_vel.y)
    v2 = rel_vel.x * rel_vel.x + rel_vel.y * rel_vel.y
    if v2 == 0:
        return None
    t = -(rel_pos.x * rel_vel.x + rel_pos.y * rel_vel.y) / v2
    if t < 0 or t > horizon_sec:
        return None
    closest = Vec2(self_pos.x + self_vel.x * t, self_pos.y + self_vel.y * t)
    obj_at_t = Vec2(obj.position.x + obj.velocity.x * t, obj.position.y + obj.velocity.y * t)
    if _distance(closest, obj_at_t) <= obj.radius:
        return t
    return None


def _static_collision(
    self_pos: Vec2,
    self_vel: Vec2,
    obj: WorldObject,
    horizon_sec: float,
) -> Optional[float]:
    if obj.velocity is not None:
        return None
    projected = _project_position(self_pos, self_vel, horizon_sec)
    if _distance(projected, obj.position) <= obj.radius:
        return horizon_sec
    return None


def _zone_violation(self_pos: Vec2, self_vel: Vec2, zone: Zone, horizon_sec: float) -> Optional[float]:
    projected = _project_position(self_pos, self_vel, horizon_sec)
    if _distance(projected, zone.center) <= zone.radius:
        return horizon_sec
    return None


@dataclass(frozen=True)
class RiskEvaluator:
    def evaluate(self, snapshot: WorldSnapshot, horizon_sec: float = 3.0) -> RiskSignal:
        try:
            if horizon_sec <= 0:
                return RiskSignal(False, "UNKNOWN", "UNKNOWN", None, None)

            risk_present = False
            risk_level = "LOW"
            risk_type = "UNKNOWN"
            time_to_risk = None

            for obj in snapshot.objects:
                ttc = _time_to_collision(
                    snapshot.self_position,
                    snapshot.self_velocity,
                    obj,
                    horizon_sec,
                )
                if ttc is not None:
                    risk_present = True
                    risk_level = "HIGH"
                    risk_type = "DYNAMIC_COLLISION"
                    time_to_risk = ttc
                    break

                ttc = _static_collision(
                    snapshot.self_position,
                    snapshot.self_velocity,
                    obj,
                    horizon_sec,
                )
                if ttc is not None:
                    risk_present = True
                    risk_level = "HIGH"
                    risk_type = "STATIC_COLLISION"
                    time_to_risk = ttc
                    break

            if not risk_present:
                for zone in snapshot.restricted_zones:
                    ttv = _zone_violation(
                        snapshot.self_position,
                        snapshot.self_velocity,
                        zone,
                        horizon_sec,
                    )
                    if ttv is not None:
                        risk_present = True
                        risk_level = "HIGH"
                        risk_type = "ZONE_VIOLATION"
                        time_to_risk = ttv
                        break

            return RiskSignal(
                risk_present=risk_present,
                risk_level=risk_level if risk_present else "LOW",
                risk_type=risk_type if risk_present else "UNKNOWN",
                time_to_risk=time_to_risk,
                confidence=None,
            )
        except Exception:
            return RiskSignal(False, "UNKNOWN", "UNKNOWN", None, None)
