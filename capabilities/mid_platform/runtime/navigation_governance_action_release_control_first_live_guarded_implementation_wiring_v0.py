# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation Wiring v0
(minimal implementation; non-effect wiring; non-action).

Builds a standardized wiring object:
`navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0`

Goal (Phase-Next-88):
- Wire the first-live guarded implementation *skeleton* to existing approval/launch/gates/contract chain
  in a recognize-only / observe-only / wire-only manner.
- Prove there is a single, unambiguous, standardized input path for future real guarded implementation.

Hard boundaries:
- MUST keep side_effects_released == False in v0.
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
    *,
    navigation_governance_action_release_control_first_live_enablement_approval_gate_v0: Any,
    navigation_governance_action_release_control_first_live_launch_dry_run_v0: Any,
    navigation_governance_action_release_control_live_release_gate_v0: Any,
    navigation_governance_action_release_control_side_effect_release_gate_v0: Any,
    release_control_first_live_guarded_implementation_skeleton_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only policy:
    - If none of the core upstream objects exist, return (False, None).
    - Otherwise, return attempted wiring object with wiring_status in
      {first_live_guarded_wired_ready, first_live_guarded_wired_not_ready, first_live_guarded_wired_blocked}.
    """
    ag = _as_dict(navigation_governance_action_release_control_first_live_enablement_approval_gate_v0)
    ld = _as_dict(navigation_governance_action_release_control_first_live_launch_dry_run_v0)
    lg = _as_dict(navigation_governance_action_release_control_live_release_gate_v0)
    sg = _as_dict(navigation_governance_action_release_control_side_effect_release_gate_v0)
    sk = _as_dict(release_control_first_live_guarded_implementation_skeleton_identity_v0)
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)

    any_core_present = bool(ag or ld or lg or sg or xs or rs or sk)
    if not any_core_present:
        return False, None

    # Rule 0: skeleton identity must be conservative and correctly scoped
    if not sk:
        return True, _blocked("skeleton_identity_missing")
    if sk.get("is_skeleton") is not True:
        return True, _blocked("skeleton_identity_not_skeleton")
    if sk.get("can_open_side_effects_released") is not False:
        return True, _blocked("skeleton_identity_not_conservative:can_open_side_effects_released")
    if sk.get("can_execute_real_release_control") is not False:
        return True, _blocked("skeleton_identity_not_conservative:can_execute_real_release_control")
    if (
        str(sk.get("release_control_first_live_guarded_implementation_skeleton_scope") or "")
        != "navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0"
    ):
        return True, _blocked("skeleton_identity_scope_mismatch")

    # Rule 1: approval gate must be approved
    if not ag or str(ag.get("approval_status") or "") != "first_live_enablement_approved":
        return True, _not_ready("approval_gate_not_approved_or_missing")

    # Rule 2: launch dry-run must be ready
    if not ld or str(ld.get("launch_status") or "") != "first_live_launch_dry_run_ready":
        return True, _not_ready("launch_dry_run_not_ready_or_missing")

    # Rule 3: live/side-effect release gates must be ready
    if not lg or str(lg.get("live_release_status") or "") != "live_release_ready":
        return True, _not_ready("live_release_gate_not_ready_or_missing")
    if not sg or str(sg.get("side_effect_release_status") or "") != "side_effect_release_ready":
        return True, _not_ready("side_effect_release_gate_not_ready_or_missing")

    # Rule 4: state/result surfaces must be present
    if not xs or not rs:
        return True, _not_ready("execution_state_or_result_missing")

    # All prerequisites satisfied => wired_ready (still non-effect)
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_guarded_wired_ready",
        "side_effects_released": False,
        "reason": "wired_ready_for_future_real_guarded_implementation_entry_but_side_effects_locked_in_v0",
        "upstream_evidence": {
            "approval_status": "first_live_enablement_approved",
            "launch_status": "first_live_launch_dry_run_ready",
            "live_release_status": "live_release_ready",
            "side_effect_release_status": "side_effect_release_ready",
            "skeleton_identity_present": True,
            "execution_state_present": True,
            "result_present": True,
        },
        "consume_mode": "minimal_implementation_non_effect_wiring",
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
        "release_control_first_live_guarded_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_guarded_wired_blocked",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_effect_wiring",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_guarded_wired_not_ready",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_non_effect_wiring",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }

