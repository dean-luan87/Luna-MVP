from world_knowledge.schema import ObjectCard, ChangeDemand
from world_knowledge.profile import EnvironmentProfile
from world_knowledge.enrichment.change_infer import CandidateInferencer


def test_candidate_generated_only_from_change_demand():
    profile = EnvironmentProfile("CN-GD-GZ", "outdoor_crosswalk", {"net": True})

    card = ObjectCard(
        object_type="traffic_light",
        tags=["safety_critical"],
        possible_states=["red", "green", "yellow"],
        change_types=["signal_state_change"],
        trust_level="trusted",
    )

    demand = ChangeDemand(
        "signal_state_change", priority=10, constraints={"object_type": "traffic_light"}
    )
    cand = CandidateInferencer().infer(demand, card, profile)
    assert cand is not None
