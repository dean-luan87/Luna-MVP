# -*- coding: utf-8 -*-
"""
Navigation Governance Action Boundary v0 (minimal implementation; non-action).

Builds a unified governance action boundary result object `navigation_governance_action_boundary_v0`
from the standardized governance decision object.

Hard boundaries:
- NOT a rollback engine; NOT an interruption engine; NOT a release-control executor.
- Does NOT trigger governance actions; no time/space anchors; no maps; no voice/memory side effects.
- Does NOT read candidate/gate/stub/raw metadata directly (only consumes standardized objects).
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_boundary_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_boundary_v0(
    *,
    navigation_rollback_and_interruption_governance_decision_v0: Any,
    navigation_rollback_and_interruption_governance_entry_v0: Any = None,
    navigation_real_executor_status_v0: Any = None,
    navigation_execution_monitoring_status_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    Output policy (consistent):
    - If governance decision object is missing OR not a valid standardized decision object => relevant-only (False, None).
    - If decision exists and valid but status unrecognized => output action_blocked (attempted=True).

    Notes:
    - Optional objects are accepted as read-only consistency context, but must NOT expand authority.
      This minimal implementation does not block/override decision mapping based on optional objects.
    """
    gd = _as_dict(navigation_rollback_and_interruption_governance_decision_v0)
    if not gd:
        return False, None

    if str(gd.get("governance_decision_scope") or "") != "navigation_rollback_and_interruption_governance_decision_v0":
        return False, None

    decision_status = str(gd.get("governance_decision_status") or "").strip()
    mapping = {
        "recommend_rollback": "request_rollback",
        "recommend_release_control": "request_release_control",
        "recommend_interrupt": "request_interrupt",
        "hold_for_governance": "hold_executor_state",
        "governance_decision_blocked": "action_blocked",
    }

    out_status = mapping.get(decision_status)
    if not out_status:
        out_status = "action_blocked"
        reason = f"unknown_governance_decision_status:{decision_status}"[:240]
    else:
        reason = f"mapped_from:{decision_status}"

    # Optional objects are read-only; keep a minimal trace in reason only if they are clearly inconsistent.
    # Do NOT block or upgrade authority.
    try:
        ge = _as_dict(navigation_rollback_and_interruption_governance_entry_v0)
        if ge and str(ge.get("governance_entry_scope") or "") == "navigation_rollback_and_interruption_governance_entry_v0":
            if str(ge.get("governance_entry_status") or "") != "governance_entry_open":
                reason = (reason + ";entry_not_open")[:240]
    except Exception:
        pass
    try:
        st = _as_dict(navigation_real_executor_status_v0)
        if st and str(st.get("executor_status_scope") or "") == "navigation_real_executor_status_v0":
            if str(st.get("object_kind") or "") != "implemented_v0":
                reason = (reason + ";executor_status_not_implemented")[:240]
    except Exception:
        pass
    try:
        mon = _as_dict(navigation_execution_monitoring_status_v0)
        if mon and str(mon.get("monitoring_status_scope") or "") == "navigation_execution_monitoring_status_v0":
            if str(mon.get("object_kind") or "") != "implemented_v0":
                reason = (reason + ";monitoring_status_not_implemented")[:240]
    except Exception:
        pass

    payload = {
        "governance_action_boundary_attempted": True,
        "governance_action_boundary_scope": _SCOPE,
        "governance_action_boundary_status": out_status,
        "reason": reason[:240],
    }
    return True, payload

