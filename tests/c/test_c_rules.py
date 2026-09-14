from c.controller import decide
from c.types import CDecision


def make_snapshot():
    return {
        "time": 0,
        "self_state": {},
        "perception_facts": {},
        "navigation_state": {},
        "device_state": {},
        "task_state": {},
        "health": {"perception": "ok"},
    }


def test_l1_perception_lost_hold():
    s = make_snapshot()
    s["health"]["perception"] = "lost"
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.layer == "L1"
    assert r.reason_code == "PERCEPTION_LOST"


def test_l1_obstacle_too_close_stop():
    s = make_snapshot()
    s["perception_facts"]["obstacle_distance"] = 0.3
    r = decide(s)
    assert r.decision == CDecision.STOP
    assert r.layer == "L1"
    assert r.reason_code == "OBSTACLE_TOO_CLOSE"


def test_l2_red_light_hold():
    s = make_snapshot()
    s["perception_facts"]["traffic_light"] = "red"
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.layer == "L2"
    assert r.reason_code == "RED_LIGHT"


def test_l2_floor_moving_hold():
    s = make_snapshot()
    s["navigation_state"]["floor_state"] = "moving"
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.layer == "L2"
    assert r.reason_code == "FLOOR_NOT_ARRIVED"


def test_l3_traffic_light_uncertain_hold():
    s = make_snapshot()
    s["perception_facts"]["confidence"] = {"traffic_light": 0.5}
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.layer == "L3"
    assert r.reason_code == "TRAFFIC_LIGHT_UNCERTAIN"


def test_pass_when_no_risk():
    s = make_snapshot()
    r = decide(s)
    assert r.decision == CDecision.PASS
    assert r.layer == "NONE"
    assert r.reason_code == "NO_RISK"
