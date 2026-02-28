import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.types import ObservationState
from task_adapter.adapter import TaskAdapter
from task_adapter.types import TaskTrigger, TaskAction


def test_task_trigger_only_on_state_transition():
    eng = ObservationEngine()
    t0 = time.time()

    triggers = [
        TaskTrigger(
            entity_id="elevator_1",
            on_state=ObservationState.STABLE,
            action=TaskAction.ANNOUNCE,
            message="电梯已到达",
        )
    ]

    adapter = TaskAdapter(triggers)

    eng.ingest("elevator_1", t0)
    eng.tick(t0)
    actions = adapter.handle_events(eng.pop_events())
    assert actions == []

    eng.tick(t0 + 0.1)
    actions = adapter.handle_events(eng.pop_events())
    assert len(actions) == 1
    assert actions[0]["message"] == "电梯已到达"

    eng.tick(t0 + 0.2)
    actions = adapter.handle_events(eng.pop_events())
    assert actions == []


def test_invisible_does_not_trigger_task():
    eng = ObservationEngine()
    t0 = time.time()

    triggers = [
        TaskTrigger(
            entity_id="traffic_light_1",
            on_state=ObservationState.INVISIBLE,
            action=TaskAction.ANNOUNCE,
            message="红绿灯不可见",
        )
    ]
    adapter = TaskAdapter(triggers)

    eng.ingest("traffic_light_1", t0)
    eng.tick(t0)
    eng.tick(t0 + 0.1)
    eng.tick(t0 + 1.0)

    actions = adapter.handle_events(eng.pop_events())
    assert actions == []


def test_recovered_can_trigger_new_task():
    eng = ObservationEngine()
    t0 = time.time()

    triggers = [
        TaskTrigger(
            entity_id="elevator_2",
            on_state=ObservationState.RECOVERED,
            action=TaskAction.ANNOUNCE,
            message="电梯重新可见",
        )
    ]
    adapter = TaskAdapter(triggers)

    eng.ingest("elevator_2", t0)
    eng.tick(t0)
    eng.tick(t0 + 0.1)
    eng.tick(t0 + 1.0)

    eng.ingest("elevator_2", t0 + 1.1)
    eng.tick(t0 + 1.1)

    actions = adapter.handle_events(eng.pop_events())
    assert len(actions) == 1
    assert actions[0]["message"] == "电梯重新可见"
