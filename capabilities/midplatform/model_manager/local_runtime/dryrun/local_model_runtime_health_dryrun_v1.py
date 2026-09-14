# -*- coding: utf-8 -*-
"""Local Model Runtime Health — dryrun health scenarios v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.runtime_health_checker_v1 import (
    check_runtime_health,
)

LOCAL_MODEL_ID = "internvl2_5"


def run_local_runtime_health_dryrun(
    *,
    gpu_memory_available_gb: float = 12,
    cuda_available: bool = True,
    temperature_celsius: float = 65,
    concurrent_slots_used: int = 0,
) -> Dict[str, Any]:
    """Dryrun health check for local runtime provider."""
    return check_runtime_health(
        model_id=LOCAL_MODEL_ID,
        gpu_memory_required_gb=8,
        gpu_memory_available_gb=gpu_memory_available_gb,
        cuda_available=cuda_available,
        temperature_celsius=temperature_celsius,
        concurrent_slots_used=concurrent_slots_used,
    )


def build_runtime_unavailable_candidate(
    *,
    model_id: str,
    reason: str,
) -> Dict[str, Any]:
    """Explicit runtime unavailability — not silent fallback."""
    return {
        "runtime_unavailable_candidate": True,
        "model_id": model_id,
        "unavailable_reason": reason,
        "not_silent_switch": True,
        "handoff_to": "routing_validation",
        "candidate_only": True,
        "not_fact": True,
    }
