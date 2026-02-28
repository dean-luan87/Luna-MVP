import time

from world_knowledge.schema import ObjectCard, ObservationSignal
from world_knowledge.profile import EnvironmentProfile
from world_knowledge.verification.gate import VerificationGate


def test_web_signals_do_not_become_trusted_without_gate():
    gate = VerificationGate()
    profile = EnvironmentProfile("CN-GD-GZ", "outdoor_crosswalk", {"net": True})

    draft = ObjectCard(
        object_type="traffic_light",
        tags=["safety_critical"],
        possible_states=["red", "green", "yellow"],
        change_types=["signal_state_change"],
    )

    sigs = [
        ObservationSignal(
            "web_snippet", {"q": "traffic light"}, "webA", time.time()
        )
    ]
    res = gate.verify(sigs, draft, profile)
    assert res.accepted is False
