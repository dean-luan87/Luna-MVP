from __future__ import annotations

from typing import Any, Dict, List

from dynamic_view.roi import RoiHint
from vision_ocr.types import ReferenceCard


def snapshot_roi_perception_debug(
    roi_hints: List[RoiHint],
    references: List[ReferenceCard],
) -> Dict[str, Any]:
    """
    Debug-only: ROI perception run summary.
    """
    roi_kinds = [r.area_type for r in roi_hints]
    ref_kinds = [r.kind for r in references]

    return {
        "roi_perception_debug": {
            "ran": bool(roi_hints),
            "roi_count": len(roi_hints),
            "roi_kinds": roi_kinds,
            "reference_count": len(references),
            "reference_kinds": ref_kinds,
        }
    }
