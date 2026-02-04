def test_no_authority_leak_into_b():
    sample_b_output = {"facts": {"objects": []}}
    assert "authority" not in sample_b_output


def test_no_ability_leak_into_c():
    sample_c_decision = {"decision": "HOLD"}
    assert "abilities" not in sample_c_decision


def test_no_control_fields_in_b_values():
    sample_b_output = {"facts": {"objects": []}, "explanation": "descriptive"}
    forbidden = {"STOP", "HOLD", "REQUEST_TAKEOVER"}
    assert not any(value in forbidden for value in sample_b_output.values() if isinstance(value, str))
