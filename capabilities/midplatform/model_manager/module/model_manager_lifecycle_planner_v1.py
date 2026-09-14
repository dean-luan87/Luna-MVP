from __future__ import annotations

from typing import Any, Dict, Mapping


def build_lifecycle_plan_v1(
    *,
    selected_model_candidate: Mapping[str, Any],
    resource_evaluation: Mapping[str, Any],
) -> Dict[str, Any]:
    selected_id = str(selected_model_candidate.get("model_id", ""))
    if not selected_id:
        return {
            "plan_status": "no_selected_model",
            "load_plan": (),
            "unload_plan": (),
            "availability_state": "unavailable",
            "candidate_only": True,
        }

    degrade = bool(resource_evaluation.get("latency_not_met", False))
    return {
        "plan_status": "lifecycle_plan_ready",
        "load_plan": (
            {
                "model_id": selected_id,
                "intent": "load_candidate",
                "executed": False,
            },
        ),
        "unload_plan": tuple(),
        "availability_state": "degraded" if degrade else "available_candidate",
        "candidate_only": True,
    }
