# -*- coding: utf-8 -*-
"""
Navigation Governance Action Approval Boundary v0 (minimal implementation; non-action).

Builds a unified approval boundary result object `navigation_governance_action_approval_boundary_v0`
from the standardized governance action boundary object.

Hard boundaries:
- NOT an approval execution chain; NOT a governance action executor.
- Does NOT trigger governance actions; no time/space anchors; no maps; no voice/memory side effects.
- Does NOT read candidate/gate/stub/raw metadata directly (only consumes standardized objects).
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_approval_boundary_v0"
_BOUNDARY_SCOPE = "navigation_governance_action_boundary_v0"

_ENTRY_SCOPE = "navigation_rollback_and_interruption_governance_entry_v0"
_DECISION_SCOPE = "navigation_rollback_and_interruption_governance_decision_v0"
_EXECUTOR_STATUS_SCOPE = "navigation_real_executor_status_v0"
_MONITORING_SCOPE = "navigation_execution_monitoring_status_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_approval_boundary_v0(
    *,
    navigation_governance_action_boundary_v0: Any,
    navigation_rollback_and_interruption_governance_decision_v0: Any = None,
    navigation_rollback_and_interruption_governance_entry_v0: Any = None,
    navigation_real_executor_status_v0: Any = None,
    navigation_execution_monitoring_status_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    Output policy:
    - If action boundary object missing or invalid => relevant-only (False, None).
    - Otherwise output exactly one of the five governance_action_approval_status values.

    Conservative minimal mapping (no external approval chain):
    - Known boundary statuses map to corresponding approved_*.
    - Unknown boundary status maps to approval_blocked.

    Optional objects only adjust reason trace; must NOT expand authority or override mapping.
    """
    b = _as_dict(navigation_governance_action_boundary_v0)
    if not b:
        return False, None
    if str(b.get("governance_action_boundary_scope") or "") != _BOUNDARY_SCOPE:
        return False, None
    if b.get("governance_action_boundary_attempted") is not True:
        return False, None

    bs = str(b.get("governance_action_boundary_status") or "").strip()
    mapping = {
        "request_rollback": "approved_rollback",
        "request_release_control": "approved_release_control",
        "request_interrupt": "approved_interrupt",
        "hold_executor_state": "approved_hold_executor_state",
        "action_blocked": "approval_blocked",
    }
    approval_status = mapping.get(bs)
    if not approval_status:
        approval_status = "approval_blocked"
        reason = f"conservative_blocked:unknown_boundary_status:{bs}"[:240]
    else:
        reason = f"mapped_from_boundary:{bs}"

    try:
        ge = _as_dict(navigation_rollback_and_interruption_governance_entry_v0)
        if ge and str(ge.get("governance_entry_scope") or "") == _ENTRY_SCOPE:
            if str(ge.get("governance_entry_status") or "") != "governance_entry_open":
                reason = (reason + ";entry_not_open")[:240]
    except Exception:
        pass
    try:
        gd = _as_dict(navigation_rollback_and_interruption_governance_decision_v0)
        if gd and str(gd.get("governance_decision_scope") or "") == _DECISION_SCOPE:
            if gd.get("governance_decision_attempted") is not True:
                reason = (reason + ";decision_not_attempted_echo")[:240]
    except Exception:
        pass
    try:
        st = _as_dict(navigation_real_executor_status_v0)
        if st and str(st.get("executor_status_scope") or "") == _EXECUTOR_STATUS_SCOPE:
            if str(st.get("object_kind") or "") != "implemented_v0":
                reason = (reason + ";executor_status_not_implemented")[:240]
    except Exception:
        pass
    try:
        mon = _as_dict(navigation_execution_monitoring_status_v0)
        if mon and str(mon.get("monitoring_status_scope") or "") == _MONITORING_SCOPE:
            if str(mon.get("object_kind") or "") != "implemented_v0":
                reason = (reason + ";monitoring_not_implemented")[:240]
    except Exception:
        pass

    payload = {
        "governance_action_approval_attempted": True,
        "governance_action_approval_scope": _SCOPE,
        "governance_action_approval_status": approval_status,
        "reason": reason[:240],
    }
    return True, payload
