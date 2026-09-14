import time

from dynamic_view.engine import ObservationEngine
from c_adapter.adapter import CAdapter
from c_adapter.types import CDecision


def test_c_reads_only_stable_state():
    eng = ObservationEngine()
    c = CAdapter()
    t0 = time.time()

    eng.ingest("traffic_light_1", t0)
    eng.tick(t0)
    stable = eng.stable_world_state()
    assert stable == {}

    eng.tick(t0 + 0.1)
    stable = eng.stable_world_state()
    assert "traffic_light_1" in stable

    decisions = c.decide(stable)
    assert decisions["traffic_light_1"] == CDecision.STOP

    eng.tick(t0 + 1.0)
    stable = eng.stable_world_state()
    assert "traffic_light_1" not in stable

    decisions = c.decide(stable)
    assert decisions == {}


def test_c_not_triggered_by_recovery_until_stable():
    eng = ObservationEngine()
    c = CAdapter()
    t0 = time.time()

    eng.ingest("elevator_1", t0)
    eng.tick(t0)
    eng.tick(t0 + 0.1)

    eng.tick(t0 + 1.0)

    eng.ingest("elevator_1", t0 + 1.1)
    eng.tick(t0 + 1.1)

    stable = eng.stable_world_state()
    assert "elevator_1" not in stable

    eng.tick(t0 + 1.2)
    stable = eng.stable_world_state()
    assert "elevator_1" in stable

    decisions = c.decide(stable)
    assert decisions["elevator_1"] == CDecision.PASS
