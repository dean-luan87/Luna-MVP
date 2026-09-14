# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Status Object v0 (implemented object; read-only builder).

Builds a standardized *implemented* object:
`navigation_governance_action_release_control_status_v0`

Hard boundaries:
- NOT proof that release_control executed; NOT a completion event.
- Does NOT trigger release_control/rollback/interrupt; no maps; no voice/memory; no mid-platform migration.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_status_v0"
_KIND = "implemented_v0"
_RC_INPUT_SCOPE = "navigation_governance_action_release_control_input_v0"
_WIRING_SCOPE = "navigation_governance_action_executor_wiring_v0"
_ACTION_STATUS_SCOPE = "navigation_governance_action_status_v0"
_READINESS_SCOPE = "navigation_governance_action_executor_readiness_gate_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_status_v0(
    *,
    navigation_governance_action_release_control_input_v0: Any,
    navigation_governance_action_executor_wiring_v0: Any,
    navigation_governance_action_status_v0: Any = None,
    navigation_governance_action_executor_readiness_gate_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid release_control input placeholder object AND valid wiring object.
    - Optional objects are read-only consistency context only (must NOT expand authority).
    """
    rc_inp = _as_dict(navigation_governance_action_release_control_input_v0)
    if not rc_inp:
        return False, None
    if str(rc_inp.get("release_control_input_scope") or "") != _RC_INPUT_SCOPE:
        return False, None
    if rc_inp.get("release_control_input_present") is not True:
        return False, None
    if str(rc_inp.get("action_type_confirmed") or "") != "release_control":
        return False, None

    wg = _as_dict(navigation_governance_action_executor_wiring_v0)
    if not wg:
        return False, None
    if str(wg.get("governance_action_executor_wiring_scope") or "") != _WIRING_SCOPE:
        return False, None
    if wg.get("governance_action_executor_wiring_attempted") is not True:
        return False, None

    # Optional: read-only consistency context only.
    st = _as_dict(navigation_governance_action_status_v0)
    st_ok = bool(
        st
        and str(st.get("governance_action_status_scope") or "") == _ACTION_STATUS_SCOPE
        and str(st.get("object_kind") or "") == "implemented_v0"
        and st.get("governance_action_status_present") is True
    )
    rg = _as_dict(navigation_governance_action_executor_readiness_gate_v0)
    rg_ok = bool(
        rg
        and str(rg.get("governance_action_executor_readiness_scope") or "") == _READINESS_SCOPE
        and rg.get("governance_action_executor_readiness_attempted") is True
    )

    payload: Dict[str, Any] = {
        "release_control_status_present": True,
        "release_control_status_scope": _SCOPE,
        "object_kind": _KIND,
        "consume_mode": "implemented_object",
        # Category 1: sub-action state (implemented object, but NOT runtime fact of completion)
        "sub_action_state_class": {
            "release_control_state_fact": "not_started",
            "notes": "implementation_v0_does_not_imply_release_control_execution",
        },
        # Category 2: action type confirmed
        "action_type_class": {
            "action_type_confirmed": "release_control",
        },
        # Category 3: anomaly / block
        "anomaly_and_block_class": {
            "blocked": False,
            "block_reason": "",
            "exception_fact": "none_reported",
        },
        # Category 4: effect / impact (placeholder)
        "effect_and_upstream_class": {
            "effect_state_fact": "unknown_not_applied",
            "notes": "does_not_imply_upstream_handover_or_migration_completed",
        },
        # Category 5: return binding / routing (placeholder)
        "route_and_return_class": {
            "route_binding_ready": False,
            "return_route_kind": "not_bound_yet",
        },
        "upstream_evidence": {
            "release_control_input_scope": _RC_INPUT_SCOPE,
            "wiring_scope": _WIRING_SCOPE,
        },
        "consistency_observations": {
            "governance_action_status_object_present": bool(st_ok),
            "readiness_gate_present": bool(rg_ok),
        },
    }
    return True, payload

