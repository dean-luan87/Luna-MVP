from map_d0.download_plan import MapDownloadPlan
from observe.timeline_map_download import snapshot_map_download_debug


def test_map_download_written_to_timeline():
    plans = [
        MapDownloadPlan(
            region_id="shanghai",
            granularity="medium",
            reason="platform arrival",
            priority=0.7,
            ttl_hours=24,
            constraints={},
        )
    ]

    snap = snapshot_map_download_debug(plans)
    assert "map_download_plans" in snap
    assert snap["map_download_plans"][0]["granularity"] == "medium"
