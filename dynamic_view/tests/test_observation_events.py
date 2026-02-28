import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.types import ObservationState


def test_events_emitted_only_on_transition():
    eng = ObservationEngine()
    t0 = time.time()

    eng.ingest("traffic_light_1", t0)
    eng.tick(t0)
    events = eng.pop_events()
    assert len(events) == 1
    assert events[0].new_state == ObservationState.APPEARED

    eng.tick(t0 + 0.1)
    events = eng.pop_events()
    assert len(events) == 1
    assert events[0].new_state == ObservationState.STABLE

    eng.tick(t0 + 0.2)
    events = eng.pop_events()
    assert events == []

    eng.tick(t0 + 1.0)
    events = eng.pop_events()
    assert len(events) == 1
    assert events[0].new_state == ObservationState.INVISIBLE
