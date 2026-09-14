from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class CityMapEntry:
    city_id: str
    name: str
    country: str = "unknown"
    available_layers: List[str] = field(default_factory=lambda: ["L1"])
    structural_anchors: List[str] = field(
        default_factory=lambda: ["road", "rail", "station"]
    )


class CityMapRegistry:
    """
    D0 registry: in-memory list of available city layers/anchors.
    """

    def __init__(self, entries: Optional[List[CityMapEntry]] = None):
        self._entries: Dict[str, CityMapEntry] = {}
        if entries:
            for e in entries:
                self._entries[e.city_id] = e

    def get(self, city_id: str) -> Optional[CityMapEntry]:
        return self._entries.get(city_id)

    def upsert(self, entry: CityMapEntry) -> None:
        self._entries[entry.city_id] = entry

    def list_city_ids(self) -> List[str]:
        return sorted(self._entries.keys())
