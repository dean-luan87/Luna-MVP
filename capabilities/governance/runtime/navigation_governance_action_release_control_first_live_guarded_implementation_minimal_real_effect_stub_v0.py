# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation Minimal Real-Effect Stub v0
(STUB; NOT executable; NO real writes; NO side effects).

定位：
- 这是 Phase-Next-92：把 minimal real-effect plan 推进到“未来真实写入器壳子”的代码承载位。
- 目标：占住未来三类允许面（execution state / result object / exception&failure path）的真实写入接口位置，
  并明确未来调用顺序与收口点，但当前仍不具备任何真实写入能力。

硬边界（写死）：
- 不把 side_effects_released 从 false 改成 true。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装真实写入已发生事实；只返回 real_effect_stub_inactive / not_implemented / placeholder-safe。

参考（冻结标准）：
- minimal real-effect plan v0：
  docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PLAN_V0.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_IDENTITY_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0"
)
RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0"
)

RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"

RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_EXCEPTION_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_exception_v0"
)


@dataclass(frozen=True)
class ReleaseControlFirstLiveGuardedMinimalRealEffectStubResult:
    ok: bool
    result_scope: str
    status: str
    reason: str
    payload: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "ok": bool(self.ok),
            "result_scope": str(self.result_scope),
            "status": str(self.status),
            "reason": str(self.reason),
        }
        if self.payload is not None:
            d["payload"] = dict(self.payload)
        return d


def get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity() -> Dict[str, Any]:
    """
    固定身份（不接线、不读取外部状态）。
    """
    return {
        "release_control_first_live_guarded_minimal_real_effect_stub_identity": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_IDENTITY_V0,
        "release_control_first_live_guarded_minimal_real_effect_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_SCOPE_V0,
        "is_stub": True,
        "is_real_effect_stub": True,
        "can_open_side_effects_released": False,
        "can_execute_real_release_control": False,
        "can_real_write_execution_state": False,
        "can_real_write_result_object": False,
        "can_real_write_failure_or_exception": False,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }


def accept_first_live_guarded_minimal_real_effect_input(
    *,
    minimal_real_effect_plan_v0: Any,
    wiring_v0: Any,
    non_effect_execution_v0: Any,
    dry_effect_simulation_v0: Any,
    approval_gate_v0: Any,
    launch_dry_run_v0: Any,
    live_release_gate_v0: Any,
    side_effect_release_gate_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    real-effect 输入接口占位（不真实消费、不触发写入；永远 side_effects_released=false）。

    未来约束（不在本轮实现）：
    - 仅接受 minimal real-effect plan 的最小进入前提满足后的标准化输入面
    - 真实写入必须严格遵守：state -> result -> (failure path)
    """
    ctx = dict(context or {})
    return ReleaseControlFirstLiveGuardedMinimalRealEffectStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_SCOPE_V0,
        status="real_effect_stub_inactive",
        reason="minimal_real_effect_stub_v0:inactive_placeholder:no_real_consumption",
        payload={
            "side_effects_released": False,
            "accepted": False,
            "entered_real_effect_write": False,
            "execute_attempted": False,
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
        },
    ).to_dict()


def write_first_live_execution_state_real_effect(*, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    execution state real-write 接口占位（不写真实 state；placeholder-safe）。
    """
    ctx = dict(context or {})
    return {
        "release_control_execution_state_present": True,
        "release_control_execution_state_scope": RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        "release_control_execution_state_fact": "minimal_real_effect_stub_no_real_write",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }


def write_first_live_result_object_real_effect(*, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    result object real-write 接口占位（不写真实 result；placeholder-safe）。
    """
    ctx = dict(context or {})
    return {
        "release_control_result_present": True,
        "release_control_result_scope": RELEASE_CONTROL_RESULT_SCOPE_V0,
        "release_control_result_state_fact": "minimal_real_effect_stub_no_real_write",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }


def write_first_live_failure_or_exception_real_effect(
    *, reason: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    failure/exception real-write 接口占位（不写真实 failure path；只回 stop-safe/reported-placeholder）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_stub_failure_or_exception_attempted": True,
        "release_control_first_live_guarded_minimal_real_effect_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_SCOPE_V0,
        "failure_or_exception_status": "stop_safe_reported_placeholder",
        "side_effects_released": False,
        "reason": str(reason or "unspecified"),
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }


def raise_first_live_minimal_real_effect_stub_exception(
    *, exc: Any, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    异常上报接口占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_stub_exception_present": True,
        "release_control_first_live_guarded_minimal_real_effect_stub_exception_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_STUB_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "minimal_real_effect_stub_v0:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }


def accept_first_live_minimal_real_effect_wiring(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0: Any,
) -> Dict[str, Any]:
    """
    minimal real-effect non-effect wiring 的 recognize-only 接口（不消费、不执行、不触发真实写入）。

    当前行为（写死）：
    - 仅识别 wiring scope + attempted + wiring_status 属于允许集合
    - 仍返回 stub 非活跃态，不进入 real write
    """
    allowed = {
        "first_live_minimal_real_effect_wired_ready",
        "first_live_minimal_real_effect_wired_not_ready",
        "first_live_minimal_real_effect_wired_blocked",
    }
    w = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0
    ok_scope = False
    st = ""
    reason = ""
    try:
        if isinstance(w, dict):
            ok_scope = (
                str(w.get("release_control_first_live_guarded_implementation_minimal_real_effect_wiring_scope") or "")
                == "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"
            )
            st = str(w.get("wiring_status") or "")
            reason = str(w.get("reason") or "")
            if ok_scope and w.get("release_control_first_live_guarded_implementation_minimal_real_effect_wiring_attempted") is True and st in allowed:
                return {
                    "accepted": True,
                    "status": "minimal_real_effect_wiring_recognized",
                    "wiring_status": st,
                    "reason": reason or "minimal_real_effect_wiring_recognized_non_action",
                    "side_effects_released": False,
                    "entered_real_effect_write": False,
                    "consume_mode": "first_live_guarded_minimal_real_effect_stub_wiring_recognize_only",
                }
    except Exception:
        pass
    return {
        "accepted": False,
        "status": "real_effect_stub_inactive",
        "reason": "minimal_real_effect_stub_v0:wiring_recognize_only:not_accepted_or_invalid_payload",
        "side_effects_released": False,
        "entered_real_effect_write": False,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }


def accept_first_live_minimal_real_effect_dry_run_execution(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0: Any,
) -> Dict[str, Any]:
    """
    minimal real-effect dry-run execution 的 recognize-only 接口（不触发真实写入）。

    当前行为（写死）：
    - 仅识别 dry-run scope + attempted + execution_status 属于允许集合
    - 仍不进入 real write；side_effects_released 保持为 false
    """
    allowed = {
        "first_live_minimal_real_effect_dry_run_executed",
        "first_live_minimal_real_effect_dry_run_not_ready",
        "first_live_minimal_real_effect_dry_run_blocked",
    }
    ex = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0
    try:
        if isinstance(ex, dict):
            ok_scope = (
                str(
                    ex.get("release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_scope")
                    or ""
                )
                == "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0"
            )
            st = str(ex.get("execution_status") or "")
            r = str(ex.get("reason") or "")
            if (
                ok_scope
                and ex.get("release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_attempted")
                is True
                and st in allowed
            ):
                return {
                    "accepted": True,
                    "status": "minimal_real_effect_dry_run_recognized",
                    "execution_status": st,
                    "reason": r or "minimal_real_effect_dry_run_recognized_non_action",
                    "side_effects_released": False,
                    "entered_real_effect_write": False,
                    "consume_mode": "first_live_guarded_minimal_real_effect_stub_dry_run_recognize_only",
                }
    except Exception:
        pass
    return {
        "accepted": False,
        "status": "real_effect_stub_inactive",
        "reason": "minimal_real_effect_stub_v0:dry_run_recognize_only:not_accepted_or_invalid_payload",
        "side_effects_released": False,
        "entered_real_effect_write": False,
        "consume_mode": "first_live_guarded_minimal_real_effect_stub_inactive",
    }

