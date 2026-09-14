from __future__ import annotations

from typing import Any, Dict, Tuple

MODULE_SCHEMA_VERSION = "field_perception_orchestrator_module_v1"
CAPABILITY_ID = "luna.field_perception_orchestrator"

BOUNDARY_FALSE_FIELDS: Tuple[str, ...] = (
    "model_invocation_executed",
    "camera_capture_executed",
    "state_mutation_executed",
    "fact_admission_executed",
    "action_execution_executed",
    "runtime_loop_executed",
)

MODULE_STATUSES = {
    "invalid_input",
    "no_visual_invocation_required",
    "plan_candidate_ready",
    "degraded_resource_plan",
    "manual_review_required",
    "internal_error",
}


def not_fact() -> Dict[str, Any]:
    return {"candidate_only": True, "fact_status": "not_fact", "write_allowed": False}
