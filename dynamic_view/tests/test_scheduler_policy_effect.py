import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.scheduler.contract import (
    ObservationContract,
    ObservationPolicy,
    ContractMode,
)
from dynamic_view.scheduler.scheduler import ObservationScheduler
from dynamic_view.types import ObservationState


def test_default_vs_task_invisible_timeout():
    scheduler = ObservationScheduler()

    default = ObservationContract(
        contract_id="default_safety",
        mode=ContractMode.AUTONOMOUS,
        entity_id=None,
        policy=ObservationPolicy(max_invisible_time=0.5, recovery_grace_time=0.2, priority=10),
    )

    follow_person = ObservationContract(
        contract_id="follow_person",
        mode=ContractMode.TASK,
        entity_id="person_1",
        policy=ObservationPolicy(max_invisible_time=5.0, recovery_grace_time=2.0, priority=50),
    )

    scheduler.register(default)
    scheduler.register(follow_person)

    eng = ObservationEngine(scheduler=scheduler)
    t0 = time.time()

    eng.ingest("person_1", t0)
    eng.ingest("traffic_light_1", t0)
    eng.tick(t0)
    eng.tick(t0 + 0.1)

    assert eng.entities["person_1"].state == ObservationState.STABLE
    assert eng.entities["traffic_light_1"].state == ObservationState.STABLE

    eng.tick(t0 + 0.6)

    assert eng.entities["traffic_light_1"].state == ObservationState.INVISIBLE
    assert eng.entities["person_1"].state == ObservationState.STABLE

    eng.tick(t0 + 5.1)

    assert eng.entities["person_1"].state == ObservationState.INVISIBLE
