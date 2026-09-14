from __future__ import annotations

from typing import Any

from dynamic_view.roi import RoiHint


def crop_by_roi(frame: Any, roi: RoiHint) -> Any:
    if roi.bbox is None:
        return frame

    x1, y1, x2, y2 = roi.bbox
    if x2 <= x1 or y2 <= y1:
        return frame

    try:
        return frame[y1:y2, x1:x2]
    except Exception:
        try:
            return [row[x1:x2] for row in frame[y1:y2]]
        except Exception:
            return frame
