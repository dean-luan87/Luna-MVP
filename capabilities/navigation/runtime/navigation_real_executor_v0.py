# -*- coding: utf-8 -*-
"""
Navigation Real Executor v0 — Minimal Module Skeleton (NOT executable).

定位：
- 这是“真实导航执行器本体”的最小模块骨架（Step 1 skeleton）。
- 只提供身份与最小接口占位：输入接口、状态回传接口、异常上报接口。

硬边界（写死）：
- 不执行真实导航动作（no-op）。
- 不接管主链控制权。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不读取散字段；未来只接受标准化输入对象 `navigation_real_executor_input_v0` 的正式实现版。
- 不伪装真实运行状态；只返回 placeholder / inactive / not_implemented 级别结果。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


EXECUTOR_IDENTITY_V0 = "navigation_real_executor_v0"
EXECUTOR_INPUT_SCOPE_V0 = "navigation_real_executor_input_v0"
EXECUTOR_STATUS_SCOPE_V0 = "navigation_real_executor_status_v0"
EXECUTOR_EXCEPTION_SCOPE_V0 = "navigation_real_executor_exception_v0"


@dataclass(frozen=True)
class ExecutorPlaceholderResult:
    """
    极小占位返回对象（用于自测与最小接口收敛）。

    注意：
    - 不包含时间/空间字段
    - 不携带地图/坐标依赖
    - 只表达 placeholder / not_implemented 语义
    """

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


def get_executor_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不做任何运行时接线、不读取外部状态）。
    """
    return {
        "executor_identity": EXECUTOR_IDENTITY_V0,
        "executor_scope": EXECUTOR_IDENTITY_V0,
        "is_skeleton": True,
        "can_execute_real_actions": False,
        "consume_mode": "skeleton_placeholder",
    }


def accept_executor_input(*, navigation_real_executor_input_v0: Any) -> Dict[str, Any]:
    """
    输入接口占位（不消费、不执行）。

    未来约束（不在本轮实现）：
    - 只允许接受标准化输入对象 `navigation_real_executor_input_v0` 的正式实现版
    - 不允许直接接受 gate/stub/placeholder/散字段

    当前行为（写死）：
    - 不执行任何动作
    - 返回 not_implemented / inactive 级别占位结果
    """
    accepted = False
    kind = ""
    try:
        if isinstance(navigation_real_executor_input_v0, dict):
            if str(navigation_real_executor_input_v0.get("executor_input_scope") or "") == EXECUTOR_INPUT_SCOPE_V0:
                kind = str(navigation_real_executor_input_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""
    return ExecutorPlaceholderResult(
        ok=False,
        result_scope=EXECUTOR_INPUT_SCOPE_V0,
        status="not_implemented",
        reason="executor_skeleton:input_interface_placeholder:no_real_consumption",
        payload={
            "accepted": bool(accepted),
            "input_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def emit_executor_status() -> Dict[str, Any]:
    """
    状态回传接口占位（不产真实运行态）。

    当前行为（写死）：
    - 不报告 running/completed/failed/interrupted 等真实态
    - 只返回 inactive/placeholder 级别对象
    """
    return {
        "executor_status_present": True,
        "executor_status_scope": EXECUTOR_STATUS_SCOPE_V0,
        "takeover_state": "inactive_skeleton_placeholder",
        "execution_state": "not_started_placeholder",
        "anomaly_state": "unknown_placeholder",
        "executor_capability_state": "unknown_placeholder",
        "status_route_binding_ready": False,
        "consume_mode": "skeleton_placeholder",
    }


def accept_executor_status_object(*, navigation_real_executor_status_v0: Any) -> Dict[str, Any]:
    """
    状态对象识别接口（不驱动任何状态迁移，不伪装真实运行事实）。

    当前行为（写死）：
    - 只识别 implemented status object（object_kind == implemented_v0）
    - 返回 not_implemented / placeholder-safe
    """
    accepted = False
    kind = ""
    try:
        if isinstance(navigation_real_executor_status_v0, dict):
            if str(navigation_real_executor_status_v0.get("executor_status_scope") or "") == EXECUTOR_STATUS_SCOPE_V0:
                kind = str(navigation_real_executor_status_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""

    return ExecutorPlaceholderResult(
        ok=False,
        result_scope=EXECUTOR_STATUS_SCOPE_V0,
        status="not_implemented",
        reason="executor_skeleton:status_object_placeholder:recognize_only",
        payload={
            "accepted": bool(accepted),
            "status_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_execution_monitoring_status_object(*, navigation_execution_monitoring_status_v0: Any) -> Dict[str, Any]:
    """
    监控对象识别接口（不驱动任何治理动作，不伪装监控已运行）。

    当前行为（写死）：
    - 只识别 implemented monitoring status object（object_kind == implemented_v0）
    - 返回 not_implemented / placeholder-safe
    """
    accepted = False
    kind = ""
    scope = ""
    try:
        if isinstance(navigation_execution_monitoring_status_v0, dict):
            scope = str(navigation_execution_monitoring_status_v0.get("monitoring_status_scope") or "")
            if scope == "navigation_execution_monitoring_status_v0":
                kind = str(navigation_execution_monitoring_status_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""
        scope = ""

    return ExecutorPlaceholderResult(
        ok=False,
        result_scope="navigation_execution_monitoring_status_v0",
        status="not_implemented",
        reason="executor_skeleton:monitoring_object_placeholder:recognize_only",
        payload={
            "accepted": bool(accepted),
            "monitoring_object_kind": str(kind),
            "monitoring_object_scope": str(scope),
            "execute_attempted": False,
            "governance_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def wire_executor_takeover(*, wiring_status: str, wiring_reason: str = "") -> Dict[str, Any]:
    """
    接线接口（最小非动作实现）。

    约束（写死）：
    - 只允许把 skeleton 带入 wired_inactive / wired_ready_to_takeover
    - 禁止 active/running/executing
    - 不触发任何真实动作/治理
    """
    st = str(wiring_status or "").strip()
    if st not in ("wired_inactive", "wired_ready_to_takeover"):
        st = "wired_inactive"
    return ExecutorPlaceholderResult(
        ok=False,
        result_scope="navigation_executor_takeover_wiring_v0",
        status=st,
        reason=str(wiring_reason or "executor_skeleton:wiring:non_action"),
        payload={
            "wired": True,
            "wired_status": st,
            "execute_attempted": False,
            "governance_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def raise_executor_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    异常上报接口占位（不吞语义，不做真实处理）。

    当前行为（写死）：
    - 不抛出异常以驱动主链
    - 返回标准化异常占位对象，表达“异常被看见，但本模块不处理”
    """
    ctx = dict(context or {})
    # 不引入时间/空间；仅保留最小语义与调用方提供的上下文键值。
    return {
        "executor_exception_present": True,
        "executor_exception_scope": EXECUTOR_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "executor_skeleton:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "skeleton_placeholder",
    }

