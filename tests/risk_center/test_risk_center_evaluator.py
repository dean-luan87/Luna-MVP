from luna_badge_v1_2.governance.risk_center.aggregator.evaluator import RiskCenter


def test_risk_center_evaluate():
    center = RiskCenter()
    signal = center.evaluate(
        {
            "ts": 0.0,
            "self": {"position": {"x": 0.0, "y": 0.0}, "velocity": {"x": 0.0, "y": 0.0}, "heading": 0.0},
            "objects": [],
            "restricted_zones": [],
        }
    )
    assert signal.domain == "VISION"
    assert signal.level in {"NONE", "LOW", "MEDIUM", "HIGH"}
