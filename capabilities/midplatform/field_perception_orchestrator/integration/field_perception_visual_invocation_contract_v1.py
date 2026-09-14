from __future__ import annotations

from typing import Any, Dict, Tuple

CAPABILITY_ID = "luna.field_perception_orchestrator"
SCHEMA_VERSION = "field_perception_visual_handoff_integration_v1"

INTEGRATION_STATUSES: Tuple[str, ...] = (
    "invalid_input",
    "no_visual_invocation_required",
    "duplicate_suppressed",
    "fresh_evidence_reused",
    "budget_degraded",
    "vision_request_candidate_ready",
    "model_requirement_candidate_ready",
    "no_eligible_model",
    "observation_request_candidate_ready",
    "handoff_ready",
    "insufficient_plan",
    "permission_rejected",
    "conflicted",
    "internal_error",
)

BOUNDARY_FALSE_FIELDS: Tuple[str, ...] = (
    "vision_model_executed",
    "camera_capture_executed",
    "model_loaded",
    "model_unloaded",
    "model_switched",
    "provider_runtime_executed",
    "vision_evidence_created",
    "observation_candidate_created",
    "fact_admission_executed",
    "field_state_write_executed",
    "state_mutation_executed",
    "action_execution_executed",
    "database_write_executed",
    "runtime_loop_executed",
    "production_runtime_executed",
)


def not_fact() -> Dict[str, Any]:
    return {"candidate_only": True, "fact_status": "not_fact", "write_allowed": False}
