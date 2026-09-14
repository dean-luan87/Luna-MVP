# -*- coding: utf-8 -*-
"""Model Lifecycle Processor — full lifecycle orchestrator v1 (sandbox)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.lifecycle.model_admission_processor_v1 import (
    complete_admission,
    register_capability_for_model,
    start_admission_pipeline,
)
from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    is_routing_eligible,
    transition_model_state,
)

ACTIVATION_POLICY_REF = "model_activation_policy_v1"
DEPRECATION_POLICY_REF = "model_deprecation_policy_v1"
BENCHMARK_SCHEMA_REF = "model_benchmark_record_schema_v1"

# In-memory sandbox registry — does not mutate production registries.
_SANDBOX_REGISTRY: Dict[str, Dict[str, Any]] = {}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _persist(model_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
    _SANDBOX_REGISTRY[model_id] = record
    return record


def reset_sandbox_registry() -> None:
    """Clear sandbox state between test cases."""
    _SANDBOX_REGISTRY.clear()


def discover_model(
    *,
    model_id: str,
    model_label: str,
    model_type: str,
    capabilities: List[str],
    owner: str = "external_teacher",
) -> Dict[str, Any]:
    """Step 0: Model discovered → registered as candidate."""
    record = {
        "model_id": model_id,
        "model_label": model_label,
        "type": model_type,
        "owner": owner,
        "capabilities": capabilities,
        "lifecycle_state": "discovered",
        "admission_status": "pending",
        "lifecycle_trace": [],
        "candidate_only": True,
        "not_fact": True,
        "sandbox": True,
    }
    result = transition_model_state(
        model_record=record,
        to_state="candidate",
        reason="registration_complete",
        trigger="lifecycle_processor",
    )
    if result.get("success"):
        record = result["model_record"]
    _persist(model_id, record)
    return {
        "discovery_id": _uid("disc"),
        "model_record": record,
        "lifecycle_state": record.get("lifecycle_state"),
        "candidate_only": True,
        "not_fact": True,
    }


def run_sandbox_evaluation(
    *,
    model_id: str,
    capability_id: str,
    reliability: float,
    latency_ms: float,
    cost_tier: str = "medium",
    unsupported_claim_rate: float = 0.0,
    scene_type: str = "unknown_scene",
    force_fail: bool = False,
) -> Dict[str, Any]:
    """Run sandbox benchmark evaluation — produces model_evaluation_record."""
    record = _SANDBOX_REGISTRY.get(model_id)
    if not record:
        return {"success": False, "error": "model_not_in_sandbox", "model_id": model_id}

    passed = not force_fail and reliability >= 0.5 and unsupported_claim_rate < 0.5
    eval_status = "passed" if passed else "failed"

    benchmark = {
        "record_id": _uid("mbr"),
        "model_id": model_id,
        "capability_id": capability_id,
        "scene_type": scene_type,
        "evaluation_status": eval_status,
        "reliability": reliability,
        "latency_ms": latency_ms,
        "cost_tier": cost_tier,
        "unsupported_claim_rate": unsupported_claim_rate,
        "routing_eligible_after_eval": passed,
        "model_evaluation_record": True,
        "candidate_only": True,
        "not_fact": True,
    }
    record["last_benchmark"] = benchmark
    _persist(model_id, record)

    return {
        "success": True,
        "benchmark_record": benchmark,
        "evaluation_status": eval_status,
        "evaluation_failed": not passed,
        "does_not_affect_current_decision": True,
        "no_auto_policy_update": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_full_lifecycle_sandbox(
    *,
    model_id: str,
    model_label: str,
    model_type: str,
    capabilities: List[str],
    capability_id: str,
    reliability: float,
    latency_ms: float,
    cost_tier: str = "medium",
    unsupported_claim_rate: float = 0.0,
    owner: str = "external_teacher",
    force_eval_fail: bool = False,
    auto_activate: bool = True,
) -> Dict[str, Any]:
    """
    Full sandbox lifecycle:
    discovered → candidate → evaluating → admitted → active
    """
    lifecycle_id = _uid("lcs")
    discovery = discover_model(
        model_id=model_id,
        model_label=model_label,
        model_type=model_type,
        capabilities=capabilities,
        owner=owner,
    )
    record = discovery["model_record"]

    admission_start = start_admission_pipeline(model_record=record)
    if not admission_start.get("success"):
        return {"success": False, "lifecycle_id": lifecycle_id, "stage": "admission_start", **admission_start}
    record = admission_start["model_record"]

    evaluation = run_sandbox_evaluation(
        model_id=model_id,
        capability_id=capability_id,
        reliability=reliability,
        latency_ms=latency_ms,
        cost_tier=cost_tier,
        unsupported_claim_rate=unsupported_claim_rate,
        force_fail=force_eval_fail,
    )
    benchmark = evaluation["benchmark_record"]

    admission = complete_admission(
        model_record=record,
        benchmark_record=benchmark,
        approve=not force_eval_fail,
    )
    record = admission["model_record"]
    _persist(model_id, record)

    activation = None
    cap_update = None
    if admission.get("admitted") and auto_activate:
        activation = activate_model(model_id=model_id)
        record = activation.get("model_record", record)
        cap_update = register_capability_for_model(
            capability_id=capability_id,
            model_id=model_id,
            provider_type="teacher" if model_type == "teacher" else "tool",
        )

    return {
        "lifecycle_id": lifecycle_id,
        "success": admission.get("admitted", False) or force_eval_fail,
        "model_id": model_id,
        "model_record": record,
        "discovery": discovery,
        "admission_start": admission_start,
        "evaluation": evaluation,
        "admission": admission,
        "activation": activation,
        "capability_registry_update": cap_update,
        "routing_eligible": is_routing_eligible(
            record.get("lifecycle_state", ""),
            admission_status=record.get("admission_status", ""),
        ),
        "lifecycle_trace": record.get("lifecycle_trace", []),
        "sandbox_only": True,
        "no_auto_execution": True,
        "candidate_only": True,
        "not_fact": True,
    }


def activate_model(*, model_id: str) -> Dict[str, Any]:
    """admitted → active."""
    record = _SANDBOX_REGISTRY.get(model_id)
    if not record:
        return {"success": False, "error": "model_not_in_sandbox"}
    result = transition_model_state(
        model_record=record,
        to_state="active",
        reason="activation_approved",
        trigger="lifecycle_processor",
    )
    if result.get("success"):
        _persist(model_id, result["model_record"])
    return {
        **result,
        "activation_policy_ref": ACTIVATION_POLICY_REF,
        "no_auto_activation": False,
        "sandbox_activation": True,
    }


def deprecate_model(
    *,
    model_id: str,
    replacement_model_id: Optional[str] = None,
    reason: str = "replacement_available",
) -> Dict[str, Any]:
    """active → deprecated; preserve trace."""
    record = _SANDBOX_REGISTRY.get(model_id)
    if not record:
        return {"success": False, "error": "model_not_in_sandbox"}
    prior_trace_len = len(record.get("lifecycle_trace", []))
    result = transition_model_state(
        model_record=record,
        to_state="deprecated",
        reason=reason,
        trigger="lifecycle_processor",
    )
    if result.get("success"):
        updated = result["model_record"]
        if replacement_model_id:
            updated["replaced_by"] = replacement_model_id
        _persist(model_id, updated)
        result["model_record"] = updated
        result["trace_preserved"] = len(updated.get("lifecycle_trace", [])) > prior_trace_len
    return {
        **result,
        "deprecation_policy_ref": DEPRECATION_POLICY_REF,
        "routing_eligible": False,
        "preserve_trace": True,
    }


def block_model(
    *,
    model_id: str,
    reason: str = "policy_violation",
    violation_type: str = "unsupported_claim_abuse",
) -> Dict[str, Any]:
    """any → blocked."""
    record = _SANDBOX_REGISTRY.get(model_id)
    if not record:
        return {"success": False, "error": "model_not_in_sandbox"}
    result = transition_model_state(
        model_record=record,
        to_state="blocked",
        reason=reason,
        trigger="lifecycle_processor",
    )
    if result.get("success"):
        updated = result["model_record"]
        updated["violation_type"] = violation_type
        _persist(model_id, updated)
        result["model_record"] = updated
    return {
        **result,
        "routing_eligible": False,
        "execution_eligible": False,
        "blocked_permanently": True,
    }


def get_sandbox_model(model_id: str) -> Optional[Dict[str, Any]]:
    return deepcopy(_SANDBOX_REGISTRY.get(model_id))
