# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Shadow Integration v0 (observe-only)

硬边界（写死）：
- 只追加 metadata shadow 对象；不改变主链输出。
- 不允许任何真实写入：三类写入通过 no-op writer 注入。
- side_effects_released 必须保持为 False（shadow 直接 blocked）。
- 默认不开：无显式 shadow_enable_signal_v0 则 not_ready。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"


def _shadow_payload(
    *,
    shadow_status: str,
    reason: str,
    would_have_entered_real_write: bool,
    would_have_written_execution_state: bool,
    would_have_written_result_object: bool,
    would_have_written_exception_or_failure: bool,
    live_implementation_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "shadow_attempted": True,
        "shadow_scope": _SCOPE,
        "shadow_status": str(shadow_status),
        "side_effects_released": False,
        "reason": str(reason or ""),
        "would_have_entered_real_write": bool(would_have_entered_real_write),
        "would_have_written_execution_state": bool(would_have_written_execution_state),
        "would_have_written_result_object": bool(would_have_written_result_object),
        "would_have_written_exception_or_failure": bool(would_have_written_exception_or_failure),
    }
    if isinstance(live_implementation_result, dict):
        out["live_implementation_result"] = dict(live_implementation_result)
    return out


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state shadow_status).
    """
    _ = context

    go_no_go = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0
    )
    cpd = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0
    )
    sig = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0
    )
    xs = navigation_governance_action_release_control_execution_state_v0
    rs = navigation_governance_action_release_control_result_v0
    ex = exception_or_failure_path_v0

    any_core_present = any(isinstance(x, dict) for x in [go_no_go, cpd, sig, xs, rs, ex])
    if not any_core_present:
        return False, None

    if side_effects_released is not False:
        return True, _shadow_payload(
            shadow_status="shadow_blocked",
            reason="side_effects_released_must_be_false_for_shadow",
            would_have_entered_real_write=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
            live_implementation_result={"blocked": True, "reason": "side_effects_released_not_false"},
        )

    if not isinstance(go_no_go, dict) or str(go_no_go.get("real_write_status") or "") != (
        "first_live_minimal_real_effect_real_write_go"
    ):
        return True, _shadow_payload(
            shadow_status="shadow_not_ready",
            reason="go_no_go_gate_not_go_or_missing",
            would_have_entered_real_write=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
        )

    if not isinstance(cpd, dict) or str(cpd.get("dry_run_status") or "") != (
        "first_live_minimal_real_effect_live_code_path_dry_run_executed"
    ):
        return True, _shadow_payload(
            shadow_status="shadow_not_ready",
            reason="live_code_path_dry_run_not_executed_or_missing",
            would_have_entered_real_write=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
        )

    if not isinstance(sig, dict):
        return True, _shadow_payload(
            shadow_status="shadow_not_ready",
            reason="missing_shadow_enable_signal_v0",
            would_have_entered_real_write=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
        )

    if not isinstance(xs, dict) or not isinstance(rs, dict) or not isinstance(ex, dict):
        return True, _shadow_payload(
            shadow_status="shadow_not_ready",
            reason="missing_execution_state_result_or_exception_path",
            would_have_entered_real_write=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
        )

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0 import (  # noqa: E402
        run_first_live_minimal_real_write_v0,
    )

    # no-op writers: return in-memory dict only; never touch any external surface.
    def _noop_execution_state_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"shadow_noop": True, "surface": "execution_state_real_write", "payload": dict(payload)}

    def _noop_result_object_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"shadow_noop": True, "surface": "result_object_real_write", "payload": dict(payload)}

    def _noop_exception_or_failure_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"shadow_noop": True, "surface": "exception_or_failure_real_write", "payload": dict(payload)}

    live_res = run_first_live_minimal_real_write_v0(
        real_write_go_no_go_gate_v0=go_no_go,
        live_code_path_dry_run_v0=cpd,
        real_write_approval_or_signal_v0=sig,
        execution_state_v0=xs,
        result_v0=rs,
        exception_or_failure_path_v0=ex,
        side_effects_released=False,
        execution_state_writer=_noop_execution_state_writer,
        result_object_writer=_noop_result_object_writer,
        exception_or_failure_writer=_noop_exception_or_failure_writer,
        context={"consume_mode": "shadow_observe_only", "shadow_scope": _SCOPE},
    )

    trace = {}
    if isinstance(live_res, dict):
        trace = dict((live_res.get("payload") or {}).get("trace") or {})
    order = trace.get("order") if isinstance(trace, dict) else None
    order_list = list(order) if isinstance(order, list) else []

    would_have_entered_real_write = "enter_controlled_short_activation_semantic" in order_list
    would_have_written_execution_state = "execution_state_real_write" in order_list
    would_have_written_result_object = "result_object_real_write" in order_list
    would_have_written_exception_or_failure = "exception_or_failure_real_write" in order_list

    ok = bool(isinstance(live_res, dict) and live_res.get("ok") is True)
    status = str(live_res.get("status") or "") if isinstance(live_res, dict) else ""
    reason = str(live_res.get("reason") or "") if isinstance(live_res, dict) else "unknown"

    if ok:
        return True, _shadow_payload(
            shadow_status="shadow_executed",
            reason="shadow_observe_only_executed_with_noop_writers",
            would_have_entered_real_write=would_have_entered_real_write,
            would_have_written_execution_state=would_have_written_execution_state,
            would_have_written_result_object=would_have_written_result_object,
            would_have_written_exception_or_failure=would_have_written_exception_or_failure,
            live_implementation_result=dict(live_res),
        )

    if status == "blocked":
        return True, _shadow_payload(
            shadow_status="shadow_blocked",
            reason=reason or "shadow_blocked",
            would_have_entered_real_write=would_have_entered_real_write,
            would_have_written_execution_state=would_have_written_execution_state,
            would_have_written_result_object=would_have_written_result_object,
            would_have_written_exception_or_failure=would_have_written_exception_or_failure,
            live_implementation_result=dict(live_res) if isinstance(live_res, dict) else None,
        )

    return True, _shadow_payload(
        shadow_status="shadow_not_ready",
        reason=reason or "shadow_not_ready",
        would_have_entered_real_write=would_have_entered_real_write,
        would_have_written_execution_state=would_have_written_execution_state,
        would_have_written_result_object=would_have_written_result_object,
        would_have_written_exception_or_failure=would_have_written_exception_or_failure,
        live_implementation_result=dict(live_res) if isinstance(live_res, dict) else None,
    )

