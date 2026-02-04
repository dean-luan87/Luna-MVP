from luna_badge_v1_2.governance.risk_layer.evaluator import RiskEvaluator
from luna_badge_v1_2.governance.risk_layer.interfaces import Vec2, WorldSnapshot
from luna_badge_v1_2.governance.risk_layer.invariants import assert_risk_invariants


def test_risk_signal_has_no_forbidden_fields():
    snapshot = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(0.0, 0.0),
        self_heading=0.0,
        objects=[],
        restricted_zones=[],
    )
    signal = RiskEvaluator().evaluate(snapshot, horizon_sec=3.0)
    assert_risk_invariants(signal)


def test_risk_evaluator_never_raises():
    snapshot = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(0.0, 0.0),
        self_heading=0.0,
        objects=[],
        restricted_zones=[],
    )
    signal = RiskEvaluator().evaluate(snapshot, horizon_sec=-1.0)
    assert signal.risk_level == "UNKNOWN"
