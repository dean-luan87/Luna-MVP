from tasks.engine import TaskEngine
from tasks.catalog import create_task


def make_snapshot():
    return {
        "perception_facts": {},
        "navigation_state": {},
        "health": {"perception": "ok"},
        "device_state": {},
        "task_state": {},
    }


def test_engine_start_and_complete_traffic_light_green():
    engine = TaskEngine()
    task = create_task("traffic_light", "t1")

    events = engine.start_task(task)
    assert any(e.type == "TASK_STATE" for e in events)

    s = make_snapshot()
    s["perception_facts"]["traffic_light"] = "green"

    tick_events = engine.tick(s)
    assert any(e.type == "SAY" for e in tick_events)
    assert engine.active_task is None


def test_engine_cancel():
    engine = TaskEngine()
    task = create_task("exit_finder", "t2")
    engine.start_task(task)
    ev = engine.cancel_active("USER_CANCEL")
    assert len(ev) > 0
    assert engine.active_task is None
