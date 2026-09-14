import pytest

from luna_badge_v1_2.governance.risk_center.interfaces.envelope import (
    EnvelopeStatus,
    evaluate_envelope,
)


def test_envelope_rejects_authority_input():
    with pytest.raises(AssertionError):
        evaluate_envelope({"authority": "A3"}, {"risk": {}})


def test_envelope_deterministic():
    snapshot = {"ts": 123.0}
    r1 = evaluate_envelope(snapshot, {"risk": {}})
    r2 = evaluate_envelope(snapshot, {"risk": {}})
    assert r1 == r2


def test_envelope_status_is_within_envelope():
    r = evaluate_envelope({"ts": 0.0}, {"risk": {}})
    assert r.status == EnvelopeStatus.WITHIN_ENVELOPE
