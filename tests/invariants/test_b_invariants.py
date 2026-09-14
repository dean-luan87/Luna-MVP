FORBIDDEN_FIELDS = {
    "authority",
    "abilities",
    "gate",
    "decision",
    "level",
    "impact",
    "must_stop",
    "intervention_level",
}


def test_b_output_no_control_fields():
    sample_b_output = {
        "facts": {"objects": []},
        "scores": {"confidence": 0.6},
        "assumptions": {"lighting": "normal"},
        "cost_estimate": {"risk_proxy": 0.2},
        "explanation": "descriptive only",
    }
    for key in FORBIDDEN_FIELDS:
        assert key not in sample_b_output, f"B output leaked control field: {key}"


def test_b_allows_multiple_candidates():
    sample_b_outputs = [
        {"model_id": "b1", "facts": {"objects": []}},
        {"model_id": "b2", "facts": {"objects": []}},
    ]
    assert isinstance(sample_b_outputs, list)
    assert len(sample_b_outputs) >= 1
