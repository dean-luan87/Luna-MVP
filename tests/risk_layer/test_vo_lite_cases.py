from luna_badge_v1_2.governance.risk_layer.dynamic.vo_lite import evaluate_vo_lite
from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2


def test_head_on_relative_motion_hits():
    event = evaluate_vo_lite(
        self_pos=Vec2(0.0, 0.0),
        self_vel=Vec2(1.0, 0.0),
        other_pos=Vec2(5.0, 0.0),
        other_vel=Vec2(-1.0, 0.0),
        horizon_sec=5.0,
        danger_radius=0.5,
    )
    assert event is not None
    assert event.type == "RELATIVE_MOTION"


def test_parallel_motion_safe():
    event = evaluate_vo_lite(
        self_pos=Vec2(0.0, 0.0),
        self_vel=Vec2(1.0, 0.0),
        other_pos=Vec2(0.0, 5.0),
        other_vel=Vec2(1.0, 0.0),
        horizon_sec=5.0,
        danger_radius=0.5,
    )
    assert event is None


def test_crossing_path_hits():
    event = evaluate_vo_lite(
        self_pos=Vec2(0.0, 0.0),
        self_vel=Vec2(1.0, 0.0),
        other_pos=Vec2(1.0, -2.0),
        other_vel=Vec2(0.0, 1.0),
        horizon_sec=5.0,
        danger_radius=1.0,
    )
    assert event is not None
    assert event.type == "RELATIVE_MOTION"


def test_horizon_sensitivity():
    short = evaluate_vo_lite(
        self_pos=Vec2(0.0, 0.0),
        self_vel=Vec2(1.0, 0.0),
        other_pos=Vec2(5.0, 0.0),
        other_vel=Vec2(-1.0, 0.0),
        horizon_sec=2.0,
        danger_radius=0.5,
    )
    long = evaluate_vo_lite(
        self_pos=Vec2(0.0, 0.0),
        self_vel=Vec2(1.0, 0.0),
        other_pos=Vec2(5.0, 0.0),
        other_vel=Vec2(-1.0, 0.0),
        horizon_sec=5.0,
        danger_radius=0.5,
    )
    assert short is None
    assert long is not None
