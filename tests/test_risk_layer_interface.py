from luna_badge_v1_2.governance.risk import (
    RiskEvaluator,
    Vec2,
    WorldObject,
    WorldSnapshot,
    Zone,
)


def test_risk_evaluator_returns_signal():
    snapshot = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(1.0, 0.0),
        self_heading=0.0,
        objects=[
            WorldObject(
                object_id="o1",
                position=Vec2(3.0, 0.0),
                velocity=None,
                radius=0.5,
                kind="obstacle",
            )
        ],
        restricted_zones=[
            Zone(zone_id="z1", center=Vec2(10.0, 0.0), radius=1.0)
        ],
    )
    evaluator = RiskEvaluator()
    signal = evaluator.evaluate(snapshot, horizon_sec=3.0)
    assert signal.risk_present is True
    assert signal.risk_level in {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}
    assert signal.risk_type in {
        "STATIC_COLLISION",
        "DYNAMIC_COLLISION",
        "ZONE_VIOLATION",
        "UNKNOWN",
    }


def test_risk_evaluator_handles_invalid_horizon():
    snapshot = WorldSnapshot(
        ts=0.0,
        self_position=Vec2(0.0, 0.0),
        self_velocity=Vec2(0.0, 0.0),
        self_heading=0.0,
        objects=[],
        restricted_zones=[],
    )
    evaluator = RiskEvaluator()
    signal = evaluator.evaluate(snapshot, horizon_sec=0.0)
    assert signal.risk_level == "UNKNOWN"
