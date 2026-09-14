from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_deviation_assessment_v1(
    input_candidate: Mapping[str, Any], progress_state: Mapping[str, Any]
) -> Dict[str, Any]:
    correction = dict(input_candidate.get("user_correction_candidate") or {})
    explicit_deviation = bool(correction.get("deviation_detected", False))
    progress_ratio = float(progress_state.get("progress_ratio", 0.0) or 0.0)
    deviation_detected = explicit_deviation or (
        progress_ratio < 0.15 and bool(progress_state.get("progress_present"))
    )
    reroute_candidate = (
        {
            "candidate_id": f"reroute_{input_candidate.get('navigation_request_id')}",
            "reason": "deviation_detected",
            "candidate_only": True,
            **not_fact(),
        }
        if deviation_detected
        else None
    )
    return {
        "schema_version": "navigation_manager_deviation_resolver_v1",
        "deviation_assessment": {
            "deviation_detected": deviation_detected,
            "deviation_source": "user_correction"
            if explicit_deviation
            else "progress_inference",
            "reroute_candidate": reroute_candidate,
        },
        **not_fact(),
    }
