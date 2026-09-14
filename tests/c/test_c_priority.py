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


def test_l1_overrides_l2():
    s = make_snapshot()
    s["perception_facts"]["traffic_light"] = "red"
    s["perception_facts"]["obstacle_distance"] = 0.2

    r = decide(s)
    assert r.decision == CDecision.STOP
    assert r.layer == "L1"
    assert r.reason_code == "OBSTACLE_TOO_CLOSE"


def test_l2_overrides_l3():
    s = make_snapshot()
    s["navigation_state"]["floor_state"] = "moving"
    s["perception_facts"]["confidence"] = {"traffic_light": 0.2}

    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.layer == "L2"
    assert r.reason_code == "FLOOR_NOT_ARRIVED"
