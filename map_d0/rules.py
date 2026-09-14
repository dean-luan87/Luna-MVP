from __future__ import annotations

from typing import List

from common.change_demand import ChangeDemand
from map_d0.types import MapCandidate


def _confidence_from_priority(priority: float | int | None, cap: float) -> float:
    if priority is None:
        return 0.6
    try:
        return min(cap, float(priority))
    except (TypeError, ValueError):
        return 0.6


def candidates_from_change_demand(d: ChangeDemand) -> List[MapCandidate]:
    out: List[MapCandidate] = []

    if d.demand_type == "exit_area":
        out.append(
            MapCandidate(
                area_type="building_exit_zone",
                hint="出口通常位于建筑边缘或通道尽头",
                confidence=_confidence_from_priority(d.priority, 0.9),
                constraints=d.constraints,
            )
        )
    elif d.demand_type == "elevator":
        out.append(
            MapCandidate(
                area_type="vertical_transport_zone",
                hint="电梯通常靠近核心筒或大厅",
                confidence=_confidence_from_priority(d.priority, 0.85),
                constraints=d.constraints,
            )
        )
    elif d.demand_type == "metro_arrival":
        out.append(
            MapCandidate(
                area_type="platform",
                hint="站台方向或到站信息区域",
                confidence=_confidence_from_priority(d.priority, 0.8),
                constraints=d.constraints,
            )
        )
    elif d.demand_type == "bus_arrival":
        out.append(
            MapCandidate(
                area_type="bus_stop",
                hint="公交站台或候车区",
                confidence=_confidence_from_priority(d.priority, 0.75),
                constraints=d.constraints,
            )
        )
    elif d.demand_type == "traffic_signal":
        out.append(
            MapCandidate(
                area_type="intersection",
                hint="路口信号灯区域",
                confidence=_confidence_from_priority(d.priority, 0.9),
                constraints=d.constraints,
            )
        )

    return out
