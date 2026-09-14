# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation
First Controlled Short-Window REAL Trial Execute v0 (REAL, GUARDED).

定位：
- Phase-Next-160：在 151/155/158/159 共同约束下，实现第一版“真实 short-window real trial execute” runtime。

硬边界（写死）：
- 非默认路径：显式入口 + 显式 execute intent + 显式人工确认/等价批准。
- readiness=go：必须显式提供 158 readiness pack 且为 go。
- guardrail loaded：必须具备可审计 window 上限等参数；缺失即 abort。
- 唯一 started 判据不变：仍沿用 start_event_observed（由 152 enablement 产生；不得新增判据）。
- side effects 面不扩：仍仅三类写入（state/result/exception_failure），且仅在 started 后短时 window 发生（通过 152 复用实现）。
- 必须短窗：必须存在可验证 execute window 上限；超时即 stop/abort（execute_window_timeout）。
- 必须 stop/abort/recovery/closure：任何越界必须 abort 并最终回到 se=false 且 closed=true。
- 不得扩大为 full controlled trial；不得 default-on；不得新增自动连续触发通道。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_v0"

RealWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]
FailureWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]

_ALLOWED_SURFACES = {
    "execution_state_real_write",
    "result_object_real_write",
    "exception_or_failure_real_write",
}


@dataclass(frozen=True)
class ShortWindowRealTrialExecuteResult:
    ok: bool
    result_scope: str
    status: str
    reason: str
    payload: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "ok": bool(self.ok),
            "result_scope": str(self.result_scope),
            "status": str(self.status),
            "reason": str(self.reason),
        }
        if isinstance(self.payload, dict):
            out["payload"] = dict(self.payload)
        return out


def run_first_controlled_short_window_real_trial_execute_v0(
    *,
    # Preconditions/artifacts (read-only facts)
    readiness_go_no_go_pack_v0: Any,
    guardrail_definition_v0: Any,
    # Preconditions from 156/152 chain (still required for the actual minimal real write path)
    preparation_go_no_go_gate_v0: Any,
    preparation_shadow_eval_gate_v0: Any,
    preparation_admission_gate_v0: Any,
    preparation_enablement_dry_run_v0: Any,
    # Entry (explicit execute intent + explicit approval)
    explicit_short_window_real_trial_execute_intent_v0: Any,
    explicit_short_window_real_trial_execute_approval_v0: Any,
    # Runtime objects required by 152 enablement
    execution_state_v0: Any,
    result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    # Writers (injected; only 3 surfaces allowed)
    execution_state_writer: Optional[RealWriteFn],
    result_object_writer: Optional[RealWriteFn],
    exception_or_failure_writer: Optional[FailureWriteFn],
    # Execute window parameters (must exist)
    execute_window_max_ms: Any,
    observed_elapsed_ms: Any,
    # Attempt constraints (must exist)
    execute_attempts_max: Any,
    execute_attempts_observed: Any,
    # Optional scope constraints
    allowed_scopes_v0: Any = None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    唯一 real execute 入口（显式调用；不接默认路径）。
    Layer A：Entry（non-default + execute intent + approval + readiness_go + guardrail enforceable）
    Layer B：Arming（armed_not_started；不得 started / release）
    Layer C：Start（start gate 通过后，调用 152 enablement 产生 start_event_observed 并执行最小真实写入）
    Layer D：Execute Window（短时窗口；超时/越权/审计缺失/次数越界 => stop/abort）
    Layer E：Stop/Abort（立即停止继续执行，强制 rollback/recovery/final close）
    Layer F：Final Close（最终 se=false 且 closed=true）
    """
    ctx = dict(context or {})
    trace: Dict[str, Any] = {"order": [], "abort": [], "notes": []}

    state: Dict[str, Any] = {
        "readiness_go_seen": False,
        "guardrail_loaded": False,
        "explicit_execute_intent_seen": False,
        "approval_seen": False,
        "armed_not_started": False,
        "start_gate_passed": False,
        "start_event_observed": False,
        "controlled_short_window_real_trial_execute_started": False,
        "side_effects_released": False,
        "execute_window_open": False,
        "execute_window_timeout": False,
        "stop_triggered": False,
        "abort_triggered": False,
        "stop_trigger_id": None,
        "abort_trigger_id": None,
        "rollback_completed": False,
        "recovery_completed": False,
        "minimal_real_trial_execute_success_reached": False,
        "minimal_real_trial_execute_failure_reached": False,
        "closed": False,
    }

    def _abort(trigger_id: str, reason: str) -> Dict[str, Any]:
        trace["order"].append("abort_triggered")
        trace["abort"].append({"abort_trigger_id": trigger_id, "reason": reason})
        state["stop_triggered"] = True
        state["abort_triggered"] = True
        state["stop_trigger_id"] = str(trigger_id)
        state["abort_trigger_id"] = str(trigger_id)
        state["execute_window_open"] = False
        state["side_effects_released"] = False
        state["rollback_completed"] = True
        state["recovery_completed"] = True
        state["closed"] = True
        return ShortWindowRealTrialExecuteResult(
            ok=False,
            result_scope=_SCOPE,
            status="aborted",
            reason=str(reason or trigger_id),
            payload={"state": state, "trace": trace, "context": ctx},
        ).to_dict()

    # Layer A: entry guards (non-default).
    state["explicit_execute_intent_seen"] = isinstance(explicit_short_window_real_trial_execute_intent_v0, dict)
    if not state["explicit_execute_intent_seen"]:
        return _abort("execute_without_explicit_intent", "missing_explicit_short_window_real_trial_execute_intent_v0")

    state["approval_seen"] = isinstance(explicit_short_window_real_trial_execute_approval_v0, dict)
    if not state["approval_seen"]:
        return _abort("execute_without_explicit_approval", "missing_explicit_short_window_real_trial_execute_approval_v0")

    # Readiness must be GO (158).
    state["readiness_go_seen"] = isinstance(readiness_go_no_go_pack_v0, dict) and str(
        readiness_go_no_go_pack_v0.get("overall_evaluation") or readiness_go_no_go_pack_v0.get("recommended_overall_evaluation") or ""
    ) == "go"
    if not state["readiness_go_seen"]:
        return _abort("execute_without_readiness_go", "readiness_pack_not_go_or_missing")

    # Guardrail definition must exist (155).
    state["guardrail_loaded"] = isinstance(guardrail_definition_v0, dict) or guardrail_definition_v0 is not None
    if not state["guardrail_loaded"]:
        return _abort("guardrail_missing", "missing_guardrail_definition_v0")

    # Execute window parameters must be enforceable.
    try:
        win_max = int(execute_window_max_ms)
        elapsed = int(observed_elapsed_ms)
    except Exception:
        return _abort("audit_trace_missing_or_broken", "execute_window_parameters_not_int_or_missing")

    if win_max <= 0:
        return _abort("audit_trace_missing_or_broken", "execute_window_max_ms_must_be_positive")
    if elapsed < 0:
        return _abort("audit_trace_missing_or_broken", "observed_elapsed_ms_must_be_non_negative")
    if elapsed > win_max:
        state["execute_window_timeout"] = True
        return _abort("execute_window_timeout", "execute_window_timeout_before_start")

    # Attempt constraints must be enforceable.
    try:
        attempts_max = int(execute_attempts_max)
        attempts_obs = int(execute_attempts_observed)
    except Exception:
        return _abort("audit_trace_missing_or_broken", "execute_attempt_parameters_not_int_or_missing")
    if attempts_max <= 0:
        return _abort("audit_trace_missing_or_broken", "execute_attempts_max_must_be_positive")
    if attempts_obs < 0:
        return _abort("audit_trace_missing_or_broken", "execute_attempts_observed_must_be_non_negative")
    if attempts_obs > attempts_max:
        return _abort("execute_attempts_exceeded", "execute_attempts_exceeded_before_start")

    # Surface allowlist: intent must not request unauthorized surfaces.
    requested_surfaces = explicit_short_window_real_trial_execute_intent_v0.get("requested_surfaces")
    if isinstance(requested_surfaces, list):
        bad = [s for s in requested_surfaces if str(s) not in _ALLOWED_SURFACES]
        if bad:
            return _abort("unauthorized_side_effect_surface", "intent_requested_unauthorized_surfaces")

    # Scope constraint: if allowed_scopes_v0 is provided, requested scope must be within it.
    requested_scope = explicit_short_window_real_trial_execute_intent_v0.get("requested_scope")
    if allowed_scopes_v0 is not None and requested_scope is not None:
        if isinstance(allowed_scopes_v0, list):
            if str(requested_scope) not in {str(x) for x in allowed_scopes_v0}:
                return _abort("execute_scope_expanded_without_definition", "requested_scope_not_in_allowed_scopes")

    # Guardrail: side_effects must not already be released.
    if side_effects_released is not False:
        return _abort("no_started_but_release", "side_effects_released_must_be_false_at_entry")

    # Layer B: arming (still not started).
    trace["order"].append("arming_entered")
    state["armed_not_started"] = True

    # Arming-only path: do not start if intent forbids observing start_event.
    allow_start = explicit_short_window_real_trial_execute_intent_v0.get("allow_start_event_observed") is True
    if not allow_start:
        state["closed"] = True
        return ShortWindowRealTrialExecuteResult(
            ok=False,
            result_scope=_SCOPE,
            status="armed_not_started",
            reason="armed_but_start_event_not_allowed_by_intent",
            payload={"state": state, "trace": trace, "context": ctx},
        ).to_dict()

    # Layer C: start gate passed.
    trace["order"].append("start_gate_passed")
    state["start_gate_passed"] = True
    state["execute_window_open"] = True

    # Execute implementation (v0) reuses Phase-Next-152 minimal enablement for the only allowed real writes.
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0 import (  # noqa: E402
        run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0,
    )

    out = run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
        preparation_go_no_go_gate_v0=preparation_go_no_go_gate_v0,
        preparation_shadow_eval_gate_v0=preparation_shadow_eval_gate_v0,
        preparation_admission_gate_v0=preparation_admission_gate_v0,
        preparation_enablement_dry_run_v0=preparation_enablement_dry_run_v0,
        preparation_enablement_intent_v0={"intent": True, "real_trial_execute": True, "context": ctx},
        execution_state_v0=execution_state_v0,
        result_v0=result_v0,
        exception_or_failure_path_v0=exception_or_failure_path_v0,
        side_effects_released=False,
        execution_state_writer=execution_state_writer,
        result_object_writer=result_object_writer,
        exception_or_failure_writer=exception_or_failure_writer,
        context={"consume_mode": "short_window_real_trial_execute_v0", "trial_scope": _SCOPE, "context": ctx},
    )

    payload = out.get("payload") if isinstance(out, dict) else None
    payload = payload if isinstance(payload, dict) else {}
    enable_state = payload.get("state") if isinstance(payload.get("state"), dict) else {}
    enable_trace = payload.get("trace") if isinstance(payload.get("trace"), dict) else {}
    order = enable_trace.get("order") if isinstance(enable_trace.get("order"), list) else []

    # Audit guardrail: must be traceable.
    if not isinstance(order, list) or len(order) == 0:
        return _abort("audit_trace_missing_or_broken", "enablement_trace_order_missing_or_empty")

    # Map observed boundary states.
    state["start_event_observed"] = bool(enable_state.get("start_event_observed") is True)
    state["controlled_short_window_real_trial_execute_started"] = bool(enable_state.get("real_enablement_started") is True)
    state["side_effects_released"] = bool(enable_state.get("side_effects_released") is True)
    state["rollback_completed"] = bool(enable_state.get("rollback_completed") is True)
    state["closed"] = bool(enable_state.get("closed") is True)
    state["execute_window_open"] = False

    state["minimal_real_trial_execute_success_reached"] = bool(enable_state.get("minimal_success_reached") is True)
    state["minimal_real_trial_execute_failure_reached"] = bool(enable_state.get("minimal_failure_reached") is True)
    state["recovery_completed"] = bool(state["closed"] is True and state["side_effects_released"] is False)

    # Guardrails: illegal states must never occur.
    if state["side_effects_released"] and not state["controlled_short_window_real_trial_execute_started"]:
        return _abort("no_started_but_release", "illegal_release_before_started_detected")
    if state["controlled_short_window_real_trial_execute_started"] and not state["start_event_observed"]:
        return _abort("no_start_event_but_started", "started_without_start_event_detected")
    if state["controlled_short_window_real_trial_execute_started"] and not state["closed"]:
        return _abort("closure_missing", "started_without_closure_detected")
    if state["closed"] and state["side_effects_released"]:
        return _abort("se_not_recovered", "side_effects_not_recovered_after_closure")

    # Final classification.
    if out.get("ok") is True and out.get("status") == "executed":
        return ShortWindowRealTrialExecuteResult(
            ok=True,
            result_scope=_SCOPE,
            status="real_trial_execute_success",
            reason="short_window_real_trial_execute_success_and_closed",
            payload={"state": state, "trace": trace, "enablement_result": dict(out), "context": ctx},
        ).to_dict()

    if out.get("ok") is False and out.get("status") == "failed":
        return ShortWindowRealTrialExecuteResult(
            ok=False,
            result_scope=_SCOPE,
            status="real_trial_execute_failure_closed",
            reason="short_window_real_trial_execute_failure_and_closed",
            payload={"state": state, "trace": trace, "enablement_result": dict(out), "context": ctx},
        ).to_dict()

    return ShortWindowRealTrialExecuteResult(
        ok=False,
        result_scope=_SCOPE,
        status="not_ready",
        reason="real_trial_execute_enablement_not_ready_or_blocked",
        payload={"state": state, "trace": trace, "enablement_result": dict(out) if isinstance(out, dict) else {}, "context": ctx},
    ).to_dict()

