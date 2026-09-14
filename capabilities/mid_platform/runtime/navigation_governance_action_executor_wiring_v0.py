# -*- coding: utf-8 -*-
"""
Navigation Governance Action Executor Wiring v0 (minimal implementation; non-action).

Builds a unified wiring result object:
`navigation_governance_action_executor_wiring_v0`

Hard boundaries:
- Does NOT execute governance actions (rollback/interrupt/release-control).
- Does NOT trigger approval chain execution; no maps; no voice/memory; no mid-platform real migration.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_executor_wiring_v0"
_INPUT_SCOPE = "navigation_governance_action_executor_input_v0"
_ACTION_STATUS_SCOPE = "navigation_governance_action_status_v0"
_APPROVAL_STATUS_SCOPE = "navigation_governance_action_approval_status_v0"
_READINESS_SCOPE = "navigation_governance_action_executor_readiness_gate_v0"
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


def _input_implemented(inp: Any) -> Optional[Dict[str, Any]]:
    d = _as_dict(inp)
    if not d:
        return None
    if str(d.get("governance_action_executor_input_scope") or "") != _INPUT_SCOPE:
        return None
    if str(d.get("object_kind") or "") != "implemented_v0":
        return None
    if d.get("governance_action_executor_input_present") is not True:
        return None
    return d


def _readiness_parsed(rg: Any) -> Optional[Dict[str, Any]]:
    d = _as_dict(rg)
    if not d:
        return None
    if str(d.get("governance_action_executor_readiness_scope") or "") != _READINESS_SCOPE:
        return None
    if d.get("governance_action_executor_readiness_attempted") is not True:
        return None
    return d


def evaluate_navigation_governance_action_executor_wiring_v0(
    *,
    navigation_governance_action_executor_input_v0: Any,
    navigation_governance_action_status_v0: Any,
    navigation_governance_action_approval_status_v0: Any,
    navigation_governance_action_executor_readiness_gate_v0: Any,
    navigation_governance_action_approval_boundary_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If neither a valid implemented executor input object nor a readiness gate object is present,
      => (False, None) (do not write wiring object).

    When applicable:
    - Returns one of: wired_inactive | wired_action_ready | blocked | not_applicable
    """
    inp = _input_implemented(navigation_governance_action_executor_input_v0)
    rg = _readiness_parsed(navigation_governance_action_executor_readiness_gate_v0)

    if not inp and not rg:
        return False, None

    act_st = _as_dict(navigation_governance_action_status_v0)
    action_status_ok = bool(
        act_st
        and str(act_st.get("governance_action_status_scope") or "") == _ACTION_STATUS_SCOPE
        and str(act_st.get("object_kind") or "") == "implemented_v0"
        and act_st.get("governance_action_status_present") is True
    )

    ap_st = _as_dict(navigation_governance_action_approval_status_v0)
    approval_status_ok = bool(
        ap_st
        and str(ap_st.get("governance_action_approval_status_scope") or "") == _APPROVAL_STATUS_SCOPE
        and str(ap_st.get("object_kind") or "") == "implemented_v0"
        and ap_st.get("governance_action_approval_status_present") is True
    )

    ap_b = _as_dict(navigation_governance_action_approval_boundary_v0)
    approval_boundary_ok = bool(
        ap_b
        and str(ap_b.get("governance_action_approval_scope") or "") == _APPROVAL_BOUNDARY_SCOPE
        and ap_b.get("governance_action_approval_attempted") is True
    )

    # Rule 1: core wiring objects missing (need full set for anything beyond not_applicable)
    if not inp:
        payload = _payload("not_applicable", "wiring:executor_input:missing")
        return True, payload

    if not rg:
        payload = _payload("not_applicable", "wiring:readiness_gate:missing")
        return True, payload

    readiness_status = str(rg.get("governance_action_executor_readiness_status") or "").strip()

    # Rule 2: readiness gate not ready_candidate => not_applicable (do not enter wiring branch)
    if readiness_status != "ready_candidate":
        payload = _payload("not_applicable", "wiring:readiness:not_ready_candidate")
        return True, payload

    # Need action + approval status surfaces for wiring per freeze
    if not action_status_ok or not approval_status_ok:
        payload = _payload("not_applicable", "wiring:core_status_surfaces:incomplete")
        return True, payload

    approved_action_type_inp = _extract(inp, "approved_action_type_class", "approved_action_type").strip()
    approval_status_inp = _extract(inp, "approved_action_type_class", "approval_status").strip()
    approved_action_type_ap = _extract(ap_st, "approved_action_type_class", "approved_action_type").strip() if ap_st else ""
    approval_status_ap = _extract(ap_st, "approval_state_class", "approval_status").strip() if ap_st else ""

    approval_status_boundary = ""
    if approval_boundary_ok and ap_b:
        approval_status_boundary = str(ap_b.get("governance_action_approval_status") or "").strip()

    ident = _get_executor_identity()

    # Rule 3: skeleton identity / capability
    if not ident:
        payload = _payload("blocked", "wiring:executor_identity:missing_or_unreadable")
        return True, payload
    if str(ident.get("governance_action_executor_identity") or "") != "navigation_governance_action_executor_v0":
        payload = _payload("blocked", "wiring:executor_identity:mismatch")
        return True, payload
    if ident.get("is_skeleton") is not True:
        payload = _payload("blocked", "wiring:executor_identity:not_skeleton_unexpected")
        return True, payload
    if ident.get("can_execute_real_actions") is not False:
        payload = _payload("blocked", "wiring:executor_identity:unexpected_can_execute")
        return True, payload

    # Rule 4: cross-object inconsistency => blocked
    if approved_action_type_ap and approved_action_type_inp and (approved_action_type_ap != approved_action_type_inp):
        payload = _payload("blocked", "wiring:approval_vs_input:action_type_mismatch")
        return True, payload
    if approval_status_ap and approval_status_inp and (approval_status_ap != approval_status_inp):
        payload = _payload("blocked", "wiring:approval_vs_input:approval_status_mismatch")
        return True, payload
    if approval_boundary_ok and approval_status_boundary and approval_status_ap and (approval_status_boundary != approval_status_ap):
        payload = _payload("blocked", "wiring:approval_boundary_vs_approval_status:mismatch")
        return True, payload
    if approval_boundary_ok and approval_status_boundary and approval_status_inp and (approval_status_boundary != approval_status_inp):
        payload = _payload("blocked", "wiring:approval_boundary_vs_input:mismatch")
        return True, payload

    # Rule 5: default conservative => wired_inactive; narrow => wired_action_ready when optional boundary audit passes
    if approval_boundary_ok and approval_status_boundary and approval_status_ap and (approval_status_boundary == approval_status_ap):
        wstatus = "wired_action_ready"
        reason = "wiring:wired_action_ready:narrow:approval_boundary_consistent"
    else:
        wstatus = "wired_inactive"
        reason = "wiring:wired_inactive:conservative_default"

    payload = _payload(wstatus, reason)
    payload["observations"] = {
        "executor_identity_present": True,
        "approval_boundary_present": bool(approval_boundary_ok),
        "readiness_status": readiness_status,
    }
    return True, payload


def _payload(status: str, reason: str) -> Dict[str, Any]:
    return {
        "governance_action_executor_wiring_attempted": True,
        "governance_action_executor_wiring_scope": _SCOPE,
        "governance_action_executor_wiring_status": str(status),
        "reason": str(reason),
        "hard_boundaries": {
            "can_execute_real_governance_actions": False,
            "wiring_is_non_action_only": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }
