# -*- coding: utf-8 -*-
"""
Navigation Real Executor Status Object v0 (implemented object; read-only builder).

Builds a minimal, standardized *implemented* object `navigation_real_executor_status_v0` from already-attached metadata.

Hard boundaries:
- NOT an executor; NOT a real runtime status from a running executor.
- Does NOT fabricate missing inputs; requires narrow, explicit upstream preconditions.
- No time/space anchors; no maps; does NOT drive mid-platform state transitions.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_real_executor_status_v0"
_KIND = "implemented_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_real_executor_status_object_v0(
    *,
    navigation_executor_takeover_stub_v0: Any,
    navigation_real_executor_input_v0: Any,
    navigation_real_execution_readiness_gate_stub_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires BOTH takeover_stub and implemented executor_input object to exist.
    - readiness gate may be provided as auxiliary consistency check but is not required.
    """
    tk = _as_dict(navigation_executor_takeover_stub_v0)
    inp = _as_dict(navigation_real_executor_input_v0)
    rg = _as_dict(navigation_real_execution_readiness_gate_stub_v0)

    if not (tk and inp):
        return False, None

    if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
        return False, None
    if str(tk.get("takeover_status") or "") != "ready_to_takeover":
        return False, None

    if str(inp.get("executor_input_scope") or "") != "navigation_real_executor_input_v0":
        return False, None
    if str(inp.get("object_kind") or "") != "implemented_v0":
        return False, None
    if str(inp.get("consume_mode") or "") != "implemented_object":
        return False, None

    # Auxiliary: if provided and explicitly blocked, stay relevant-only (do not output).
    if rg and str(rg.get("readiness_scope") or "") == "navigation_real_execution_readiness_gate_stub_v0":
        if str(rg.get("readiness_status") or "") == "blocked":
            return False, None

    # Implemented status object must not fabricate real runtime facts (running/completed/failed/etc).
    payload: Dict[str, Any] = {
        "executor_status_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        # Required categories (minimal, safe semantics)
        "takeover_state": {
            "takeover_boundary_source_scope": "navigation_executor_takeover_stub_v0",
            "takeover_boundary_status": "ready_to_takeover",
            "takeover_fact": "not_taken_over_yet",
        },
        "execution_state": {
            "execution_fact": "not_started",
            "execution_allowed_to_start": False,
            "reason": "status_object_implementation_v0_does_not_imply_runtime",
        },
        "anomaly_state": {
            "anomaly_fact": "unknown_not_observed",
            "suggest_upstream_fallback": False,
        },
        # Optional categories may remain minimal
        "executor_capability_state": {
            "capability_fact": "unknown_not_reported",
            "degraded": None,
        },
        "status_route_binding": {
            "binding_ready": False,
            "binding_kind": "not_implemented_yet",
        },
        # Minimal upstream evidence echo for observability (no anchors)
        "upstream_evidence": {
            "takeover_scope": "navigation_executor_takeover_stub_v0",
            "takeover_status": "ready_to_takeover",
            "input_object_kind": "implemented_v0",
        },
    }
    return True, payload

