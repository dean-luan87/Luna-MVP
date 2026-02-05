from map_d0.candidate_provider import MapCandidateProvider
from common.change_demand import ChangeDemand


def test_exit_area_candidate():
    p = MapCandidateProvider()
    demands = [
        ChangeDemand(
            demand_type="exit_area",
            priority=0.7,
            constraints={"meaning": "exit"},
            source="ocr_reference",
        )
    ]
    cands = p.propose(demands)
    assert len(cands) == 1
    assert cands[0].area_type == "building_exit_zone"
