from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, List
import time


@dataclass(frozen=True)
class LayerPackage:
    """
    City-level offline package metadata (L1/L2 only).
    """

    city_id: str
    layer: str
    version: str
    size_bytes: int = 0
    checksum: str = ""
    url: str = ""
    updated_at_ts: float = field(default_factory=lambda: time.time())


@dataclass
class LocalPackageState:
    """
    Local package state (device-specific).
    """

    is_present: bool = False
    local_path: Optional[str] = None
    last_checked_ts: float = 0.0
    last_used_ts: float = 0.0


class CityPackageManifest:
    """
    In-memory city package manifest.
    """

    def __init__(self, packages: Optional[List[LayerPackage]] = None):
        self._pk: Dict[str, Dict[str, LayerPackage]] = {}
        if packages:
            for p in packages:
                self.upsert(p)

    def upsert(self, pkg: LayerPackage) -> None:
        self._pk.setdefault(pkg.city_id, {})[pkg.layer] = pkg

    def get(self, city_id: str, layer: str) -> Optional[LayerPackage]:
        return self._pk.get(city_id, {}).get(layer)

    def list_layers(self, city_id: str) -> List[str]:
        return sorted(self._pk.get(city_id, {}).keys())
