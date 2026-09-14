from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from map_d0.context import MapContext


@dataclass(frozen=True)
class MapCandidate:
    """
    地图给出的“可能性候选”，不是事实
    """

    area_type: str
    hint: str
    confidence: float
    constraints: Dict[str, Any] = field(default_factory=dict)
    source: str = "map_reference"


__all__ = [
    "MapCandidate",
    "MapContext",
]
