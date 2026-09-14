from dynamic_view.scheduler.contract import (
    ObservationContract,
    ObservationPolicy,
    ContractMode,
)
from dynamic_view.scheduler.scheduler import ObservationScheduler


def test_default_autonomous_contract_applies_to_all():
    sch = ObservationScheduler()

    default = ObservationContract(
        contract_id="default_safety",
        mode=ContractMode.AUTONOMOUS,
        entity_id=None,
        policy=ObservationPolicy(max_invisible_time=0.5, recovery_grace_time=0.2, priority=10),
    )
    sch.register(default)

    p1 = sch.effective_policy("traffic_light_1")
    p2 = sch.effective_policy("elevator_1")

    assert p1.max_invisible_time == 0.5
    assert p2.max_invisible_time == 0.5


def test_task_contract_overrides_by_merge():
    sch = ObservationScheduler()

    default = ObservationContract(
        contract_id="default_safety",
        mode=ContractMode.AUTONOMOUS,
        entity_id=None,
        policy=ObservationPolicy(max_invisible_time=0.5, recovery_grace_time=0.2, priority=10),
    )
    follow_cat = ObservationContract(
        contract_id="follow_cat",
        mode=ContractMode.TASK,
        entity_id="cat_42",
        policy=ObservationPolicy(max_invisible_time=5.0, recovery_grace_time=2.0, priority=50),
    )

    sch.register(default)
    sch.register(follow_cat)

    p_cat = sch.effective_policy("cat_42")
    p_other = sch.effective_policy("traffic_light_1")

    assert p_cat.max_invisible_time == 5.0
    assert p_cat.priority == 50

    assert p_other.max_invisible_time == 0.5
    assert p_other.priority == 10


def test_revoke_task_contract_falls_back_to_default():
    sch = ObservationScheduler()

    default = ObservationContract(
        contract_id="default_safety",
        mode=ContractMode.AUTONOMOUS,
        entity_id=None,
        policy=ObservationPolicy(max_invisible_time=0.5, recovery_grace_time=0.2, priority=10),
    )
    follow_person = ObservationContract(
        contract_id="follow_person",
        mode=ContractMode.TASK,
        entity_id="person_7",
        policy=ObservationPolicy(max_invisible_time=8.0, recovery_grace_time=2.5, priority=40),
    )

    sch.register(default)
    sch.register(follow_person)

    sch.revoke("follow_person")

    p = sch.effective_policy("person_7")
    assert p.max_invisible_time == 0.5
    assert p.priority == 10
