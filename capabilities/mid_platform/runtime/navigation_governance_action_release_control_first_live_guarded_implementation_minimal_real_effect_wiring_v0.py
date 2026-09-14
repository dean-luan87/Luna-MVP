# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation Minimal Real-Effect Wiring v0
(minimal implementation; non-effect wiring; non-action).

Builds a standardized wiring object:
`navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0`

Goal (Phase-Next-93):
- Wire the minimal real-effect stub entry surface to approval / launch / gates / dry-effect simulation
  in a recognize-only / observe-only manner.
- Prove there is a single, unambiguous legal ingress for future minimal real-effect writes (still locked).

Hard boundaries:
- MUST keep side_effects_released == False in v0.
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"
)


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
    *,
    navigation_governance_action_release_control_first_live_enablement_approval_gate_v0: Any,
    navigation_governance_action_release_control_first_live_launch_dry_run_v0: Any,
    navigation_governance_action_release_control_live_release_gate_v0: Any,
    navigation_governance_action_release_control_side_effect_release_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only policy (caller may pre-filter):
    - If none of the core upstream metadata objects exist, evaluator may return (False, None).
    - Otherwise, return attempted wiring object with wiring_status in
      {first_live_minimal_real_effect_wired_ready, first_live_minimal_real_effect_wired_not_ready,
       first_live_minimal_real_effect_wired_blocked}.
    """
    ag = _as_dict(navigation_governance_action_release_control_first_live_enablement_approval_gate_v0)
    ld = _as_dict(navigation_governance_action_release_control_first_live_launch_dry_run_v0)
    lg = _as_dict(navigation_governance_action_release_control_live_release_gate_v0)
    sg = _as_dict(navigation_governance_action_release_control_side_effect_release_gate_v0)
    ds = _as_dict(navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0)
    stub = _as_dict(release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0)
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)

    any_core_present = bool(ag or ld or lg or sg or ds or xs or rs or stub)
    if not any_core_present:
        return False, None

    # Rule 0: minimal real-effect stub identity must be conservative and correctly scoped
    if not stub:
        return True, _blocked("minimal_real_effect_stub_identity_missing")
    if stub.get("is_stub") is not True:
        return True, _blocked("minimal_real_effect_stub_identity_not_stub")
    if stub.get("is_real_effect_stub") is not True:
        return True, _blocked("minimal_real_effect_stub_identity_not_real_effect_stub")
    if stub.get("can_open_side_effects_released") is not False:
        return True, _blocked("minimal_real_effect_stub_identity_not_conservative:can_open_side_effects_released")
    if stub.get("can_execute_real_release_control") is not False:
        return True, _blocked("minimal_real_effect_stub_identity_not_conservative:can_execute_real_release_control")
    if stub.get("can_real_write_execution_state") is not False:
        return True, _blocked("minimal_real_effect_stub_identity_not_conservative:can_real_write_execution_state")
    if stub.get("can_real_write_result_object") is not False:
        return True, _blocked("minimal_real_effect_stub_identity_not_conservative:can_real_write_result_object")
    if stub.get("can_real_write_failure_or_exception") is not False:
        return True, _blocked("minimal_real_effect_stub_identity_not_conservative:can_real_write_failure_or_exception")
    if (
        str(stub.get("release_control_first_live_guarded_minimal_real_effect_stub_scope") or "")
        != "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0"
    ):
        return True, _blocked("minimal_real_effect_stub_identity_scope_mismatch")

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

    # Rule 4: dry-effect simulation must be simulated
    if not ds or str(ds.get("simulation_status") or "") != "first_live_guarded_dry_effect_simulated":
        return True, _not_ready("dry_effect_simulation_not_simulated_or_missing")

    # Rule 5: state/result surfaces must be present
    if not xs or not rs:
        return True, _not_ready("execution_state_or_result_missing")

    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_wired_ready",
        "side_effects_released": False,
        "reason": "wired_ready_for_future_minimal_real_effect_stub_entry_but_side_effects_locked_in_v0",
        "upstream_evidence": {
            "approval_status": "first_live_enablement_approved",
            "launch_status": "first_live_launch_dry_run_ready",
            "live_release_status": "live_release_ready",
            "side_effect_release_status": "side_effect_release_ready",
            "simulation_status": "first_live_guarded_dry_effect_simulated",
            "minimal_real_effect_stub_identity_present": True,
            "execution_state_present": True,
            "result_present": True,
        },
        "consume_mode": "minimal_implementation_minimal_real_effect_non_effect_wiring",
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
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_wired_blocked",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_minimal_real_effect_non_effect_wiring",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_wired_not_ready",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_minimal_real_effect_non_effect_wiring",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }
