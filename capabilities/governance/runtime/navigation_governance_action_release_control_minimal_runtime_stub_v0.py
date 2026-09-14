# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Minimal Runtime Stub v0 (STUB; NOT executable).

定位：
- 这是 `release_control minimal runtime contract` 的代码承载位（Phase-Next-72）。
- 只占住 runtime 入口与回传顺序接口位：runtime 输入接口、execution state 更新接口、result 更新接口、异常接口。

硬边界（写死）：
- 不进入真实 runtime。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装 execution_started/execution_completed/result_completed 等真实事实；只返回 placeholder-safe / inactive / not_implemented。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_MINIMAL_RUNTIME_IDENTITY_V0 = "navigation_governance_action_release_control_minimal_runtime_stub_v0"
RELEASE_CONTROL_MINIMAL_RUNTIME_SCOPE_V0 = "navigation_governance_action_release_control_minimal_runtime_stub_v0"

RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"
RELEASE_CONTROL_RUNTIME_EXCEPTION_SCOPE_V0 = "navigation_governance_action_release_control_minimal_runtime_exception_v0"


@dataclass(frozen=True)
class ReleaseControlMinimalRuntimeStubResult:
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


def get_release_control_minimal_runtime_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不接线、不读取外部状态）。
    """
    return {
        "release_control_minimal_runtime_identity": RELEASE_CONTROL_MINIMAL_RUNTIME_IDENTITY_V0,
        "release_control_minimal_runtime_scope": RELEASE_CONTROL_MINIMAL_RUNTIME_SCOPE_V0,
        "is_stub": True,
        "can_enter_real_runtime": False,
        "can_execute_real_release_control": False,
        "consume_mode": "runtime_stub_placeholder",
    }


def accept_release_control_runtime_input(*, executor_input_bridge_v0: Any) -> Dict[str, Any]:
    """
    runtime 输入接口占位（不真实消费、不进入 runtime）。

    未来约束（不在本轮实现）：
    - 只接受 bridge_status==executor_input_bridge_ready 且 consumable_by_executor==true 的最终输入包
    """
    observed: Dict[str, Any] = {}
    try:
        if isinstance(executor_input_bridge_v0, dict):
            observed = {
                "bridge_scope": str(executor_input_bridge_v0.get("release_control_executor_input_bridge_scope") or ""),
                "bridge_status": str(executor_input_bridge_v0.get("bridge_status") or ""),
                "consumable_by_executor": bool(executor_input_bridge_v0.get("consumable_by_executor") is True),
            }
    except Exception:
        observed = {}

    return ReleaseControlMinimalRuntimeStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_MINIMAL_RUNTIME_SCOPE_V0,
        status="not_implemented",
        reason="release_control_minimal_runtime_stub:input_placeholder:no_runtime_entry",
        payload={
            "entered_runtime": False,
            "execute_attempted": False,
            "consume_mode": "runtime_stub_placeholder",
            "observed_bridge": dict(observed),
        },
    ).to_dict()


def emit_runtime_execution_state_update() -> Dict[str, Any]:
    """
    execution state 更新接口占位（不推进真实执行状态）。
    """
    return {
        "release_control_execution_state_present": True,
        "release_control_execution_state_scope": RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        "release_control_execution_state_fact": "not_started_safe",
        "consume_mode": "runtime_stub_placeholder",
    }


def emit_runtime_result_update() -> Dict[str, Any]:
    """
    result object 更新接口占位（不产出真实执行结果）。
    """
    return {
        "release_control_result_present": True,
        "release_control_result_scope": RELEASE_CONTROL_RESULT_SCOPE_V0,
        "release_control_result_state_fact": "not_executed_safe",
        "consume_mode": "runtime_stub_placeholder",
    }


def raise_runtime_execution_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    exception / failure path 占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_minimal_runtime_exception_present": True,
        "release_control_minimal_runtime_exception_scope": RELEASE_CONTROL_RUNTIME_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "release_control_minimal_runtime_stub:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "runtime_stub_placeholder",
    }

