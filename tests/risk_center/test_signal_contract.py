from luna_badge_v1_2.governance.risk_center.interfaces.signal import EnvelopeSignal
from luna_badge_v1_2.governance.risk_center.invariants import assert_envelope_invariants


def test_envelope_signal_contract():
    signal = EnvelopeSignal(
        present=True,
        level="MEDIUM",
        domain="VISION",
        type="RELATIVE_MOTION",
        time_to_event=1.0,
        reason_codes=["CURVATURE_BREAKS_CPA"],
    )
    assert signal.present is True
    assert signal.level in {"NONE", "LOW", "MEDIUM", "HIGH"}
    assert signal.domain == "VISION"
    assert_envelope_invariants(signal)
