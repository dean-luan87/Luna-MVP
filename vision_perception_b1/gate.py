from __future__ import annotations

from typing import List

from dynamic_view.roi import RoiHint


def should_run(roi_hints: List[RoiHint]) -> bool:
    """
    ROI 是唯一授权来源
    """
    return bool(roi_hints)
