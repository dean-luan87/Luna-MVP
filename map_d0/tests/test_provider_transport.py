from map_d0.candidate_provider import MapCandidateProvider
from common.change_demand import ChangeDemand


def test_metro_candidate():
    p = MapCandidateProvider()
    demands = [
        ChangeDemand(
            demand_type="metro_arrival",
            priority=0.6,
            constraints={"line": "2"},
            source="ocr_reference",
        )
    ]
    cands = p.propose(demands)
    assert cands[0].area_type == "platform"
