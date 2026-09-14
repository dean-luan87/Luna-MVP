from __future__ import annotations

from typing import List, Dict, Any

from map_d0.download_plan import MapDownloadPlan


def snapshot_map_download_debug(
    plans: List[MapDownloadPlan],
) -> Dict[str, Any]:
    """
    Debug-only: MapDownloadPlan → timeline snapshot
    """
    if not plans:
        return {}

    return {
        "map_download_plans": [
            {
                "region_id": p.region_id,
                "granularity": p.granularity,
                "priority": p.priority,
                "ttl_hours": p.ttl_hours,
                "reason": p.reason,
                "source": p.source,
                "constraints": p.constraints,
            }
            for p in plans
        ]
    }
