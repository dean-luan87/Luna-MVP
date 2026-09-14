from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from capabilities.midplatform.model_manager.module.model_manager_module_types_v1 import (
    MODEL_MANAGER_MODULE_STATUSES_V1,
)


def _normalize_status(status: str) -> str:
    if status in MODEL_MANAGER_MODULE_STATUSES_V1:
        return status
    return "internal_error"


def build_module_output_v1(
    *,
    module_status: str,
    required_capability: str,
    admitted_model_candidates: Sequence[Mapping[str, Any]],
    rejected_model_candidates: Sequence[Mapping[str, Any]],
    selected_model_candidate: Mapping[str, Any],
    fallback_candidates: Sequence[Mapping[str, Any]],
    ownership_decision: Mapping[str, Any],
    resource_evaluation: Mapping[str, Any],
    routing_candidate: Mapping[str, Any],
    lifecycle_plan: Mapping[str, Any],
    health_summary: Mapping[str, Any],
    rejection_reasons: Iterable[str],
    diagnostics: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    return {
        "module_status": _normalize_status(module_status),
        "requested_capability": required_capability,
        "admitted_model_candidates": tuple(dict(x) for x in admitted_model_candidates),
        "rejected_model_candidates": tuple(dict(x) for x in rejected_model_candidates),
        "selected_model_candidate": dict(selected_model_candidate),
        "fallback_candidates": tuple(dict(x) for x in fallback_candidates),
        "ownership_decision": dict(ownership_decision),
        "resource_evaluation": dict(resource_evaluation),
        "routing_candidate": dict(routing_candidate),
        "lifecycle_plan": dict(lifecycle_plan),
        "health_summary": dict(health_summary),
        "rejection_reasons": tuple(str(x) for x in rejection_reasons),
        "diagnostics": dict(diagnostics),
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "candidate_only": True,
        "not_fact": True,
        "model_inference_executed": False,
        "model_load_executed": False,
        "model_unload_executed": False,
        "model_download_executed": False,
        "model_training_executed": False,
        "provider_call_executed": False,
        "state_mutation_executed": False,
        "fact_promotion_executed": False,
        "action_trigger_executed": False,
        "production_runtime_executed": False,
    }
