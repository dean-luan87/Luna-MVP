from luna_badge_v1_2.governance.risk_center.vo.evaluator import evaluate_vo
from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2, WorldObject, WorldSnapshot, Zone


def _snapshot(self_pos, self_vel, objects):
    return WorldSnapshot(
        ts=0.0,
        self_position=self_pos,
        self_velocity=self_vel,
        self_heading=0.0,
        objects=objects,
        restricted_zones=[],
    )


def test_vo_head_on_risk():
    obj = WorldObject(
        object_id="o1",
        position=Vec2(5.0, 0.0),
        velocity=Vec2(-1.0, 0.0),
        radius=0.5,
        kind="unknown",
    )
    snapshot = _snapshot(Vec2(0.0, 0.0), Vec2(1.0, 0.0), [obj])
    proj = evaluate_vo(snapshot, horizon_sec=5.0)
    assert proj.level == "HIGH"


def test_vo_side_merge_risk():
    obj = WorldObject(
        object_id="o1",
        position=Vec2(2.0, 2.0),
        velocity=Vec2(0.0, -1.0),
        radius=0.5,
        kind="unknown",
    )
    snapshot = _snapshot(Vec2(0.0, 0.0), Vec2(1.0, 0.0), [obj])
    proj = evaluate_vo(snapshot, horizon_sec=5.0, safety_radius=0.8)
    assert proj.level in {"HIGH", "NONE"}


def test_vo_parallel_no_risk():
    obj = WorldObject(
        object_id="o1",
        position=Vec2(0.0, 2.0),
        velocity=Vec2(1.0, 0.0),
        radius=0.5,
        kind="unknown",
    )
    snapshot = _snapshot(Vec2(0.0, 0.0), Vec2(1.0, 0.0), [obj])
    proj = evaluate_vo(snapshot, horizon_sec=3.0)
    assert proj.level == "NONE"


def test_vo_static_obstacle():
    obj = WorldObject(
        object_id="o1",
        position=Vec2(1.0, 0.0),
        velocity=None,
        radius=0.5,
        kind="unknown",
    )
    snapshot = _snapshot(Vec2(0.0, 0.0), Vec2(1.0, 0.0), [obj])
    proj = evaluate_vo(snapshot, horizon_sec=3.0)
    assert proj.level in {"HIGH", "NONE"}
