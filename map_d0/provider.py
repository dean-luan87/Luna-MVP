from __future__ import annotations

from typing import Optional

from map_d0.context import MapContext
from map_d0.registry import CityMapRegistry
from map_d0.active_zone import ActiveZoneEstimator, GpsFix


class CityResolver:
    """
    D0 v0: resolve city_id by external input only.
    """

    def resolve_city_id(self, fix: GpsFix) -> Optional[str]:
        return None


class MapContextProvider:
    """
    D0 provider: produces MapContext (reference only).
    """

    def __init__(
        self,
        registry: CityMapRegistry,
        zone: ActiveZoneEstimator,
        resolver: Optional[CityResolver] = None,
    ):
        self.registry = registry
        self.zone = zone
        self.resolver = resolver or CityResolver()

    def build(
        self, fix: Optional[GpsFix], forced_city_id: Optional[str] = None
    ) -> MapContext:
        if fix is None and forced_city_id is None:
            return MapContext(
                city_id=None,
                available_layers=[],
                structural_anchors=[],
                active_zone_radius_m=0,
                confidence=0.0,
            )

        city_id = forced_city_id
        radius_m = 0

        if fix is not None:
            radius_m = self.zone.update(fix)
            if city_id is None:
                city_id = self.resolver.resolve_city_id(fix)

        if city_id is None:
            return MapContext(
                city_id=None,
                available_layers=[],
                structural_anchors=[],
                active_zone_radius_m=int(radius_m),
                confidence=0.1 if radius_m > 0 else 0.0,
                meta={"note": "city_unknown"},
            )

        entry = self.registry.get(city_id)
        if entry is None:
            return MapContext(
                city_id=city_id,
                available_layers=["L1"],
                structural_anchors=["road", "rail", "station"],
                active_zone_radius_m=int(radius_m),
                confidence=0.2,
                meta={"note": "city_not_registered"},
            )

        return MapContext(
            city_id=entry.city_id,
            available_layers=list(entry.available_layers),
            structural_anchors=list(entry.structural_anchors),
            active_zone_radius_m=int(radius_m),
            confidence=0.85,
            meta={"city_name": entry.name, "country": entry.country},
        )
