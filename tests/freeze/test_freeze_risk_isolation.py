def test_risk_does_not_affect_decision(freeze_inputs, low_risk_controller, high_risk_controller):
    r1 = low_risk_controller.process(
        "nav",
        freeze_inputs["model_outputs"],
        freeze_inputs["system_snapshot"],
    )
    r2 = high_risk_controller.process(
        "nav",
        freeze_inputs["model_outputs"],
        freeze_inputs["system_snapshot"],
    )
    assert r1["decision"] == r2["decision"]
    assert (
        r1["decision_trace"]["bc_snapshot"]["bc_action"]
        == r2["decision_trace"]["bc_snapshot"]["bc_action"]
    )
    assert "risk" not in r1.get("reason", "").lower()
    assert "risk" not in r2.get("reason", "").lower()
