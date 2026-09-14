# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Implementation Dry-Run Execution v0

定位：
- Phase-Next-98：在 implementation wiring == wired_ready 的前提下，让 implementation skeleton 第一次跑通
  “未来真实实现层的干跑执行链（state -> result -> failure/exception closure）”，但保持零真实副作用。

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


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"


def _blocked(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_scope": _SCOPE,
        "execution_status": "first_live_minimal_real_effect_implementation_dry_run_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_dry_run_execution_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["execution_trace"] = dict(trace)
    return out


def _not_ready(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_scope": _SCOPE,
        "execution_status": "first_live_minimal_real_effect_implementation_dry_run_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_dry_run_execution_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["execution_trace"] = dict(trace)
    return out


def _executed(reason: str, *, trace: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_scope": _SCOPE,
        "execution_status": "first_live_minimal_real_effect_implementation_dry_run_executed",
        "side_effects_released": False,
        "execution_trace": dict(trace),
        "reason": str(reason or "executed"),
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_dry_run_execution_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of wiring/state/result exist, returns (False, None).
    - Otherwise returns (True, attempted dry-run object with 3-state execution_status).

    Success chain (fixed order):
    - execution_state_real_write_placeholder_call_from_implementation
    - result_object_real_write_placeholder_call_from_implementation
    - failure_or_exception_real_write_placeholder_closure_from_implementation
    """
    iw = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0
    sk = release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0

    any_core_present = any(isinstance(x, dict) for x in [iw, xs, rs])
    if not any_core_present:
        return False, None

    trace: Dict[str, Any] = {
        "execution_chain_order": [],
        "placeholder_call_results": {},
    }

    if not isinstance(iw, dict):
        return True, _not_ready("missing_implementation_wiring_v0", trace=trace)

    if str(iw.get("wiring_status") or "") != "first_live_minimal_real_effect_implementation_wired_ready":
        return True, _not_ready("implementation_wiring_not_wired_ready", trace=trace)

    if not isinstance(sk, dict):
        return True, _blocked("missing_implementation_skeleton_identity_v0", trace=trace)
    if sk.get("is_skeleton") is not True or sk.get("is_real_effect_implementation_skeleton") is not True:
        return True, _blocked("implementation_skeleton_identity_mismatch", trace=trace)
    if sk.get("can_open_side_effects_released") is not False:
        return True, _blocked("implementation_skeleton_identity_not_conservative:can_open_side_effects_released", trace=trace)

    if not isinstance(xs, dict):
        return True, _not_ready("missing_execution_state_v0", trace=trace)
    if not isinstance(rs, dict):
        return True, _not_ready("missing_result_v0", trace=trace)

    # Dry-run placeholder calls: strictly call skeleton placeholder interfaces.
    try:
        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
            write_first_live_execution_state_real_effect_from_implementation,
            write_first_live_failure_or_exception_real_effect_from_implementation,
            write_first_live_result_object_real_effect_from_implementation,
        )
    except Exception:
        return True, _blocked("failed_to_import_implementation_skeleton_placeholder_interfaces", trace=trace)

    try:
        trace["execution_chain_order"].append(
            "execution_state_real_write_placeholder_call_from_implementation"
        )
        r1 = write_first_live_execution_state_real_effect_from_implementation(
            context={"dry_run": True, "phase": "implementation_dry_run_execution_v0"}
        )
        trace["placeholder_call_results"]["execution_state_real_write"] = r1 if isinstance(r1, dict) else {"ok": False}

        trace["execution_chain_order"].append(
            "result_object_real_write_placeholder_call_from_implementation"
        )
        r2 = write_first_live_result_object_real_effect_from_implementation(
            context={"dry_run": True, "phase": "implementation_dry_run_execution_v0"}
        )
        trace["placeholder_call_results"]["result_object_real_write"] = r2 if isinstance(r2, dict) else {"ok": False}

        trace["execution_chain_order"].append(
            "failure_or_exception_real_write_placeholder_closure_from_implementation"
        )
        r3 = write_first_live_failure_or_exception_real_effect_from_implementation(
            reason="dry_run_placeholder_closure",
            context={"dry_run": True, "phase": "implementation_dry_run_execution_v0"},
        )
        trace["placeholder_call_results"]["failure_or_exception_real_write_closure"] = (
            r3 if isinstance(r3, dict) else {"ok": False}
        )
    except Exception:
        return True, _blocked("implementation_dry_run_execution_placeholder_call_exception", trace=trace)

    return True, _executed(
        "implementation_dry_run_executed_with_placeholder_only_and_side_effects_locked_in_v0",
        trace=trace,
    )

