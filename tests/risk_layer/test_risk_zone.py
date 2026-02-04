from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2, WorldSnapshot, Zone
from luna_badge_v1_2.governance.risk_layer.zone_risk import evaluate_zone_violation


def test_zone_violation_hits():
    snap = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(1.0, 0.0),
        self_heading=0.0,
        objects=[],
        restricted_zones=[Zone("z1", Vec2(3.0, 0.0), 0.5)],
    )
    signal = evaluate_zone_violation(snap, horizon_sec=3.0)
    assert signal is not None
    assert signal.risk_type == "ZONE_VIOLATION"


def test_zone_violation_miss():
    snap = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(1.0, 0.0),
        self_heading=0.0,
        objects=[],
        restricted_zones=[Zone("z1", Vec2(10.0, 0.0), 0.5)],
    )
    signal = evaluate_zone_violation(snap, horizon_sec=2.0)
    assert signal is None
