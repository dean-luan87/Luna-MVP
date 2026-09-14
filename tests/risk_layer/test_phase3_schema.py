from luna_badge_v1_2.governance.risk_center.phase3.schema import (
    SCHEMA_VERSION,
    RiskAcceleration,
    RiskCurvature,
    RiskIrreversibility,
    RiskPhase3Output,
)


def test_phase3_schema_fixed():
    output = RiskPhase3Output(
        acceleration=RiskAcceleration.UNKNOWN,
        curvature=RiskCurvature.UNKNOWN,
        irreversibility=RiskIrreversibility.UNKNOWN,
    )
    assert output.schema_version == SCHEMA_VERSION
    assert set(item.value for item in RiskAcceleration) == {"INCREASING", "STABLE", "DECREASING", "UNKNOWN"}
    assert set(item.value for item in RiskCurvature) == {"TOWARD_RISK", "STABLE", "AWAY_FROM_RISK", "UNKNOWN"}
    assert set(item.value for item in RiskIrreversibility) == {"REVERSIBLE", "LIKELY_IRREVERSIBLE", "UNKNOWN"}
