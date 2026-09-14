from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence

from capabilities.midplatform.model_manager.runtime.runtime_health_checker_v1 import (
    check_runtime_health,
)
from capabilities.midplatform.model_manager.runtime.runtime_resource_profile_v1 import (
    build_resource_profile,
    is_resource_available,
)


def evaluate_resources_v1(
    *,
    admitted_candidates: Sequence[Mapping[str, Any]],
    resource_snapshot: Mapping[str, Any],
    latency_requirement: int,
    memory_budget: int,
    offline_required: bool,
) -> Dict[str, Any]:
    if not admitted_candidates:
        return {
            "resource_ok": False,
            "resource_insufficient": False,
            "latency_not_met": False,
            "offline_mismatch": False,
            "per_candidate": tuple(),
        }

    per_candidate = []
    resource_insufficient = False
    latency_not_met = False
    offline_mismatch = False

    for c in admitted_candidates:
        mode = str(c.get("execution_mode", "external_api") or "external_api")
        model_id = str(c.get("model_id", ""))
        latency = int(resource_snapshot.get("latency_ms", 0) or 0)
        if latency_requirement and latency and latency > latency_requirement:
            latency_not_met = True

        if offline_required and mode == "external_api":
            offline_mismatch = True

        profile = build_resource_profile(
            model_id=model_id,
            execution_mode=mode,
            gpu_memory_required_gb=float(
                resource_snapshot.get("gpu_memory_required_gb", 0) or 0
            ),
            gpu_memory_available_gb=float(
                resource_snapshot.get("gpu_memory_available_gb", 0) or 0
            ),
            cpu_load_percent=float(resource_snapshot.get("cpu_load_percent", 0) or 0),
            inference_time_ms_avg=float(latency or 0),
            concurrent_limit=int(resource_snapshot.get("concurrent_limit", 1) or 1),
            cost_tier=str(resource_snapshot.get("cost_tier", "medium")),
            api_quota_available=bool(
                resource_snapshot.get("api_quota_available", True)
            ),
            runtime_status=str(resource_snapshot.get("runtime_status", "available")),
        )

        health = check_runtime_health(
            model_id=model_id,
            gpu_memory_required_gb=float(
                resource_snapshot.get("gpu_memory_required_gb", 0) or 0
            ),
            gpu_memory_available_gb=float(
                resource_snapshot.get("gpu_memory_available_gb", 0) or 0
            ),
            cuda_available=bool(resource_snapshot.get("cuda_available", True)),
            temperature_celsius=float(
                resource_snapshot.get("temperature_celsius", 65) or 65
            ),
            cpu_load_percent=float(resource_snapshot.get("cpu_load_percent", 40) or 40),
            concurrent_slots_used=int(
                resource_snapshot.get("concurrent_slots_used", 0) or 0
            ),
            concurrent_limit=int(resource_snapshot.get("concurrent_limit", 1) or 1),
        )

        available = is_resource_available(profile)
        if (
            not available
            or int(
                resource_snapshot.get("memory_available", memory_budget)
                or memory_budget
            )
            < memory_budget
        ):
            resource_insufficient = True

        per_candidate.append(
            {
                "model_id": model_id,
                "execution_mode": mode,
                "resource_profile": profile,
                "health": health,
                "resource_available": available,
            }
        )

    resource_ok = not (resource_insufficient or latency_not_met or offline_mismatch)
    return {
        "resource_ok": resource_ok,
        "resource_insufficient": resource_insufficient,
        "latency_not_met": latency_not_met,
        "offline_mismatch": offline_mismatch,
        "per_candidate": tuple(per_candidate),
    }
