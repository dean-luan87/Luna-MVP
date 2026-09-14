from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def build_ocr_manager_human_correction_candidates_v1(
    input_candidate: Mapping[str, Any],
    raw_evidence: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], ...]:
    corrections = input_candidate.get("human_correction_input") or ()
    if not corrections:
        return tuple()

    by_evidence = {str(item.get("evidence_id") or ""): item for item in raw_evidence}
    candidates = []
    for index, correction in enumerate(corrections):
        if not isinstance(correction, dict):
            continue
        target = str(correction.get("original_ocr_ref") or "")
        corrected_text = str(correction.get("corrected_text_candidate") or "").strip()
        if not target or not corrected_text:
            continue
        source = by_evidence.get(target) or {}
        candidates.append(
            {
                "correction_id": f"human_correction_{index}",
                "correction_target": str(
                    correction.get("correction_target") or "text_block"
                ),
                "correction_type": str(
                    correction.get("correction_type") or "manual_text_update"
                ),
                "original_ocr_ref": target,
                "corrected_text_candidate": corrected_text,
                "user_correction_source": str(
                    correction.get("user_correction_source") or "human_ui"
                ),
                "reviewer_candidate": str(
                    correction.get("reviewer_candidate") or "pending_review"
                ),
                "correction_confidence": float(
                    correction.get("correction_confidence") or 0.8
                ),
                "correction_trace": {
                    "source_ref": input_candidate.get("source_ref"),
                    "request_id": input_candidate.get("request_id"),
                    "original_raw_text": source.get("raw_text"),
                },
                "training_signal_candidate": {
                    "signal_type": "human_correction",
                    "eligible": True,
                    "fact_promotion_allowed": False,
                },
                "candidate_only": True,
                "not_fact": True,
            }
        )
    return tuple(candidates)
