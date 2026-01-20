from dataclasses import dataclass
from typing import Dict, Any

from ...risk_layer.interfaces import Vec2, WorldObject, WorldSnapshot, Zone


@dataclass(frozen=True)
class ContextSnapshot:
    data: Dict[str, Any]


def build_world_snapshot(system_snapshot: dict) -> WorldSnapshot:
    self_info = system_snapshot.get("self", {})
    position = self_info.get("position") or {}
    velocity = self_info.get("velocity") or {}
    heading = self_info.get("heading", 0.0)

    def _vec2(value):
        if isinstance(value, Vec2):
            return value
        if isinstance(value, dict):
            return Vec2(float(value.get("x", 0.0)), float(value.get("y", 0.0)))
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return Vec2(float(value[0]), float(value[1]))
        return Vec2(0.0, 0.0)

    objects = []
    for obj in system_snapshot.get("objects", []):
        if isinstance(obj, WorldObject):
            objects.append(obj)
            continue
        if isinstance(obj, dict):
            objects.append(
                WorldObject(
                    object_id=str(obj.get("object_id", "unknown")),
                    position=_vec2(obj.get("position", {})),
                    velocity=_vec2(obj["velocity"]) if "velocity" in obj and obj["velocity"] is not None else None,
                    radius=float(obj.get("radius", 0.0)),
                    kind=str(obj.get("kind", "unknown")),
                    acceleration=_vec2(obj["acceleration"]) if "acceleration" in obj and obj["acceleration"] is not None else None,
                )
            )

    zones = []
    for zone in system_snapshot.get("restricted_zones", []):
        if isinstance(zone, Zone):
            zones.append(zone)
            continue
        if isinstance(zone, dict):
            zones.append(
                Zone(
                    zone_id=str(zone.get("zone_id", "unknown")),
                    center=_vec2(zone.get("center", {})),
                    radius=float(zone.get("radius", 0.0)),
                )
            )

    return WorldSnapshot(
        ts=float(system_snapshot.get("ts", 0.0)),
        self_position=_vec2(position),
        self_velocity=_vec2(velocity),
        self_heading=float(heading),
        objects=objects,
        restricted_zones=zones,
    )
