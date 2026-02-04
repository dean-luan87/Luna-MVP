from luna_badge_v1_2.governance.risk_center.phase3.irreversibility import evaluate_irreversibility
from luna_badge_v1_2.governance.risk_center.phase3.schema import RiskIrreversibility


def test_irreversibility_unknown():
    assert evaluate_irreversibility({"time_to_risk": None}) == RiskIrreversibility.UNKNOWN


def test_irreversibility_likely():
    assert evaluate_irreversibility({"time_to_risk": 0.5}, min_brake_time=1.0) == RiskIrreversibility.LIKELY_IRREVERSIBLE


def test_irreversibility_reversible():
    assert evaluate_irreversibility({"time_to_risk": 2.0}, min_brake_time=1.0) == RiskIrreversibility.REVERSIBLE
