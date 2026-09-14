from tasks.catalog import create_task
from tasks.engine import TaskEngine


def make_snapshot():
    return {
        "perception_facts": {},
        "navigation_state": {},
        "health": {"perception": "ok"},
        "device_state": {},
        "task_state": {},
    }


def test_floor_arrival_flow():
    engine = TaskEngine()
    task = create_task("floor_arrival", "f1")
    engine.start_task(task)

    s = make_snapshot()
    s["navigation_state"]["floor_state"] = "moving"
    ev1 = engine.tick(s)
    assert any(e.type == "SAY" for e in ev1)

    s["navigation_state"]["floor_state"] = "arrived"
    ev2 = engine.tick(s)
    assert any(e.type == "SAY" for e in ev2)
    assert engine.active_task is None


def test_elevator_button_requires_target():
    engine = TaskEngine()
    task = create_task("elevator_button", "e1", meta={})
    engine.start_task(task)

    s = make_snapshot()
    ev = engine.tick(s)
    assert any(e.type == "SAY" for e in ev)
    assert engine.active_task is None


def test_exit_finder_blocked_then_found():
    engine = TaskEngine()
    task = create_task("exit_finder", "x1")
    engine.start_task(task)

    s = make_snapshot()
    ev1 = engine.tick(s)
    assert any(e.type == "SAY" for e in ev1)
    assert engine.active_task is not None

    s["perception_facts"]["exit_found"] = True
    ev2 = engine.tick(s)
    assert any(e.type == "SAY" for e in ev2)
    assert engine.active_task is None
