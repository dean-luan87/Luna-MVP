from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence


def build_ocr_manager_diagnostics_v1(
    *,
    module_status: str,
    governance: Mapping[str, Any],
    engine_capability: Mapping[str, Any],
    region_attribution_candidates: Sequence[Mapping[str, Any]],
    layout_candidates: Sequence[Mapping[str, Any]],
    reading_order_candidates: Sequence[Mapping[str, Any]],
    enhancement_candidates: Sequence[Mapping[str, Any]],
    correction_candidates: Sequence[Mapping[str, Any]],
    crossmodal_consistency_candidates: Sequence[Mapping[str, Any]],
    rejection_reasons: Sequence[str],
) -> Dict[str, Any]:
    boundary_flags = {
        "fact_admission_executed": False,
        "state_mutation_executed": False,
        "action_execution_executed": False,
        "navigation_decision_executed": False,
        "speech_output_executed": False,
        "database_write_executed": False,
        "provider_recall_executed": False,
        "external_lookup_executed": False,
        "model_training_executed": False,
        "production_runtime_executed": False,
    }
    unresolved_items = []
    if any(
        bool(item.get("unresolved_attribution"))
        for item in region_attribution_candidates
    ):
        unresolved_items.append("region_attribution")
    if any(bool(item.get("ambiguous_order")) for item in reading_order_candidates):
        unresolved_items.append("reading_order")
    if any(
        str(item.get("status") or "") in {"unresolved_candidate", "conflict_candidate"}
        for item in crossmodal_consistency_candidates
    ):
        unresolved_items.append("crossmodal_consistency")

    return {
        "module_status": module_status,
        "request_status": "accepted" if governance.get("admitted") else "rejected",
        "engine_candidate_status": str(
            (
                (engine_capability.get("selected_engine") or {}).get("engine_readiness")
                or "unavailable"
            )
        ),
        "region_status": "unresolved"
        if "region_attribution" in unresolved_items
        else "ready",
        "layout_status": "ready" if layout_candidates else "none",
        "reading_order_status": "ambiguous"
        if "reading_order" in unresolved_items
        else "ready",
        "enhancement_status": "ready" if enhancement_candidates else "none",
        "correction_status": "ready" if correction_candidates else "none",
        "crossmodal_status": "unresolved"
        if "crossmodal_consistency" in unresolved_items
        else "ready",
        "unresolved_items": tuple(unresolved_items),
        "rejection_reasons": tuple(rejection_reasons),
        "warnings": tuple({f"unresolved_{name}" for name in unresolved_items}),
        "boundary_flags": boundary_flags,
    }
