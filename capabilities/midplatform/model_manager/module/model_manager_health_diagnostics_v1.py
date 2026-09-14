from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping


def build_health_and_diagnostics_v1(
    *,
    request_id: str,
    required_capability: str,
    module_status: str,
    rejection_reasons: Iterable[str],
    ownership_decision: Mapping[str, Any],
    resource_evaluation: Mapping[str, Any],
    lifecycle_plan: Mapping[str, Any],
) -> Dict[str, Any]:
    reasons = tuple(str(x) for x in rejection_reasons)
    health = {
        "module_status": module_status,
        "ownership_ok": bool(ownership_decision.get("ownership_ok", False)),
        "resource_ok": bool(resource_evaluation.get("resource_ok", False)),
        "availability_state": str(lifecycle_plan.get("availability_state", "unknown")),
    }
    diagnostics = {
        "request_id": request_id,
        "required_capability": required_capability,
        "rejection_reasons": reasons,
        "ownership_reason": str(ownership_decision.get("ownership_reason", "")),
        "resource_flags": {
            "resource_insufficient": bool(
                resource_evaluation.get("resource_insufficient", False)
            ),
            "latency_not_met": bool(resource_evaluation.get("latency_not_met", False)),
            "offline_mismatch": bool(
                resource_evaluation.get("offline_mismatch", False)
            ),
        },
        "candidate_only": True,
        "not_fact": True,
    }
    return {
        "health_summary": health,
        "diagnostics": diagnostics,
    }
