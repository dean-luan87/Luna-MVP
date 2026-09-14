# -*- coding: utf-8 -*-
"""Model Admission Processor — admission pipeline v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    transition_model_state,
)

ADMISSION_STAGES = (
    "model_candidate",
    "security_review",
    "capability_review",
    "benchmark",
    "admission_decision",
    "available_pool",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def start_admission_pipeline(
    *,
    model_record: Dict[str, Any],
) -> Dict[str, Any]:
    """Begin admission: candidate → evaluating."""
    result = transition_model_state(
        model_record=model_record,
        to_state="evaluating",
        reason="admission_pipeline_started",
        trigger="admission_processor",
    )
    if not result.get("success"):
        return result

    record = result["model_record"]
    record["admission_pipeline"] = [
        {"stage": "model_candidate", "status": "completed"},
        {"stage": "security_review", "status": "completed"},
        {"stage": "capability_review", "status": "completed"},
        {"stage": "benchmark", "status": "in_progress"},
        {"stage": "admission_decision", "status": "pending"},
        {"stage": "available_pool", "status": "pending"},
    ]
    return {
        "success": True,
        "admission_id": _uid("adm"),
        "model_record": record,
        "pipeline_started": True,
        "no_auto_admission": True,
        "candidate_only": True,
        "not_fact": True,
    }


def complete_admission(
    *,
    model_record: Dict[str, Any],
    benchmark_record: Dict[str, Any],
    approve: bool = True,
) -> Dict[str, Any]:
    """Complete admission after benchmark — evaluating → admitted or back to candidate."""
    eval_status = benchmark_record.get("evaluation_status", "failed")
    passed = approve and eval_status == "passed"

    if not passed:
        result = transition_model_state(
            model_record=model_record,
            to_state="candidate",
            reason="evaluation_failed",
            trigger="admission_processor",
        )
        record = result.get("model_record", model_record)
        pipeline = list(record.get("admission_pipeline") or [])
        for stage in pipeline:
            if stage.get("stage") == "benchmark":
                stage["status"] = "failed"
        record["admission_pipeline"] = pipeline
        record["admission_status"] = "rejected"
        return {
            "success": True,
            "admitted": False,
            "model_record": record,
            "benchmark_record": benchmark_record,
            "routing_eligible": False,
            "evaluation_failed": True,
            "no_auto_admission": True,
            "candidate_only": True,
            "not_fact": True,
        }

    result = transition_model_state(
        model_record=model_record,
        to_state="admitted",
        reason="benchmark_passed",
        trigger="admission_processor",
    )
    record = result["model_record"]
    pipeline = list(record.get("admission_pipeline") or [])
    for stage in pipeline:
        if stage.get("stage") in ("benchmark", "admission_decision", "available_pool"):
            stage["status"] = "completed" if stage["stage"] != "available_pool" else "pending"
    record["admission_pipeline"] = pipeline
    record["benchmark_record_ref"] = benchmark_record.get("record_id")

    return {
        "success": True,
        "admitted": True,
        "model_record": record,
        "benchmark_record": benchmark_record,
        "routing_eligible": result.get("routing_eligible", False),
        "no_auto_admission": True,
        "candidate_only": True,
        "not_fact": True,
    }


def register_capability_for_model(
    *,
    capability_id: str,
    model_id: str,
    provider_type: str = "tool",
    priority: int = 2,
    capability_registry: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Add admitted model to capability registry (sandbox copy)."""
    registry = capability_registry or {"capabilities": []}
    caps = list(registry.get("capabilities") or [])
    entry = next((c for c in caps if c.get("capability_id") == capability_id), None)
    provider = {
        "model_id": model_id,
        "provider_type": provider_type,
        "priority": priority,
        "status": "active",
        "candidate_only": True,
    }
    if entry:
        providers = list(entry.get("providers") or [])
        if not any(p.get("model_id") == model_id for p in providers):
            providers.append(provider)
        entry["providers"] = providers
    else:
        caps.append({
            "capability_id": capability_id,
            "providers": [provider],
            "candidate_only": True,
        })
    registry["capabilities"] = caps
    return {
        "capability_id": capability_id,
        "model_id": model_id,
        "registry_updated": True,
        "capability_registry": registry,
        "candidate_only": True,
        "not_fact": True,
    }
