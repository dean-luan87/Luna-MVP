# -*- coding: utf-8 -*-
"""
Navigation Governance Action Executor Input Object Placeholder v0 (read-only; non-action).

Builds a unified read-only placeholder object `navigation_governance_action_executor_input_v0` for observability.

Hard boundaries:
- NOT a governance action command; NOT proof of approval chain execution.
- Does NOT trigger rollback/interrupt/release-control; no maps; no voice/memory; no mid-platform migration.
- No time/space anchors; does not fabricate missing upstream objects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_executor_input_v0"
_APPROVAL_SCOPE = "navigation_governance_action_approval_boundary_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _executor_skeleton_ok() -> bool:
    try:
        from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
            get_governance_action_executor_identity,
        )

        ident = get_governance_action_executor_identity()
        if not isinstance(ident, dict):
            return False
        if ident.get("is_skeleton") is not True:
            return False
        if str(ident.get("governance_action_executor_identity") or "") != "navigation_governance_action_executor_v0":
            return False
        if ident.get("can_execute_real_actions") is not False:
            return False
        return True
    except Exception:
        return False


def _approval_status_to_action_type(approval_status: str) -> str:
    s = str(approval_status or "").strip()
    if s == "approved_interrupt":
        return "interrupt"
    if s == "approved_release_control":
        return "release_control"
    if s == "approved_rollback":
        return "rollback_request"
    if s == "approved_hold_executor_state":
        return "hold"
    if s == "approval_blocked":
        return "hold"
    return "hold"


def evaluate_navigation_governance_action_executor_input_placeholder_v0(
    *,
    navigation_governance_action_approval_boundary_v0: Any,
    navigation_governance_action_boundary_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid approval boundary object AND governance action executor skeleton identity ok.
    - Optional action boundary is read-only consistency context only (must NOT expand authority).
    """
    ap = _as_dict(navigation_governance_action_approval_boundary_v0)
    if not ap:
        return False, None
    if str(ap.get("governance_action_approval_scope") or "") != _APPROVAL_SCOPE:
        return False, None
    if ap.get("governance_action_approval_attempted") is not True:
        return False, None

    if not _executor_skeleton_ok():
        return False, None

    approval_status = str(ap.get("governance_action_approval_status") or "").strip()
    approved_action_type = _approval_status_to_action_type(approval_status)

    # Optional: boundary echo only (no authority expansion, no blocking overrides)
    _ = navigation_governance_action_boundary_v0

    payload: Dict[str, Any] = {
        "governance_action_executor_input_present": True,
        "governance_action_executor_input_scope": _SCOPE,
        "approved_action_type": approved_action_type,
        "execution_prerequisites_ready": False,
        "constraint_profile": "placeholder_minimal_constraints",
        "return_binding_ready": False,
        "consume_mode": "read_only",
        "reason": "governance_action_executor_input_placeholder_v0:read_only:not_executable",
        "upstream_evidence": {
            "approval_scope": _APPROVAL_SCOPE,
            "approval_status": approval_status,
        },
    }
    return True, payload

