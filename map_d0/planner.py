from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import time

from map_d0.context import MapContext
from map_d0.packages import CityPackageManifest, LocalPackageState
from map_d0.download_plan import MapDownloadPlan


@dataclass(frozen=True)
class DownloadIntent:
    """
    Suggestion only, not executed.
    """

    city_id: str
    layer: str
    reason: str
    priority: int
    pkg_version: Optional[str] = None


class MapDownloadPlanner:
    """
    v0: suggest L1/L2 downloads based on MapContext.
    """

    def __init__(self, manifest: CityPackageManifest):
        self.manifest = manifest
        self.local_state: Dict[str, Dict[str, LocalPackageState]] = {}

    def _state(self, city_id: str, layer: str) -> LocalPackageState:
        return self.local_state.setdefault(city_id, {}).setdefault(
            layer, LocalPackageState()
        )

    def mark_used(self, city_id: str, layer: str) -> None:
        st = self._state(city_id, layer)
        st.last_used_ts = time.time()

    def plan(self, map_ctx: MapContext, task_forced: bool = False) -> List[DownloadIntent]:
        if not map_ctx.city_id:
            return []

        city_id = map_ctx.city_id
        intents: List[DownloadIntent] = []

        pkg_l1 = self.manifest.get(city_id, "L1")
        st_l1 = self._state(city_id, "L1")
        if pkg_l1 and not st_l1.is_present:
            intents.append(
                DownloadIntent(
                    city_id=city_id,
                    layer="L1",
                    reason="enter_city",
                    priority=2,
                    pkg_version=pkg_l1.version,
                )
            )

        pkg_l2 = self.manifest.get(city_id, "L2")
        st_l2 = self._state(city_id, "L2")
        need_l2 = (map_ctx.active_zone_radius_m >= 1200) or task_forced
        if pkg_l2 and need_l2 and not st_l2.is_present:
            intents.append(
                DownloadIntent(
                    city_id=city_id,
                    layer="L2",
                    reason="task_target" if task_forced else "active_zone_expand",
                    priority=1 if task_forced else 3,
                    pkg_version=pkg_l2.version,
                )
            )

        return intents


def _granularity_by_area(area_type: str) -> str:
    if area_type in ("intersection", "traffic_signal"):
        return "coarse"
    if area_type in ("platform", "metro_arrival", "bus_arrival"):
        return "medium"
    if area_type in ("building_exit_zone", "elevator_zone"):
        return "fine"
    return "coarse"


def plan_download_from_roi_debug(
    roi_debug: Dict[str, Any],
    city: str | None = None,
    dry_run: bool = True,
) -> List[MapDownloadPlan]:
    """
    从 ROI Debug 生成下载计划（dry-run）
    """
    plans: List[MapDownloadPlan] = []

    roi_hints = roi_debug.get("roi_hints", [])
    roi_hit = roi_debug.get("roi_hit", {}).get("hit", False)

    base_priority = 0.3
    boost = 0.4 if roi_hit else 0.0

    for r in roi_hints:
        area_type = r.get("area_type")
        gran = _granularity_by_area(area_type)

        region_id = city or f"roi:{area_type}"

        plans.append(
            MapDownloadPlan(
                region_id=region_id,
                granularity=gran,
                reason=r.get("hint", "roi suggested"),
                priority=min(1.0, base_priority + boost),
                ttl_hours=24 if roi_hit else 6,
                constraints=r.get("constraints") or {},
                source="roi_debug",
            )
        )

    return plans
