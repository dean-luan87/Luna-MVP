from luna_badge_v1_2.governance.risk_center.interfaces.envelope import EnvelopeStatus, EnvelopeSignal


def test_envelope_contract():
    signal = EnvelopeSignal(
        status=EnvelopeStatus.WITHIN_ENVELOPE,
        reasons=[],
        confidence=1.0,
        timestamp=0.0,
    )
    assert signal.status == EnvelopeStatus.WITHIN_ENVELOPE
