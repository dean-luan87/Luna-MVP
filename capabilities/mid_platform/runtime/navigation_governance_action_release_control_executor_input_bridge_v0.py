# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Executor Input Bridge v0 (minimal implementation; non-action).

Builds a standardized bridge object:
`navigation_governance_action_release_control_executor_input_bridge_v0`

Hard boundaries:
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.

Purpose:
- Collapse multiple preconditions into ONE final, observable bridge object that the minimal executor
  is allowed to consume in the future.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_executor_input_bridge_v0"

_RC_INPUT_SCOPE = "navigation_governance_action_release_control_input_v0"
_RC_EXECUTION_STATE_SCOPE = "navigation_governance_action_release_control_execution_state_v0"
_RC_RESULT_SCOPE = "navigation_governance_action_release_control_result_v0"
_RC_READINESS_SCOPE = "navigation_governance_action_release_control_readiness_gate_v0"
_RC_WIRING_SCOPE = "navigation_governance_action_release_control_wiring_v0"

_MIN_EXECUTOR_SCOPE = "navigation_governance_action_release_control_minimal_executor_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
    *,
    navigation_governance_action_release_control_input_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    navigation_governance_action_release_control_readiness_gate_v0: Any,
    navigation_governance_action_release_control_wiring_v0: Any,
    release_control_minimal_executor_identity: Any,
    navigation_governance_action_approval_status_v0: Any = None,
    navigation_governance_action_executor_wiring_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only / output policy:
    - If absolutely none of the core objects exist, return (False, None).
    - Otherwise return attempted bridge object with status in {ready, not_ready, blocked}.

    Conservatism:
    - Even when bridge_status == executor_input_bridge_ready, consumable_by_executor MUST remain False in v0.
    """
    inp = _as_dict(navigation_governance_action_release_control_input_v0)
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)
    rg = _as_dict(navigation_governance_action_release_control_readiness_gate_v0)
    wg = _as_dict(navigation_governance_action_release_control_wiring_v0)
    ident = _as_dict(release_control_minimal_executor_identity)

    any_core_present = bool(inp or xs or rs or rg or wg or ident)
    if not any_core_present:
        return False, None

    missing: Dict[str, bool] = {
        "input_missing": not bool(inp),
        "execution_state_missing": not bool(xs),
        "result_missing": not bool(rs),
        "readiness_missing": not bool(rg),
        "wiring_missing": not bool(wg),
        "executor_identity_missing": not bool(ident),
    }
    if any(missing.values()):
        return True, {
            "release_control_executor_input_bridge_attempted": True,
            "release_control_executor_input_bridge_scope": _SCOPE,
            "bridge_status": "executor_input_bridge_not_ready",
            "consumable_by_executor": False,
            "reason": "missing_core_sources_for_bridge",
            "missing": dict(missing),
            "consume_mode": "minimal_implementation_non_action",
            "hard_boundaries": {
                "no_real_release_control": True,
                "no_real_governance_actions": True,
                "no_route_change": True,
                "no_voice_or_memory_side_effects": True,
                "no_mid_platform_real_migration": True,
                "no_time_or_space_anchors": True,
            },
        }

    # Basic scope/kind checks (do not overfit; keep minimal and readable).
    if str(inp.get("release_control_input_scope") or "") != _RC_INPUT_SCOPE:
        return True, _blocked("input_scope_mismatch")
    if str(xs.get("release_control_execution_state_scope") or "") != _RC_EXECUTION_STATE_SCOPE:
        return True, _blocked("execution_state_scope_mismatch")
    if str(rs.get("release_control_result_scope") or "") != _RC_RESULT_SCOPE:
        return True, _blocked("result_scope_mismatch")
    if str(rg.get("release_control_readiness_scope") or "") != _RC_READINESS_SCOPE:
        return True, _blocked("readiness_scope_mismatch")
    if str(wg.get("release_control_wiring_scope") or "") != _RC_WIRING_SCOPE:
        return True, _blocked("wiring_scope_mismatch")

    # Must be implemented objects for the 3 core contracts.
    if str(inp.get("object_kind") or "") != "implemented_v0":
        return True, _blocked("input_not_implemented_object")
    if str(xs.get("object_kind") or "") != "implemented_v0":
        return True, _blocked("execution_state_not_implemented_object")
    if str(rs.get("object_kind") or "") != "implemented_v0":
        return True, _blocked("result_not_implemented_object")

    # Type confirmation: release_control.
    at_inp = str(inp.get("action_type_confirmed") or (inp.get("action_type_class") or {}).get("action_type_confirmed") or "")
    at_xs = str((xs.get("action_type_class") or {}).get("action_type_confirmed") or xs.get("action_type_confirmed") or "")
    at_rs = str((rs.get("action_type_class") or {}).get("action_type_confirmed") or rs.get("action_type_confirmed") or "")
    if any(x != "release_control" for x in [at_inp, at_xs, at_rs]):
        return True, _blocked("action_type_not_release_control")

    # Readiness gate must be ready_candidate.
    rg_status = str(rg.get("release_control_readiness_status") or "")
    if rg.get("release_control_readiness_attempted") is not True:
        return True, _blocked("readiness_not_attempted")
    if rg_status != "ready_candidate":
        # Conservative: treat as not_ready rather than blocked unless it's clearly invalid.
        return True, _not_ready(f"readiness_status:{rg_status or 'missing'}")

    # Wiring must be wired_inactive or wired_action_ready.
    wg_status = str(wg.get("release_control_wiring_status") or "")
    if wg.get("release_control_wiring_attempted") is not True:
        return True, _blocked("wiring_not_attempted")
    if wg_status not in {"wired_inactive", "wired_action_ready"}:
        return True, _blocked(f"wiring_status:{wg_status or 'missing'}")

    # Minimal executor identity/capability must match and must be skeleton/non-executable in v0.
    if str(ident.get("release_control_minimal_executor_scope") or "") != _MIN_EXECUTOR_SCOPE:
        return True, _blocked("executor_identity_scope_mismatch")
    if ident.get("can_execute_real_release_control") is not False:
        return True, _blocked("executor_capability_not_conservative")

    payload: Dict[str, Any] = {
        "release_control_executor_input_bridge_attempted": True,
        "release_control_executor_input_bridge_scope": _SCOPE,
        "bridge_status": "executor_input_bridge_ready",
        "consumable_by_executor": False,
        "reason": "bridge_ready_but_consumption_locked_in_v0",
        "upstream_evidence": {
            "input_scope": _RC_INPUT_SCOPE,
            "execution_state_scope": _RC_EXECUTION_STATE_SCOPE,
            "result_scope": _RC_RESULT_SCOPE,
            "readiness_scope": _RC_READINESS_SCOPE,
            "wiring_scope": _RC_WIRING_SCOPE,
            "executor_scope": _MIN_EXECUTOR_SCOPE,
            "optional_approval_status_present": bool(_as_dict(navigation_governance_action_approval_status_v0)),
            "optional_executor_wiring_present": bool(_as_dict(navigation_governance_action_executor_wiring_v0)),
        },
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "no_real_release_control": True,
            "no_real_governance_actions": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }
    return True, payload


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        "release_control_executor_input_bridge_attempted": True,
        "release_control_executor_input_bridge_scope": _SCOPE,
        "bridge_status": "executor_input_bridge_blocked",
        "consumable_by_executor": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "no_real_release_control": True,
            "no_real_governance_actions": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_executor_input_bridge_attempted": True,
        "release_control_executor_input_bridge_scope": _SCOPE,
        "bridge_status": "executor_input_bridge_not_ready",
        "consumable_by_executor": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "no_real_release_control": True,
            "no_real_governance_actions": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }

