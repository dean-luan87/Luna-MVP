from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Sequence, Tuple


def build_ocr_manager_raw_evidence_v1(
    input_candidate: Mapping[str, Any],
    engine_capability: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    fixture = input_candidate.get("synthetic_integration_fixture") or {}
    text_items: Sequence[Mapping[str, Any]] = (
        fixture.get("text_items") if isinstance(fixture.get("text_items"), list) else []
    )

    if not text_items and str(fixture.get("raw_text") or "").strip():
        text_items = (
            {
                "raw_text": str(fixture.get("raw_text") or ""),
                "confidence": float(fixture.get("confidence") or 0.5),
                "language": str(fixture.get("language") or "unknown"),
                "bbox": fixture.get("bbox") or {"x1": 0, "y1": 0, "x2": 0, "y2": 0},
            },
        )

    now = datetime.now(timezone.utc).isoformat()
    engine_ref = str(
        (
            (engine_capability.get("selected_engine") or {}).get("engine_identity")
            or "unknown_engine"
        )
    )
    evidence = []
    for index, item in enumerate(text_items):
        raw_text = str(item.get("raw_text") or "")
        if not raw_text.strip():
            continue
        evidence.append(
            {
                "evidence_id": f"ocr_raw_{input_candidate.get('request_id')}_{index}",
                "raw_text": raw_text,
                "normalized_text_candidate": str(
                    item.get("normalized_text_candidate") or raw_text.strip()
                ),
                "region_ref": str(item.get("region_ref") or f"region_{index}"),
                "line_ref": str(item.get("line_ref") or f"line_{index}"),
                "engine_ref": engine_ref,
                "confidence": float(item.get("confidence") or 0.0),
                "language_candidate": str(item.get("language") or "unknown"),
                "bounding_geometry": item.get("bbox")
                or {"x1": 0, "y1": 0, "x2": 0, "y2": 0},
                "source_frame_ref": str(input_candidate.get("frame_ref") or ""),
                "captured_at": str(item.get("captured_at") or now),
                "evidence_status": "candidate",
            }
        )
    return tuple(evidence)
