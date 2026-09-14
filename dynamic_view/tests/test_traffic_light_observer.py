import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.types import ObservationState
from dynamic_view.observers.traffic_light import TrafficLightObserver


def test_traffic_light_lifecycle():
    eng = ObservationEngine()
    obs = TrafficLightObserver("traffic_light_1")
    t0 = time.time()

    obs.set_color(None)
    eng.tick(t0)
    assert "traffic_light_1" not in eng.entities

    obs.set_color("RED")
    ev = obs.poll()
    eng.ingest(ev.entity_id, t0)
    eng.tick(t0)
    assert eng.entities["traffic_light_1"].state == ObservationState.APPEARED

    eng.tick(t0 + 0.1)
    assert eng.entities["traffic_light_1"].state == ObservationState.STABLE

    obs.set_color(None)
    eng.tick(t0 + 1.0)
    assert eng.entities["traffic_light_1"].state == ObservationState.INVISIBLE

    obs.set_color("GREEN")
    ev = obs.poll()
    eng.ingest(ev.entity_id, t0 + 1.1)
    eng.tick(t0 + 1.1)
    assert eng.entities["traffic_light_1"].state == ObservationState.RECOVERED

    eng.tick(t0 + 1.2)
    assert eng.entities["traffic_light_1"].state == ObservationState.STABLE
