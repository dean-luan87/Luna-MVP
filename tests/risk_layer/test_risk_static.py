from luna_badge_v1_2.governance.risk_layer.interfaces import (
    Vec2,
    WorldObject,
    WorldSnapshot,
    Zone,
)
from luna_badge_v1_2.governance.risk_layer.static_risk import evaluate_static_collision


def _snapshot(self_pos, self_vel, objects):
    return WorldSnapshot(
        ts=0.0,
        self_position=self_pos,
        self_velocity=self_vel,
        self_heading=0.0,
        objects=objects,
        restricted_zones=[],
    )


def test_static_collision_within_horizon():
    snap = _snapshot(
        Vec2(0.0, 0.0),
        Vec2(1.0, 0.0),
        [
            WorldObject("o1", Vec2(2.0, 0.0), None, 0.5, "obstacle"),
        ],
    )
    signal = evaluate_static_collision(snap, horizon_sec=3.0)
    assert signal is not None
    assert signal.risk_type == "STATIC_COLLISION"


def test_static_collision_outside_horizon():
    snap = _snapshot(
        Vec2(0.0, 0.0),
        Vec2(1.0, 0.0),
        [
            WorldObject("o1", Vec2(10.0, 0.0), None, 0.5, "obstacle"),
        ],
    )
    signal = evaluate_static_collision(snap, horizon_sec=2.0)
    assert signal is None
