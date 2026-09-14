# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Guarded Launch Dry-Run v0 (Minimal Implementation)

定位：
- Phase-Next-101：在 admission == admitted 之后、真实最小写入实现之前，做“最终发车演练层”的最小非动作实现。

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


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0"


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_scope": _SCOPE,
        "launch_status": "first_live_minimal_real_effect_launch_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_guarded_launch_dry_run_v0_non_effect",
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_scope": _SCOPE,
        "launch_status": "first_live_minimal_real_effect_launch_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_guarded_launch_dry_run_v0_non_effect",
    }


def _launch_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_scope": _SCOPE,
        "launch_status": "first_live_minimal_real_effect_launch_ready",
        "side_effects_released": False,
        "reason": str(reason or "launch_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_guarded_launch_dry_run_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_enablement_approval_gate_v0: Any,
    navigation_governance_action_release_control_first_live_launch_dry_run_v0: Any,
    navigation_governance_action_release_control_live_release_gate_v0: Any,
    navigation_governance_action_release_control_side_effect_release_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    side_effects_released: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core upstream dicts exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state launch_status).
    """
    adm = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0
    ag = navigation_governance_action_release_control_first_live_enablement_approval_gate_v0
    ld = navigation_governance_action_release_control_first_live_launch_dry_run_v0
    lg = navigation_governance_action_release_control_live_release_gate_v0
    sg = navigation_governance_action_release_control_side_effect_release_gate_v0
    ds = navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0
    idr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0
    sk = release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0

    any_core_present = any(isinstance(x, dict) for x in [adm, ag, ld, lg, sg, ds, idr, xs, rs])
    if not any_core_present and side_effects_released is None and not isinstance(sk, dict):
        return False, None

    # hard block: side_effects_released must remain false if present
    if side_effects_released is True:
        return True, _blocked("side_effects_released_true_is_not_allowed_in_guarded_launch_dry_run_v0")
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

    # must have admission admitted
    if not isinstance(adm, dict):
        return True, _not_ready("missing_admission_gate_v0")
    if _get(adm, "admission_status") != "first_live_minimal_real_effect_admitted":
        return True, _not_ready("admission_not_admitted")

    # presence required for last-check
    required_presence = [
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
        return True, _not_ready("missing_required_upstream_objects_for_guarded_launch_dry_run_v0")

    # readiness checks
    if _get(ag, "approval_status") != "first_live_enablement_approved":
        return True, _not_ready("approval_gate_not_approved")
    if _get(ld, "launch_status") != "first_live_launch_dry_run_ready":
        return True, _not_ready("launch_dry_run_not_ready")
    if _get(lg, "live_release_status") != "live_release_ready":
        return True, _not_ready("live_release_gate_not_ready")
    if _get(sg, "side_effect_release_status") != "side_effect_release_ready":
        return True, _not_ready("side_effect_release_gate_not_ready")
    if _get(ds, "simulation_status") != "first_live_guarded_dry_effect_simulated":
        return True, _not_ready("dry_effect_simulation_not_simulated")
    if _get(idr, "execution_status") != "first_live_minimal_real_effect_implementation_dry_run_executed":
        return True, _not_ready("implementation_dry_run_execution_not_executed")

    return True, _launch_ready("launch_ready_after_admission_but_side_effects_remain_locked_in_v0")

