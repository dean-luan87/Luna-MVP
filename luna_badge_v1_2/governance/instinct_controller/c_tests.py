from .c_controller import CController
from .c_state import CState, CStateContext
from .c_types import CAction


def _base_snapshot():
    return {
        "perception_state": "READY",
        "calibration_state": "READY",
    }


def test_emergency_stop_on_gate_block():
    controller = CController()
    out = controller.handle(
        system_snapshot=_base_snapshot(),
        perception_summary={"nearest_obstacle_distance": 2.0},
        gate_result="BLOCK",
        last_state=CStateContext(state=CState.INACTIVE, fail_count=0),
    )
    assert out.action == CAction.STOP


def test_hard_block_on_perception_failed():
    controller = CController()
    out = controller.handle(
        system_snapshot={"perception_state": "FAILED", "calibration_state": "READY"},
        perception_summary={},
        gate_result="PASS",
        last_state=CStateContext(state=CState.INACTIVE, fail_count=0),
    )
    assert out.action == CAction.HOLD


def test_fail_safe_request_takeover():
    controller = CController()
    out = controller.handle(
        system_snapshot=_base_snapshot(),
        perception_summary={},
        gate_result="PASS",
        last_state=CStateContext(state=CState.INACTIVE, fail_count=0),
    )
    assert out.action == CAction.REQUEST_TAKEOVER


def test_failed_state_blocks_rules():
    controller = CController()
    out = controller.handle(
        system_snapshot=_base_snapshot(),
        perception_summary={"nearest_obstacle_distance": 0.2},
        gate_result="PASS",
        last_state=CStateContext(state=CState.FAILED, fail_count=3),
    )
    assert out.action == CAction.REQUEST_TAKEOVER
