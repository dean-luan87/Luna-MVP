# -*- coding: utf-8 -*-
"""
Navigation Governance Action Status Placeholder v0 (read-only; non-action).

Builds a unified read-only placeholder object `navigation_governance_action_status_v0` for observability.

Hard boundaries:
- NOT a governance action runtime status; NOT proof that governance actions executed.
- Does NOT trigger rollback/interrupt/release-control; no maps; no voice/memory; no mid-platform migration.
- No time/space anchors; does not fabricate missing upstream objects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_status_v0"
_BOUNDARY_SCOPE = "navigation_governance_action_boundary_v0"


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


def _boundary_status_to_action_type(boundary_status: str) -> Tuple[str, str]:
    """
    Returns (action_type, action_block_state placeholder semantics).
    action_block_state: not_blocked_placeholder vs blocked_placeholder only.
    """
    s = str(boundary_status or "").strip()
    if s == "request_interrupt":
        return "interrupt", "not_blocked_placeholder"
    if s == "request_release_control":
        return "release_control", "not_blocked_placeholder"
    if s == "request_rollback":
        return "rollback_request", "not_blocked_placeholder"
    if s == "hold_executor_state":
        return "hold", "not_blocked_placeholder"
    if s == "action_blocked":
        return "hold", "blocked_placeholder"
    # Unknown boundary status => still placeholder-safe, do not pretend execution
    return "hold", "not_blocked_placeholder"


def evaluate_navigation_governance_action_status_placeholder_v0(
    *,
    navigation_governance_action_boundary_v0: Any,
    navigation_rollback_and_interruption_governance_decision_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid `navigation_governance_action_boundary_v0` dict AND governance action executor skeleton importable/identity ok.
    - Optional governance decision is read-only consistency context only (must not expand authority).
    """
    b = _as_dict(navigation_governance_action_boundary_v0)
    if not b:
        return False, None
    if str(b.get("governance_action_boundary_scope") or "") != _BOUNDARY_SCOPE:
        return False, None
    if b.get("governance_action_boundary_attempted") is not True:
        return False, None

    if not _executor_skeleton_ok():
        return False, None

    bs = str(b.get("governance_action_boundary_status") or "").strip()
    action_type, block_st = _boundary_status_to_action_type(bs)

    # Optional: read-only decision echo (no authority expansion; no blocking overrides)
    _ = navigation_rollback_and_interruption_governance_decision_v0

    payload: Dict[str, Any] = {
        "governance_action_status_present": True,
        "governance_action_status_scope": _SCOPE,
        "action_type": action_type,
        "action_state": "idle_placeholder",
        "action_effect_state": "unknown_not_applied",
        "action_block_state": block_st,
        "route_binding_ready": False,
        "consume_mode": "read_only",
        "reason": "governance_action_status_placeholder_v0:read_only:not_runtime_status",
    }
    return True, payload
