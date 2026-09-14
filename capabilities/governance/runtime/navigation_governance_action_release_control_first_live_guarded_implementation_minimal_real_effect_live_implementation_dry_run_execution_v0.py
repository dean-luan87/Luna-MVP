# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Dry-Run Execution v0

定位：
- Phase-Next-120：在 live implementation wiring == wired_ready 的前提下，让 live implementation 第一次跑通
  “未来真实最小写入顺序的 runtime 干跑链（state -> result -> failure/exception closure）”，但保持零真实副作用。

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

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0"


def _blocked(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_scope": _SCOPE,
        "execution_status": "first_live_minimal_real_effect_live_dry_run_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_implementation_dry_run_execution_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["execution_trace"] = dict(trace)
    return out


def _not_ready(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_scope": _SCOPE,
        "execution_status": "first_live_minimal_real_effect_live_dry_run_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_implementation_dry_run_execution_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["execution_trace"] = dict(trace)
    return out


def _executed(reason: str, *, trace: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_scope": _SCOPE,
        "execution_status": "first_live_minimal_real_effect_live_dry_run_executed",
        "side_effects_released": False,
        "execution_trace": dict(trace),
        "reason": str(reason or "executed"),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_implementation_dry_run_execution_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0: Any,
    release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of wiring/state/result exist, returns (False, None).
    - Otherwise returns (True, attempted dry-run object with 3-state execution_status).

    Success chain (fixed order):
    - execution_state_placeholder_update_from_live_implementation
    - result_object_placeholder_update_from_live_implementation
    - failure_or_exception_placeholder_closure_from_live_implementation
    """
    lw = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0
    sk = release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0
    stub = release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0

    any_core_present = any(isinstance(x, dict) for x in [lw, xs, rs])
    if not any_core_present:
        return False, None

    trace: Dict[str, Any] = {"execution_chain_order": [], "placeholder_call_results": {}}

    if not isinstance(lw, dict):
        return True, _not_ready("missing_live_implementation_wiring_v0", trace=trace)
    if str(lw.get("wiring_status") or "") != "first_live_minimal_real_effect_live_wired_ready":
        return True, _not_ready("live_implementation_wiring_not_wired_ready", trace=trace)

    if not isinstance(sk, dict):
        return True, _blocked("missing_live_implementation_skeleton_identity_v0", trace=trace)
    if sk.get("is_skeleton") is not True or sk.get("is_live_implementation_skeleton") is not True:
        return True, _blocked("live_implementation_skeleton_identity_mismatch", trace=trace)
    if sk.get("can_open_side_effects_released") is not False:
        return True, _blocked("live_implementation_skeleton_identity_not_conservative:can_open_side_effects_released", trace=trace)

    if not isinstance(stub, dict):
        return True, _blocked("missing_live_implementation_stub_identity_v0", trace=trace)
    if stub.get("is_stub") is not True or stub.get("is_live_implementation_stub") is not True:
        return True, _blocked("live_implementation_stub_identity_mismatch", trace=trace)
    if stub.get("side_effects_released") is not False:
        return True, _blocked("live_implementation_stub_identity_not_conservative:side_effects_released", trace=trace)

    if not isinstance(xs, dict):
        return True, _not_ready("missing_execution_state_v0", trace=trace)
    if not isinstance(rs, dict):
        return True, _not_ready("missing_result_v0", trace=trace)

    # Dry-run placeholder calls: strictly call stub -> skeleton placeholder interfaces.
    try:
        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0 import (  # noqa: E402
            emit_live_execution_state_real_effect_placeholder_from_stub,
            emit_live_failure_or_exception_real_effect_placeholder_from_stub,
            emit_live_result_object_real_effect_placeholder_from_stub,
        )
    except Exception:
        return True, _blocked("failed_to_import_live_implementation_stub_placeholder_interfaces", trace=trace)

    try:
        trace["execution_chain_order"].append("execution_state_placeholder_update_from_live_implementation")
        r1 = emit_live_execution_state_real_effect_placeholder_from_stub(
            context={"dry_run": True, "phase": "live_implementation_dry_run_execution_v0"}
        )
        trace["placeholder_call_results"]["execution_state_placeholder"] = (
            r1 if isinstance(r1, dict) else {"ok": False}
        )

        trace["execution_chain_order"].append("result_object_placeholder_update_from_live_implementation")
        r2 = emit_live_result_object_real_effect_placeholder_from_stub(
            context={"dry_run": True, "phase": "live_implementation_dry_run_execution_v0"}
        )
        trace["placeholder_call_results"]["result_object_placeholder"] = (
            r2 if isinstance(r2, dict) else {"ok": False}
        )

        trace["execution_chain_order"].append(
            "failure_or_exception_placeholder_closure_from_live_implementation"
        )
        r3 = emit_live_failure_or_exception_real_effect_placeholder_from_stub(
            reason="dry_run_placeholder_closure",
            context={"dry_run": True, "phase": "live_implementation_dry_run_execution_v0"},
        )
        trace["placeholder_call_results"]["failure_or_exception_placeholder_closure"] = (
            r3 if isinstance(r3, dict) else {"ok": False}
        )
    except Exception:
        return True, _blocked("live_implementation_dry_run_execution_placeholder_call_exception", trace=trace)

    return True, _executed(
        "live_implementation_dry_run_executed_with_stub_skeleton_placeholders_only_and_side_effects_locked_in_v0",
        trace=trace,
    )

