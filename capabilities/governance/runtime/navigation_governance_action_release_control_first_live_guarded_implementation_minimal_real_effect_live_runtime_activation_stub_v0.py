# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Minimal Runtime Activation Stub v0

定位：
- Phase-Next-121：为未来真实最小写入实现中的“短时受控激活 side_effects_released”占位。
- 当前只提供 runtime activation stub 的身份与 placeholder-safe 接口，不具备任何真实激活能力。

硬边界（写死）：
- 不把 side_effects_released 从 false 改成 true（不做真实激活）。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入时间/空间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装真实激活已发生事实；只返回 inactive / not_implemented / placeholder-safe。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_IDENTITY_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_v0"
)
RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_v0"
)


@dataclass(frozen=True)
class ReleaseControlFirstLiveGuardedMinimalRealEffectLiveRuntimeActivationStubResult:
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


def get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity() -> Dict[str, Any]:
    """
    固定身份（不接线、不读取外部状态）。
    """
    return {
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_stub_identity": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_IDENTITY_V0,
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_SCOPE_V0,
        "is_stub": True,
        "is_live_runtime_activation_stub": True,
        "side_effects_released": False,
        "can_open_side_effects_released": False,
        "activation_mode": "inactive_placeholder",
        "consume_mode": "first_live_guarded_minimal_real_effect_live_runtime_activation_stub_inactive",
    }


def accept_first_live_minimal_real_effect_runtime_activation_input(
    *,
    live_implementation_wiring_v0: Any,
    live_implementation_dry_run_execution_v0: Any,
    activation_contract_v0: Any,
    activation_gate_v0: Any,
    activation_dry_run_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    exception_or_failure_path_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    输入接口占位：当前不消费、不判断、不激活；只返回 placeholder-safe。
    """
    _ = (
        live_implementation_wiring_v0,
        live_implementation_dry_run_execution_v0,
        activation_contract_v0,
        activation_gate_v0,
        activation_dry_run_v0,
        execution_state_v0,
        result_v0,
        exception_or_failure_path_v0,
        side_effects_released,
    )
    ctx = dict(context or {})
    return ReleaseControlFirstLiveGuardedMinimalRealEffectLiveRuntimeActivationStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_SCOPE_V0,
        status="live_runtime_activation_stub_inactive",
        reason="live_runtime_activation_stub_v0:inactive_placeholder:no_real_activation",
        payload={
            "side_effects_released": False,
            "entered_activation": False,
            "exited_activation": False,
            "accepted": False,
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_live_runtime_activation_stub_inactive",
        },
    ).to_dict()


def enter_live_runtime_activation_placeholder(
    *, reason: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    进入受控短时激活态的占位接口（当前不激活）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_enter_attempted": True,
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_SCOPE_V0,
        "activation_enter_status": "inactive_placeholder",
        "side_effects_released": False,
        "reason": str(reason or "unspecified"),
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_live_runtime_activation_stub_inactive",
    }


def exit_live_runtime_activation_placeholder(
    *, reason: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    退出受控短时激活态并恢复 false 的占位接口（当前始终 false）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_exit_attempted": True,
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_SCOPE_V0,
        "activation_exit_status": "inactive_placeholder",
        "side_effects_released": False,
        "reason": str(reason or "unspecified"),
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_live_runtime_activation_stub_inactive",
    }


def raise_first_live_minimal_real_effect_runtime_activation_stub_exception(
    *, exc: Any, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    异常上报占位接口（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_stub_exception_present": True,
        "release_control_first_live_guarded_minimal_real_effect_live_runtime_activation_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_LIVE_RUNTIME_ACTIVATION_STUB_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_live_runtime_activation_stub_inactive",
    }

