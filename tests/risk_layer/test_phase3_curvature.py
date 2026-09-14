from luna_badge_v1_2.governance.risk_center.phase3.curvature import evaluate_curvature
from luna_badge_v1_2.governance.risk_center.phase3.schema import RiskCurvature


def test_curvature_insufficient_data():
    assert evaluate_curvature([]) == RiskCurvature.UNKNOWN
    assert evaluate_curvature([{"min_distance": 2.0}, {"min_distance": 1.8}]) == RiskCurvature.UNKNOWN


def test_curvature_toward_risk():
    history = [
        {"min_distance": 3.0},
        {"min_distance": 2.5},
        {"min_distance": 2.0},
        {"min_distance": 1.8},
    ]
    assert evaluate_curvature(history) == RiskCurvature.TOWARD_RISK


def test_curvature_away_from_risk():
    history = [
        {"min_distance": 1.5},
        {"min_distance": 1.7},
        {"min_distance": 2.0},
        {"min_distance": 2.3},
    ]
    assert evaluate_curvature(history) == RiskCurvature.AWAY_FROM_RISK
