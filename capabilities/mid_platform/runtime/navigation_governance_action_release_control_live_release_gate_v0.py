# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Live Release Gate v0 (minimal implementation; non-action).

Builds a standardized gate object:
`navigation_governance_action_release_control_live_release_gate_v0`

Hard boundaries:
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- side_effects_released MUST remain False in v0.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_live_release_gate_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_live_release_gate_v0(
    *,
    navigation_governance_action_release_control_executor_input_bridge_v0: Any,
    navigation_governance_action_release_control_guarded_live_stub_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    navigation_governance_action_release_control_guarded_live_identity_v0: Any,
    navigation_governance_action_release_control_minimal_executor_identity_v0: Any,
    navigation_governance_action_release_control_readiness_gate_v0: Any = None,
    navigation_governance_action_release_control_wiring_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If none of the core inputs exist, return (False, None).
    - Otherwise, return attempted gate object with status in {ready, not_ready, blocked}.
    """
    br = _as_dict(navigation_governance_action_release_control_executor_input_bridge_v0)
    gs = _as_dict(navigation_governance_action_release_control_guarded_live_stub_v0)
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)
    gid = _as_dict(navigation_governance_action_release_control_guarded_live_identity_v0)
    eid = _as_dict(navigation_governance_action_release_control_minimal_executor_identity_v0)

    any_core_present = bool(br or gs or xs or rs or gid or eid)
    if not any_core_present:
        return False, None

    # Rule 1: bridge not ready => not_ready
    if not br or str(br.get("bridge_status") or "") != "executor_input_bridge_ready":
        return True, _not_ready("bridge_not_ready_or_missing")

    # Rule 2: guarded candidate not established or side_effects_released != false => blocked
    if not gs or not isinstance(gs.get("payload"), dict):
        return True, _blocked("guarded_stub_state_missing")
    payload = gs.get("payload") or {}
    if payload.get("live_stub_entered") is not True:
        return True, _blocked("guarded_candidate_not_entered")
    if payload.get("side_effects_released") is not False:
        return True, _blocked("guarded_side_effects_not_locked")

    # Rule 3: execution state / result object not present => not_ready
    if not xs or not rs:
        return True, _not_ready("execution_state_or_result_missing")

    # Rule 4: identity / capability invalid => blocked
    if not gid or gid.get("can_enter_real_live_execution") is not False:
        return True, _blocked("guarded_identity_not_conservative")
    if not eid or eid.get("can_execute_real_release_control") is not False:
        return True, _blocked("executor_identity_not_conservative")

    # Rule 5: prerequisites satisfied => ready (but still do NOT release side effects in v0)
    out: Dict[str, Any] = {
        "release_control_live_release_gate_attempted": True,
        "release_control_live_release_gate_scope": _SCOPE,
        "live_release_status": "live_release_ready",
        "side_effects_released": False,
        "reason": "gate_ready_but_side_effects_locked_in_v0",
        "upstream_evidence": {
            "bridge_status": "executor_input_bridge_ready",
            "guarded_entered": True,
            "guarded_side_effects_locked": True,
            "execution_state_present": True,
            "result_present": True,
            "optional_readiness_present": bool(_as_dict(navigation_governance_action_release_control_readiness_gate_v0)),
            "optional_wiring_present": bool(_as_dict(navigation_governance_action_release_control_wiring_v0)),
        },
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "no_real_release_control": True,
            "no_real_governance_actions": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
            "side_effects_released_locked_false": True,
        },
    }
    return True, out


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        "release_control_live_release_gate_attempted": True,
        "release_control_live_release_gate_scope": _SCOPE,
        "live_release_status": "live_release_blocked",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_live_release_gate_attempted": True,
        "release_control_live_release_gate_scope": _SCOPE,
        "live_release_status": "live_release_not_ready",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }

