from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def _xy(item: Mapping[str, Any]) -> Tuple[float, float]:
    geom = (
        item.get("bounding_geometry")
        if isinstance(item.get("bounding_geometry"), dict)
        else {}
    )
    return float(geom.get("y1") or 0.0), float(geom.get("x1") or 0.0)


def build_ocr_manager_reading_order_candidates_v1(
    raw_evidence: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], ...]:
    if not raw_evidence:
        return tuple()

    ordered = tuple(sorted(raw_evidence, key=_xy))
    ordered_refs = tuple(str(item.get("line_ref") or "") for item in ordered)
    x_positions = [
        float(((item.get("bounding_geometry") or {}).get("x1") or 0.0))
        for item in ordered
        if isinstance(item.get("bounding_geometry"), dict)
    ]
    multi_column = len(x_positions) >= 2 and max(x_positions) - min(x_positions) > 120
    vertical_text = any(
        "vertical" in str(item.get("raw_text") or "").lower() for item in ordered
    )
    ambiguous = multi_column or vertical_text

    return (
        {
            "order_id": "reading_order_primary",
            "reading_order_candidate": ordered_refs,
            "left_to_right_candidate": not vertical_text,
            "top_to_bottom_candidate": True,
            "vertical_text_candidate": vertical_text,
            "multi_column_candidate": multi_column,
            "ambiguous_order": ambiguous,
            "unresolved_order": ambiguous,
            "candidate_only": True,
        },
    )
