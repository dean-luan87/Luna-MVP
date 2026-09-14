from __future__ import annotations

from typing import Any, Dict, Mapping


CAPABILITY_NORMALIZATION_V1 = {
    "detection": "object_detection",
    "object_detection": "object_detection",
    "ocr": "text_recognition",
    "text_recognition": "text_recognition",
    "precise_ocr": "text_recognition",
    "tracking": "object_detection",
    "temporal_tracking": "object_detection",
    "segmentation": "spatial_mapping",
    "depth": "spatial_mapping",
    "spatial_mapping": "spatial_mapping",
}


def normalize_visual_capabilities_for_model_manager_v1(
    capabilities: tuple[str, ...],
) -> tuple[str, ...]:
    normalized = []
    for capability in capabilities:
        mapped = CAPABILITY_NORMALIZATION_V1.get(str(capability), "")
        if mapped:
            normalized.append(mapped)
    return tuple(dict.fromkeys(normalized))


def _select_primary_required_capability_v1(
    normalized_capabilities: tuple[str, ...],
) -> str:
    for preferred in ("text_recognition", "object_detection", "spatial_mapping"):
        if preferred in normalized_capabilities:
            return preferred
    return normalized_capabilities[0] if normalized_capabilities else ""


def build_model_requirement_candidate_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    budget = dict(input_candidate.get("resource_budget") or {})
    effective_capabilities = tuple(
        str(x) for x in (input_candidate.get("requested_visual_capabilities") or ())
    )
    normalized_capabilities = normalize_visual_capabilities_for_model_manager_v1(
        effective_capabilities
    )
    classes = tuple(
        str(x) for x in (budget.get("preferred_model_classes") or ("teacher", "tool"))
    )
    fallback_classes = tuple(
        str(x) for x in (budget.get("fallback_model_classes") or ("tool",))
    )
    return {
        "requirement_id": f"model_req::{input_candidate.get('plan_id')}",
        "source_plan_id": input_candidate.get("plan_id"),
        "required_capabilities": normalized_capabilities,
        "source_effective_capability_plan": effective_capabilities,
        "primary_required_capability": _select_primary_required_capability_v1(
            normalized_capabilities
        ),
        "preferred_model_classes": classes,
        "fallback_model_classes": fallback_classes,
        "minimum_confidence": float(
            input_candidate.get("confidence_requirement") or 0.8
        ),
        "latency_class": str(budget.get("latency_class") or "near_real_time"),
        "memory_budget": int(
            budget.get("memory_budget") or budget.get("memory_budget_mb") or 2048
        ),
        "compute_budget": int(
            budget.get("compute_budget") or budget.get("compute_budget_units") or 2
        ),
        "device_constraints": dict(budget.get("device_constraints") or {}),
        "admission_required": True,
        "ownership_required": True,
        "version_constraints": dict(input_candidate.get("version_snapshot") or {}),
        "candidate_only": True,
    }
