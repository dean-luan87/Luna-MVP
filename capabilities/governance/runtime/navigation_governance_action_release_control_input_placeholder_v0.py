# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Input Contract Placeholder v0 (read-only; non-action).

Builds a standardized placeholder object:
`navigation_governance_action_release_control_input_v0`

Hard boundaries:
- NOT executable input; NOT a command; NOT proof of release_control execution.
- Does NOT trigger release_control/rollback/interrupt; no maps; no voice/memory; no mid-platform migration.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_input_v0"
_INPUT_SCOPE = "navigation_governance_action_executor_input_v0"
_READINESS_SCOPE = "navigation_governance_action_executor_readiness_gate_v0"
_WIRING_SCOPE = "navigation_governance_action_executor_wiring_v0"
_APPROVAL_STATUS_SCOPE = "navigation_governance_action_approval_status_v0"
_ACTION_STATUS_SCOPE = "navigation_governance_action_status_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _extract(d: Dict[str, Any], *path: str) -> str:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict):
            return ""
        cur = cur.get(p)
    return str(cur or "")


def evaluate_navigation_governance_action_release_control_input_placeholder_v0(
    *,
    navigation_governance_action_executor_input_v0: Any,
    navigation_governance_action_executor_readiness_gate_v0: Any,
    navigation_governance_action_executor_wiring_v0: Any,
    navigation_governance_action_approval_status_v0: Any = None,
    navigation_governance_action_status_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - Requires valid implemented executor input object AND valid readiness gate object AND valid wiring object.
    - Requires executor input approved_action_type == release_control.
    - Optional status objects are read-only consistency context only (must NOT expand authority).

    Note:
    - This placeholder is intentionally conservative: execution_prerequisites_consistent is always False.
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

    approved_action_type = _extract(inp, "approved_action_type_class", "approved_action_type").strip()
    if approved_action_type != "release_control":
        return False, None

    rg = _as_dict(navigation_governance_action_executor_readiness_gate_v0)
    if not rg:
        return False, None
    if str(rg.get("governance_action_executor_readiness_scope") or "") != _READINESS_SCOPE:
        return False, None
    if rg.get("governance_action_executor_readiness_attempted") is not True:
        return False, None

    wg = _as_dict(navigation_governance_action_executor_wiring_v0)
    if not wg:
        return False, None
    if str(wg.get("governance_action_executor_wiring_scope") or "") != _WIRING_SCOPE:
        return False, None
    if wg.get("governance_action_executor_wiring_attempted") is not True:
        return False, None

    # Optional: consistency context only
    ap = _as_dict(navigation_governance_action_approval_status_v0)
    ap_ok = bool(
        ap
        and str(ap.get("governance_action_approval_status_scope") or "") == _APPROVAL_STATUS_SCOPE
        and str(ap.get("object_kind") or "") == "implemented_v0"
        and ap.get("governance_action_approval_status_present") is True
    )
    st = _as_dict(navigation_governance_action_status_v0)
    st_ok = bool(
        st
        and str(st.get("governance_action_status_scope") or "") == _ACTION_STATUS_SCOPE
        and str(st.get("object_kind") or "") == "implemented_v0"
        and st.get("governance_action_status_present") is True
    )

    payload: Dict[str, Any] = {
        "release_control_input_present": True,
        "release_control_input_scope": _SCOPE,
        "object_kind": "placeholder_v0",
        "action_type_confirmed": "release_control",
        "execution_prerequisites_consistent": False,
        "constraint_profile": "release_control_placeholder_minimal_constraints",
        "control_surface": "upstream_control_handover_only",
        "consume_mode": "read_only",
        "upstream_evidence": {
            "executor_input_scope": _INPUT_SCOPE,
            "readiness_scope": _READINESS_SCOPE,
            "wiring_scope": _WIRING_SCOPE,
            "approved_action_type": approved_action_type,
        },
        "consistency_observations": {
            "approval_status_object_present": bool(ap_ok),
            "action_status_object_present": bool(st_ok),
        },
        "hard_boundaries": {
            "can_execute_real_release_control": False,
            "can_execute_real_governance_actions": False,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }
    return True, payload

