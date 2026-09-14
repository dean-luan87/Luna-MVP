from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def build_ocr_manager_region_attribution_v1(
    raw_evidence: Sequence[Mapping[str, Any]],
    input_candidate: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    known_region_ids = {
        str(region.get("region_id") or "")
        for region in (input_candidate.get("region_candidates") or [])
        if isinstance(region, dict)
    }

    candidates = []
    for index, item in enumerate(raw_evidence):
        region_ref = str(item.get("region_ref") or f"region_{index}")
        unresolved = region_ref not in known_region_ids and len(known_region_ids) > 0
        candidates.append(
            {
                "region_id": region_ref,
                "region_type": "text_region",
                "line_id": str(item.get("line_ref") or f"line_{index}"),
                "text_block_id": f"text_block_{index}",
                "parent_region": "poster_region"
                if "poster" in region_ref
                else "object_or_sign_region",
                "overlapping_region_candidates": tuple(
                    sorted(rid for rid in known_region_ids if rid and rid != region_ref)
                ),
                "unresolved_attribution": unresolved,
                "attribution_confidence_candidate": float(
                    item.get("confidence") or 0.0
                ),
                "candidate_only": True,
            }
        )
    return tuple(candidates)
