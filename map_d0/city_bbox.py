from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from map_d0.active_zone import GpsFix


@dataclass(frozen=True)
class CityBBox:
    city_id: str
    name: str
    country: str
    # (min_lon, min_lat, max_lon, max_lat)
    bbox: tuple[float, float, float, float]


class BBoxCityResolver:
    """
    v0: bbox-based city resolver.
    """

    def __init__(self, boxes: List[CityBBox]):
        self.boxes = list(boxes)

    def resolve_city_id(self, fix: GpsFix) -> Optional[str]:
        lon, lat = fix.lon, fix.lat
        for b in self.boxes:
            min_lon, min_lat, max_lon, max_lat = b.bbox
            if (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat):
                return b.city_id
        return None
