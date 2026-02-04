from __future__ import annotations

from typing import List, Dict, Any

from common.change_demand import ChangeDemand
from vision_ocr.types import ReferenceCard


def _make_constraints(card: ReferenceCard, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    constraints: Dict[str, Any] = {
        "meaning": card.meaning,
        "kind": card.kind,
        "confidence": card.confidence,
    }
    if card.attrs:
        constraints["attrs"] = dict(card.attrs)
    if extra:
        constraints.update(extra)
    return constraints


def reference_to_change_demands(cards: List[ReferenceCard]) -> List[ChangeDemand]:
    demands: List[ChangeDemand] = []

    for c in cards:
        if c.meaning == "exit":
            demands.append(
                ChangeDemand(
                    demand_type="exit_area",
                    priority=5,
                    constraints=_make_constraints(c, {"reason": "exit_sign_detected"}),
                    source="ocr_reference",
                )
            )
        elif c.meaning == "elevator":
            demands.append(
                ChangeDemand(
                    demand_type="elevator",
                    priority=5,
                    constraints=_make_constraints(c, {"reason": "elevator_sign_detected"}),
                    source="ocr_reference",
                )
            )
        elif c.meaning == "metro_line":
            demands.append(
                ChangeDemand(
                    demand_type="metro_arrival",
                    priority=5,
                    constraints=_make_constraints(
                        c,
                        {
                            "reason": "metro_line_detected",
                            "line": c.attrs.get("line") if c.attrs else None,
                        },
                    ),
                    source="ocr_reference",
                )
            )
        elif c.meaning == "bus_route":
            demands.append(
                ChangeDemand(
                    demand_type="bus_arrival",
                    priority=5,
                    constraints=_make_constraints(
                        c,
                        {
                            "reason": "bus_route_detected",
                            "route": c.attrs.get("route") if c.attrs else None,
                        },
                    ),
                    source="ocr_reference",
                )
            )
        elif c.meaning == "signal_countdown":
            demands.append(
                ChangeDemand(
                    demand_type="traffic_signal",
                    priority=5,
                    constraints=_make_constraints(c, {"reason": "signal_countdown_detected"}),
                    source="ocr_reference",
                )
            )

    return demands
