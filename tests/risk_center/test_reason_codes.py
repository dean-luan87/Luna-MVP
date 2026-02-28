from luna_badge_v1_2.governance.risk_center import EnvelopeSignal
from luna_badge_v1_2.governance.risk_center.invariants import assert_reason_codes_append_only


def test_reason_codes_append_only():
    prev = EnvelopeSignal(True, "LOW", "VISION", "STATIC", None, ["A"])
    curr = EnvelopeSignal(True, "MEDIUM", "VISION", "STATIC", None, ["A", "B"])
    assert_reason_codes_append_only(prev, curr)
