from __future__ import annotations

from typing import List

from dynamic_view.roi import RoiHint
from .schema import PalRoiHint
from .config import PAL_ROI_TTL_S


def pal_hint_to_roi(pal_hint: PalRoiHint) -> RoiHint:
    ttl = pal_hint.ttl_s or PAL_ROI_TTL_S
    ttl = min(ttl, PAL_ROI_TTL_S)
    return RoiHint(
        area_type=pal_hint.roi_kind,
        hint=pal_hint.reason,
        bbox=pal_hint.area,
        weight=max(0.0, min(1.0, pal_hint.confidence)),
        constraints={
            "ttl_s": ttl,
            "confidence": pal_hint.confidence,
            "reason": pal_hint.reason,
        },
        source="pal_attention",
    )


def convert_pal_to_rois(pal_hints: List[PalRoiHint]) -> List[RoiHint]:
    return [pal_hint_to_roi(h) for h in pal_hints]
