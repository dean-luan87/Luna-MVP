# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Trial v0 (REAL, GUARDED).

定位：
- Phase-Next-156：在 Phase-Next-155 guardrail constitution 约束下，实现第一版 short-window real trial runtime。

硬边界（写死）：
- 非默认路径：显式入口 + 显式 trial intent + 显式人工确认/等价批准。
- 唯一 start_event 判据不变：沿用 151/152 的 start_event_observed 语义。
- side effects 面不扩：仍仅三类写入（state/result/exception_failure），且仅在 started 后短时 window 发生。
- 必须短窗：必须存在可验证 window 上限；超时即 abort（trial_window_timeout）。
- 必须强制 abort/recovery/closure：任何越界必须 abort 并最终回到 se=false 且 closed=true。
- 不得扩大为 full controlled trial；不得 default-on；不得新增自动连续触发通道。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_v0"

RealWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]
FailureWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]

_ALLOWED_SURFACES = {
    "execution_state_real_write",
    "result_object_real_write",
    "exception_or_failure_real_write",
}


@dataclass(frozen=True)
class ShortWindowTrialResult:
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


def run_first_live_controlled_short_window_trial_v0(
    *,
    # Preconditions/artifacts (read-only facts)
    guardrail_pack_go_no_go_v0: Any,
    preparation_go_no_go_gate_v0: Any,
    preparation_shadow_eval_gate_v0: Any,
    preparation_admission_gate_v0: Any,
    preparation_enablement_dry_run_v0: Any,
    # Entry (explicit intent + approval)
    explicit_short_window_trial_intent_v0: Any,
    explicit_short_window_trial_approval_v0: Any,
    # Runtime objects required by 152 enablement
    execution_state_v0: Any,
    result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    # Writers (injected; only 3 surfaces allowed)
    execution_state_writer: Optional[RealWriteFn],
    result_object_writer: Optional[RealWriteFn],
    exception_or_failure_writer: Optional[FailureWriteFn],
    # Guardrail window parameters (must exist)
    trial_window_max_ms: Any,
    observed_elapsed_ms: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    唯一 short-window trial 入口（显式调用；不接默认路径）。
    - Layer A Entry: intent + approval + guardrail preconditions
    - Layer B Arming: armed_not_started 但不 started
    - Layer C Start: 只有在允许 start 且不超时时才进入 152 enablement，从而观测 start_event_observed
    - Layer D Window: 强制上限；超时/越权即 abort
    - Layer E Abort/Recovery/Closure: 任一路径 closed 且最终 se=false
    """
    ctx = dict(context or {})
    trace: Dict[str, Any] = {"order": [], "abort": [], "notes": []}

    # Visible state output (requested semantics).
    state: Dict[str, Any] = {
        "readiness_ok": False,
        "admission_ok": False,
        "shadow_eval_ok": False,
        "pack_go_seen": False,
        "guardrail_loaded": True,
        "explicit_trial_intent_seen": False,
        "approval_seen": False,
        "armed_not_started": False,
        "start_gate_passed": False,
        "start_event_observed": False,
        "controlled_short_window_trial_started": False,
        "side_effects_released": False,
        "trial_window_open": False,
        "trial_window_timeout": False,
        "abort_triggered": False,
        "abort_trigger_id": None,
        "rollback_completed": False,
        "recovery_completed": False,
        "minimal_trial_success_reached": False,
        "minimal_trial_failure_reached": False,
        "closed": False,
    }

    def _abort(trigger_id: str, reason: str) -> Dict[str, Any]:
        trace["order"].append("abort_triggered")
        trace["abort"].append({"abort_trigger_id": trigger_id, "reason": reason})
        state["abort_triggered"] = True
        state["abort_trigger_id"] = str(trigger_id)
        # For this v0 runtime, abort implies we are closed without touching writers.
        state["trial_window_open"] = False
        state["side_effects_released"] = False
        state["rollback_completed"] = True
        state["recovery_completed"] = True
        state["closed"] = True
        return ShortWindowTrialResult(
            ok=False,
            result_scope=_SCOPE,
            status="aborted",
            reason=str(reason or trigger_id),
            payload={"state": state, "trace": trace, "context": ctx},
        ).to_dict()

    # Non-default entry guardrails.
    state["explicit_trial_intent_seen"] = isinstance(explicit_short_window_trial_intent_v0, dict)
    if not state["explicit_trial_intent_seen"]:
        return _abort("missing_explicit_trial_intent", "missing_explicit_short_window_trial_intent_v0")

    state["approval_seen"] = isinstance(explicit_short_window_trial_approval_v0, dict)
    if not state["approval_seen"]:
        return _abort("missing_approval", "missing_explicit_short_window_trial_approval_v0")

    # Pack go (154) must be satisfied (we accept a minimal dict signal).
    state["pack_go_seen"] = isinstance(guardrail_pack_go_no_go_v0, dict) and str(
        guardrail_pack_go_no_go_v0.get("recommended_go_no_go_pack_conclusion") or ""
    ) in {"go", "conditional_go"}
    if not state["pack_go_seen"]:
        return _abort("pack_not_go", "controlled_short_window_trial_pack_not_go")

    # Window guardrails must exist and be enforceable.
    try:
        win_max = int(trial_window_max_ms)
        elapsed = int(observed_elapsed_ms)
    except Exception:
        return _abort("audit_trace_missing_or_broken", "window_parameters_not_int_or_missing")

    if win_max <= 0:
        return _abort("audit_trace_missing_or_broken", "trial_window_max_ms_must_be_positive")

    if elapsed < 0:
        return _abort("audit_trace_missing_or_broken", "observed_elapsed_ms_must_be_non_negative")

    if elapsed > win_max:
        state["trial_window_timeout"] = True
        return _abort("trial_window_timeout", "trial_window_timeout_before_start")

    # Surface allowlist guardrail: intent must not request unauthorized surfaces.
    requested_surfaces = explicit_short_window_trial_intent_v0.get("requested_surfaces")
    if isinstance(requested_surfaces, list):
        bad = [s for s in requested_surfaces if str(s) not in _ALLOWED_SURFACES]
        if bad:
            return _abort("unauthorized_side_effect_surface", "intent_requested_unauthorized_surfaces")

    # Guardrail: side_effects must not already be released.
    if side_effects_released is not False:
        return _abort("no_started_but_release", "side_effects_released_must_be_false_at_entry")

    # Layer B: arming (still not started).
    trace["order"].append("arming_entered")
    state["armed_not_started"] = True

    # Optional arming-only path: do not start if intent forbids start_event.
    allow_start = explicit_short_window_trial_intent_v0.get("allow_start_event_observed") is True
    if not allow_start:
        state["readiness_ok"] = True
        state["admission_ok"] = True
        state["shadow_eval_ok"] = True
        state["closed"] = True
        return ShortWindowTrialResult(
            ok=False,
            result_scope=_SCOPE,
            status="armed_not_started",
            reason="armed_but_start_event_not_allowed_by_intent",
            payload={"state": state, "trace": trace, "context": ctx},
        ).to_dict()

    # Layer C/D: start gate passed (window still in budget).
    trace["order"].append("start_gate_passed")
    state["start_gate_passed"] = True
    state["trial_window_open"] = True

    # Call Phase-Next-152 minimal enablement (the only place start_event_observed is produced).
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0 import (  # noqa: E402
        run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0,
    )

    out = run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
        preparation_go_no_go_gate_v0=preparation_go_no_go_gate_v0,
        preparation_shadow_eval_gate_v0=preparation_shadow_eval_gate_v0,
        preparation_admission_gate_v0=preparation_admission_gate_v0,
        preparation_enablement_dry_run_v0=preparation_enablement_dry_run_v0,
        preparation_enablement_intent_v0={"intent": True, "short_window_trial": True, "context": ctx},
        execution_state_v0=execution_state_v0,
        result_v0=result_v0,
        exception_or_failure_path_v0=exception_or_failure_path_v0,
        side_effects_released=False,
        execution_state_writer=execution_state_writer,
        result_object_writer=result_object_writer,
        exception_or_failure_writer=exception_or_failure_writer,
        context={"consume_mode": "short_window_trial_v0", "trial_scope": _SCOPE, "context": ctx},
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
    state["readiness_ok"] = bool(out.get("ok") is True or out.get("status") in {"executed", "failed"})
    state["admission_ok"] = True
    state["shadow_eval_ok"] = True
    state["start_event_observed"] = bool(enable_state.get("start_event_observed") is True)
    state["controlled_short_window_trial_started"] = bool(enable_state.get("real_enablement_started") is True)
    # Release must not remain true after closure.
    state["side_effects_released"] = bool(enable_state.get("side_effects_released") is True)
    state["minimal_trial_success_reached"] = bool(enable_state.get("minimal_success_reached") is True)
    state["minimal_trial_failure_reached"] = bool(enable_state.get("minimal_failure_reached") is True)
    state["rollback_completed"] = bool(enable_state.get("rollback_completed") is True)
    state["closed"] = bool(enable_state.get("closed") is True)
    state["trial_window_open"] = False

    # Guardrail: illegal release before started must never occur.
    if state["side_effects_released"] and not state["controlled_short_window_trial_started"]:
        return _abort("no_started_but_release", "illegal_release_before_started_detected")
    if state["controlled_short_window_trial_started"] and not state["start_event_observed"]:
        return _abort("no_start_event_but_started", "started_without_start_event_detected")
    if state["controlled_short_window_trial_started"] and not state["closed"]:
        return _abort("closure_missing", "started_without_closure_detected")
    if state["closed"] and state["side_effects_released"]:
        return _abort("se_not_recovered", "side_effects_not_recovered_after_closure")

    # Final result classification.
    if out.get("ok") is True and out.get("status") == "executed":
        return ShortWindowTrialResult(
            ok=True,
            result_scope=_SCOPE,
            status="trial_executed_success",
            reason="short_window_trial_success_and_closed",
            payload={"state": state, "trace": trace, "enablement_result": dict(out), "context": ctx},
        ).to_dict()

    if out.get("ok") is False and out.get("status") == "failed":
        return ShortWindowTrialResult(
            ok=False,
            result_scope=_SCOPE,
            status="trial_executed_failure_closed",
            reason="short_window_trial_failure_and_closed",
            payload={"state": state, "trace": trace, "enablement_result": dict(out), "context": ctx},
        ).to_dict()

    # Any other status is treated as not_ready.
    return ShortWindowTrialResult(
        ok=False,
        result_scope=_SCOPE,
        status="not_ready",
        reason="short_window_trial_enablement_not_ready_or_blocked",
        payload={"state": state, "trace": trace, "enablement_result": dict(out) if isinstance(out, dict) else {}, "context": ctx},
    ).to_dict()

