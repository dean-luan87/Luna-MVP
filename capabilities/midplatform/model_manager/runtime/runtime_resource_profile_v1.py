# -*- coding: utf-8 -*-
"""Runtime Resource Profile — unified local/external resource view v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

EXECUTION_MODES = ("external_api", "local_runtime")


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_resource_profile(
    *,
    model_id: str,
    execution_mode: str,
    gpu_memory_required_gb: float = 0,
    gpu_memory_available_gb: float = 0,
    cpu_load_percent: float = 0,
    inference_time_ms_avg: float = 0,
    concurrent_limit: int = 1,
    cost_tier: str = "medium",
    api_quota_available: bool = True,
    runtime_status: str = "available",
) -> Dict[str, Any]:
    """Build unified resource profile for any execution mode."""
    if execution_mode == "external_api":
        resource = {
            "cost_tier": cost_tier,
            "latency_ms_avg": inference_time_ms_avg,
            "api_quota_available": api_quota_available,
            "runtime_status": "available" if api_quota_available else "offline",
        }
    else:
        resource = {
            "gpu_memory_required_gb": gpu_memory_required_gb,
            "gpu_memory_available_gb": gpu_memory_available_gb,
            "cpu_load_percent": cpu_load_percent,
            "inference_time_ms_avg": inference_time_ms_avg,
            "concurrent_limit": concurrent_limit,
            "runtime_status": runtime_status,
        }

    return {
        "profile_id": _uid("lrp"),
        "model_id": model_id,
        "execution_mode": execution_mode,
        "resource": resource,
        "candidate_only": True,
        "not_fact": True,
    }


def is_resource_available(profile: Dict[str, Any]) -> bool:
    """Check if provider is available for routing."""
    mode = profile.get("execution_mode", "")
    resource = profile.get("resource") or {}
    status = resource.get("runtime_status", "available")

    if status in ("offline", "insufficient", "busy"):
        return False

    if mode == "local_runtime":
        required = resource.get("gpu_memory_required_gb", 0)
        available = resource.get("gpu_memory_available_gb", 0)
        return available >= required and status == "available"

    if mode == "external_api":
        return resource.get("api_quota_available", True) is True

    return status == "available"


def resource_availability_score(profile: Dict[str, Any]) -> float:
    """0-1 score for routing — lower when resource constrained."""
    if not is_resource_available(profile):
        return 0.0
    mode = profile.get("execution_mode", "")
    resource = profile.get("resource") or {}
    if mode == "local_runtime":
        required = resource.get("gpu_memory_required_gb", 1) or 1
        available = resource.get("gpu_memory_available_gb", 0)
        headroom = max(0, available - required) / required
        return round(min(1.0, 0.5 + headroom * 0.5), 2)
    return 1.0 if resource.get("api_quota_available") else 0.0
