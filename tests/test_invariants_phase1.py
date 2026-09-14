from luna_badge_v1_2.governance.output_controller.validator import OutputValidator
from luna_badge_v1_2.governance.instinct_controller.c_controller import CController


def test_b_output_forbidden_fields_rejected():
    validator = OutputValidator()
    normalized = {
        "model_id": "b-model",
        "data": {"foo": "bar"},
        "meta": {"authority": "A1"},
    }
    ok, reason = validator.validate(normalized)
    assert not ok
    assert "Forbidden field" in reason


def test_c_decide_output_is_restricted():
    c = CController()
    snap = {
        "perception_state": "READY",
        "calibration_state": "READY",
        "gate": "PASS",
        "nearest_obstacle_distance_m": 100.0,
        "approach_speed_mps": 0.1,
    }
    decision = c.decide(snap)
    assert decision in {"STOP", "HOLD", "REQUEST_TAKEOVER"}
