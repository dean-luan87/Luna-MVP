from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def build_ocr_manager_crossmodal_consistency_v1(
    raw_evidence: Sequence[Mapping[str, Any]],
    input_candidate: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    context = input_candidate.get("crossmodal_context") or {}
    expected_text = str(context.get("expected_text") or "").strip().lower()
    known_entity = str(context.get("known_entity_candidate") or "").strip().lower()

    if not raw_evidence:
        return (
            {
                "consistency_id": "crossmodal_unresolved_0",
                "status": "unresolved_candidate",
                "compared_with": "task_context",
                "detail": "no_raw_text_evidence",
                "candidate_only": True,
            },
        )

    statuses = []
    for index, item in enumerate(raw_evidence):
        text = str(
            item.get("normalized_text_candidate") or item.get("raw_text") or ""
        ).lower()
        status = "unresolved_candidate"
        detail = "insufficient_crossmodal_signal"
        if expected_text and expected_text in text:
            status = "consistent_candidate"
            detail = "expected_text_matched"
        elif expected_text and text and expected_text not in text:
            status = "inconsistent_candidate"
            detail = "expected_text_not_found"
        if (
            known_entity
            and text
            and known_entity not in text
            and status == "inconsistent_candidate"
        ):
            status = "conflict_candidate"
            detail = "known_entity_conflict"

        statuses.append(
            {
                "consistency_id": f"crossmodal_{index}",
                "status": status,
                "compared_with": "visual_object/poster/task_context/known_entity",
                "detail": detail,
                "candidate_only": True,
            }
        )
    return tuple(statuses)
