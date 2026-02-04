from __future__ import annotations

from typing import Any, Dict, List

from roi_confirmation_c2.events import ROIManualEvent


def snapshot_roi_manual_debug(
    events: List[ROIManualEvent],
    version: str = "c2.1",
) -> Dict[str, Any]:
    if not events:
        return {}
    return {
        "roi_manual_debug": {
            "version": version,
            "events": [e.to_dict() for e in events],
        }
    }
