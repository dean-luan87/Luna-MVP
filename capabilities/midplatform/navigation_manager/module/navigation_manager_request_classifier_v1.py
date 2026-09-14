from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    SUPPORTED_NAVIGATION_MODES,
    not_fact,
)


def build_navigation_request_classification_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    mode = str(input_candidate.get("navigation_mode") or "")
    route_required = mode in {
        "route_following",
        "deviation_check",
        "crossing_support",
        "obstacle_support",
        "find_landmark",
        "arrival_check",
        "resume_navigation",
    }
    visual_evidence_preferred = mode in {
        "crossing_support",
        "obstacle_support",
        "find_landmark",
        "baseline_safety",
    }
    return {
        "schema_version": "navigation_manager_request_classifier_v1",
        "navigation_mode": mode,
        "navigation_mode_supported": mode in SUPPORTED_NAVIGATION_MODES,
        "route_required": route_required,
        "visual_evidence_preferred": visual_evidence_preferred,
        "pause_requested": mode == "pause_navigation",
        "resume_requested": mode == "resume_navigation",
        **not_fact(),
    }
