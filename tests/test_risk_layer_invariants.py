import pytest

from luna_badge_v1_2.governance.invariants import (
    FORBIDDEN_KEYS_IN_C_INPUT,
    assert_c_input_invariants,
)
from luna_badge_v1_2.governance.risk.risk_signal import RiskSignal


def test_risk_signal_is_advisory_only():
    risk = RiskSignal(
        risk_present=True,
        risk_level="HIGH",
        risk_type="STATIC_COLLISION",
        time_to_risk=None,
        confidence=None,
    )
    forbidden = {"action", "decision", "STOP"}
    assert forbidden.isdisjoint(risk.__dict__.keys())


def test_c_input_rejects_risk_fields(monkeypatch):
    monkeypatch.setenv("LUNA_INVARIANTS", "DEBUG")
    snapshot = {key: "X" for key in FORBIDDEN_KEYS_IN_C_INPUT}
    with pytest.raises(AssertionError):
        assert_c_input_invariants(snapshot)
