# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Implementation Non-Effect Wiring v0

定位：
- Phase-Next-97：把 minimal real-effect implementation skeleton 与现有 gates / simulation / minimal real-effect dry-run execution
  做一次“非副作用接线”，形成未来真实实现层的单一合法入口对象。

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


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0"


def _blocked(reason: str, *, upstream: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_implementation_wired_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_wiring_v0_non_effect",
        "hard_boundaries": {
            "side_effects_released_must_remain_false": True,
            "no_real_release_control": True,
            "no_real_rollback": True,
            "no_real_interrupt": True,
            "no_route_change": True,
            "no_voice_output": True,
            "no_memory_write": True,
            "no_mid_platform_real_migration": True,
        },
    }
    if isinstance(upstream, dict):
        out["upstream_evidence"] = dict(upstream)
    return out


def _not_ready(reason: str, *, upstream: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_implementation_wired_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_wiring_v0_non_effect",
        "hard_boundaries": {
            "side_effects_released_must_remain_false": True,
            "no_real_release_control": True,
            "no_real_rollback": True,
            "no_real_interrupt": True,
            "no_route_change": True,
            "no_voice_output": True,
            "no_memory_write": True,
            "no_mid_platform_real_migration": True,
        },
    }
    if isinstance(upstream, dict):
        out["upstream_evidence"] = dict(upstream)
    return out


def _wired_ready(reason: str, *, upstream: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_scope": _SCOPE,
        "wiring_status": "first_live_minimal_real_effect_implementation_wired_ready",
        "side_effects_released": False,
        "reason": str(reason or "wired_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_wiring_v0_non_effect",
        "hard_boundaries": {
            "side_effects_released_must_remain_false": True,
            "no_real_release_control": True,
            "no_real_rollback": True,
            "no_real_interrupt": True,
            "no_route_change": True,
            "no_voice_output": True,
            "no_memory_write": True,
            "no_mid_platform_real_migration": True,
        },
    }
    if isinstance(upstream, dict):
        out["upstream_evidence"] = dict(upstream)
    return out


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
    *,
    navigation_governance_action_release_control_first_live_enablement_approval_gate_v0: Any,
    navigation_governance_action_release_control_first_live_launch_dry_run_v0: Any,
    navigation_governance_action_release_control_live_release_gate_v0: Any,
    navigation_governance_action_release_control_side_effect_release_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core inputs exist, returns (False, None).
    - Otherwise returns (True, attempted wiring object with 3-state wiring_status).
    """
    ag = navigation_governance_action_release_control_first_live_enablement_approval_gate_v0
    ld = navigation_governance_action_release_control_first_live_launch_dry_run_v0
    lg = navigation_governance_action_release_control_live_release_gate_v0
    sg = navigation_governance_action_release_control_side_effect_release_gate_v0
    ds = navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0
    dr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0
    sk = release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0

    any_core_present = any(isinstance(x, dict) for x in [ag, ld, lg, sg, ds, dr, xs, rs])
    if not any_core_present and not isinstance(sk, dict):
        return False, None

    upstream: Dict[str, Any] = {
        "approval_gate_present": isinstance(ag, dict),
        "launch_dry_run_present": isinstance(ld, dict),
        "live_release_gate_present": isinstance(lg, dict),
        "side_effect_release_gate_present": isinstance(sg, dict),
        "dry_effect_simulation_present": isinstance(ds, dict),
        "minimal_real_effect_dry_run_execution_present": isinstance(dr, dict),
        "execution_state_present": isinstance(xs, dict),
        "result_present": isinstance(rs, dict),
        "implementation_skeleton_identity_present": isinstance(sk, dict),
    }

    # skeleton identity must be present and conservative
    if not isinstance(sk, dict):
        return True, _blocked("missing_implementation_skeleton_identity_v0", upstream=upstream)
    if sk.get("is_skeleton") is not True or sk.get("is_real_effect_implementation_skeleton") is not True:
        return True, _blocked("implementation_skeleton_identity_mismatch", upstream=upstream)
    if sk.get("can_open_side_effects_released") is not False:
        return True, _blocked("implementation_skeleton_identity_not_conservative:can_open_side_effects_released", upstream=upstream)

    # helper: read status string from dicts
    def _get(d: Any, key: str) -> str:
        return str(d.get(key) or "") if isinstance(d, dict) else ""

    # If any upstream explicitly reports blocked, collapse to blocked (when present)
    blocked_signals = [
        _get(ag, "approval_status") == "first_live_enablement_blocked",
        _get(ld, "launch_status") == "first_live_launch_dry_run_blocked",
        _get(lg, "live_release_status") == "live_release_blocked",
        _get(sg, "side_effect_release_status") == "side_effect_release_blocked",
        _get(ds, "simulation_status") == "first_live_guarded_dry_effect_blocked",
        _get(dr, "execution_status") == "first_live_minimal_real_effect_dry_run_blocked",
    ]
    if any(blocked_signals):
        return True, _blocked("blocked_by_upstream_gate_or_simulation_or_dry_run", upstream=upstream)

    # Presence checks (must be in place to be wired_ready)
    required_presence = [
        isinstance(ag, dict),
        isinstance(ld, dict),
        isinstance(lg, dict),
        isinstance(sg, dict),
        isinstance(ds, dict),
        isinstance(dr, dict),
        isinstance(xs, dict),
        isinstance(rs, dict),
    ]
    if not all(required_presence):
        return True, _not_ready("missing_required_upstream_objects_for_implementation_wiring", upstream=upstream)

    # Status checks (must match exact ready states)
    if _get(ag, "approval_status") != "first_live_enablement_approved":
        return True, _not_ready("approval_gate_not_approved", upstream=upstream)
    if _get(ld, "launch_status") != "first_live_launch_dry_run_ready":
        return True, _not_ready("launch_dry_run_not_ready", upstream=upstream)
    if _get(lg, "live_release_status") != "live_release_ready":
        return True, _not_ready("live_release_gate_not_ready", upstream=upstream)
    if _get(sg, "side_effect_release_status") != "side_effect_release_ready":
        return True, _not_ready("side_effect_release_gate_not_ready", upstream=upstream)
    if _get(ds, "simulation_status") != "first_live_guarded_dry_effect_simulated":
        return True, _not_ready("dry_effect_simulation_not_simulated", upstream=upstream)
    if _get(dr, "execution_status") != "first_live_minimal_real_effect_dry_run_executed":
        return True, _not_ready("minimal_real_effect_dry_run_execution_not_executed", upstream=upstream)

    return True, _wired_ready(
        "wired_ready_for_future_minimal_real_effect_implementation_skeleton_entry_but_side_effects_locked_in_v0",
        upstream=upstream,
    )

