from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController


def test_c_stop_prevents_execute(freeze_inputs):
    ctrl = ModelOutputController()
    ctrl._c.decide = lambda _snapshot: "STOP"
    result = ctrl.process("nav", freeze_inputs["model_outputs"], freeze_inputs["system_snapshot"])
    assert result["decision"] != "execute"
    assert result["decision_trace"]["bc_snapshot"]["bc_action"] in {"FORCE_STOP", "HOLD", "FALLBACK"}


def test_c_hold_prevents_execute(freeze_inputs):
    ctrl = ModelOutputController()
    ctrl._c.decide = lambda _snapshot: "HOLD"
    result = ctrl.process("nav", freeze_inputs["model_outputs"], freeze_inputs["system_snapshot"])
    assert result["decision"] != "execute"
    assert result["decision_trace"]["bc_snapshot"]["bc_action"] in {"FORCE_STOP", "HOLD", "FALLBACK"}
