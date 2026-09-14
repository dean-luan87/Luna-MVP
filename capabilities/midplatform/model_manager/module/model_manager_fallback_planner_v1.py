from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Tuple


def build_fallback_candidates_v1(
    *,
    admitted_model_candidates: Iterable[Mapping[str, Any]],
    selected_model_candidate: Mapping[str, Any],
    rejected_model_candidates: Iterable[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], ...]:
    selected_id = str(selected_model_candidate.get("model_id", ""))
    fallbacks = []
    for row in admitted_model_candidates:
        model_id = str(row.get("model_id", ""))
        if not model_id or model_id == selected_id:
            continue
        fallbacks.append(
            {
                "model_id": model_id,
                "reason": "admitted_backup_candidate",
            }
        )

    if not fallbacks and any(True for _ in rejected_model_candidates):
        fallbacks.append(
            {
                "model_id": "human_review",
                "reason": "all_models_rejected",
            }
        )

    return tuple(fallbacks)
