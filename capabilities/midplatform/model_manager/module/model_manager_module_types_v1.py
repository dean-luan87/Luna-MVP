from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

MODEL_MANAGER_MODULE_STATUSES_V1: Tuple[str, ...] = (
    "invalid_input",
    "no_eligible_model",
    "admission_rejected",
    "unavailable",
    "resource_insufficient",
    "ownership_blocked",
    "degraded",
    "fallback_available",
    "candidate_ready",
    "routing_ready",
    "lifecycle_plan_ready",
    "internal_error",
)


@dataclass(frozen=True)
class ModelManagerModuleRequestV1:
    request_id: str
    requested_capability: str
    task_ref: str
    device_ref: str
    region_ref: str
    resource_snapshot: Dict[str, Any]
    allowed_model_classes: Tuple[str, ...]
    forbidden_model_ids: Tuple[str, ...]
    latency_requirement: int
    memory_budget: int
    offline_required: bool
    privacy_requirement: str
    ownership_context: Dict[str, Any]
    version_snapshot: Dict[str, str]
    trace_context: Dict[str, Any]


@dataclass(frozen=True)
class ModelManagerModuleResultV1:
    module_status: str
    requested_capability: str
    admitted_model_candidates: Tuple[Dict[str, Any], ...]
    rejected_model_candidates: Tuple[Dict[str, Any], ...]
    selected_model_candidate: Dict[str, Any]
    fallback_candidates: Tuple[Dict[str, Any], ...]
    ownership_decision: Dict[str, Any]
    resource_evaluation: Dict[str, Any]
    routing_candidate: Dict[str, Any]
    lifecycle_plan: Dict[str, Any]
    health_summary: Dict[str, Any]
    rejection_reasons: Tuple[str, ...]
    diagnostics: Dict[str, Any]
    trace_ref: str
    replay_key: str
    model_inference_executed: bool
    model_load_executed: bool
    model_unload_executed: bool
    model_download_executed: bool
    model_training_executed: bool
    provider_call_executed: bool
    state_mutation_executed: bool
    fact_promotion_executed: bool
    action_trigger_executed: bool
    production_runtime_executed: bool
