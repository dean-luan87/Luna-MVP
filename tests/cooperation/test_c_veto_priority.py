def test_c_stop_veto_clears_candidates(mock_controller, base_snapshot, mock_valid_output):
    mock_controller._c.decide = lambda _: "STOP"

    result = mock_controller.process(
        "navigation",
        [mock_valid_output()],
        base_snapshot,
    )

    snap = result["decision_trace"]["bc_snapshot"]
    assert snap["used_candidates"] == []
    assert snap["bc_action"] == "FORCE_STOP"
