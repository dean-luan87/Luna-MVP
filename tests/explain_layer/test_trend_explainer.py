import pytest

from luna_badge_v1_2.governance.explain_layer.trend_explainer import explain_trend


@pytest.mark.parametrize(
    "phase3,expected_tag,expected_confidence",
    [
        (
            {"acceleration": "INCREASING", "curvature": None, "irreversibility": None},
            "RISK_ACCELERATION_PERSISTENT",
            "HIGH",
        ),
        (
            {"acceleration": None, "curvature": "TOWARD_RISK", "irreversibility": None},
            "CURVATURE_TOWARD_RISK",
            "HIGH",
        ),
        (
            {"acceleration": None, "curvature": None, "irreversibility": "LIKELY_IRREVERSIBLE"},
            "IRREVERSIBILITY_HIGH",
            "HIGH",
        ),
    ],
)
def test_trend_explainer_tags(phase3, expected_tag, expected_confidence):
    tags, confidence = explain_trend(phase3)
    assert expected_tag in tags
    assert confidence == expected_confidence
