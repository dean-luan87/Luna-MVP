from __future__ import annotations

from typing import Any, Dict

MODULE_SCHEMA_VERSION = "navigation_manager_module_v1"
CAPABILITY_ID = "luna.navigation_manager"

SUPPORTED_NAVIGATION_MODES = {
    "route_following",
    "route_memory",
    "deviation_check",
    "crossing_support",
    "obstacle_support",
    "find_landmark",
    "arrival_check",
    "resume_navigation",
    "pause_navigation",
    "baseline_safety",
}

MODULE_STATUSES = {
    "invalid_input",
    "request_rejected",
    "route_unavailable",
    "route_ready",
    "navigation_active",
    "navigation_paused",
    "deviation_detected",
    "reroute_candidate_ready",
    "crossing_attention_required",
    "obstacle_attention_required",
    "guidance_candidate_ready",
    "arrival_candidate_ready",
    "insufficient_evidence",
    "conflicted",
    "degraded",
    "internal_error",
}

BOUNDARY_FALSE_FIELDS = (
    "real_map_lookup_executed",
    "real_gps_read_executed",
    "real_camera_read_executed",
    "real_reroute_executed",
    "navigation_action_executed",
    "fact_admission_executed",
    "fact_promotion_executed",
    "field_state_write_executed",
    "state_mutation_executed",
    "speech_output_executed",
    "database_write_executed",
    "provider_runtime_executed",
    "production_runtime_executed",
)


def not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}
