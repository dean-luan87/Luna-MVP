from __future__ import annotations

from typing import Any, Dict, List

from roi_confirmation_c2.schema import ROIDefaultEntry


def snapshot_roi_confirmation_debug(
    entries: List[ROIDefaultEntry],
    version: str = "c2-v0",
) -> Dict[str, Any]:
    if not entries:
        return {}
    return {
        "roi_confirmation_debug": {
            "version": version,
            "confirmed": [e.to_dict() for e in entries],
        }
    }
