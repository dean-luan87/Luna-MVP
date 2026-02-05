from map_d0 import CityMapRegistry, CityMapEntry, ActiveZoneEstimator, MapContextProvider, GpsFix


def test_map_context_city_unknown():
    reg = CityMapRegistry([])
    zone = ActiveZoneEstimator()
    p = MapContextProvider(reg, zone)

    ctx = p.build(GpsFix(lat=0.0, lon=0.0, accuracy_m=20.0))
    assert ctx.city_id is None
    assert ctx.confidence >= 0.0
    assert ctx.active_zone_radius_m > 0


def test_map_context_registered_city():
    reg = CityMapRegistry(
        [
            CityMapEntry(
                city_id="shanghai",
                name="Shanghai",
                country="CN",
                available_layers=["L1", "L2"],
            )
        ]
    )
    zone = ActiveZoneEstimator()
    p = MapContextProvider(reg, zone)

    ctx = p.build(
        GpsFix(lat=31.2, lon=121.4, accuracy_m=10.0),
        forced_city_id="shanghai",
    )
    assert ctx.city_id == "shanghai"
    assert "L1" in ctx.available_layers
    assert ctx.confidence >= 0.8
