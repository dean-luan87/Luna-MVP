from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2, WorldObject, WorldSnapshot
from luna_badge_v1_2.governance.risk_layer.dynamic_risk import evaluate_dynamic_collision


def _snapshot(self_pos, self_vel, objects):
    return WorldSnapshot(
        ts=0.0,
        self_position=self_pos,
        self_velocity=self_vel,
        self_heading=0.0,
        objects=objects,
        restricted_zones=[],
    )


def test_dynamic_collision_head_on():
    snap = _snapshot(
        Vec2(0.0, 0.0),
        Vec2(1.0, 0.0),
        [
            WorldObject("o1", Vec2(5.0, 0.0), Vec2(-1.0, 0.0), 0.5, "vehicle"),
        ],
    )
    signal = evaluate_dynamic_collision(snap, horizon_sec=3.0)
    assert signal is not None
    assert signal.risk_type == "DYNAMIC_COLLISION"


def test_dynamic_collision_parallel_no_risk():
    snap = _snapshot(
        Vec2(0.0, 0.0),
        Vec2(1.0, 0.0),
        [
            WorldObject("o1", Vec2(0.0, 5.0), Vec2(1.0, 0.0), 0.5, "vehicle"),
        ],
    )
    signal = evaluate_dynamic_collision(snap, horizon_sec=3.0)
    assert signal is None


def test_dynamic_collision_zero_relative_velocity():
    snap = _snapshot(
        Vec2(0.0, 0.0),
        Vec2(1.0, 0.0),
        [
            WorldObject("o1", Vec2(1.0, 0.0), Vec2(1.0, 0.0), 0.5, "vehicle"),
        ],
    )
    signal = evaluate_dynamic_collision(snap, horizon_sec=3.0)
    assert signal is None
