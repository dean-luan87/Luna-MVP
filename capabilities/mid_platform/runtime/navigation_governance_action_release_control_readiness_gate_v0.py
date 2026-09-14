# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Readiness Gate v0 (minimal implementation; non-action).

Builds a unified readiness gate result object:
`navigation_governance_action_release_control_readiness_gate_v0`

Hard boundaries:
- Does NOT execute release_control/rollback/interrupt.
- Does NOT trigger approval chain; no maps; no voice/memory; no mid-platform real migration.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_readiness_gate_v0"
_RC_INPUT_SCOPE = "navigation_governance_action_release_control_input_v0"
_RC_STATUS_SCOPE = "navigation_governance_action_release_control_status_v0"
_WIRING_SCOPE = "navigation_governance_action_executor_wiring_v0"
_EXECUTOR_READINESS_SCOPE = "navigation_governance_action_executor_readiness_gate_v0"
_APPROVAL_STATUS_SCOPE = "navigation_governance_action_approval_status_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _get_release_control_identity() -> Optional[Dict[str, Any]]:
    try:
        from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (
            get_release_control_identity,
        )

        ident = get_release_control_identity()
        return ident if isinstance(ident, dict) else None
    except Exception:
        return None


def evaluate_navigation_governance_action_release_control_readiness_gate_v0(
    *,
    navigation_governance_action_release_control_input_v0: Any,
    navigation_governance_action_release_control_status_v0: Any,
    navigation_governance_action_executor_wiring_v0: Any,
    navigation_governance_action_executor_readiness_gate_v0: Any,
    navigation_governance_action_approval_status_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If primary input object missing/invalid => (False, None) (do not write any gate object).

    When applicable:
    - Returns one of: ready_candidate | not_ready | blocked
    """
    rc_inp = _as_dict(navigation_governance_action_release_control_input_v0)
    if not rc_inp:
        return False, None
    if str(rc_inp.get("release_control_input_scope") or "") != _RC_INPUT_SCOPE:
        return False, None
    if str(rc_inp.get("object_kind") or "") != "implemented_v0":
        return False, None
    if rc_inp.get("release_control_input_present") is not True:
        return False, None
    if str((rc_inp.get("action_type_confirm_class") or {}).get("action_type_confirmed") or "") != "release_control":
        return False, None

    ident = _get_release_control_identity()
    if not ident:
        status = "blocked"
        reason = "release_control_readiness:identity:missing_or_unreadable"
    else:
        if str(ident.get("release_control_action_identity") or "") != "navigation_governance_action_release_control_v0":
            status = "blocked"
            reason = "release_control_readiness:identity:mismatch"
        elif ident.get("is_skeleton") is not True:
            status = "blocked"
            reason = "release_control_readiness:identity:not_skeleton_unexpected"
        elif ident.get("can_execute_real_release_control") is not False:
            status = "blocked"
            reason = "release_control_readiness:identity:unexpected_can_execute"
        else:
            status = ""
            reason = ""

    # Sub-action status surface must be in place (implemented).
    rc_st = _as_dict(navigation_governance_action_release_control_status_v0)
    rc_status_ok = bool(
        rc_st
        and str(rc_st.get("release_control_status_scope") or "") == _RC_STATUS_SCOPE
        and str(rc_st.get("object_kind") or "") == "implemented_v0"
        and rc_st.get("release_control_status_present") is True
        and str((rc_st.get("action_type_class") or {}).get("action_type_confirmed") or "") == "release_control"
    )

    # Upstream: wiring + executor readiness must be in place.
    wg = _as_dict(navigation_governance_action_executor_wiring_v0)
    wiring_ok = bool(
        wg
        and str(wg.get("governance_action_executor_wiring_scope") or "") == _WIRING_SCOPE
        and wg.get("governance_action_executor_wiring_attempted") is True
    )
    rg = _as_dict(navigation_governance_action_executor_readiness_gate_v0)
    exec_ready_ok = bool(
        rg
        and str(rg.get("governance_action_executor_readiness_scope") or "") == _EXECUTOR_READINESS_SCOPE
        and rg.get("governance_action_executor_readiness_attempted") is True
    )

    # Optional: approval status observation only
    ap = _as_dict(navigation_governance_action_approval_status_v0)
    approval_ok = bool(
        ap
        and str(ap.get("governance_action_approval_status_scope") or "") == _APPROVAL_STATUS_SCOPE
        and str(ap.get("object_kind") or "") == "implemented_v0"
        and ap.get("governance_action_approval_status_present") is True
    )

    if not status:
        # Rule: upstream inconsistency => blocked
        if not wiring_ok or not exec_ready_ok:
            status = "blocked"
            reason = "release_control_readiness:upstream:wiring_or_executor_readiness_missing"
        # Rule: sub-action status surface not ready => not_ready
        elif not rc_status_ok:
            status = "not_ready"
            reason = "release_control_readiness:status_surface:not_ready"
        else:
            # Rule: constraints say not ready => not_ready
            prereq = rc_inp.get("execution_prerequisites_class") or {}
            if prereq.get("execution_prerequisites_ready") is True:
                # Even if some upstream mistakenly says ready, remain conservative here.
                status = "not_ready"
                reason = "release_control_readiness:constraints:conservative_not_ready"
            else:
                status = "ready_candidate"
                reason = "release_control_readiness:ready_candidate:objects_present_and_consistent"

    payload: Dict[str, Any] = {
        "release_control_readiness_attempted": True,
        "release_control_readiness_scope": _SCOPE,
        "release_control_readiness_status": str(status),
        "reason": str(reason),
        "observations": {
            "release_control_input_present": True,
            "release_control_status_object_present": bool(rc_status_ok),
            "executor_wiring_present": bool(wiring_ok),
            "executor_readiness_present": bool(exec_ready_ok),
            "approval_status_object_present": bool(approval_ok),
        },
        "hard_boundaries": {
            "can_execute_real_release_control": False,
            "can_execute_real_governance_actions": False,
            "can_trigger_approval_chain": False,
            "can_change_route": False,
            "can_trigger_voice_or_memory": False,
            "can_trigger_mid_platform_real_migration": False,
            "no_time_or_space_anchors": True,
        },
    }
    return True, payload

