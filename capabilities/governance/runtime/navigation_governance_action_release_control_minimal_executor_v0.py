# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Minimal Executor v0 (SKELETON; NOT executable).

定位：
- 这是 `release_control` 子动作未来“最小真实执行单元”的不可执行骨架（Phase-Next-68）。
- 只提供身份与最小接口占位：输入接口、execution state 回传接口、result object 回传接口、异常上报接口。

硬边界（写死）：
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装 execution_started/execution_completed 等真实执行事实；只返回 placeholder / inactive / not_implemented。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_MINIMAL_EXECUTOR_IDENTITY_V0 = "navigation_governance_action_release_control_minimal_executor_v0"
RELEASE_CONTROL_MINIMAL_EXECUTOR_SCOPE_V0 = "navigation_governance_action_release_control_minimal_executor_v0"

RELEASE_CONTROL_INPUT_SCOPE_V0 = "navigation_governance_action_release_control_input_v0"
RELEASE_CONTROL_READINESS_SCOPE_V0 = "navigation_governance_action_release_control_readiness_gate_v0"
RELEASE_CONTROL_WIRING_SCOPE_V0 = "navigation_governance_action_release_control_wiring_v0"
RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"
RELEASE_CONTROL_EXECUTION_EXCEPTION_SCOPE_V0 = "navigation_governance_action_release_control_execution_exception_v0"
RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_SCOPE_V0 = "navigation_governance_action_release_control_executor_input_bridge_v0"


@dataclass(frozen=True)
class ReleaseControlMinimalExecutorSkeletonResult:
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


def get_release_control_minimal_executor_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不接线、不读取外部状态）。
    """
    return {
        "release_control_minimal_executor_identity": RELEASE_CONTROL_MINIMAL_EXECUTOR_IDENTITY_V0,
        "release_control_minimal_executor_scope": RELEASE_CONTROL_MINIMAL_EXECUTOR_SCOPE_V0,
        "is_skeleton": True,
        "can_execute_real_release_control": False,
        "can_execute_real_actions": False,
        "consume_mode": "skeleton_placeholder",
    }


def accept_release_control_execution_input(
    *,
    navigation_governance_action_release_control_input_v0: Any,
    navigation_governance_action_release_control_readiness_gate_v0: Any,
    navigation_governance_action_release_control_wiring_v0: Any,
    navigation_governance_action_release_control_execution_state_v0: Any,
    navigation_governance_action_release_control_result_v0: Any,
) -> Dict[str, Any]:
    """
    输入接口占位（不消费、不执行）。

    未来约束（不在本轮实现）：
    - 只允许接受 implemented input object + readiness ready_candidate + wiring wired_* + execution_state/result 在位
    - 禁止直接消费 request_* / approved_* / raw metadata
    """
    kinds: Dict[str, str] = {}
    try:
        if isinstance(navigation_governance_action_release_control_input_v0, dict):
            kinds["input_object_kind"] = str(
                navigation_governance_action_release_control_input_v0.get("object_kind") or ""
            )
        if isinstance(navigation_governance_action_release_control_readiness_gate_v0, dict):
            kinds["readiness_status"] = str(
                navigation_governance_action_release_control_readiness_gate_v0.get(
                    "release_control_readiness_status"
                )
                or ""
            )
        if isinstance(navigation_governance_action_release_control_wiring_v0, dict):
            kinds["wiring_status"] = str(
                navigation_governance_action_release_control_wiring_v0.get("release_control_wiring_status") or ""
            )
        if isinstance(navigation_governance_action_release_control_execution_state_v0, dict):
            kinds["execution_state_kind"] = str(
                navigation_governance_action_release_control_execution_state_v0.get("object_kind") or ""
            )
        if isinstance(navigation_governance_action_release_control_result_v0, dict):
            kinds["result_object_kind"] = str(
                navigation_governance_action_release_control_result_v0.get("object_kind") or ""
            )
    except Exception:
        kinds = {}

    return ReleaseControlMinimalExecutorSkeletonResult(
        ok=False,
        result_scope=RELEASE_CONTROL_MINIMAL_EXECUTOR_SCOPE_V0,
        status="not_implemented",
        reason="release_control_minimal_executor_skeleton:input_placeholder:no_real_execution",
        payload={
            "accepted": False,
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
            "observed_kinds": dict(kinds),
        },
    ).to_dict()


def accept_release_control_executor_input_bridge(
    *, navigation_governance_action_release_control_executor_input_bridge_v0: Any
) -> Dict[str, Any]:
    """
    最终执行输入桥接对象识别接口（recognize-only；不执行 release_control）。

    当前行为（写死）：
    - 只识别 scope + attempted + bridge_status 属于允许集合（recognize-only）
    - 返回 not_implemented
    """
    accepted = False
    st = ""
    try:
        allowed = {
            "executor_input_bridge_ready",
            "executor_input_bridge_not_ready",
            "executor_input_bridge_blocked",
        }
        if isinstance(navigation_governance_action_release_control_executor_input_bridge_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_executor_input_bridge_v0.get(
                        "release_control_executor_input_bridge_scope"
                    )
                    or ""
                )
                == RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_SCOPE_V0
            ):
                if navigation_governance_action_release_control_executor_input_bridge_v0.get(
                    "release_control_executor_input_bridge_attempted"
                ) is True:
                    st = str(
                        navigation_governance_action_release_control_executor_input_bridge_v0.get(
                            "bridge_status"
                        )
                        or ""
                    )
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return ReleaseControlMinimalExecutorSkeletonResult(
        ok=False,
        result_scope=RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_SCOPE_V0,
        status="not_implemented",
        reason="release_control_minimal_executor_skeleton:executor_input_bridge:recognize_only",
        payload={
            "accepted": bool(accepted),
            "bridge_status": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def emit_release_control_execution_state() -> Dict[str, Any]:
    """
    execution state 回传接口占位（不生成真实执行态）。
    """
    return {
        "release_control_execution_state_present": True,
        "release_control_execution_state_scope": RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        "release_control_execution_state": "inactive_placeholder",
        "consume_mode": "skeleton_placeholder",
    }


def emit_release_control_result_object() -> Dict[str, Any]:
    """
    result object 回传接口占位（不生成真实结果态）。
    """
    return {
        "release_control_result_present": True,
        "release_control_result_scope": RELEASE_CONTROL_RESULT_SCOPE_V0,
        "release_control_result_state": "not_implemented_placeholder",
        "consume_mode": "skeleton_placeholder",
    }


def raise_release_control_execution_exception(
    *, exc: Any, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    异常上报接口占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_execution_exception_present": True,
        "release_control_execution_exception_scope": RELEASE_CONTROL_EXECUTION_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "release_control_minimal_executor_skeleton:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "skeleton_placeholder",
    }

