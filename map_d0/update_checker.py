from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import time

from map_d0.packages import LayerPackage, LocalPackageState


@dataclass(frozen=True)
class UpdateDecision:
    city_id: str
    layer: str
    need_update: bool
    reason: str
    target_version: Optional[str] = None


class UpdateChecker:
    """
    更新检查：
    - 不定时
    - 不全量
    - 用到才查
    """

    def __init__(self, min_interval_sec: int = 24 * 3600):
        self.min_interval_sec = min_interval_sec

    def check(self, pkg: LayerPackage, state: LocalPackageState) -> UpdateDecision:
        now = time.time()

        if state.last_checked_ts <= 0:
            return UpdateDecision(pkg.city_id, pkg.layer, True, "never_checked", pkg.version)

        if now - state.last_checked_ts < self.min_interval_sec:
            return UpdateDecision(pkg.city_id, pkg.layer, False, "interval_not_reached")

        if state.is_present and pkg.version:
            return UpdateDecision(pkg.city_id, pkg.layer, True, "version_mismatch", pkg.version)

        return UpdateDecision(pkg.city_id, pkg.layer, False, "up_to_date")
