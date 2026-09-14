from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple


def run_model_admission_v1(
    *,
    provider_records: Sequence[Mapping[str, Any]],
    allowed_model_classes: Iterable[str],
    forbidden_model_ids: Iterable[str],
    privacy_requirement: str,
) -> Dict[str, Any]:
    allowed = {str(x) for x in allowed_model_classes if str(x)}
    forbidden = {str(x) for x in forbidden_model_ids}

    admitted = []
    rejected = []

    for row in provider_records:
        model_id = str(row.get("model_id", ""))
        model_class = str(row.get("provider_type", row.get("type", "")))
        lifecycle = str(row.get("lifecycle_state", "candidate"))
        admission = str(row.get("admission_status", "pending"))

        reasons = []
        if model_id in forbidden:
            reasons.append("forbidden_model_id")
        if allowed and model_class not in allowed:
            reasons.append("class_not_allowed")
        if lifecycle in {"blocked", "deprecated"}:
            reasons.append("lifecycle_not_routable")
        if admission not in {"admitted", "active", ""}:
            reasons.append("admission_not_ready")
        if (
            privacy_requirement == "high"
            and str(row.get("execution_mode", "")) == "external_api"
        ):
            reasons.append("privacy_restricted_external_api")

        candidate = {
            "model_id": model_id,
            "provider_type": model_class,
            "lifecycle_state": lifecycle,
            "admission_status": admission,
            "execution_mode": str(row.get("execution_mode", "")),
        }

        if reasons:
            rejected.append({**candidate, "rejection_reasons": tuple(reasons)})
        else:
            admitted.append({**candidate, "admitted": True})

    return {
        "admitted_model_candidates": tuple(admitted),
        "rejected_model_candidates": tuple(rejected),
        "admission_rejected": len(admitted) == 0,
    }
