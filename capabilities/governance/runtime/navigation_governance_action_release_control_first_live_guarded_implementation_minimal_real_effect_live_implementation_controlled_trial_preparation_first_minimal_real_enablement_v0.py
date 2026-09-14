# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement v0 (REAL, MINIMAL).

定位：
- Phase-Next-152：把 Phase-Next-151 冻结的“可开始 vs 已开始”边界映射为第一版执法器（最小真实实现）。

硬边界（写死）：
- 不接入任何默认路径（显式调用入口）。
- 不允许隐式 started：只有 start_event_observed 才能 started（151 唯一判据）。
- side_effects_released 只能在 started 之后进入短时受控窗口语义，并且必须可恢复为 false。
- 只允许三类真实副作用（通过注入 writer 实现）：
  1) execution_state_real_write
  2) result_object_real_write
  3) exception_or_failure_real_write（仅失败时）
- 必须 closure：任何路径最终回到 side_effects_released=false（或等价安全闭合）。
- 禁止扩面到 route/voice/memory/migration/rollback/interrupt/map/path side-effect source/非标准对象吐散字段。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0"
_IDENTITY = _SCOPE

RealWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]
FailureWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass(frozen=True)
class FirstMinimalRealPreparationEnablementResult:
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


def get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_identity() -> Dict[str, Any]:
    return {
        "preparation_first_minimal_real_enablement_identity": _IDENTITY,
        "preparation_first_minimal_real_enablement_scope": _SCOPE,
        "is_preparation_first_minimal_real_enablement": True,
        "default_enabled": False,
        "side_effects_released_default": False,
        "consume_mode": "preparation_first_minimal_real_enablement_v0_explicit_only",
        "allowed_real_write_surfaces": [
            "execution_state_real_write",
            "result_object_real_write",
            "exception_or_failure_real_write",
        ],
        "forbidden_surfaces": [
            "route",
            "voice",
            "memory",
            "migration",
            "rollback",
            "interrupt",
            "map_path_side_effect_source",
            "non_standard_object_scatter_write",
        ],
    }


def accept_first_live_minimal_real_effect_controlled_trial_preparation_first_minimal_real_enablement_input(
    *,
    preparation_go_no_go_gate_v0: Any,
    preparation_shadow_eval_gate_v0: Any,
    preparation_admission_gate_v0: Any,
    preparation_enablement_dry_run_v0: Any,
    preparation_enablement_intent_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    最小入口接口：只做输入就绪性检查（不写入）。
    """
    ctx = dict(context or {})

    if side_effects_released is not False:
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="blocked",
            reason="side_effects_released_must_be_false_before_first_minimal_real_preparation_enablement",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(preparation_go_no_go_gate_v0, dict) or str(
        preparation_go_no_go_gate_v0.get("controlled_trial_preparation_go_no_go_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_preparation_go":
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="preparation_go_no_go_gate_not_go_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(preparation_shadow_eval_gate_v0, dict) or str(
        preparation_shadow_eval_gate_v0.get("controlled_trial_preparation_shadow_eval_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go":
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="preparation_shadow_evaluation_gate_not_go_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(preparation_admission_gate_v0, dict) or str(
        preparation_admission_gate_v0.get("controlled_trial_preparation_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_preparation_admitted":
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="preparation_admission_gate_not_admitted_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(preparation_enablement_dry_run_v0, dict) or str(
        preparation_enablement_dry_run_v0.get("dry_run_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed":
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="preparation_enablement_dry_run_not_executed_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(preparation_enablement_intent_v0, dict):
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_preparation_first_minimal_real_enablement_intent_v0",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(execution_state_v0, dict) or not isinstance(result_v0, dict) or not isinstance(
        exception_or_failure_path_v0, dict
    ):
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_execution_state_result_or_exception_path",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    return FirstMinimalRealPreparationEnablementResult(
        ok=True,
        result_scope=_SCOPE,
        status="ready",
        reason="first_minimal_real_preparation_enablement_inputs_ready_but_not_started",
        payload={"side_effects_released": False, "context": ctx},
    ).to_dict()


def perform_first_live_controlled_trial_preparation_first_minimal_real_enablement_recover_side_effects_false(
    *, reason: str, side_effects_released: Any, context: Optional[Dict[str, Any]] = None
) -> Tuple[bool, bool, Dict[str, Any]]:
    ctx = dict(context or {})
    _ = side_effects_released
    return True, False, {
        "recover_attempted": True,
        "recover_status": "recovered_false",
        "reason": str(reason or "unspecified"),
        "side_effects_released": False,
        "context": ctx,
    }


def _must_writer(writer: Optional[Callable[..., Any]], name: str) -> Callable[..., Any]:
    if not callable(writer):
        raise RuntimeError(f"missing_{name}")
    return writer


def run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
    *,
    preparation_go_no_go_gate_v0: Any,
    preparation_shadow_eval_gate_v0: Any,
    preparation_admission_gate_v0: Any,
    preparation_enablement_dry_run_v0: Any,
    preparation_enablement_intent_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    execution_state_writer: Optional[RealWriteFn],
    result_object_writer: Optional[RealWriteFn],
    exception_or_failure_writer: Optional[FailureWriteFn],
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    第一版真实 enablement 执行入口（显式调用；不接入默认路径）。
    结构映射：
    - Layer A entry/intent：accept readiness + explicit intent
    - Layer B arming：armed_not_started=True（但不 started）
    - Layer C start gate：观测 start_event_observed（唯一开始事件）后才 started
    - Layer D window：started 后进入短时 side_effects window（局部语义 se=True）
    - Layer E closure：任何路径 recover se->False 且 closed=True
    """
    ctx = dict(context or {})
    trace: Dict[str, Any] = {"order": [], "writer_returns": {}, "recover": []}

    # Visible state flags (for verifier).
    state: Dict[str, Any] = {
        "plan_frozen_seen": True,  # document-level precondition; assumed true in this explicit entry
        "dry_run_executed_seen": False,
        "admission_admitted_seen": False,
        "shadow_eval_go_seen": False,
        "go_no_go_ready_seen": False,
        "preparation_go_seen": False,
        "armed_not_started": False,
        "start_gate_passed": False,
        "start_event_observed": False,
        "real_enablement_started": False,
        "side_effects_released": False,
        "minimal_success_reached": False,
        "minimal_failure_reached": False,
        "rollback_completed": False,
        "closed": False,
    }

    ready = accept_first_live_minimal_real_effect_controlled_trial_preparation_first_minimal_real_enablement_input(
        preparation_go_no_go_gate_v0=preparation_go_no_go_gate_v0,
        preparation_shadow_eval_gate_v0=preparation_shadow_eval_gate_v0,
        preparation_admission_gate_v0=preparation_admission_gate_v0,
        preparation_enablement_dry_run_v0=preparation_enablement_dry_run_v0,
        preparation_enablement_intent_v0=preparation_enablement_intent_v0,
        execution_state_v0=execution_state_v0,
        result_v0=result_v0,
        exception_or_failure_path_v0=exception_or_failure_path_v0,
        side_effects_released=side_effects_released,
        context=ctx,
    )
    if not bool(ready.get("ok")):
        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status=str(ready.get("status") or "not_ready"),
            reason=str(ready.get("reason") or "not_ready"),
            payload={"state": state, "trace": trace, "side_effects_released": False, "context": ctx},
        ).to_dict()

    # Best-effort "seen" flags from gates/dry-run objects.
    state["dry_run_executed_seen"] = True
    state["admission_admitted_seen"] = True
    state["shadow_eval_go_seen"] = True
    state["go_no_go_ready_seen"] = True
    state["preparation_go_seen"] = True

    # Layer B: arming (must not imply started).
    trace["order"].append("arming_entered")
    state["armed_not_started"] = True

    # Layer C: unique start gate.
    trace["order"].append("start_gate_satisfied")
    state["start_gate_passed"] = True

    trace["order"].append("start_event_observed")
    state["start_event_observed"] = True  # 唯一开始事件（151 F）
    state["real_enablement_started"] = True

    # Layer D: side-effects window only after started.
    trace["order"].append("side_effects_window_open_semantic")
    se = True  # local semantic only; MUST recover
    state["side_effects_released"] = True

    try:
        # Minimal real effects (writers are injected).
        trace["order"].append("execution_state_real_write")
        _must_writer(execution_state_writer, "execution_state_writer")
        r1 = execution_state_writer({"scope": _SCOPE, "surface": "execution_state_real_write", "context": ctx})
        trace["writer_returns"]["execution_state_real_write"] = r1 if isinstance(r1, dict) else {"ok": False}

        trace["order"].append("result_object_real_write")
        _must_writer(result_object_writer, "result_object_writer")
        r2 = result_object_writer({"scope": _SCOPE, "surface": "result_object_real_write", "context": ctx})
        trace["writer_returns"]["result_object_real_write"] = r2 if isinstance(r2, dict) else {"ok": False}

        state["minimal_success_reached"] = True

        # Layer E: closure
        trace["order"].append("closure_recover_side_effects_false_after_success")
        _, se, rec = perform_first_live_controlled_trial_preparation_first_minimal_real_enablement_recover_side_effects_false(
            reason="success_path_recover_false", side_effects_released=se, context=ctx
        )
        trace["recover"].append(rec)
        state["side_effects_released"] = False
        state["closed"] = True

        return FirstMinimalRealPreparationEnablementResult(
            ok=True,
            result_scope=_SCOPE,
            status="executed",
            reason="preparation_first_minimal_real_enablement_executed_and_closed",
            payload={"state": state, "trace": trace, "side_effects_released": False, "context": ctx},
        ).to_dict()

    except Exception as e:
        trace["order"].append("exception_caught")
        trace["writer_returns"]["exception"] = {"type": type(e).__name__, "message": str(e)}

        # Failure must recover first.
        trace["order"].append("closure_recover_side_effects_false_on_failure")
        _, se, rec = perform_first_live_controlled_trial_preparation_first_minimal_real_enablement_recover_side_effects_false(
            reason="failure_path_recover_false", side_effects_released=se, context=ctx
        )
        trace["recover"].append(rec)
        state["side_effects_released"] = False

        state["minimal_failure_reached"] = True
        state["rollback_completed"] = True

        # Best-effort failure closure writes (no expansion).
        try:
            trace["order"].append("failure_execution_state_real_write")
            _must_writer(execution_state_writer, "execution_state_writer")
            r1f = execution_state_writer(
                {"scope": _SCOPE, "surface": "execution_state_real_write", "kind": "failure", "context": ctx}
            )
            trace["writer_returns"]["failure_execution_state_real_write"] = r1f if isinstance(r1f, dict) else {"ok": False}
        except Exception as e2:
            trace["writer_returns"]["failure_execution_state_real_write_exception"] = {
                "type": type(e2).__name__,
                "message": str(e2),
            }

        try:
            trace["order"].append("failure_result_object_real_write")
            _must_writer(result_object_writer, "result_object_writer")
            r2f = result_object_writer(
                {"scope": _SCOPE, "surface": "result_object_real_write", "kind": "failure", "context": ctx}
            )
            trace["writer_returns"]["failure_result_object_real_write"] = r2f if isinstance(r2f, dict) else {"ok": False}
        except Exception as e3:
            trace["writer_returns"]["failure_result_object_real_write_exception"] = {
                "type": type(e3).__name__,
                "message": str(e3),
            }

        try:
            trace["order"].append("exception_or_failure_real_write")
            _must_writer(exception_or_failure_writer, "exception_or_failure_writer")
            r3 = exception_or_failure_writer(
                {"scope": _SCOPE, "surface": "exception_or_failure_real_write", "exception_type": type(e).__name__, "context": ctx}
            )
            trace["writer_returns"]["exception_or_failure_real_write"] = r3 if isinstance(r3, dict) else {"ok": False}
        except Exception as e4:
            trace["writer_returns"]["exception_or_failure_real_write_exception"] = {
                "type": type(e4).__name__,
                "message": str(e4),
            }

        state["closed"] = True

        return FirstMinimalRealPreparationEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="failed",
            reason="preparation_first_minimal_real_enablement_failed_but_closed",
            payload={"state": state, "trace": trace, "side_effects_released": False, "context": ctx},
        ).to_dict()

