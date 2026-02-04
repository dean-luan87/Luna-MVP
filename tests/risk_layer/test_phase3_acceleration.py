from luna_badge_v1_2.governance.risk_center.phase3.acceleration import evaluate_acceleration
from luna_badge_v1_2.governance.risk_center.phase3.schema import RiskAcceleration


def test_acceleration_insufficient_data():
    assert evaluate_acceleration([]) == RiskAcceleration.UNKNOWN
    assert evaluate_acceleration([{"time_to_risk": 2.0}, {"time_to_risk": 1.9}]) == RiskAcceleration.UNKNOWN


def test_acceleration_increasing_trend():
    history = [
        {"time_to_risk": 3.0},
        {"time_to_risk": 2.8},
        {"time_to_risk": 2.5},
        {"time_to_risk": 2.2},
    ]
    assert evaluate_acceleration(history) == RiskAcceleration.INCREASING


def test_acceleration_decreasing_trend():
    history = [
        {"time_to_risk": 1.0},
        {"time_to_risk": 1.2},
        {"time_to_risk": 1.4},
    ]
    assert evaluate_acceleration(history) == RiskAcceleration.DECREASING
