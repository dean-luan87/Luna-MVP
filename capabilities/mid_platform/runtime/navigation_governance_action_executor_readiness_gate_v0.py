# -*- coding: utf-8 -*-
"""
Navigation Governance Action Executor Readiness Gate v0 (minimal implementation; non-action).

Builds a unified readiness gate result object:
`navigation_governance_action_executor_readiness_gate_v0`

Hard boundaries:
- Does NOT execute governance actions (rollback/interrupt/release-control).
- Does NOT execute approval chain, does NOT change route/proposal, does NOT trigger voice/memory.
- No time/space anchors; no maps/coordinates; no mid-platform real migration.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_executor_readiness_gate_v0"
_INPUT_SCOPE = "navigation_governance_action_executor_input_v0"
_ACTION_STATUS_SCOPE = "navigation_governance_action_status_v0"
_APPROVAL_STATUS_SCOPE = "navigation_governance_action_approval_status_v0"
_APPROVAL_BOUNDARY_SCOPE = "navigation_governance_action_approval_boundary_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _get_executor_identity() -> Optional[Dict[str, Any]]:
    try:
        from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
            get_governance_action_executor_identity,
        )

        ident = get_governance_action_executor_identity()
        return ident if isinstance(ident, dict) else None
    except Exception:
        return None


def _extract(d: Dict[str, Any], *path: str) -> str:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict):
            return ""
        cur = cur.get(p)
    return str(cur or "")


def evaluate_navigation_governance_action_executor_readiness_gate_v0(
    *,
    navigation_governance_action_executor_input_v0: Any,
    navigation_governance_action_status_v0: Any,
    navigation_governance_action_approval_status_v0: Any,
    navigation_governance_action_approval_boundary_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If the primary input object is missing/invalid => (False, None) (do not write any gate object).

    When applicable:
    - Always returns one of: ready_candidate | not_ready | blocked
    """
    inp = _as_dict(navigation_governance_action_executor_input_v0)
    if not inp:
        return False, None
    if str(inp.get("governance_action_executor_input_scope") or "") != _INPUT_SCOPE:
        return False, None
    if str(inp.get("object_kind") or "") != "implemented_v0":
        return False, None
    if inp.get("governance_action_executor_input_present") is not True:
        return False, None

    ident = _get_executor_identity()
    if not ident:
        status = "blocked"
        reason = "readiness_gate:executor_identity:missing_or_unreadable"
    else:
        if str(ident.get("governance_action_executor_identity") or "") != "navigation_governance_action_executor_v0":
            status = "blocked"
            reason = "readiness_gate:executor_identity:mismatch"
        elif ident.get("is_skeleton") is not True:
            status = "blocked"
            reason = "readiness_gate:executor_identity:not_skeleton_unexpected"
        else:
            status = ""
            reason = ""

    approved_action_type_inp = _extract(inp, "approved_action_type_class", "approved_action_type").strip()
    approval_status_inp = _extract(inp, "approved_action_type_class", "approval_status").strip()
    constraint_profile = _extract(inp, "execution_constraints_class", "constraint_profile").strip()

    # Gate 4: status return surface must be in place (implemented).
    act_st = _as_dict(navigation_governance_action_status_v0)
    action_status_ok = bool(
        act_st
        and str(act_st.get("governance_action_status_scope") or "") == _ACTION_STATUS_SCOPE
        and str(act_st.get("object_kind") or "") == "implemented_v0"
        and act_st.get("governance_action_status_present") is True
    )

    # Gate 5: approval status consistency must be in place + consistent.
    ap_st = _as_dict(navigation_governance_action_approval_status_v0)
    approval_status_ok = bool(
        ap_st
        and str(ap_st.get("governance_action_approval_status_scope") or "") == _APPROVAL_STATUS_SCOPE
        and str(ap_st.get("object_kind") or "") == "implemented_v0"
        and ap_st.get("governance_action_approval_status_present") is True
    )
    approved_action_type_ap = ""
    approval_status_ap = ""
    if approval_status_ok and ap_st:
        approved_action_type_ap = _extract(ap_st, "approved_action_type_class", "approved_action_type").strip()
        approval_status_ap = _extract(ap_st, "approval_state_class", "approval_status").strip()

    # Optional consistency: approval boundary echoes.
    ap_b = _as_dict(navigation_governance_action_approval_boundary_v0)
    approval_boundary_ok = bool(
        ap_b
        and str(ap_b.get("governance_action_approval_scope") or "") == _APPROVAL_BOUNDARY_SCOPE
        and ap_b.get("governance_action_approval_attempted") is True
    )
    approval_status_boundary = ""
    if approval_boundary_ok and ap_b:
        approval_status_boundary = str(ap_b.get("governance_action_approval_status") or "").strip()

    # If already blocked by identity, keep it; otherwise evaluate remaining gates.
    if not status:
        # Rule 4: status return surface not ready => not_ready
        if not action_status_ok:
            status = "not_ready"
            reason = "readiness_gate:action_status_surface:not_ready"
        # Approval status object missing => not_ready (precondition)
        elif not approval_status_ok:
            status = "not_ready"
            reason = "readiness_gate:approval_status_surface:not_ready"
        else:
            # Rule 3: approval status vs input object inconsistency => blocked
            if approved_action_type_ap and approved_action_type_inp and (approved_action_type_ap != approved_action_type_inp):
                status = "blocked"
                reason = "readiness_gate:approval_vs_input:action_type_mismatch"
            elif approval_status_ap and approval_status_inp and (approval_status_ap != approval_status_inp):
                status = "blocked"
                reason = "readiness_gate:approval_vs_input:approval_status_mismatch"
            elif approval_boundary_ok and approval_status_boundary and approval_status_ap and (approval_status_boundary != approval_status_ap):
                status = "blocked"
                reason = "readiness_gate:approval_boundary_vs_approval_status:mismatch"
            elif approval_boundary_ok and approval_status_boundary and approval_status_inp and (approval_status_boundary != approval_status_inp):
                status = "blocked"
                reason = "readiness_gate:approval_boundary_vs_input:mismatch"
            # Rule 5: explicit constraint says do not enter action layer => not_ready
            elif constraint_profile in ("deny_action_layer_v0", "deny_action_layer"):
                status = "not_ready"
                reason = "readiness_gate:constraints:deny_action_layer"
            else:
                status = "ready_candidate"
                reason = "readiness_gate:ready_candidate:objects_present_and_consistent"

    payload: Dict[str, Any] = {
        "governance_action_executor_readiness_attempted": True,
        "governance_action_executor_readiness_scope": _SCOPE,
        "governance_action_executor_readiness_status": str(status),
        "reason": str(reason),
        "observations": {
            "input_object_present": True,
            "executor_identity_present": bool(ident),
            "action_status_object_present": bool(action_status_ok),
            "approval_status_object_present": bool(approval_status_ok),
            "approval_boundary_present": bool(approval_boundary_ok),
            "approved_action_type": approved_action_type_inp,
            "constraint_profile": constraint_profile,
        },
        "hard_boundaries": {
            "can_execute_real_governance_actions": False,
            "can_trigger_approval_chain": False,
            "can_change_route": False,
            "can_trigger_voice_or_memory": False,
            "can_trigger_mid_platform_real_migration": False,
            "no_time_or_space_anchors": True,
        },
    }
    return True, payload

