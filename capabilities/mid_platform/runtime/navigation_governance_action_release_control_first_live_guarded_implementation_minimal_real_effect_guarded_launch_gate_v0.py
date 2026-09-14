# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Guarded Launch Gate v0 (Minimal Implementation)

定位：
- Phase-Next-103：把 guarded launch gate 从“设计冻结”推进到“统一对象的最小非动作实现”。

硬边界（写死）：
- side_effects_released 必须保持为 False。
- 不触发真实 release_control / rollback / interrupt。
- 不接地图、不引入时间/空间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_scope": _SCOPE,
        "launch_admission_status": "first_live_minimal_real_effect_launch_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_guarded_launch_gate_v0_non_effect",
    }


def _not_admitted(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_scope": _SCOPE,
        "launch_admission_status": "first_live_minimal_real_effect_launch_not_admitted",
        "side_effects_released": False,
        "reason": str(reason or "not_admitted"),
        "consume_mode": "first_live_guarded_minimal_real_effect_guarded_launch_gate_v0_non_effect",
    }


def _launch_admitted(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_scope": _SCOPE,
        "launch_admission_status": "first_live_minimal_real_effect_launch_admitted",
        "side_effects_released": False,
        "reason": str(reason or "launch_admitted"),
        "consume_mode": "first_live_guarded_minimal_real_effect_guarded_launch_gate_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_enablement_approval_gate_v0: Any,
    navigation_governance_action_release_control_first_live_launch_dry_run_v0: Any,
    navigation_governance_action_release_control_live_release_gate_v0: Any,
    navigation_governance_action_release_control_side_effect_release_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_signal_v0: Any,
    side_effects_released: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core upstream metadata dicts exist, returns (False, None).
    - Otherwise returns (True, attempted gate object with 3-state launch_admission_status).

    Notes:
    - launch_signal_v0 is semantic placeholder input; missing signal => launch_not_admitted.
    """
    adm = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0
    ldr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0
    ag = navigation_governance_action_release_control_first_live_enablement_approval_gate_v0
    ld = navigation_governance_action_release_control_first_live_launch_dry_run_v0
    lg = navigation_governance_action_release_control_live_release_gate_v0
    sg = navigation_governance_action_release_control_side_effect_release_gate_v0
    ds = navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0
    idr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0
    sk = release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0
    sig = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_signal_v0

    any_core_present = any(
        isinstance(x, dict)
        for x in [adm, ldr, ag, ld, lg, sg, ds, idr, xs, rs]
    )
    if not any_core_present and not isinstance(sk, dict) and sig is None and side_effects_released is None:
        return False, None

    # hard block: side_effects_released must remain false if present
    if side_effects_released is True:
        return True, _blocked("side_effects_released_true_is_not_allowed_in_guarded_launch_gate_v0")
    if side_effects_released not in (None, False):
        return True, _blocked("side_effects_released_value_invalid_or_unsafe")

    # skeleton identity must be present and conservative
    if not isinstance(sk, dict):
        return True, _blocked("missing_implementation_skeleton_identity_v0")
    if sk.get("is_skeleton") is not True or sk.get("is_real_effect_implementation_skeleton") is not True:
        return True, _blocked("implementation_skeleton_identity_mismatch")
    if sk.get("can_open_side_effects_released") is not False:
        return True, _blocked("implementation_skeleton_identity_not_conservative:can_open_side_effects_released")

    def _get(d: Any, key: str) -> str:
        return str(d.get(key) or "") if isinstance(d, dict) else ""

    # Presence must be in place for the final gate
    required_presence = [
        isinstance(adm, dict),
        isinstance(ldr, dict),
        isinstance(ag, dict),
        isinstance(ld, dict),
        isinstance(lg, dict),
        isinstance(sg, dict),
        isinstance(ds, dict),
        isinstance(idr, dict),
        isinstance(xs, dict),
        isinstance(rs, dict),
    ]
    if not all(required_presence):
        return True, _not_admitted("missing_required_upstream_objects_for_guarded_launch_gate_v0")

    if _get(adm, "admission_status") != "first_live_minimal_real_effect_admitted":
        return True, _not_admitted("admission_not_admitted")
    if _get(ldr, "launch_status") != "first_live_minimal_real_effect_launch_ready":
        return True, _not_admitted("guarded_launch_dry_run_not_launch_ready")

    if _get(ag, "approval_status") != "first_live_enablement_approved":
        return True, _not_admitted("approval_gate_not_approved")
    if _get(ld, "launch_status") != "first_live_launch_dry_run_ready":
        return True, _not_admitted("launch_dry_run_not_ready")
    if _get(lg, "live_release_status") != "live_release_ready":
        return True, _not_admitted("live_release_gate_not_ready")
    if _get(sg, "side_effect_release_status") != "side_effect_release_ready":
        return True, _not_admitted("side_effect_release_gate_not_ready")
    if _get(ds, "simulation_status") != "first_live_guarded_dry_effect_simulated":
        return True, _not_admitted("dry_effect_simulation_not_simulated")
    if _get(idr, "execution_status") != "first_live_minimal_real_effect_implementation_dry_run_executed":
        return True, _not_admitted("implementation_dry_run_execution_not_executed")

    # Launch signal must exist (semantic placeholder only)
    if not isinstance(sig, dict):
        return True, _not_admitted("missing_guarded_launch_signal_v0")

    return True, _launch_admitted(
        "launch_admitted_by_signal_and_all_preconditions_met_but_side_effects_remain_locked_in_v0"
    )

