# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Activation Dry-Run v0 (Minimal Implementation)

定位：
- Phase-Next-113：把 activation dry-run 从“设计冻结”推进到“统一对象的最小非动作实现”。

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


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0"


def _blocked(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_scope": _SCOPE,
        "activation_dry_run_status": "first_live_minimal_real_effect_activation_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_activation_dry_run_v0_non_effect",
    }


def _not_ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_scope": _SCOPE,
        "activation_dry_run_status": "first_live_minimal_real_effect_activation_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_activation_dry_run_v0_non_effect",
    }


def _ready(reason: str) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_scope": _SCOPE,
        "activation_dry_run_status": "first_live_minimal_real_effect_activation_ready",
        "side_effects_released": False,
        "reason": str(reason or "ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_activation_dry_run_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0: Any,
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
    - If none of the core upstream metadata dicts exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state activation_dry_run_status).
    """
    adm = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0
    lgate = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0
    pc = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0
    cg = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0
    cdr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0
    agate = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0
    ag = navigation_governance_action_release_control_first_live_enablement_approval_gate_v0
    ld = navigation_governance_action_release_control_first_live_launch_dry_run_v0
    live = navigation_governance_action_release_control_live_release_gate_v0
    seg = navigation_governance_action_release_control_side_effect_release_gate_v0
    ds = navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0
    idr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0
    sk = release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0

    any_core_present = any(
        isinstance(x, dict)
        for x in [adm, lgate, pc, cg, cdr, agate, ag, ld, live, seg, ds, idr, xs, rs]
    )
    if not any_core_present and not isinstance(sk, dict) and side_effects_released is None:
        return False, None

    # hard block: side_effects_released must remain false if present
    if side_effects_released is True:
        return True, _blocked("side_effects_released_true_is_not_allowed_in_activation_dry_run_v0")
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

    required_presence = [
        isinstance(adm, dict),
        isinstance(lgate, dict),
        isinstance(pc, dict),
        isinstance(cg, dict),
        isinstance(cdr, dict),
        isinstance(agate, dict),
        isinstance(ag, dict),
        isinstance(ld, dict),
        isinstance(live, dict),
        isinstance(seg, dict),
        isinstance(ds, dict),
        isinstance(idr, dict),
        isinstance(xs, dict),
        isinstance(rs, dict),
    ]
    if not all(required_presence):
        return True, _not_ready("missing_required_upstream_objects_for_activation_dry_run_v0")

    if _get(agate, "activation_admission_status") != "first_live_minimal_real_effect_activation_admitted":
        return True, _not_ready("activation_gate_not_activation_admitted")

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

    if _get(ag, "approval_status") != "first_live_enablement_approved":
        return True, _not_ready("approval_gate_not_approved")
    if _get(ld, "launch_status") != "first_live_launch_dry_run_ready":
        return True, _not_ready("launch_dry_run_not_ready")
    if _get(live, "live_release_status") != "live_release_ready":
        return True, _not_ready("live_release_gate_not_ready")
    if _get(seg, "side_effect_release_status") != "side_effect_release_ready":
        return True, _not_ready("side_effect_release_gate_not_ready")
    if _get(ds, "simulation_status") != "first_live_guarded_dry_effect_simulated":
        return True, _not_ready("dry_effect_simulation_not_simulated")
    if _get(idr, "execution_status") != "first_live_minimal_real_effect_implementation_dry_run_executed":
        return True, _not_ready("implementation_dry_run_execution_not_executed")

    return True, _ready(
        "activation_ready_after_activation_admitted_but_side_effects_remain_locked_in_v0"
    )

