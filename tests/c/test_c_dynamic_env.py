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


def test_human_too_close_stop():
    s = make_snapshot()
    s["perception_facts"]["human_proximity_m"] = 0.4
    r = decide(s)
    assert r.decision == CDecision.STOP
    assert r.reason_code == "HUMAN_TOO_CLOSE"


def test_passage_blocked_hold():
    s = make_snapshot()
    s["navigation_state"]["passage_state"] = "blocked"
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.reason_code == "PASSAGE_BLOCKED"


def test_facility_unavailable_hold():
    s = make_snapshot()
    s["navigation_state"]["facility_state"] = "unavailable"
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.reason_code == "FACILITY_UNAVAILABLE"


def test_low_confidence_hold():
    s = make_snapshot()
    s["perception_facts"]["confidence"] = {"exit": 0.4}
    r = decide(s)
    assert r.decision == CDecision.HOLD
    assert r.layer == "L3"
