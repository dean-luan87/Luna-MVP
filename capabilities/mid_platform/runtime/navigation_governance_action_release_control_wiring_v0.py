# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Wiring v0 (minimal implementation; non-action).

Builds a unified wiring result object:
`navigation_governance_action_release_control_wiring_v0`

Hard boundaries:
- Does NOT execute release_control/rollback/interrupt.
- Does NOT trigger approval chain; no maps; no voice/memory; no mid-platform real migration.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_wiring_v0"
_RC_INPUT_SCOPE = "navigation_governance_action_release_control_input_v0"
_RC_STATUS_SCOPE = "navigation_governance_action_release_control_status_v0"
_RC_READINESS_SCOPE = "navigation_governance_action_release_control_readiness_gate_v0"
_EXECUTOR_WIRING_SCOPE = "navigation_governance_action_executor_wiring_v0"
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


def evaluate_navigation_governance_action_release_control_wiring_v0(
    *,
    navigation_governance_action_release_control_input_v0: Any,
    navigation_governance_action_release_control_status_v0: Any,
    navigation_governance_action_release_control_readiness_gate_v0: Any,
    navigation_governance_action_executor_wiring_v0: Any = None,
    navigation_governance_action_approval_status_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If neither a valid release_control input object nor a readiness gate object is present,
      => (False, None) (do not write wiring object).
    - Otherwise returns one of: wired_inactive | wired_action_ready | blocked | not_applicable
    """
    rc_inp = _as_dict(navigation_governance_action_release_control_input_v0)
    rc_rg = _as_dict(navigation_governance_action_release_control_readiness_gate_v0)

    if not rc_inp and not rc_rg:
        return False, None

    # Core object validity checks (per freeze). If missing -> not_applicable.
    if not rc_inp:
        return True, _payload("not_applicable", "release_control_wiring:input:missing")
    if (
        str(rc_inp.get("release_control_input_scope") or "") != _RC_INPUT_SCOPE
        or str(rc_inp.get("object_kind") or "") != "implemented_v0"
        or rc_inp.get("release_control_input_present") is not True
    ):
        return True, _payload("not_applicable", "release_control_wiring:input:invalid")
    if str((rc_inp.get("action_type_confirm_class") or {}).get("action_type_confirmed") or "") != "release_control":
        return True, _payload("not_applicable", "release_control_wiring:input:not_release_control")

    rc_st = _as_dict(navigation_governance_action_release_control_status_v0)
    if not rc_st:
        return True, _payload("not_applicable", "release_control_wiring:status:missing")
    if (
        str(rc_st.get("release_control_status_scope") or "") != _RC_STATUS_SCOPE
        or str(rc_st.get("object_kind") or "") != "implemented_v0"
        or rc_st.get("release_control_status_present") is not True
    ):
        return True, _payload("not_applicable", "release_control_wiring:status:invalid")
    if str((rc_st.get("action_type_class") or {}).get("action_type_confirmed") or "") != "release_control":
        return True, _payload("blocked", "release_control_wiring:status:action_type_mismatch")

    if not rc_rg:
        return True, _payload("not_applicable", "release_control_wiring:readiness_gate:missing")
    if (
        str(rc_rg.get("release_control_readiness_scope") or "") != _RC_READINESS_SCOPE
        or rc_rg.get("release_control_readiness_attempted") is not True
    ):
        return True, _payload("not_applicable", "release_control_wiring:readiness_gate:invalid")
    if str(rc_rg.get("release_control_readiness_status") or "").strip() != "ready_candidate":
        return True, _payload("not_applicable", "release_control_wiring:readiness:not_ready_candidate")

    ident = _get_release_control_identity()
    if not ident:
        return True, _payload("blocked", "release_control_wiring:identity:missing_or_unreadable")
    if str(ident.get("release_control_action_identity") or "") != "navigation_governance_action_release_control_v0":
        return True, _payload("blocked", "release_control_wiring:identity:mismatch")
    if ident.get("is_skeleton") is not True:
        return True, _payload("blocked", "release_control_wiring:identity:not_skeleton_unexpected")
    if ident.get("can_execute_real_release_control") is not False:
        return True, _payload("blocked", "release_control_wiring:identity:unexpected_can_execute")

    # Optional consistency signals (no authority expansion)
    ex_w = _as_dict(navigation_governance_action_executor_wiring_v0)
    executor_wiring_ok = bool(
        ex_w
        and str(ex_w.get("governance_action_executor_wiring_scope") or "") == _EXECUTOR_WIRING_SCOPE
        and ex_w.get("governance_action_executor_wiring_attempted") is True
    )
    ap = _as_dict(navigation_governance_action_approval_status_v0)
    approval_ok = bool(
        ap
        and str(ap.get("governance_action_approval_status_scope") or "") == _APPROVAL_STATUS_SCOPE
        and str(ap.get("object_kind") or "") == "implemented_v0"
        and ap.get("governance_action_approval_status_present") is True
    )

    # Default conservative: wired_inactive. Narrow: wired_action_ready when optional consistencies are present.
    if executor_wiring_ok and approval_ok:
        status = "wired_action_ready"
        reason = "release_control_wiring:wired_action_ready:narrow:optional_consistencies_present"
    else:
        status = "wired_inactive"
        reason = "release_control_wiring:wired_inactive:conservative_default"

    payload = _payload(status, reason)
    payload["observations"] = {
        "executor_wiring_present": bool(executor_wiring_ok),
        "approval_status_object_present": bool(approval_ok),
    }
    return True, payload


def _payload(status: str, reason: str) -> Dict[str, Any]:
    return {
        "release_control_wiring_attempted": True,
        "release_control_wiring_scope": _SCOPE,
        "release_control_wiring_status": str(status),
        "reason": str(reason),
        "hard_boundaries": {
            "can_execute_real_release_control": False,
            "wiring_is_non_action_only": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }

