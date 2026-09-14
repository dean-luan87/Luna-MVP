from __future__ import annotations

from typing import List

from dynamic_view.attention import AttentionWindow
from dynamic_view.roi import RoiHint


def attention_to_roi(windows: List[AttentionWindow]) -> List[RoiHint]:
    """
    AttentionWindow -> RoiHint
    不强制提供 bbox；仅语义偏置
    """
    rois: List[RoiHint] = []
    for w in windows:
        rois.append(
            RoiHint(
                area_type=w.area_type,
                hint=w.hint,
                bbox=None,
                weight=1.1,
                constraints=w.constraints,
                source=w.source,
            )
        )
    return rois
