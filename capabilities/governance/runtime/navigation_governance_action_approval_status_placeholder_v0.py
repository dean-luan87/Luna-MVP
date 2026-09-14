# -*- coding: utf-8 -*-
"""
Navigation Governance Action Approval Status Placeholder v0 (read-only; non-action).

Builds a unified read-only placeholder object `navigation_governance_action_approval_status_v0`
for observability of the approval boundary layer.

Hard boundaries:
- NOT an approval execution chain status; NOT proof that approval ran.
- Does NOT trigger approval/governance actions; no maps; no voice/memory; no mid-platform migration.
- No time/space anchors; does not fabricate missing upstream objects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_approval_status_v0"
_APPROVAL_BOUNDARY_SCOPE = "navigation_governance_action_approval_boundary_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _approval_boundary_to_placeholder_state(approval_status: str) -> str:
    s = str(approval_status or "").strip()
    if s.startswith("approved_"):
        return "approved_placeholder"
    if s == "approval_blocked":
        return "approval_blocked_placeholder"
    return "unresolved_like_placeholder"


def _approval_boundary_to_action_type(approval_status: str) -> str:
    s = str(approval_status or "").strip()
    if s == "approved_interrupt":
        return "interrupt"
    if s == "approved_release_control":
        return "release_control"
    if s == "approved_rollback":
        return "rollback_request"
    if s == "approved_hold_executor_state":
        return "hold"
    # blocked/unknown => hold (safe placeholder)
    return "hold"


def evaluate_navigation_governance_action_approval_status_placeholder_v0(
    *,
    navigation_governance_action_approval_boundary_v0: Any,
    navigation_governance_action_boundary_v0: Any = None,
    navigation_governance_action_executor_input_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid approval boundary object.
    - Optional action boundary / executor input are read-only consistency context only (must NOT expand authority).
    """
    ap = _as_dict(navigation_governance_action_approval_boundary_v0)
    if not ap:
        return False, None
    if str(ap.get("governance_action_approval_scope") or "") != _APPROVAL_BOUNDARY_SCOPE:
        return False, None
    if ap.get("governance_action_approval_attempted") is not True:
        return False, None

    approval_status = str(ap.get("governance_action_approval_status") or "").strip()
    approval_state = _approval_boundary_to_placeholder_state(approval_status)
    approved_action_type = _approval_boundary_to_action_type(approval_status)

    # Optional: read-only context (no authority expansion)
    _ = navigation_governance_action_boundary_v0
    _ = navigation_governance_action_executor_input_v0

    payload: Dict[str, Any] = {
        "governance_action_approval_status_present": True,
        "governance_action_approval_status_scope": _SCOPE,
        "approval_state": approval_state,
        "approved_action_type": approved_action_type,
        "approval_effect_state": "unknown_not_applied",
        "route_binding_ready": False,
        "consume_mode": "read_only",
        "reason": "approval_status_placeholder_v0:read_only:not_approval_chain_status",
    }
    return True, payload

