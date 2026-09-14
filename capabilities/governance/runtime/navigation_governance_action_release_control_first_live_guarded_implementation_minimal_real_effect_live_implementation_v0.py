# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation v0 (First Minimal Real Write Code)

定位：
- Phase-Next-128（step2）：在所有边界冻结与干跑链闭合后，落第一版“真实但极小”的写入代码。
- 仅允许三类真实副作用（通过注入 writer 实现）：
  1) execution_state_real_write
  2) result_object_real_write
  3) exception_or_failure_real_write

硬边界（写死）：
- 不接入任何默认路径（本模块不在 dispatcher 中被默认调用）。
- 无显式 real-write approval/signal 不得进入真实写入。
- side_effects_released != False 时直接 fail-safe / blocked。
- 不允许 route / voice / memory / migration。
- 不允许 rollback / interrupt。
- 失败路径优先级高于成功路径：任一异常先恢复 side_effects_released=false，再按固定顺序收口写入。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple


_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0"

_IDENTITY = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0"
)


RealWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]
FailureWriteFn = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass(frozen=True)
class ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult:
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
        if self.payload is not None:
            out["payload"] = dict(self.payload)
        return out


def get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_identity() -> Dict[str, Any]:
    """
    固定身份（不接线、不读取外部状态）。
    """
    return {
        "release_control_first_live_guarded_minimal_real_effect_live_implementation_identity": _IDENTITY,
        "release_control_first_live_guarded_minimal_real_effect_live_implementation_scope": _SCOPE,
        "is_live_implementation": True,
        "is_first_minimal_real_write_code": True,
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
        "consume_mode": "first_live_guarded_minimal_real_effect_live_implementation_v0_explicit_only",
    }


def accept_first_live_minimal_real_effect_live_implementation_input(
    *,
    real_write_go_no_go_gate_v0: Any,
    live_code_path_dry_run_v0: Any,
    real_write_approval_or_signal_v0: Any,
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
        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status="blocked",
            reason="side_effects_released_must_be_false_before_real_write",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(real_write_go_no_go_gate_v0, dict) or str(
        real_write_go_no_go_gate_v0.get("real_write_status") or ""
    ) != "first_live_minimal_real_effect_real_write_go":
        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="go_no_go_gate_not_go_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(live_code_path_dry_run_v0, dict) or str(
        live_code_path_dry_run_v0.get("dry_run_status") or ""
    ) != "first_live_minimal_real_effect_live_code_path_dry_run_executed":
        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="live_code_path_dry_run_not_executed_or_missing",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(real_write_approval_or_signal_v0, dict):
        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_real_write_approval_or_signal_v0",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    if not isinstance(execution_state_v0, dict) or not isinstance(result_v0, dict) or not isinstance(
        exception_or_failure_path_v0, dict
    ):
        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_execution_state_result_or_exception_path",
            payload={"side_effects_released": False, "context": ctx},
        ).to_dict()

    return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
        ok=True,
        result_scope=_SCOPE,
        status="ready",
        reason="inputs_ready_for_first_minimal_real_write_code_but_not_executed",
        payload={"side_effects_released": False, "context": ctx},
    ).to_dict()


def perform_first_live_recover_side_effects_false(
    *, reason: str, side_effects_released: Any, context: Optional[Dict[str, Any]] = None
) -> Tuple[bool, bool, Dict[str, Any]]:
    """
    恢复 side_effects_released=false（语义层；不允许保留半开启）。
    Returns: (ok, new_side_effects_released, record)
    """
    ctx = dict(context or {})
    _ = side_effects_released
    return True, False, {
        "recover_attempted": True,
        "recover_status": "recovered_false",
        "reason": str(reason or "unspecified"),
        "side_effects_released": False,
        "context": ctx,
    }


def perform_first_live_execution_state_real_write(
    *,
    execution_state_writer: Optional[RealWriteFn],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    if not callable(execution_state_writer):
        raise RuntimeError("missing_execution_state_writer")
    return execution_state_writer(dict(payload))


def perform_first_live_result_object_real_write(
    *,
    result_object_writer: Optional[RealWriteFn],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    if not callable(result_object_writer):
        raise RuntimeError("missing_result_object_writer")
    return result_object_writer(dict(payload))


def perform_first_live_exception_or_failure_real_write(
    *,
    exception_or_failure_writer: Optional[FailureWriteFn],
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    if not callable(exception_or_failure_writer):
        raise RuntimeError("missing_exception_or_failure_writer")
    return exception_or_failure_writer(dict(payload))


def run_first_live_minimal_real_write_v0(
    *,
    real_write_go_no_go_gate_v0: Any,
    live_code_path_dry_run_v0: Any,
    real_write_approval_or_signal_v0: Any,
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
    第一版真实最小写入执行入口（显式调用；不接入默认路径）。
    - 正常路径：短时激活语义 -> 写 state -> 写 result -> 恢复 false
    - 异常路径：先恢复 false -> 写失败 state -> 写失败 result -> 写 exception/failure -> 交还
    """
    ctx = dict(context or {})
    trace: Dict[str, Any] = {"order": [], "writer_returns": {}, "recover": []}

    # Pre-check (no writes)
    ready = accept_first_live_minimal_real_effect_live_implementation_input(
        real_write_go_no_go_gate_v0=real_write_go_no_go_gate_v0,
        live_code_path_dry_run_v0=live_code_path_dry_run_v0,
        real_write_approval_or_signal_v0=real_write_approval_or_signal_v0,
        execution_state_v0=execution_state_v0,
        result_v0=result_v0,
        exception_or_failure_path_v0=exception_or_failure_path_v0,
        side_effects_released=side_effects_released,
        context=ctx,
    )
    if not bool(ready.get("ok")):
        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status=str(ready.get("status") or "not_ready"),
            reason=str(ready.get("reason") or "not_ready"),
            payload={"side_effects_released": False, "trace": trace, "context": ctx},
        ).to_dict()

    # Enter short-lived activation semantic (local only)
    trace["order"].append("enter_controlled_short_activation_semantic")
    se = True  # local semantic only; MUST recover to False

    try:
        trace["order"].append("execution_state_real_write")
        r1 = perform_first_live_execution_state_real_write(
            execution_state_writer=execution_state_writer,
            payload={"scope": _SCOPE, "surface": "execution_state_real_write", "context": ctx},
        )
        trace["writer_returns"]["execution_state_real_write"] = r1 if isinstance(r1, dict) else {"ok": False}

        trace["order"].append("result_object_real_write")
        r2 = perform_first_live_result_object_real_write(
            result_object_writer=result_object_writer,
            payload={"scope": _SCOPE, "surface": "result_object_real_write", "context": ctx},
        )
        trace["writer_returns"]["result_object_real_write"] = r2 if isinstance(r2, dict) else {"ok": False}

        # Normal completion: recover false
        trace["order"].append("recover_side_effects_false")
        ok_rec, se, rec = perform_first_live_recover_side_effects_false(
            reason="normal_path_recover", side_effects_released=se, context=ctx
        )
        trace["recover"].append(rec)
        if not ok_rec or se is not False:
            raise RuntimeError("failed_to_recover_side_effects_false_on_success")

        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=True,
            result_scope=_SCOPE,
            status="executed",
            reason="first_minimal_real_write_completed_within_allowed_surfaces_only",
            payload={"side_effects_released": False, "trace": trace, "context": ctx},
        ).to_dict()
    except Exception as e:
        # Failure path: recover false first
        trace["order"].append("failure_recover_side_effects_false_first")
        _, se, rec0 = perform_first_live_recover_side_effects_false(
            reason=f"failure_recover_first:{type(e).__name__}", side_effects_released=se, context=ctx
        )
        trace["recover"].append(rec0)
        se = False

        # Then attempt failure writes in fixed order (best-effort)
        try:
            trace["order"].append("failure_execution_state_real_write")
            rfs = perform_first_live_execution_state_real_write(
                execution_state_writer=execution_state_writer,
                payload={
                    "scope": _SCOPE,
                    "surface": "execution_state_real_write",
                    "mode": "failure",
                    "context": ctx,
                },
            )
            trace["writer_returns"]["failure_execution_state_real_write"] = (
                rfs if isinstance(rfs, dict) else {"ok": False}
            )
        except Exception as e2:
            trace["writer_returns"]["failure_execution_state_real_write"] = {
                "ok": False,
                "error": type(e2).__name__,
            }

        try:
            trace["order"].append("failure_result_object_real_write")
            rfr = perform_first_live_result_object_real_write(
                result_object_writer=result_object_writer,
                payload={
                    "scope": _SCOPE,
                    "surface": "result_object_real_write",
                    "mode": "failure",
                    "context": ctx,
                },
            )
            trace["writer_returns"]["failure_result_object_real_write"] = (
                rfr if isinstance(rfr, dict) else {"ok": False}
            )
        except Exception as e3:
            trace["writer_returns"]["failure_result_object_real_write"] = {"ok": False, "error": type(e3).__name__}

        try:
            trace["order"].append("exception_or_failure_real_write")
            rfe = perform_first_live_exception_or_failure_real_write(
                exception_or_failure_writer=exception_or_failure_writer,
                payload={
                    "scope": _SCOPE,
                    "surface": "exception_or_failure_real_write",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "context": ctx,
                },
            )
            trace["writer_returns"]["exception_or_failure_real_write"] = (
                rfe if isinstance(rfe, dict) else {"ok": False}
            )
        except Exception as e4:
            trace["writer_returns"]["exception_or_failure_real_write"] = {"ok": False, "error": type(e4).__name__}

        return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveImplementationResult(
            ok=False,
            result_scope=_SCOPE,
            status="failed",
            reason=f"first_minimal_real_write_failed:{type(e).__name__}",
            payload={"side_effects_released": False, "trace": trace, "context": ctx},
        ).to_dict()

