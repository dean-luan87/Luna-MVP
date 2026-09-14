from __future__ import annotations

from typing import Any, Dict, Mapping


def build_invocation_budget_guard_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    budget = dict(input_candidate.get("resource_budget") or {})
    requested = tuple(input_candidate.get("requested_visual_capabilities") or ())

    memory = int(budget.get("memory_budget") or budget.get("memory_budget_mb") or 2048)
    compute = int(
        budget.get("compute_budget") or budget.get("compute_budget_units") or 2
    )
    latency = int(
        budget.get("latency_budget") or budget.get("latency_budget_ms") or 2000
    )
    power = int(budget.get("power_budget") or 2)
    concurrent_limit = int(budget.get("concurrent_invocation_limit") or 2)

    if memory < 768 or compute <= 0 or power <= 0 or concurrent_limit <= 0:
        level = "critical"
    elif memory < 1536 or compute < 2 or latency < 1000 or concurrent_limit == 1:
        level = "constrained"
    else:
        level = "normal"

    if level == "normal":
        effective = requested
        degraded = tuple()
        resolution_level = input_candidate.get("resolution_level")
        reason = "within_budget"
    elif level == "constrained":
        keep = [x for x in requested if x in {"detection", "ocr", "tracking"}]
        effective = tuple(keep) if keep else ((requested[0],) if requested else tuple())
        degraded = tuple(x for x in requested if x not in effective)
        resolution_level = "low"
        reason = "constrained_budget_degradation"
    else:
        keep = [x for x in requested if x in {"detection", "ocr"}]
        effective = tuple(keep[:1]) if keep else ("detection",)
        degraded = tuple(x for x in requested if x not in effective)
        resolution_level = "low"
        reason = "critical_budget_minimum_safety_plan"

    return {
        "budget_decision": {
            "budget_level": level,
            "budget_decision": "allow_with_current_plan"
            if level == "normal"
            else "allow_with_degradation",
            "original_capability_plan": requested,
            "effective_capability_plan": effective,
            "degraded_capabilities": degraded,
            "degradation_reason": reason,
            "effective_resolution_level": resolution_level,
        }
    }
