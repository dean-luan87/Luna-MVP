from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping

from capabilities.midplatform.model_manager.registry.multi_provider_selection_v1 import (
    select_multi_provider_candidate,
)


def build_routing_candidate_v1(
    *,
    required_capability: str,
    admitted_model_candidates: Iterable[Mapping[str, Any]],
    resource_snapshot: Mapping[str, Any],
) -> Dict[str, Any]:
    admitted_ids = {str(x.get("model_id", "")) for x in admitted_model_candidates}

    runtime_availability = {
        "internvl2_5": {
            "available": bool(resource_snapshot.get("local_runtime_available", True)),
        },
        "external_api": {
            "network_available": bool(resource_snapshot.get("network_available", True)),
            "qwen_available": bool(resource_snapshot.get("qwen_available", True)),
            "gemini_available": bool(resource_snapshot.get("gemini_available", True)),
        },
    }

    routed = select_multi_provider_candidate(
        capability_id=required_capability,
        runtime_availability=runtime_availability,
        historical_performance=dict(
            resource_snapshot.get("historical_performance") or {}
        ),
        scoring_mode=str(resource_snapshot.get("scoring_mode", "balanced")),
        execute=False,
    )

    selected = routed.get("selected_provider") or {}
    selected_id = str(selected.get("model_id", ""))
    if selected_id and selected_id not in admitted_ids:
        selected = {}

    return {
        "routing_candidate": routed,
        "selected_model_candidate": selected,
        "routing_ready": bool(selected),
    }
