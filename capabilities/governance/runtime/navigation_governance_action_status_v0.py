# -*- coding: utf-8 -*-
"""
Navigation Governance Action Status Object v0 (implemented object; read-only builder).

Builds a standardized *implemented* object `navigation_governance_action_status_v0` from legal upstream metadata.

Hard boundaries:
- NOT proof that governance actions executed; NOT a completion event.
- Does NOT trigger rollback/interrupt/release-control; no maps; no voice/memory; no mid-platform migration.
- No time/space anchors; does not fabricate missing upstream objects.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_status_v0"
_KIND = "implemented_v0"
_BOUNDARY_SCOPE = "navigation_governance_action_boundary_v0"
_DECISION_SCOPE = "navigation_rollback_and_interruption_governance_decision_v0"


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


def _map_boundary_to_action_type_and_block(boundary_status: str) -> Tuple[str, str, str]:
    """
    Returns (action_type_fact, block_fact, boundary_status_echo).
    block_fact: semantic, not *_placeholder strings.
    """
    s = str(boundary_status or "").strip()
    if s == "request_interrupt":
        return "interrupt", "not_blocked", s
    if s == "request_release_control":
        return "release_control", "not_blocked", s
    if s == "request_rollback":
        return "rollback_request", "not_blocked", s
    if s == "hold_executor_state":
        return "hold", "not_blocked", s
    if s == "action_blocked":
        return "hold", "boundary_category_blocked", s
    return "hold", "unknown_boundary_status", s


def evaluate_navigation_governance_action_status_v0(
    *,
    navigation_governance_action_boundary_v0: Any,
    navigation_rollback_and_interruption_governance_decision_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid implemented boundary object + governance action executor skeleton identity ok.
    - Optional governance decision: read-only consistency echo only (must not expand authority).
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
    action_type_fact, block_fact, bs_echo = _map_boundary_to_action_type_and_block(bs)

    gd = _as_dict(navigation_rollback_and_interruption_governance_decision_v0)
    decision_echo = ""
    if gd and str(gd.get("governance_decision_scope") or "") == _DECISION_SCOPE:
        decision_echo = str(gd.get("governance_decision_status") or "")[:120]

    payload: Dict[str, Any] = {
        "governance_action_status_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        "governance_action_status_present": True,
        "action_type_class": {
            "action_type_fact": action_type_fact,
            "boundary_status": bs_echo,
            "boundary_source_scope": _BOUNDARY_SCOPE,
        },
        "action_state_class": {
            "execution_fact": "not_started",
            "reason": "governance_action_status_implementation_v0_does_not_imply_real_action_execution",
        },
        "anomaly_and_block_class": {
            "exception_fact": "none_reported",
            "block_fact": block_fact,
        },
        "effect_and_upstream_class": {
            "effect_fact": "not_applied",
            "notes": "implementation_v0_does_not_imply_route_or_mid_platform_effect",
        },
        "route_and_return_class": {
            "route_binding_ready": False,
            "return_route_kind": "not_bound_yet",
        },
        "upstream_evidence": {
            "governance_action_executor_identity": "navigation_governance_action_executor_v0",
            "governance_decision_status_echo": decision_echo,
        },
    }
    return True, payload
