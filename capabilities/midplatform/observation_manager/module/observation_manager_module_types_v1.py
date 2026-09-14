from __future__ import annotations

from typing import Any, Dict

MODULE_SCHEMA_VERSION = "observation_manager_module_v1"
CAPABILITY_ID = "luna.observation_manager"

SUPPORTED_REQUEST_TYPES = {
    "baseline_safety",
    "task_driven",
    "navigation_support",
    "find_object",
    "find_text",
    "read_text",
    "scene_understanding",
    "human_correction_review",
    "passive_observation",
    "verification_observation",
}

MODULE_STATUSES = {
    "invalid_input",
    "request_rejected",
    "context_incomplete",
    "attention_plan_ready",
    "evidence_requested",
    "evidence_partial",
    "evidence_insufficient",
    "evidence_conflicted",
    "observation_candidate_ready",
    "admission_handoff_ready",
    "no_observation_required",
    "degraded",
    "internal_error",
}

BOUNDARY_FALSE_FIELDS = (
    "fact_admission_executed",
    "fact_promotion_executed",
    "field_state_write_executed",
    "state_mutation_executed",
    "action_execution_executed",
    "navigation_decision_executed",
    "speech_output_executed",
    "provider_runtime_executed",
    "model_training_executed",
    "database_write_executed",
    "production_runtime_executed",
)


def not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}
