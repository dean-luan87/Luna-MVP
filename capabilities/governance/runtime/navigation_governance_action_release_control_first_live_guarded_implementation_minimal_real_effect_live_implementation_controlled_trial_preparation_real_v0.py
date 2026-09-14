# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Code v0 (REAL, MINIMAL).

定位：
- Phase-Next-144：在所有 gate/implementation/dry-run 都在位后，
  第一次落“真实但极小”的 controlled trial preparation 启用代码。

硬边界（写死）：
- 不接入任何默认路径（显式调用入口）。
- 只允许三类真实副作用（通过注入 writer 实现）：
  1) execution_state_real_write
  2) result_object_real_write
  3) exception_or_failure_real_write
- 无显式 preparation real-code approval/signal 不得进入真实启用。
- side_effects_released != False 直接 fail-safe / blocked。
- 失败路径优先级高于成功路径：任一异常先恢复 side_effects_released=false，再按固定顺序收口写入。
- 禁止：route/voice/memory/migration/rollback/interrupt/map/path side-effect source/非标准对象吐散字段。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_real_v0"
_IDENTITY = _SCOPE

RealWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]
FailureWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass(frozen=True)
class ControlledTrialPreparationRealResult:
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


def get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_real_identity() -> Dict[str, Any]:
    return {
        "controlled_trial_preparation_real_identity": _IDENTITY,
        "controlled_trial_preparation_real_scope": _SCOPE,
        "is_controlled_trial_preparation_real": True,
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
        "default_enabled": False,
        "side_effects_released_default": False,
        "consume_mode": "controlled_trial_preparation_real_v0_explicit_only",
    }


def accept_first_live_minimal_real_effect_controlled_trial_preparation_real_input(
    *,
    controlled_trial_preparation_admission_gate_v0: Any,
    controlled_trial_preparation_dry_run_v0: Any,
    controlled_trial_go_no_go_gate_v0: Any,
    controlled_trial_first_minimal_real_enablement_v0: Any,
    preparation_real_approval_or_signal_v0: Any,
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
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="blocked",
            reason="side_effects_released_must_be_false_before_controlled_trial_preparation_real",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(controlled_trial_preparation_admission_gate_v0, dict) or str(
        controlled_trial_preparation_admission_gate_v0.get("controlled_trial_preparation_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_preparation_admitted":
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="controlled_trial_preparation_admission_gate_not_admitted_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(controlled_trial_preparation_dry_run_v0, dict) or str(
        controlled_trial_preparation_dry_run_v0.get("dry_run_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed":
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="controlled_trial_preparation_dry_run_not_executed_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(controlled_trial_go_no_go_gate_v0, dict) or str(
        controlled_trial_go_no_go_gate_v0.get("controlled_trial_go_no_go_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_go":
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="controlled_trial_go_no_go_gate_not_go_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(controlled_trial_first_minimal_real_enablement_v0, dict) or str(
        controlled_trial_first_minimal_real_enablement_v0.get("real_enablement_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_real_enablement_ready":
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="controlled_trial_first_minimal_real_enablement_not_ready_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(preparation_real_approval_or_signal_v0, dict):
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_preparation_real_approval_or_signal_v0",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(execution_state_v0, dict) or not isinstance(result_v0, dict) or not isinstance(
        exception_or_failure_path_v0, dict
    ):
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_execution_state_result_or_exception_path",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    return ControlledTrialPreparationRealResult(
        ok=True,
        result_scope=_SCOPE,
        status="ready",
        reason="controlled_trial_preparation_real_inputs_ready_but_not_executed",
        payload={"side_effects_released": False, "context": ctx},
    ).to_dict()


def perform_first_live_controlled_trial_preparation_recover_side_effects_false(
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


def perform_first_live_controlled_trial_preparation_execution_state_real_write(
    *, execution_state_writer: Optional[RealWriteFn], payload: Dict[str, Any]
) -> Dict[str, Any]:
    if not callable(execution_state_writer):
        raise RuntimeError("missing_execution_state_writer")
    return execution_state_writer(dict(payload))


def perform_first_live_controlled_trial_preparation_result_object_real_write(
    *, result_object_writer: Optional[RealWriteFn], payload: Dict[str, Any]
) -> Dict[str, Any]:
    if not callable(result_object_writer):
        raise RuntimeError("missing_result_object_writer")
    return result_object_writer(dict(payload))


def perform_first_live_controlled_trial_preparation_exception_or_failure_real_write(
    *, exception_or_failure_writer: Optional[FailureWriteFn], payload: Dict[str, Any]
) -> Dict[str, Any]:
    if not callable(exception_or_failure_writer):
        raise RuntimeError("missing_exception_or_failure_writer")
    return exception_or_failure_writer(dict(payload))


def run_first_live_controlled_trial_first_minimal_real_preparation_v0(
    *,
    controlled_trial_preparation_admission_gate_v0: Any,
    controlled_trial_preparation_dry_run_v0: Any,
    controlled_trial_go_no_go_gate_v0: Any,
    controlled_trial_first_minimal_real_enablement_v0: Any,
    preparation_real_approval_or_signal_v0: Any,
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
    第一版真实最小 controlled trial preparation 执行入口（显式调用；不接入默认路径）。
    - 正常路径：短时激活语义 -> 写 state -> 写 result -> 恢复 false
    - 异常路径：先恢复 false -> 写失败 state -> 写失败 result -> 写 exception/failure -> 交还
    """
    ctx = dict(context or {})
    trace: Dict[str, Any] = {"order": [], "writer_returns": {}, "recover": []}

    ready = accept_first_live_minimal_real_effect_controlled_trial_preparation_real_input(
        controlled_trial_preparation_admission_gate_v0=controlled_trial_preparation_admission_gate_v0,
        controlled_trial_preparation_dry_run_v0=controlled_trial_preparation_dry_run_v0,
        controlled_trial_go_no_go_gate_v0=controlled_trial_go_no_go_gate_v0,
        controlled_trial_first_minimal_real_enablement_v0=controlled_trial_first_minimal_real_enablement_v0,
        preparation_real_approval_or_signal_v0=preparation_real_approval_or_signal_v0,
        execution_state_v0=execution_state_v0,
        result_v0=result_v0,
        exception_or_failure_path_v0=exception_or_failure_path_v0,
        side_effects_released=side_effects_released,
        context=ctx,
    )
    if not bool(ready.get("ok")):
        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status=str(ready.get("status") or "not_ready"),
            reason=str(ready.get("reason") or "not_ready"),
            payload={"side_effects_released": False, "trace": trace, "context": ctx},
        ).to_dict()

    trace["order"].append("enter_controlled_short_activation_semantic")
    se = True  # local semantic only; MUST recover to False

    try:
        trace["order"].append("execution_state_real_write")
        r1 = perform_first_live_controlled_trial_preparation_execution_state_real_write(
            execution_state_writer=execution_state_writer,
            payload={"scope": _SCOPE, "surface": "execution_state_real_write", "context": ctx},
        )
        trace["writer_returns"]["execution_state_real_write"] = r1 if isinstance(r1, dict) else {"ok": False}

        trace["order"].append("result_object_real_write")
        r2 = perform_first_live_controlled_trial_preparation_result_object_real_write(
            result_object_writer=result_object_writer,
            payload={"scope": _SCOPE, "surface": "result_object_real_write", "context": ctx},
        )
        trace["writer_returns"]["result_object_real_write"] = r2 if isinstance(r2, dict) else {"ok": False}

        trace["order"].append("recover_side_effects_false_after_success")
        _, se, rec = perform_first_live_controlled_trial_preparation_recover_side_effects_false(
            reason="success_path_recover_false", side_effects_released=se, context=ctx
        )
        trace["recover"].append(rec)

        return ControlledTrialPreparationRealResult(
            ok=True,
            result_scope=_SCOPE,
            status="executed",
            reason="controlled_trial_preparation_first_minimal_real_writes_executed",
            payload={"side_effects_released": False, "trace": trace, "context": ctx},
        ).to_dict()

    except Exception as e:  # fail-safe: best-effort recover + closure writes
        trace["order"].append("exception_caught")
        trace["writer_returns"]["exception"] = {"type": type(e).__name__, "message": str(e)}

        trace["order"].append("recover_side_effects_false_on_failure")
        _, se, rec = perform_first_live_controlled_trial_preparation_recover_side_effects_false(
            reason="failure_path_recover_false", side_effects_released=se, context=ctx
        )
        trace["recover"].append(rec)

        # Best-effort closure writes (no expansion).
        try:
            trace["order"].append("failure_execution_state_real_write")
            r1f = perform_first_live_controlled_trial_preparation_execution_state_real_write(
                execution_state_writer=execution_state_writer,
                payload={"scope": _SCOPE, "surface": "execution_state_real_write", "kind": "failure", "context": ctx},
            )
            trace["writer_returns"]["failure_execution_state_real_write"] = (
                r1f if isinstance(r1f, dict) else {"ok": False}
            )
        except Exception as e2:
            trace["writer_returns"]["failure_execution_state_real_write_exception"] = {
                "type": type(e2).__name__,
                "message": str(e2),
            }

        try:
            trace["order"].append("failure_result_object_real_write")
            r2f = perform_first_live_controlled_trial_preparation_result_object_real_write(
                result_object_writer=result_object_writer,
                payload={"scope": _SCOPE, "surface": "result_object_real_write", "kind": "failure", "context": ctx},
            )
            trace["writer_returns"]["failure_result_object_real_write"] = (
                r2f if isinstance(r2f, dict) else {"ok": False}
            )
        except Exception as e3:
            trace["writer_returns"]["failure_result_object_real_write_exception"] = {
                "type": type(e3).__name__,
                "message": str(e3),
            }

        try:
            trace["order"].append("exception_or_failure_real_write")
            r3 = perform_first_live_controlled_trial_preparation_exception_or_failure_real_write(
                exception_or_failure_writer=exception_or_failure_writer,
                payload={
                    "scope": _SCOPE,
                    "surface": "exception_or_failure_real_write",
                    "exception_type": type(e).__name__,
                    "context": ctx,
                },
            )
            trace["writer_returns"]["exception_or_failure_real_write"] = r3 if isinstance(r3, dict) else {"ok": False}
        except Exception as e4:
            trace["writer_returns"]["exception_or_failure_real_write_exception"] = {
                "type": type(e4).__name__,
                "message": str(e4),
            }

        return ControlledTrialPreparationRealResult(
            ok=False,
            result_scope=_SCOPE,
            status="failed",
            reason="controlled_trial_preparation_real_execution_failed_fail_safe_closed",
            payload={"side_effects_released": False, "trace": trace, "context": ctx},
        ).to_dict()

