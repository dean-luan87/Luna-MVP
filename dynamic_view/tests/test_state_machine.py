import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.types import ObservationState


def test_full_lifecycle():
    eng = ObservationEngine()
    now = time.time()

    eng.tick(now)
    assert eng.entities == {}

    eng.ingest("traffic_light_1", now)
    eng.tick(now)
    assert eng.entities["traffic_light_1"].state == ObservationState.APPEARED

    eng.tick(now + 0.1)
    assert eng.entities["traffic_light_1"].state == ObservationState.STABLE

    eng.tick(now + 1.0)
    assert eng.entities["traffic_light_1"].state == ObservationState.INVISIBLE

    eng.ingest("traffic_light_1", now + 1.1)
    eng.tick(now + 1.1)
    assert eng.entities["traffic_light_1"].state == ObservationState.RECOVERED

    eng.tick(now + 1.2)
    assert eng.entities["traffic_light_1"].state == ObservationState.STABLE


def test_invisible_to_disappeared_by_ttl():
    eng = ObservationEngine()
    now = time.time()

    eng.ingest("traffic_light_2", now)
    eng.tick(now)
    eng.tick(now + 0.1)
    assert eng.entities["traffic_light_2"].state == ObservationState.STABLE

    eng.tick(now + 1.0)
    assert eng.entities["traffic_light_2"].state == ObservationState.INVISIBLE

    eng.tick(now + 5.0)
    assert eng.entities["traffic_light_2"].state == ObservationState.DISAPPEARED


def test_no_direct_stable_to_disappeared():
    eng = ObservationEngine()
    now = time.time()

    eng.ingest("traffic_light_3", now)
    eng.tick(now)
    eng.tick(now + 0.1)
    assert eng.entities["traffic_light_3"].state == ObservationState.STABLE

    eng.tick(now + 10.0)
    assert eng.entities["traffic_light_3"].state == ObservationState.INVISIBLE
