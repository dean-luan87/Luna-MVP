from map_d0.download_plan import MapDownloadPlan


def test_plan_schema():
    p = MapDownloadPlan(
        region_id="city:test",
        granularity="coarse",
        reason="test",
        priority=0.5,
        ttl_hours=12,
        constraints={},
    )
    assert p.region_id
    assert 0 <= p.priority <= 1
