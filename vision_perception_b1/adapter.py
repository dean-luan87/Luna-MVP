from __future__ import annotations

from typing import List, Dict, Any

from vision_ocr.types import ReferenceCard
from dynamic_view.roi import RoiHint


def to_reference_cards(tokens: List[Dict[str, Any]], roi: RoiHint) -> List[ReferenceCard]:
    cards: List[ReferenceCard] = []
    for t in tokens:
        cards.append(
            ReferenceCard(
                kind="vision_reference",
                meaning=t.get("text") or t.get("label") or "",
                confidence=float(t.get("confidence", 0.0) or 0.0),
                bbox=roi.bbox,
                attrs={
                    "roi_kind": roi.area_type,
                    "roi_bbox": roi.bbox,
                },
            )
        )
    return cards
