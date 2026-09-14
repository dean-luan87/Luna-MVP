from __future__ import annotations

from typing import Dict, Any, List

from dynamic_view.roi import RoiHint


def snapshot_pal_roi_debug(
    enabled: bool,
    pal_hint_count: int,
    roi_hints: List[RoiHint],
) -> Dict[str, Any]:
    return {
        "pal_roi_debug": {
            "enabled": bool(enabled),
            "pal_hints": int(pal_hint_count),
            "roi_emitted": len(roi_hints),
            "roi_kinds": [r.area_type for r in roi_hints],
        }
    }
