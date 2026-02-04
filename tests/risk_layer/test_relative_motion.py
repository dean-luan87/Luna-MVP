from luna_badge_v1_2.governance.risk_layer.dynamic.relative_motion import (
    compute_relative_acceleration,
    compute_time_to_closest_approach,
)
from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2


def test_tca_returns_none_when_stationary():
    tca = compute_time_to_closest_approach(Vec2(1.0, 0.0), Vec2(0.0, 0.0))
    assert tca is None


def test_tca_returns_none_when_moving_away():
    tca = compute_time_to_closest_approach(Vec2(1.0, 0.0), Vec2(1.0, 0.0))
    assert tca is None


def test_relative_acceleration_decelerates_closing():
    acc = compute_relative_acceleration(
        self_vel=Vec2(1.0, 0.0),
        self_acc=Vec2(-1.0, 0.0),
        other_vel=Vec2(0.0, 0.0),
        other_acc=Vec2(0.0, 0.0),
    )
    assert acc < 0


def test_relative_acceleration_accelerates_closing():
    acc = compute_relative_acceleration(
        self_vel=Vec2(1.0, 0.0),
        self_acc=Vec2(1.0, 0.0),
        other_vel=Vec2(0.0, 0.0),
        other_acc=Vec2(0.0, 0.0),
    )
    assert acc > 0
