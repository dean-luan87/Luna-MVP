# -*- coding: utf-8 -*-
"""Local Model Resource Scheduler — runtime availability v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.runtime_resource_profile_v1 import (
    build_resource_profile,
    is_resource_available,
)


def schedule_runtime_resources(
    *,
    model_ids: List[str],
    gpu_memory_available_gb: float = 12,
    internvl_status: str = "available",
    api_available: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """Build resource profiles for all candidate providers."""
    profiles: Dict[str, Dict[str, Any]] = {}

    if "internvl2_5" in model_ids:
        profiles["internvl2_5"] = build_resource_profile(
            model_id="internvl2_5",
            execution_mode="local_runtime",
            gpu_memory_required_gb=8,
            gpu_memory_available_gb=gpu_memory_available_gb,
            inference_time_ms_avg=2000,
            runtime_status=internvl_status,
        )
    if "qwen_vl" in model_ids:
        profiles["qwen_vl"] = build_resource_profile(
            model_id="qwen_vl",
            execution_mode="external_api",
            inference_time_ms_avg=3000,
            cost_tier="medium",
            api_quota_available=api_available,
        )
    if "gemini_vision" in model_ids:
        profiles["gemini_vision"] = build_resource_profile(
            model_id="gemini_vision",
            execution_mode="external_api",
            inference_time_ms_avg=500,
            cost_tier="high",
            api_quota_available=api_available,
        )
    return profiles


def check_runtime_slot(
    profile: Dict[str, Any],
) -> Dict[str, Any]:
    """Check if runtime slot is available for scheduling."""
    available = is_resource_available(profile)
    resource = profile.get("resource") or {}
    return {
        "model_id": profile.get("model_id"),
        "execution_mode": profile.get("execution_mode"),
        "runtime_available": available,
        "runtime_status": resource.get("runtime_status", "unknown"),
        "scheduler_decision": "eligible" if available else "deferred",
        "candidate_only": True,
        "not_fact": True,
    }
