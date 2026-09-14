# -*- coding: utf-8 -*-
"""Runtime Health Checker — local model environment validation v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

HEALTH_CHECKS = (
    "cuda_available",
    "vram_sufficient",
    "runtime_responsive",
    "temperature_within_limit",
    "concurrent_slot_available",
)


def check_runtime_health(
    *,
    model_id: str,
    gpu_memory_required_gb: float,
    gpu_memory_available_gb: float,
    cuda_available: bool = True,
    temperature_celsius: float = 65,
    cpu_load_percent: float = 40,
    concurrent_slots_used: int = 0,
    concurrent_limit: int = 1,
    max_temperature: float = 85,
) -> Dict[str, Any]:
    """Environment + runtime compatibility check for local models."""
    checks: List[Dict[str, Any]] = []

    cuda_ok = cuda_available
    checks.append({"check_id": "cuda_available", "passed": cuda_ok})

    vram_ok = gpu_memory_available_gb >= gpu_memory_required_gb
    checks.append({"check_id": "vram_sufficient", "passed": vram_ok})

    runtime_ok = cuda_ok and vram_ok
    checks.append({"check_id": "runtime_responsive", "passed": runtime_ok})

    temp_ok = temperature_celsius <= max_temperature
    checks.append({"check_id": "temperature_within_limit", "passed": temp_ok})

    slot_ok = concurrent_slots_used < concurrent_limit
    checks.append({"check_id": "concurrent_slot_available", "passed": slot_ok})

    all_passed = all(c["passed"] for c in checks)
    failure_reason = None
    if not vram_ok:
        failure_reason = "gpu_memory_insufficient"
    elif not cuda_ok:
        failure_reason = "cuda_unavailable"
    elif not slot_ok:
        failure_reason = "runtime_busy"

    return {
        "model_id": model_id,
        "health_status": "healthy" if all_passed else "unhealthy",
        "checks": checks,
        "all_passed": all_passed,
        "failure_reason": failure_reason,
        "routing_eligible": all_passed,
        "candidate_only": True,
        "not_fact": True,
    }
