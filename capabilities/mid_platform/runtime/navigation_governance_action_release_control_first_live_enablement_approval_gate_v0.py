# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Enablement Approval Gate v0
(minimal implementation; non-action).

Builds a standardized gate object:
`navigation_governance_action_release_control_first_live_enablement_approval_gate_v0`

Hard boundaries:
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- MUST keep side_effects_released == False in v0.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def _approval_signal_present_and_granted(sig: Any) -> Tuple[bool, bool]:
    """
    Minimal semantic placeholder:
    - presence: dict/object exists
    - granted: conservative check for a boolean grant field
    """
    if sig is None:
        return False, False
    if isinstance(sig, dict):
        present = True
        granted = bool(sig.get("approved") is True or sig.get("approval_granted") is True)
        return present, granted
    # Non-dict: treat as present but not granted (conservative)
    return True, False


def evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
    *,
    navigation_governance_action_release_control_first_live_enablement_dry_run_v0: Any,
    navigation_governance_action_release_control_live_release_gate_v0: Any,
    navigation_governance_action_release_control_side_effect_release_gate_v0: Any,
    navigation_governance_action_release_control_guarded_live_stub_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    navigation_governance_action_release_control_guarded_live_identity_v0: Any,
    navigation_governance_action_release_control_minimal_executor_identity_v0: Any,
    release_control_first_live_enablement_approval_signal_v0: Any = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only:
    - If none of the core inputs exist, return (False, None).
    - Otherwise, return attempted gate object with approval_status in
      {approved, not_approved, blocked}.
    """
    dr = _as_dict(navigation_governance_action_release_control_first_live_enablement_dry_run_v0)
    lg = _as_dict(navigation_governance_action_release_control_live_release_gate_v0)
    sg = _as_dict(navigation_governance_action_release_control_side_effect_release_gate_v0)
    gs = _as_dict(navigation_governance_action_release_control_guarded_live_stub_v0)
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)
    gid = _as_dict(navigation_governance_action_release_control_guarded_live_identity_v0)
    eid = _as_dict(navigation_governance_action_release_control_minimal_executor_identity_v0)

    any_core_present = bool(dr or lg or sg or gs or xs or rs or gid or eid)
    if not any_core_present:
        return False, None

    sig_present, sig_granted = _approval_signal_present_and_granted(
        release_control_first_live_enablement_approval_signal_v0
    )

    # Rule 1: dry-run not ready => not_approved
    if not dr or str(dr.get("dry_run_status") or "") != "enablement_dry_run_ready":
        return True, _not_approved(
            "dry_run_not_ready_or_missing",
            approval_signal_present=sig_present,
            approval_signal_granted=sig_granted,
        )

    # Rule 2: live / side-effect gate not ready => not_approved
    if not lg or str(lg.get("live_release_status") or "") != "live_release_ready":
        return True, _not_approved(
            "live_release_gate_not_ready_or_missing",
            approval_signal_present=sig_present,
            approval_signal_granted=sig_granted,
        )
    if not sg or str(sg.get("side_effect_release_status") or "") != "side_effect_release_ready":
        return True, _not_approved(
            "side_effect_release_gate_not_ready_or_missing",
            approval_signal_present=sig_present,
            approval_signal_granted=sig_granted,
        )

    # Rule 3: guarded candidate not established or side_effects_released != false => blocked
    if not gs or not isinstance(gs.get("payload"), dict):
        return True, _blocked("guarded_stub_state_missing")
    payload = gs.get("payload") or {}
    if payload.get("live_stub_entered") is not True:
        return True, _blocked("guarded_candidate_not_entered")
    if payload.get("side_effects_released") is not False:
        return True, _blocked("guarded_side_effects_not_locked")

    # Required surfaces in place (execution state / result)
    if not xs or not rs:
        return True, _not_approved(
            "execution_state_or_result_missing",
            approval_signal_present=sig_present,
            approval_signal_granted=sig_granted,
        )

    # Rule 4: identity / capability invalid => blocked
    if not gid or gid.get("can_enter_real_live_execution") is not False:
        return True, _blocked("guarded_identity_not_conservative")
    if not eid or eid.get("can_execute_real_release_control") is not False:
        return True, _blocked("executor_identity_not_conservative")

    # Rule 5: approval signal missing => not_approved
    if not sig_present or not sig_granted:
        return True, _not_approved(
            "approval_signal_missing_or_not_granted",
            approval_signal_present=sig_present,
            approval_signal_granted=sig_granted,
        )

    # Rule 6: prerequisites satisfied + approval granted => approved (still locked in v0)
    out: Dict[str, Any] = {
        "release_control_first_live_enablement_approval_gate_attempted": True,
        "release_control_first_live_enablement_approval_gate_scope": _SCOPE,
        "approval_status": "first_live_enablement_approved",
        "side_effects_released": False,
        "reason": "approved_to_enter_first_live_enablement_but_side_effects_locked_in_v0",
        "upstream_evidence": {
            "dry_run_status": "enablement_dry_run_ready",
            "live_release_status": "live_release_ready",
            "side_effect_release_status": "side_effect_release_ready",
            "guarded_entered": True,
            "guarded_side_effects_locked": True,
            "execution_state_present": True,
            "result_present": True,
            "approval_signal_present": sig_present,
            "approval_signal_granted": sig_granted,
        },
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
            "no_real_governance_actions": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }
    return True, out


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_enablement_approval_gate_attempted": True,
        "release_control_first_live_enablement_approval_gate_scope": _SCOPE,
        "approval_status": "first_live_enablement_blocked",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }


def _not_approved(
    reason: str,
    *,
    approval_signal_present: bool,
    approval_signal_granted: bool,
) -> Dict[str, Any]:
    return {
        "release_control_first_live_enablement_approval_gate_attempted": True,
        "release_control_first_live_enablement_approval_gate_scope": _SCOPE,
        "approval_status": "first_live_enablement_not_approved",
        "side_effects_released": False,
        "reason": str(reason),
        "upstream_evidence": {
            "approval_signal_present": bool(approval_signal_present),
            "approval_signal_granted": bool(approval_signal_granted),
        },
        "consume_mode": "minimal_implementation_non_action",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }

