# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation Dry-Effect Simulation v0
(minimal implementation; non-action; NO side effects).

Builds a standardized simulation object:
`navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0`

Goal (Phase-Next-90):
- After non-effect execution is executed, simulate "if allowed real side effects were released",
  what *targets* the code path would point to, and verify forbidden targets are excluded.
- This is a dry simulation only: it must not open side effects and must not write anything real.

Hard boundaries:
- MUST keep side_effects_released == False in v0.
- NOT an executor; does NOT trigger release_control/rollback/interrupt.
- No maps; no voice/memory; no mid-platform real migration; no route/proposal changes.
- Consumes ONLY standardized objects; does not fabricate missing evidence.
- No time/space anchors.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"

_ALLOWED_TARGETS: Tuple[str, ...] = (
    "execution_state_update_target",
    "result_object_update_target",
    "failure_or_exception_path_target",
)
_FORBIDDEN_TARGET_PREFIXES: Tuple[str, ...] = (
    "route_",
    "voice_",
    "memory_",
    "migration_",
    "rollback_",
    "interrupt_",
    "map_",
)


def _as_dict(x: Any) -> Optional[Dict[str, Any]]:
    return x if isinstance(x, dict) else None


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0: Any,
    release_control_first_live_guarded_implementation_skeleton_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Returns (applicable, payload).

    relevant-only policy:
    - If none of the core upstream objects exist, return (False, None).
    - Otherwise, return attempted simulation object with simulation_status in
      {simulated, not_ready, blocked}.
    """
    ex = _as_dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0
    )
    sk = _as_dict(release_control_first_live_guarded_implementation_skeleton_identity_v0)
    xs = _as_dict(navigation_governance_action_release_control_execution_state_v0)
    rs = _as_dict(navigation_governance_action_release_control_result_v0)

    any_core_present = bool(ex or sk or xs or rs)
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

    # Rule 1: non-effect execution must be executed
    if not ex or str(ex.get("execution_status") or "") != "first_live_guarded_non_effect_executed":
        return True, _not_ready("non_effect_execution_not_executed_or_missing")

    # Rule 2: state/result surfaces must be present
    if not xs or not rs:
        return True, _not_ready("execution_state_or_result_missing")

    # Dry simulation: enumerate target intents (must be limited to allowed targets)
    targets: List[str] = list(_ALLOWED_TARGETS)

    # Forbidden target isolation check (defensive)
    forbidden_hits: List[str] = []
    for t in targets:
        if t not in _ALLOWED_TARGETS:
            forbidden_hits.append(t)
            continue
        for pref in _FORBIDDEN_TARGET_PREFIXES:
            if str(t).startswith(pref):
                forbidden_hits.append(t)
                break

    if forbidden_hits:
        return True, _blocked("forbidden_simulation_targets_detected")

    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_dry_effect_simulation_attempted": True,
        "release_control_first_live_guarded_implementation_dry_effect_simulation_scope": _SCOPE,
        "simulation_status": "first_live_guarded_dry_effect_simulated",
        "side_effects_released": False,
        "simulation_targets": list(targets),
        "reason": "dry_effect_simulated_targets_limited_to_allowed_surfaces_only",
        "upstream_evidence": {
            "execution_status": "first_live_guarded_non_effect_executed",
            "execution_state_present": True,
            "result_present": True,
            "targets_count": len(targets),
            "forbidden_hits_count": len(forbidden_hits),
        },
        "consume_mode": "minimal_implementation_dry_effect_simulation",
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
        "release_control_first_live_guarded_implementation_dry_effect_simulation_attempted": True,
        "release_control_first_live_guarded_implementation_dry_effect_simulation_scope": _SCOPE,
        "simulation_status": "first_live_guarded_dry_effect_blocked",
        "side_effects_released": False,
        "simulation_targets": [],
        "reason": str(reason),
        "consume_mode": "minimal_implementation_dry_effect_simulation",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_dry_effect_simulation_attempted": True,
        "release_control_first_live_guarded_implementation_dry_effect_simulation_scope": _SCOPE,
        "simulation_status": "first_live_guarded_dry_effect_not_ready",
        "side_effects_released": False,
        "simulation_targets": [],
        "reason": str(reason),
        "consume_mode": "minimal_implementation_dry_effect_simulation",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
        },
    }

