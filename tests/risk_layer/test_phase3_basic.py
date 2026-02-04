from luna_badge_v1_2.governance.risk_center.phase3.evaluator import evaluate_phase3
from luna_badge_v1_2.governance.risk_center.phase3.schema import RiskAcceleration, RiskCurvature, RiskIrreversibility


def test_phase3_defaults_unknown_on_empty():
    output = evaluate_phase3([])
    assert output.acceleration == RiskAcceleration.UNKNOWN
    assert output.curvature == RiskCurvature.UNKNOWN
    assert output.irreversibility == RiskIrreversibility.UNKNOWN
