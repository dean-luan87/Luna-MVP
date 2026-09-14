import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.types import ObservationState
from dynamic_view.observers.generic import GenericPresenceObserver, GenericSignalObserver


def test_generic_presence_observer_lifecycle():
    eng = ObservationEngine()
    t0 = time.time()

    ctx = {"visible": False}
    obs = GenericPresenceObserver(
        entity_id="elevator_generic_1",
        evaluator=lambda c: bool(c["visible"]),
        ctx=ctx,
    )

    eng.tick(t0)
    assert "elevator_generic_1" not in eng.entities

    ctx["visible"] = True
    ev = obs.poll()
    eng.ingest(ev.entity_id, ev.timestamp)
    eng.tick(t0)
    assert eng.entities["elevator_generic_1"].state == ObservationState.APPEARED

    eng.tick(t0 + 0.1)
    assert eng.entities["elevator_generic_1"].state == ObservationState.STABLE

    ctx["visible"] = False
    eng.tick(t0 + 1.0)
    assert eng.entities["elevator_generic_1"].state == ObservationState.INVISIBLE

    ctx["visible"] = True
    ev = obs.poll()
    eng.ingest(ev.entity_id, t0 + 1.1)
    eng.tick(t0 + 1.1)
    assert eng.entities["elevator_generic_1"].state == ObservationState.RECOVERED
    eng.tick(t0 + 1.2)
    assert eng.entities["elevator_generic_1"].state == ObservationState.STABLE


def test_generic_signal_observer_lifecycle():
    eng = ObservationEngine()
    t0 = time.time()

    ctx = {"color": None}
    obs = GenericSignalObserver(
        entity_id="traffic_light_generic_1",
        reader=lambda c: c.get("color"),
        validator=lambda v: v in ("RED", "GREEN"),
        ctx=ctx,
    )

    eng.tick(t0)
    assert "traffic_light_generic_1" not in eng.entities

    ctx["color"] = "RED"
    ev = obs.poll()
    eng.ingest(ev.entity_id, ev.timestamp)
    eng.tick(t0)
    assert eng.entities["traffic_light_generic_1"].state == ObservationState.APPEARED

    eng.tick(t0 + 0.1)
    assert eng.entities["traffic_light_generic_1"].state == ObservationState.STABLE

    ctx["color"] = None
    eng.tick(t0 + 1.0)
    assert eng.entities["traffic_light_generic_1"].state == ObservationState.INVISIBLE

    ctx["color"] = "GREEN"
    ev = obs.poll()
    eng.ingest(ev.entity_id, t0 + 1.1)
    eng.tick(t0 + 1.1)
    assert eng.entities["traffic_light_generic_1"].state == ObservationState.RECOVERED
    eng.tick(t0 + 1.2)
    assert eng.entities["traffic_light_generic_1"].state == ObservationState.STABLE
