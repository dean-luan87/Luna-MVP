from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class MapDownloadPlan:
    """
    仅下载计划（dry-run），不执行
    """

    region_id: str
    granularity: str
    reason: str
    priority: float
    ttl_hours: int
    constraints: Dict[str, Any]
    source: str = "roi_debug"
