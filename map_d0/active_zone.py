from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import math
import time


@dataclass(frozen=True)
class GpsFix:
    lat: float
    lon: float
    accuracy_m: float = 30.0
    ts: Optional[float] = None


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


class ActiveZoneEstimator:
    """
    D0 activity radius estimator.
    """

    def __init__(self, min_radius_m: int = 300, max_radius_m: int = 3000):
        self.min_radius_m = int(min_radius_m)
        self.max_radius_m = int(max_radius_m)
        self._last: Optional[GpsFix] = None
        self._radius_m: int = self.min_radius_m
        self._last_update_ts: float = 0.0

    def update(self, fix: GpsFix) -> int:
        ts = fix.ts or time.time()
        if self._last is None:
            self._last = fix
            self._radius_m = max(self.min_radius_m, int(fix.accuracy_m * 5))
            self._radius_m = min(self._radius_m, self.max_radius_m)
            self._last_update_ts = ts
            return self._radius_m

        dist = _haversine_m(self._last.lat, self._last.lon, fix.lat, fix.lon)
        base = int(max(self.min_radius_m, fix.accuracy_m * 5))
        dynamic = int(min(self.max_radius_m, base + dist))
        self._radius_m = dynamic
        self._last = fix
        self._last_update_ts = ts
        return self._radius_m

    def current_radius_m(self) -> int:
        return int(self._radius_m)
