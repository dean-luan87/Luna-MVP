from map_d0.packages import CityPackageManifest, LayerPackage
from map_d0.planner import MapDownloadPlanner
from map_d0.context import MapContext


def test_planner_suggests_l1_on_enter_city():
    manifest = CityPackageManifest(
        [
            LayerPackage(city_id="shanghai", layer="L1", version="2026.01"),
            LayerPackage(city_id="shanghai", layer="L2", version="2026.01"),
        ]
    )
    planner = MapDownloadPlanner(manifest)

    ctx = MapContext(
        city_id="shanghai",
        available_layers=["L1", "L2"],
        structural_anchors=["road"],
        active_zone_radius_m=300,
        confidence=0.85,
    )
    intents = planner.plan(ctx, task_forced=False)

    assert any(i.layer == "L1" and i.reason == "enter_city" for i in intents)
    assert not any(i.layer == "L2" for i in intents)


def test_planner_suggests_l2_when_task_forced():
    manifest = CityPackageManifest(
        [
            LayerPackage(city_id="shanghai", layer="L1", version="2026.01"),
            LayerPackage(city_id="shanghai", layer="L2", version="2026.01"),
        ]
    )
    planner = MapDownloadPlanner(manifest)

    ctx = MapContext(
        city_id="shanghai",
        available_layers=["L1", "L2"],
        structural_anchors=["road"],
        active_zone_radius_m=300,
        confidence=0.85,
    )
    intents = planner.plan(ctx, task_forced=True)

    assert any(i.layer == "L2" and i.reason == "task_target" for i in intents)
