# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Code Path Dry-Run v0

定位：
- Phase-Next-125：在未来真实写入代码执行前，对 minimal code skeleton 的固定调用顺序做最后一次代码路径级零副作用演练。

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

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0"


def _blocked(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_scope": _SCOPE,
        "dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_code_path_dry_run_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["dry_run_trace"] = dict(trace)
    return out


def _not_ready(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_scope": _SCOPE,
        "dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_code_path_dry_run_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["dry_run_trace"] = dict(trace)
    return out


def _executed(reason: str, *, trace: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_scope": _SCOPE,
        "dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed",
        "side_effects_released": False,
        "dry_run_trace": dict(trace),
        "reason": str(reason or "executed"),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_code_path_dry_run_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state dry_run_status).

    Strict execution chain (fixed order):
    1) accept_first_live_minimal_real_effect_live_code_input
    2) perform_first_live_execution_state_real_write_placeholder
    3) perform_first_live_result_object_real_write_placeholder
    4) perform_first_live_exception_or_failure_real_write_placeholder
    5) perform_first_live_recover_side_effects_false_placeholder
    """
    lw = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0
    ldr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0
    act_stub = release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity_v0
    rp = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0
    gn = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0

    any_core_present = any(isinstance(x, dict) for x in [lw, ldr, rp, gn, xs, rs]) or act_stub is not None
    if not any_core_present and side_effects_released is None and exception_or_failure_path_v0 is None:
        return False, None

    trace: Dict[str, Any] = {"code_path_order": [], "placeholder_call_results": {}}

    # hard block: side_effects_released must remain false if present
    if side_effects_released is True:
        return True, _blocked("side_effects_released_true_is_not_allowed_in_live_code_path_dry_run_v0", trace=trace)
    if side_effects_released not in (None, False):
        return True, _blocked("side_effects_released_value_invalid_or_unsafe", trace=trace)

    if not isinstance(lw, dict) or str(lw.get("wiring_status") or "") != "first_live_minimal_real_effect_live_wired_ready":
        return True, _not_ready("live_implementation_wiring_not_wired_ready_or_missing", trace=trace)

    if not isinstance(ldr, dict) or str(ldr.get("execution_status") or "") != "first_live_minimal_real_effect_live_dry_run_executed":
        return True, _not_ready("live_implementation_dry_run_execution_not_executed_or_missing", trace=trace)

    if not isinstance(rp, dict):
        return True, _not_ready("missing_rollout_plan_v0", trace=trace)

    if not isinstance(gn, dict):
        return True, _not_ready("missing_go_no_go_gate_v0", trace=trace)
    if str(gn.get("real_write_status") or "") != "first_live_minimal_real_effect_real_write_go":
        return True, _not_ready("go_no_go_gate_not_go", trace=trace)

    if act_stub is None:
        return True, _not_ready("missing_live_runtime_activation_stub_identity_v0", trace=trace)

    if not isinstance(xs, dict) or not isinstance(rs, dict) or exception_or_failure_path_v0 is None:
        return True, _not_ready("missing_state_result_or_exception_path", trace=trace)

    try:
        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_skeleton_v0 import (  # noqa: E402
            accept_first_live_minimal_real_effect_live_code_input,
            perform_first_live_exception_or_failure_real_write_placeholder,
            perform_first_live_execution_state_real_write_placeholder,
            perform_first_live_recover_side_effects_false_placeholder,
            perform_first_live_result_object_real_write_placeholder,
        )
    except Exception:
        return True, _blocked("failed_to_import_live_code_skeleton_interfaces", trace=trace)

    try:
        trace["code_path_order"].append("accept_first_live_minimal_real_effect_live_code_input")
        r0 = accept_first_live_minimal_real_effect_live_code_input(
            real_write_go_no_go_gate_v0=gn,
            rollout_plan_v0=rp,
            live_implementation_wiring_v0=lw,
            live_implementation_dry_run_execution_v0=ldr,
            live_runtime_activation_stub_identity_v0=act_stub,
            execution_state_v0=xs,
            result_v0=rs,
            exception_or_failure_path_v0=exception_or_failure_path_v0,
            side_effects_released=side_effects_released,
            context={"dry_run": True, "phase": "live_code_path_dry_run_v0"},
        )
        trace["placeholder_call_results"]["accept_live_code_input"] = r0 if isinstance(r0, dict) else {"ok": False}

        trace["code_path_order"].append("perform_first_live_execution_state_real_write_placeholder")
        r1 = perform_first_live_execution_state_real_write_placeholder(
            context={"dry_run": True, "phase": "live_code_path_dry_run_v0"}
        )
        trace["placeholder_call_results"]["execution_state_write"] = r1 if isinstance(r1, dict) else {"ok": False}

        trace["code_path_order"].append("perform_first_live_result_object_real_write_placeholder")
        r2 = perform_first_live_result_object_real_write_placeholder(
            context={"dry_run": True, "phase": "live_code_path_dry_run_v0"}
        )
        trace["placeholder_call_results"]["result_write"] = r2 if isinstance(r2, dict) else {"ok": False}

        trace["code_path_order"].append("perform_first_live_exception_or_failure_real_write_placeholder")
        r3 = perform_first_live_exception_or_failure_real_write_placeholder(
            reason="dry_run_placeholder_exception_or_failure_write",
            context={"dry_run": True, "phase": "live_code_path_dry_run_v0"},
        )
        trace["placeholder_call_results"]["exception_or_failure_write"] = r3 if isinstance(r3, dict) else {"ok": False}

        trace["code_path_order"].append("perform_first_live_recover_side_effects_false_placeholder")
        r4 = perform_first_live_recover_side_effects_false_placeholder(
            reason="dry_run_recover_side_effects_false_placeholder",
            context={"dry_run": True, "phase": "live_code_path_dry_run_v0"},
        )
        trace["placeholder_call_results"]["recover_side_effects_false"] = r4 if isinstance(r4, dict) else {"ok": False}
    except Exception:
        return True, _blocked("live_code_path_dry_run_placeholder_call_exception", trace=trace)

    return True, _executed(
        "live_code_path_dry_run_executed_with_minimal_code_skeleton_placeholders_only_and_side_effects_locked_in_v0",
        trace=trace,
    )

