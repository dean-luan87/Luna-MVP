from luna_badge_v1_2.governance.risk_center import EnvelopeBus, EnvelopeSignal
from luna_badge_v1_2.governance.risk_center.invariants import assert_envelope_invariants


def test_envelope_bus_contract():
    signal = EnvelopeSignal(True, "LOW", "VISION", "STATIC", None, [])
    bus = EnvelopeBus(signals=[signal])
    assert len(bus.signals) == 1
    assert_envelope_invariants(bus.signals[0])
