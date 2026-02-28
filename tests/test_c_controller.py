from luna_badge_v1_2.governance.instinct_controller.c_controller import CController
from luna_badge_v1_2.governance.instinct_controller.c_types import CAction
from luna_badge_v1_2.governance.instinct_controller.c_state import CState, CStateContext


def mock_system_snapshot(
    perception_state="READY",
    calibration_state="READY",
    hardware_state="OK",
):
    return {
        "perception_state": perception_state,
        "calibration_state": calibration_state,
        "hardware_state": hardware_state,
    }


def mock_perception_summary(
    obstacle_distance=10.0,
    left_safe=True,
    right_safe=True,
    approaching_fast=False,
):
    return {
        "nearest_obstacle_distance": obstacle_distance,
        "left_safer": left_safe,
        "right_safer": right_safe,
        "dynamic_target_fast_approach": approaching_fast,
    }


def mock_gate(result="PASS"):
    return result


def mock_c_state(state=CState.INACTIVE, fail_count=0):
    return CStateContext(state=state, fail_count=fail_count)


def test_import_c_controller():
    c = CController()
    assert c is not None


def test_emergency_stop_on_gate_block():
    c = CController()
    out = c.handle(
        system_snapshot=mock_system_snapshot(),
        perception_summary=mock_perception_summary(obstacle_distance=1.0),
        gate_result=mock_gate("BLOCK"),
        last_state=mock_c_state(),
    )
    assert out.action == CAction.STOP
    assert out.confidence == 1.0


def test_hard_block_on_perception_failure():
    c = CController()
    out = c.handle(
        system_snapshot=mock_system_snapshot(perception_state="FAILED"),
        perception_summary=mock_perception_summary(),
        gate_result=mock_gate("PASS"),
        last_state=mock_c_state(),
    )
    assert out.action == CAction.HOLD


def test_simple_avoid_left():
    c = CController()
    out = c.handle(
        system_snapshot=mock_system_snapshot(),
        perception_summary=mock_perception_summary(
            obstacle_distance=3.0,
            left_safe=True,
            right_safe=False,
        ),
        gate_result=mock_gate("PASS"),
        last_state=mock_c_state(),
    )
    assert out.action == CAction.AVOID_LEFT


def test_fail_safe_when_no_rule_matches():
    c = CController()
    out = c.handle(
        system_snapshot=mock_system_snapshot(),
        perception_summary=mock_perception_summary(
            obstacle_distance=100.0,
            left_safe=False,
            right_safe=False,
        ),
        gate_result=mock_gate("PASS"),
        last_state=mock_c_state(),
    )
    assert out.action == CAction.REQUEST_TAKEOVER


def test_failed_state_is_terminal():
    c = CController()
    out = c.handle(
        system_snapshot=mock_system_snapshot(),
        perception_summary=mock_perception_summary(),
        gate_result=mock_gate("PASS"),
        last_state=mock_c_state(state=CState.FAILED, fail_count=10),
    )
    assert out.action == CAction.REQUEST_TAKEOVER
    assert out.c_state == CState.FAILED


def test_authority_pollution_assertion():
    c = CController()
    polluted_snapshot = mock_system_snapshot()
    polluted_snapshot["authority"] = "A1"

    try:
        c.handle(
            system_snapshot=polluted_snapshot,
            perception_summary=mock_perception_summary(),
            gate_result=mock_gate("PASS"),
            last_state=mock_c_state(),
        )
        assert False, "authority pollution not detected"
    except AssertionError:
        pass
