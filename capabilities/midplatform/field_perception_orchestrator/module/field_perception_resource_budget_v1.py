from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_resource_budget_plan_v1(
    resource_budget: Mapping[str, Any],
    requested_capabilities: tuple[str, ...],
) -> Dict[str, Any]:
    cpu = int(
        resource_budget.get("cpu_budget", resource_budget.get("cpu_cores", 2)) or 2
    )
    memory = int(
        resource_budget.get("memory_budget_mb", resource_budget.get("memory_mb", 2048))
        or 2048
    )
    latency = int(resource_budget.get("latency_budget_ms", 2500) or 2500)

    degraded = cpu < 2 or memory < 1024
    if degraded:
        requested = tuple(
            cap
            for cap in requested_capabilities
            if cap in {"detection", "ocr", "tracking"}
        )
    else:
        requested = requested_capabilities
    if not requested and requested_capabilities:
        requested = (requested_capabilities[0],)

    resolution = "low" if degraded else "standard"
    temporal_window = "short" if latency < 1000 else "normal"
    return {
        "schema_version": "field_perception_resource_budget_v1",
        "resource_degraded": degraded,
        "requested_visual_capabilities_budgeted": requested,
        "resolution_level": resolution,
        "temporal_window": temporal_window,
        "observation_priority": "high" if degraded else "normal",
    }
