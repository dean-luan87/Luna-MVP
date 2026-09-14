# -*- coding: utf-8 -*-
"""
Navigation Governance Action Approval Status Object v0 (implemented object; read-only builder).

Builds a standardized *implemented* object `navigation_governance_action_approval_status_v0`
from legal upstream metadata (approval boundary; optional consistency context).

Hard boundaries:
- NOT proof that approval chain executed; NOT an approval-completed event.
- Does NOT trigger approval/governance actions; no maps; no voice/memory; no mid-platform migration.
- No time/space anchors; does not fabricate missing upstream objects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_approval_status_v0"
_KIND = "implemented_v0"
_APPROVAL_BOUNDARY_SCOPE = "navigation_governance_action_approval_boundary_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _approval_status_to_state_fact(approval_status: str) -> str:
    """
    Minimal semantic state for the approval boundary layer.
    This is NOT runtime approval chain state; it only reflects the current boundary result category.
    """
    s = str(approval_status or "").strip()
    if s.startswith("approved_"):
        return "approved"
    if s == "approval_blocked":
        return "approval_blocked"
    return "unresolved_like"


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
    return "hold"


def evaluate_navigation_governance_action_approval_status_v0(
    *,
    navigation_governance_action_approval_boundary_v0: Any,
    navigation_governance_action_boundary_v0: Any = None,
    navigation_governance_action_executor_input_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid approval boundary object.
    - Optional objects are read-only consistency context only (must NOT expand authority).
    """
    ap = _as_dict(navigation_governance_action_approval_boundary_v0)
    if not ap:
        return False, None
    if str(ap.get("governance_action_approval_scope") or "") != _APPROVAL_BOUNDARY_SCOPE:
        return False, None
    if ap.get("governance_action_approval_attempted") is not True:
        return False, None

    approval_status = str(ap.get("governance_action_approval_status") or "").strip()
    state_fact = _approval_status_to_state_fact(approval_status)
    action_type = _approval_status_to_action_type(approval_status)

    # Optional: read-only context (no authority expansion)
    _ = navigation_governance_action_boundary_v0
    _ = navigation_governance_action_executor_input_v0

    payload: Dict[str, Any] = {
        "governance_action_approval_status_present": True,
        "governance_action_approval_status_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        "approval_state_class": {
            "approval_state_fact": state_fact,
            "approval_status_source_scope": _APPROVAL_BOUNDARY_SCOPE,
            "approval_status": approval_status,
            "reason": "approval_status_object_implementation_v0_does_not_imply_approval_chain_execution",
        },
        "approved_action_type_class": {
            "approved_action_type": action_type,
            "notes": "type_only_not_effective",
        },
        "block_and_exception_class": {
            "blocked": state_fact == "approval_blocked",
            "consistency_check_failed": False,
            "exception_fact": "none_reported",
        },
        "effect_and_upstream_class": {
            "approval_effect_fact": "not_applied",
            "notes": "implementation_v0_does_not_imply_route_or_mid_platform_effect",
        },
        "route_and_return_class": {
            "route_binding_ready": False,
            "return_route_kind": "not_bound_yet",
        },
        "upstream_evidence": {
            "approval_scope": _APPROVAL_BOUNDARY_SCOPE,
            "approval_status": approval_status,
        },
    }
    return True, payload

