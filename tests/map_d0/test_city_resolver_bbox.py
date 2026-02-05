from map_d0.city_bbox import CityBBox, BBoxCityResolver
from map_d0.active_zone import GpsFix


def test_bbox_city_resolver_hits():
    r = BBoxCityResolver(
        [
            CityBBox(
                "shanghai",
                "Shanghai",
                "CN",
                bbox=(120.85, 30.65, 122.20, 31.87),
            ),
        ]
    )
    cid = r.resolve_city_id(GpsFix(lat=31.23, lon=121.47, accuracy_m=10))
    assert cid == "shanghai"


def test_bbox_city_resolver_miss():
    r = BBoxCityResolver(
        [
            CityBBox(
                "shanghai",
                "Shanghai",
                "CN",
                bbox=(120.85, 30.65, 122.20, 31.87),
            ),
        ]
    )
    cid = r.resolve_city_id(GpsFix(lat=22.54, lon=114.06, accuracy_m=10))
    assert cid is None
