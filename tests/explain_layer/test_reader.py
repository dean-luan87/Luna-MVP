import pytest

from luna_badge_v1_2.governance.explain_layer.reader import read_phase3


def test_reader_rejects_forbidden_fields():
    snapshot = {
        "decision": "fallback",
        "acceleration": "INCREASING",
        "curvature": "TOWARD_RISK",
        "irreversibility": "LIKELY_IRREVERSIBLE",
    }
    with pytest.raises(AssertionError):
        read_phase3(snapshot)


def test_reader_accepts_phase3_snapshot():
    snapshot = {
        "acceleration": "STABLE",
        "curvature": "STABLE",
        "irreversibility": "REVERSIBLE",
    }
    result = read_phase3(snapshot)
    assert result["acceleration"] == "STABLE"
