# -*- coding: utf-8 -*-
"""Local Model Runtime Adapter — Model Manager runtime bridge v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.runtime_health_checker_v1 import (
    check_runtime_health,
)
from capabilities.midplatform.model_manager.runtime.runtime_resource_profile_v1 import (
    build_resource_profile,
    is_resource_available,
)

ADAPTER_ID = "local_vlm_adapter"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def invoke_local_runtime(
    *,
    model_record: Dict[str, Any],
    resource_profile: Dict[str, Any],
    provider_request: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Local Runtime Adapter — planning only, no real inference.
    Model Manager → Local Runtime Adapter → GPU/CPU Runtime → Model.
    """
    invoke_id = _uid("lri")
    model_id = model_record.get("model_id", "")

    if model_record.get("lifecycle_state") not in ("active", "admitted"):
        return {
            "invoke_id": invoke_id,
            "invoked": False,
            "skip_reason": "lifecycle_not_active",
            "model_id": model_id,
            "adapter_id": ADAPTER_ID,
            "candidate_only": True,
        }

    if not is_resource_available(resource_profile):
        return {
            "invoke_id": invoke_id,
            "invoked": False,
            "not_available": True,
            "reason": resource_profile.get("resource", {}).get("runtime_status", "unavailable"),
            "model_id": model_id,
            "adapter_id": ADAPTER_ID,
            "provider_error_candidate": True,
            "candidate_only": True,
            "not_fact": True,
        }

    return {
        "invoke_id": invoke_id,
        "invoked": True,
        "model_id": model_id,
        "adapter_id": ADAPTER_ID,
        "execution_mode": "local_runtime",
        "evidence_candidate": {
            "evidence_type": "visual_reasoning_candidate",
            "provider_id": model_id,
            "managed_by": "model_manager",
            "execution_mode": "local_runtime",
            "candidate_only": True,
            "not_fact": True,
        },
        "not_executed": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_local_model_record(
    *,
    model_id: str,
    model_label: str,
    capabilities: list,
    gpu_memory_required_gb: float = 8,
) -> Dict[str, Any]:
    """Unified registry record — same shape as external models."""
    return {
        "model_id": model_id,
        "model_label": model_label,
        "type": "vision_language_model",
        "execution_mode": "local_runtime",
        "provider_adapter": ADAPTER_ID,
        "owner": "local_runtime",
        "capabilities": capabilities,
        "lifecycle_state": "candidate",
        "admission_status": "pending",
        "resource_profile": {
            "gpu_memory_required_gb": gpu_memory_required_gb,
            "concurrent_limit": 1,
        },
        "candidate_only": True,
        "not_fact": True,
    }


def run_environment_check(
    model_record: Dict[str, Any],
    *,
    gpu_memory_available_gb: float,
    cuda_available: bool = True,
) -> Dict[str, Any]:
    """Environment check step in local admission pipeline."""
    required = (model_record.get("resource_profile") or {}).get("gpu_memory_required_gb", 8)
    return check_runtime_health(
        model_id=model_record.get("model_id", ""),
        gpu_memory_required_gb=required,
        gpu_memory_available_gb=gpu_memory_available_gb,
        cuda_available=cuda_available,
    )
