ALLOWED_DECISIONS = {"STOP", "HOLD", "REQUEST_TAKEOVER"}


def test_c_decision_is_atomic():
    sample_c_decision = {"decision": "HOLD"}
    assert isinstance(sample_c_decision, dict)
    assert "decision" in sample_c_decision
    assert sample_c_decision["decision"] in ALLOWED_DECISIONS


def test_c_no_candidates():
    sample_c_decision = {"decision": "REQUEST_TAKEOVER"}
    forbidden = {"candidates", "assumptions", "options"}
    for key in forbidden:
        assert key not in sample_c_decision
