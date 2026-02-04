def test_debugview_contains_no_decision_fields(freeze_inputs):
    from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController

    ctrl = ModelOutputController()
    result = ctrl.process("nav", freeze_inputs["model_outputs"], freeze_inputs["system_snapshot"])
    debug_view = result["decision_trace"]["bc_snapshot"]["debug_view"]
    for forbidden in ("decision", "selected_result", "reason"):
        assert forbidden not in debug_view
