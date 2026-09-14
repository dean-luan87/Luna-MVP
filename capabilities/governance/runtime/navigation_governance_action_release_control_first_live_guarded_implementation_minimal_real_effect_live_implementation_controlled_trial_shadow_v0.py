# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Shadow Trial v0 (observe-only).

硬边界（写死）：
- 只追加 metadata shadow trial 对象；不改变主链输出。
- 不允许任何真实写入：三类写入通过 no-op writer 注入。
- side_effects_released 必须保持为 False（shadow 直接 blocked）。
- 默认不开：无显式 shadow_trial_enable_signal_v0 则 not_ready。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0"


def _shadow_payload(
    *,
    shadow_trial_status: str,
    reason: str,
    would_have_entered_real_trial_enablement: bool,
    would_have_written_execution_state: bool,
    would_have_written_result_object: bool,
    would_have_written_exception_or_failure: bool,
    live_trial_enablement_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "shadow_trial_attempted": True,
        "shadow_trial_scope": _SCOPE,
        "shadow_trial_status": str(shadow_trial_status),
        "side_effects_released": False,
        "reason": str(reason or ""),
        "would_have_entered_real_trial_enablement": bool(would_have_entered_real_trial_enablement),
        "would_have_written_execution_state": bool(would_have_written_execution_state),
        "would_have_written_result_object": bool(would_have_written_result_object),
        "would_have_written_exception_or_failure": bool(would_have_written_exception_or_failure),
    }
    if isinstance(live_trial_enablement_result, dict):
        out["live_trial_enablement_result"] = dict(live_trial_enablement_result)
    return out


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
    *,
    controlled_trial_go_no_go_gate_v0: Any,
    controlled_trial_enablement_dry_run_v0: Any,
    controlled_trial_first_minimal_real_enablement_v0: Any,
    shadow_trial_enable_signal_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state shadow_trial_status).
    """
    _ = context

    any_core_present = any(
        isinstance(x, dict)
        for x in [
            controlled_trial_go_no_go_gate_v0,
            controlled_trial_enablement_dry_run_v0,
            controlled_trial_first_minimal_real_enablement_v0,
            shadow_trial_enable_signal_v0,
            execution_state_v0,
            result_v0,
            exception_or_failure_path_v0,
        ]
    )
    if not any_core_present:
        return False, None

    if side_effects_released is not False:
        return True, _shadow_payload(
            shadow_trial_status="shadow_trial_blocked",
            reason="side_effects_released_must_be_false_for_shadow_trial",
            would_have_entered_real_trial_enablement=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
            live_trial_enablement_result={"blocked": True, "reason": "side_effects_released_not_false"},
        )

    if not isinstance(shadow_trial_enable_signal_v0, dict):
        return True, _shadow_payload(
            shadow_trial_status="shadow_trial_not_ready",
            reason="missing_shadow_trial_enable_signal_v0",
            would_have_entered_real_trial_enablement=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
        )

    if not isinstance(execution_state_v0, dict) or not isinstance(result_v0, dict) or not isinstance(
        exception_or_failure_path_v0, dict
    ):
        return True, _shadow_payload(
            shadow_trial_status="shadow_trial_not_ready",
            reason="missing_execution_state_result_or_exception_path",
            would_have_entered_real_trial_enablement=False,
            would_have_written_execution_state=False,
            would_have_written_result_object=False,
            would_have_written_exception_or_failure=False,
        )

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_real_enablement_v0 import (  # noqa: E402
        run_first_live_controlled_trial_first_minimal_real_enablement_v0,
    )

    def _noop_execution_state_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"shadow_noop": True, "surface": "execution_state_real_write", "payload": dict(payload)}

    def _noop_result_object_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"shadow_noop": True, "surface": "result_object_real_write", "payload": dict(payload)}

    def _noop_exception_or_failure_writer(payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"shadow_noop": True, "surface": "exception_or_failure_real_write", "payload": dict(payload)}

    live_res = run_first_live_controlled_trial_first_minimal_real_enablement_v0(
        controlled_trial_go_no_go_gate_v0=controlled_trial_go_no_go_gate_v0,
        controlled_trial_enablement_dry_run_v0=controlled_trial_enablement_dry_run_v0,
        controlled_trial_first_minimal_real_enablement_v0=controlled_trial_first_minimal_real_enablement_v0,
        real_enablement_approval_or_signal_v0=shadow_trial_enable_signal_v0,
        execution_state_v0=execution_state_v0,
        result_v0=result_v0,
        exception_or_failure_path_v0=exception_or_failure_path_v0,
        side_effects_released=False,
        execution_state_writer=_noop_execution_state_writer,
        result_object_writer=_noop_result_object_writer,
        exception_or_failure_writer=_noop_exception_or_failure_writer,
        context={"consume_mode": "controlled_trial_shadow_trial_observe_only", "shadow_scope": _SCOPE},
    )

    trace = {}
    if isinstance(live_res, dict):
        trace = dict((live_res.get("payload") or {}).get("trace") or {})
    order = trace.get("order") if isinstance(trace, dict) else None
    order_list = list(order) if isinstance(order, list) else []

    would_have_entered_real_trial_enablement = "enter_controlled_short_activation_semantic" in order_list
    would_have_written_execution_state = "execution_state_real_write" in order_list
    would_have_written_result_object = "result_object_real_write" in order_list
    would_have_written_exception_or_failure = "exception_or_failure_real_write" in order_list

    ok = bool(isinstance(live_res, dict) and live_res.get("ok") is True)
    status = str(live_res.get("status") or "") if isinstance(live_res, dict) else ""
    reason = str(live_res.get("reason") or "") if isinstance(live_res, dict) else "unknown"

    if ok:
        return True, _shadow_payload(
            shadow_trial_status="shadow_trial_executed",
            reason="shadow_trial_observe_only_executed_with_noop_writers",
            would_have_entered_real_trial_enablement=would_have_entered_real_trial_enablement,
            would_have_written_execution_state=would_have_written_execution_state,
            would_have_written_result_object=would_have_written_result_object,
            would_have_written_exception_or_failure=would_have_written_exception_or_failure,
            live_trial_enablement_result=dict(live_res),
        )

    if status == "blocked":
        return True, _shadow_payload(
            shadow_trial_status="shadow_trial_blocked",
            reason=reason or "shadow_trial_blocked",
            would_have_entered_real_trial_enablement=would_have_entered_real_trial_enablement,
            would_have_written_execution_state=would_have_written_execution_state,
            would_have_written_result_object=would_have_written_result_object,
            would_have_written_exception_or_failure=would_have_written_exception_or_failure,
            live_trial_enablement_result=dict(live_res) if isinstance(live_res, dict) else None,
        )

    return True, _shadow_payload(
        shadow_trial_status="shadow_trial_not_ready",
        reason=reason or "shadow_trial_not_ready",
        would_have_entered_real_trial_enablement=would_have_entered_real_trial_enablement,
        would_have_written_execution_state=would_have_written_execution_state,
        would_have_written_result_object=would_have_written_result_object,
        would_have_written_exception_or_failure=would_have_written_exception_or_failure,
        live_trial_enablement_result=dict(live_res) if isinstance(live_res, dict) else None,
    )

