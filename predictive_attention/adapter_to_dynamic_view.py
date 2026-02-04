from __future__ import annotations

from typing import List, Optional, Dict, Any

from dynamic_view.roi import RoiHint
from predictive_attention.schema import AttentionHint


def _hint_label(hint: AttentionHint) -> str:
    if hint.reason_codes:
        return ",".join(hint.reason_codes)
    return "pal_hint"


def to_roi_hints(hints: List[AttentionHint]) -> List[RoiHint]:
    out: List[RoiHint] = []
    for h in hints:
        bbox = h.area_rect_img
        constraints: Dict[str, Any] = {
            "priority": int(h.priority),
            "confidence": h.confidence,
            "ttl_s": h.ttl_s,
            "reason_codes": list(h.reason_codes),
        }
        if h.meta:
            constraints.update(h.meta)
        out.append(
            RoiHint(
                area_type=h.roi_kind.value,
                hint=_hint_label(h),
                bbox=bbox,
                weight=max(0.0, min(1.0, h.confidence)),
                constraints=constraints,
                source="pal",
            )
        )
    return out
