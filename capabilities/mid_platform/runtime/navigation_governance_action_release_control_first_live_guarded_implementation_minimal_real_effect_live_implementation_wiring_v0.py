# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Non-Effect Wiring v0
(minimal implementation; non-effect wiring; non-action).

Builds a standardized wiring object:
`navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0`

Goal (Phase-Next-119):
- Wire the *live implementation plan* (frozen) into a runtime-visible non-effect wiring object,
  proving the future live minimal implementation has a single, standardized ingress readiness signal.
- Still MUST NOT execute any real writes and MUST keep side_effects_released == False.

Hard boundaries:
- MUST keep side_effects_released == False in v0.
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0"


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    side_effects_released: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only policy:
    - If none of the core upstream objects exist, return (False, None).
    - Otherwise, return attempted wiring object with wiring_status in:
      {first_live_minimal_real_effect_live_wired_ready,
       first_live_minimal_real_effect_live_wired_not_ready,
       first_live_minimal_real_effect_live_wired_blocked}.
    """
    adm = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0
    )
    lgate = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0
    )
    pc = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0
    )
    cg = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0
    )
    cdr = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0
    )
    ag = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0
    )
    adr = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0
    )
    sk = _as_dict(
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0
    )
    stub = _as_dict(
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0
    )
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)

    any_core_present = any(
        isinstance(x, dict) for x in [adm, lgate, pc, cg, cdr, ag, adr, xs, rs, sk, stub]
    )
    if not any_core_present and side_effects_released is None:
        return False, None

    # hard block: side_effects_released must remain false if present
    if side_effects_released is True:
        return True, _blocked("side_effects_released_true_is_not_allowed_in_live_implementation_wiring_v0")
    if side_effects_released not in (None, False):
        return True, _blocked("side_effects_released_value_invalid_or_unsafe")

    # Rule 0: live implementation skeleton identity must be present and conservative
    if not isinstance(sk, dict):
        return True, _blocked("missing_live_implementation_skeleton_identity_v0")
    if sk.get("is_skeleton") is not True or sk.get("is_live_implementation_skeleton") is not True:
        return True, _blocked("live_implementation_skeleton_identity_mismatch")
    if sk.get("can_open_side_effects_released") is not False:
        return True, _blocked("live_implementation_skeleton_identity_not_conservative:can_open_side_effects_released")
    if (
        str(sk.get("release_control_first_live_guarded_minimal_real_effect_live_implementation_skeleton_scope") or "")
        != "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0"
    ):
        return True, _blocked("live_implementation_skeleton_identity_scope_mismatch")

    # Rule 0b: live implementation stub identity must be present and conservative
    if not isinstance(stub, dict):
        return True, _blocked("missing_live_implementation_stub_identity_v0")
    if stub.get("is_stub") is not True or stub.get("is_live_implementation_stub") is not True:
        return True, _blocked("live_implementation_stub_identity_mismatch")
    if stub.get("side_effects_released") is not False:
        return True, _blocked("live_implementation_stub_identity_not_conservative:side_effects_released")
    if (
        str(stub.get("release_control_first_live_guarded_minimal_real_effect_live_implementation_stub_scope") or "")
        != "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0"
    ):
        return True, _blocked("live_implementation_stub_identity_scope_mismatch")

    def _get(d: Any, key: str) -> str:
        return str(d.get(key) or "") if isinstance(d, dict) else ""

    required_presence = [
        isinstance(adm, dict),
        isinstance(lgate, dict),
        isinstance(pc, dict),
        isinstance(cg, dict),
        isinstance(cdr, dict),
        isinstance(ag, dict),
        isinstance(adr, dict),
        isinstance(xs, dict),
        isinstance(rs, dict),
    ]
    if not all(required_presence):
        return True, _not_ready("missing_required_upstream_objects_for_live_implementation_wiring_v0")

    if _get(adm, "admission_status") != "first_live_minimal_real_effect_admitted":
        return True, _not_ready("admission_not_admitted")
    if _get(lgate, "launch_admission_status") != "first_live_minimal_real_effect_launch_admitted":
        return True, _not_ready("guarded_launch_gate_not_launch_admitted")
    if _get(pc, "pre_commit_status") != "first_live_minimal_real_effect_pre_commit_ready":
        return True, _not_ready("pre_commit_dry_run_not_pre_commit_ready")
    if _get(cg, "commit_admission_status") != "first_live_minimal_real_effect_commit_admitted":
        return True, _not_ready("commit_gate_not_commit_admitted")
    if _get(cdr, "commit_dry_run_status") != "first_live_minimal_real_effect_commit_ready":
        return True, _not_ready("commit_dry_run_not_commit_ready")
    if _get(ag, "activation_admission_status") != "first_live_minimal_real_effect_activation_admitted":
        return True, _not_ready("activation_gate_not_activation_admitted")
    if _get(adr, "activation_dry_run_status") != "first_live_minimal_real_effect_activation_ready":
        return True, _not_ready("activation_dry_run_not_activation_ready")

    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_live_wired_ready",
        "side_effects_released": False,
        "reason": "wired_ready_for_future_live_implementation_entry_but_side_effects_locked_in_v0",
        "upstream_evidence": {
            "admission_status": "first_live_minimal_real_effect_admitted",
            "launch_admission_status": "first_live_minimal_real_effect_launch_admitted",
            "pre_commit_status": "first_live_minimal_real_effect_pre_commit_ready",
            "commit_admission_status": "first_live_minimal_real_effect_commit_admitted",
            "commit_dry_run_status": "first_live_minimal_real_effect_commit_ready",
            "activation_admission_status": "first_live_minimal_real_effect_activation_admitted",
            "activation_dry_run_status": "first_live_minimal_real_effect_activation_ready",
            "live_implementation_skeleton_identity_present": True,
            "live_implementation_stub_identity_present": True,
            "execution_state_present": True,
            "result_present": True,
        },
        "consume_mode": "minimal_implementation_live_implementation_non_effect_wiring",
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
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_live_wired_blocked",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_live_implementation_non_effect_wiring",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_live_wired_not_ready",
        "side_effects_released": False,
        "reason": str(reason),
        "consume_mode": "minimal_implementation_live_implementation_non_effect_wiring",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }

