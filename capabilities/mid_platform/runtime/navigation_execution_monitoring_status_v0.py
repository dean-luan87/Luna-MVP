# -*- coding: utf-8 -*-
"""
Navigation Execution Monitoring Status v0 (implemented object; minimal monitoring loop builder).

Builds a minimal, standardized *implemented* monitoring status object `navigation_execution_monitoring_status_v0`
from already-attached metadata (executor status object + takeover boundary).

Hard boundaries:
- NOT a governance engine; does NOT trigger interrupts/rollback; does NOT change mainline dispatch/route/proposal.
- Does NOT fabricate missing inputs; requires narrow, explicit upstream preconditions.
- No time/space anchors; no maps; no voice/memory side effects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_execution_monitoring_status_v0"
_KIND = "implemented_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_execution_monitoring_status_v0(
    *,
    navigation_real_executor_status_v0: Any,
    navigation_executor_takeover_stub_v0: Any,
    navigation_real_executor_input_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires BOTH takeover_stub and implemented executor status object to exist.
    - input object may be provided as auxiliary consistency check but is not required.
    """
    st = _as_dict(navigation_real_executor_status_v0)
    tk = _as_dict(navigation_executor_takeover_stub_v0)
    inp = _as_dict(navigation_real_executor_input_v0)

    if not (st and tk):
        return False, None

    if str(st.get("executor_status_scope") or "") != "navigation_real_executor_status_v0":
        return False, None
    if str(st.get("object_kind") or "") != "implemented_v0":
        return False, None
    if str(st.get("consume_mode") or "") != "implemented_object":
        return False, None

    if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
        return False, None
    if str(tk.get("takeover_status") or "") != "ready_to_takeover":
        # monitoring minimal loop implementation: only relevant in the narrow pre-execution handoff window
        return False, None

    if inp is not None:
        if str(inp.get("executor_input_scope") or "") != "navigation_real_executor_input_v0":
            return False, None
        # Only accept implemented input object; do not treat placeholder as evidence.
        if str(inp.get("object_kind") or "") != "implemented_v0":
            return False, None
        if str(inp.get("consume_mode") or "") != "implemented_object":
            return False, None

    # Implemented monitoring object MUST NOT claim real monitoring loop is running.
    payload: Dict[str, Any] = {
        "monitoring_status_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        # Required monitoring categories (minimal, safe semantics)
        "takeover_monitor": {
            "takeover_boundary_source_scope": "navigation_executor_takeover_stub_v0",
            "takeover_boundary_status": "ready_to_takeover",
            "takeover_monitor_fact": "pre_execution_window",
        },
        "execution_monitor": {
            "execution_monitor_fact": "not_started",
            "upstream_report_required": False,
            "reason": "monitoring_loop_implementation_v0_does_not_imply_runtime",
        },
        "anomaly_monitor": {
            "anomaly_monitor_fact": "unknown_not_observed",
            "upstream_report_required": False,
        },
        # Optional categories may remain minimal
        "degradation_monitor": {
            "degradation_monitor_fact": "unknown_not_reported",
        },
        "route_monitor": {
            "route_binding_ready": False,
            "route_kind": "not_implemented_yet",
        },
        # Minimal observability echo (no anchors)
        "upstream_evidence": {
            "executor_status_kind": "implemented_v0",
            "takeover_status": "ready_to_takeover",
            "input_object_kind": (str(inp.get("object_kind")) if isinstance(inp, dict) else ""),
        },
        # Explicitly write that no governance should be triggered by this object (consumer guardrail).
        "governance_guardrail": {
            "may_trigger_governance": False,
            "notes": "implemented monitoring object is observation-only in v0",
        },
    }
    return True, payload

