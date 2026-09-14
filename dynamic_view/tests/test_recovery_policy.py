import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.scheduler.contract import (
    ObservationContract,
    ObservationPolicy,
    ContractMode,
)
from dynamic_view.scheduler.scheduler import ObservationScheduler
from dynamic_view.types import ObservationState


def test_recovery_behavior_diff_by_policy():
    scheduler = ObservationScheduler()

    default = ObservationContract(
        contract_id="default_safety",
        mode=ContractMode.AUTONOMOUS,
        entity_id=None,
        policy=ObservationPolicy(
            max_invisible_time=0.5,
            recovery_grace_time=0.2,
            priority=10,
        ),
    )

    follow_cat = ObservationContract(
        contract_id="follow_cat",
        mode=ContractMode.TASK,
        entity_id="cat_1",
        policy=ObservationPolicy(
            max_invisible_time=1.0,
            recovery_grace_time=1.0,
            priority=50,
        ),
    )

    scheduler.register(default)
    scheduler.register(follow_cat)

    eng = ObservationEngine(scheduler=scheduler)
    t0 = time.time()

    eng.ingest("cat_1", t0)
    eng.tick(t0)
    eng.tick(t0 + 0.1)

    eng.tick(t0 + 1.2)
    assert eng.entities["cat_1"].state == ObservationState.INVISIBLE

    eng.ingest("cat_1", t0 + 1.8)
    eng.tick(t0 + 1.8)
    assert eng.entities["cat_1"].state == ObservationState.RECOVERED

    eng.tick(t0 + 1.9)
    eng.tick(t0 + 3.0)
    assert eng.entities["cat_1"].state == ObservationState.INVISIBLE

    eng.ingest("cat_1", t0 + 4.2)
    eng.tick(t0 + 4.2)
    assert eng.entities["cat_1"].state == ObservationState.APPEARED
