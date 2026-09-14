# -*- coding: utf-8 -*-
"""
Navigation Real Executor Status Placeholder v0 (read-only).

Builds a minimal, observable placeholder object `navigation_real_executor_status_v0` from already-attached metadata.

Hard boundaries:
- NOT an executor; NOT a real status return from executor; does NOT trigger navigation; no maps.
- Does NOT fabricate missing inputs; no time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "navigation_real_executor_status_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_real_executor_status_placeholder_v0(
    *,
    navigation_executor_takeover_stub_v0: Any,
    navigation_real_executor_input_v0: Any,
    navigation_real_execution_readiness_gate_stub_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires BOTH takeover_stub and executor_input placeholder to exist.
    - readiness gate may be provided as auxiliary evidence but is not required.
    """
    tk = _as_dict(navigation_executor_takeover_stub_v0)
    inp = _as_dict(navigation_real_executor_input_v0)
    rg = _as_dict(navigation_real_execution_readiness_gate_stub_v0)

    if not (tk and inp):
        return False, None

    # Minimal sanity: ensure the two sources are from our known scopes (avoid treating unrelated dicts as evidence).
    if str(tk.get("takeover_scope") or "") != "navigation_executor_takeover_stub_v0":
        return False, None
    if str(inp.get("executor_input_scope") or "") != "navigation_real_executor_input_v0":
        return False, None
    if inp.get("consume_mode") != "read_only":
        return False, None

    # Auxiliary: if provided and explicitly blocked, stay relevant-only (do not output a status placeholder).
    if rg and str(rg.get("readiness_scope") or "") == "navigation_real_execution_readiness_gate_stub_v0":
        if str(rg.get("readiness_status") or "") == "blocked":
            return False, None

    # Placeholder object MUST NOT look like real executor states.
    return True, {
        "executor_status_present": True,
        "executor_status_scope": _SCOPE,
        "takeover_state": "placeholder_pre_execution",
        "execution_state": "not_started_placeholder",
        "anomaly_state": "unknown_placeholder",
        "executor_capability_state": "unknown_placeholder",
        "status_route_binding_ready": False,
        "consume_mode": "read_only",
    }

