def test_c_stop_forces_bc_stop(mock_controller, base_snapshot, mock_valid_output):
    mock_controller._c.decide = lambda _: "STOP"

    result = mock_controller.process(
        task_domain="navigation",
        model_outputs=[mock_valid_output()],
        system_snapshot=base_snapshot,
    )

    snap = result["decision_trace"]["bc_snapshot"]
    assert result["decision"] == "fallback"
    assert result["reason"] == "c_force_stop"
    assert snap["bc_action"] == "FORCE_STOP"
    assert snap["c_decision"] == "STOP"


def test_c_hold_blocks_but_allows_recovery(mock_controller, base_snapshot, mock_valid_output):
    mock_controller._c.decide = lambda _: "HOLD"

    result = mock_controller.process(
        "navigation",
        [mock_valid_output()],
        base_snapshot,
    )

    snap = result["decision_trace"]["bc_snapshot"]
    assert result["decision"] == "fallback"
    assert result["reason"] == "c_hold"
    assert snap["bc_action"] == "HOLD"
    assert snap["can_recover"] is True


def test_c_request_takeover_has_highest_priority(mock_controller, base_snapshot, mock_valid_output):
    mock_controller._c.decide = lambda _: "REQUEST_TAKEOVER"

    result = mock_controller.process(
        "navigation",
        [mock_valid_output()],
        base_snapshot,
    )

    snap = result["decision_trace"]["bc_snapshot"]
    assert result["decision"] == "fallback"
    assert result["reason"] == "c_request_takeover"
    assert snap["bc_action"] == "REQUEST_TAKEOVER"


def test_no_c_veto_allows_arbitration(mock_controller, base_snapshot, mock_valid_output):
    mock_controller._c.decide = lambda _: "NONE"

    result = mock_controller.process(
        "navigation",
        [mock_valid_output()],
        base_snapshot,
    )

    assert result["decision"] in ("commit", "fallback")
    assert result["reason"] not in {"c_force_stop", "c_hold", "c_request_takeover"}
