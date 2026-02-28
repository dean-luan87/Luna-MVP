import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.types import ObservationState
from dynamic_view.observers.elevator import ElevatorObserver


def test_elevator_visibility_lifecycle():
    eng = ObservationEngine()
    obs = ElevatorObserver(entity_id="elevator_1")

    t0 = time.time()

    obs.set_visible(False)
    eng.tick(t0)
    assert "elevator_1" not in eng.entities

    obs.set_visible(True)
    ev = obs.poll()
    eng.ingest(ev.entity_id, ev.timestamp)
    eng.tick(t0)
    assert eng.entities["elevator_1"].state == ObservationState.APPEARED

    eng.tick(t0 + 0.1)
    assert eng.entities["elevator_1"].state == ObservationState.STABLE

    obs.set_visible(False)
    eng.tick(t0 + 1.0)
    assert eng.entities["elevator_1"].state == ObservationState.INVISIBLE

    eng.tick(t0 + 1.5)
    assert eng.entities["elevator_1"].state == ObservationState.INVISIBLE

    obs.set_visible(True)
    ev = obs.poll()
    eng.ingest(ev.entity_id, t0 + 1.6)
    eng.tick(t0 + 1.6)
    assert eng.entities["elevator_1"].state == ObservationState.RECOVERED

    eng.tick(t0 + 1.7)
    assert eng.entities["elevator_1"].state == ObservationState.STABLE
