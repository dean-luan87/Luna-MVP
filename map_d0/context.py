from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass(frozen=True)
class MapContext:
    """
    D0: read-only spatial reference context.
    - no state (signals/availability)
    - no decision impact
    """

    city_id: Optional[str] = None
    available_layers: List[str] = field(default_factory=list)
    structural_anchors: List[str] = field(default_factory=list)
    active_zone_radius_m: int = 0
    confidence: float = 0.0
    source: str = "map_d0"
    meta: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "city_id": self.city_id,
            "available_layers": list(self.available_layers),
            "structural_anchors": list(self.structural_anchors),
            "active_zone_radius_m": int(self.active_zone_radius_m),
            "confidence": float(self.confidence),
            "source": self.source,
            "meta": dict(self.meta),
        }
