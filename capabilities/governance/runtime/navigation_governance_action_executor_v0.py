# -*- coding: utf-8 -*-
"""
Navigation Governance Action Executor v0 — Minimal Module Skeleton (NOT executable).

定位：
- 这是“治理动作执行器本体”的最小模块骨架（Phase-Next-33 skeleton）。
- 只提供身份与最小接口占位：输入接口、状态回传接口、异常上报接口。

硬边界（写死）：
- 不执行真实治理动作（no-op）。
- 不执行真实回退/中断/释放控制权动作。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不读取散字段；未来只接受“被批准的 action boundary”正式对象。
- 不伪装真实动作执行状态；只返回 placeholder / inactive / not_implemented 级别结果。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


GOVERNANCE_ACTION_EXECUTOR_IDENTITY_V0 = "navigation_governance_action_executor_v0"
GOVERNANCE_ACTION_BOUNDARY_SCOPE_V0 = "navigation_governance_action_boundary_v0"
GOVERNANCE_ACTION_APPROVAL_SCOPE_V0 = "navigation_governance_action_approval_boundary_v0"
GOVERNANCE_ACTION_STATUS_SCOPE_V0 = "navigation_governance_action_status_v0"
GOVERNANCE_ACTION_EXCEPTION_SCOPE_V0 = "navigation_governance_action_exception_v0"


@dataclass(frozen=True)
class GovernanceExecutorPlaceholderResult:
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


def get_governance_action_executor_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不做任何运行时接线、不读取外部状态）。
    """
    return {
        "governance_action_executor_identity": GOVERNANCE_ACTION_EXECUTOR_IDENTITY_V0,
        "governance_action_executor_scope": GOVERNANCE_ACTION_EXECUTOR_IDENTITY_V0,
        "is_skeleton": True,
        "can_execute_real_actions": False,
        "can_self_authorize_action": False,
        "consume_mode": "skeleton_placeholder",
    }


def accept_governance_action_boundary(*, approved_action_boundary_v0: Any) -> Dict[str, Any]:
    """
    输入接口占位（不消费、不执行）。

    未来约束（不在本轮实现）：
    - 只允许接受“被批准的 action boundary”正式对象（而不是 request_* 建议对象）
    - 不允许直接接受 entry/decision/散字段

    当前行为（写死）：
    - 不执行任何治理动作
    - 返回 not_implemented / inactive 级别占位结果
    """
    accepted = False
    scope = ""
    status = ""
    try:
        if isinstance(approved_action_boundary_v0, dict):
            scope = str(approved_action_boundary_v0.get("governance_action_boundary_scope") or "")
            status = str(approved_action_boundary_v0.get("governance_action_boundary_status") or "")
            accepted = scope == GOVERNANCE_ACTION_BOUNDARY_SCOPE_V0
    except Exception:
        accepted = False
        scope = ""
        status = ""

    return GovernanceExecutorPlaceholderResult(
        ok=False,
        result_scope=GOVERNANCE_ACTION_BOUNDARY_SCOPE_V0,
        status="not_implemented",
        reason="governance_action_executor_skeleton:boundary_input_placeholder:no_real_consumption",
        payload={
            "accepted": bool(accepted),
            "boundary_scope": str(scope),
            "boundary_status": str(status),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_governance_action_executor_input_object(
    *, navigation_governance_action_executor_input_v0: Any
) -> Dict[str, Any]:
    """
    正式输入对象识别接口（不执行治理动作）。

    当前行为（写死）：
    - 只识别 implemented input object（object_kind == implemented_v0）
    - 返回 not_implemented / recognize-only 级别结果
    """
    accepted = False
    kind = ""
    try:
        if isinstance(navigation_governance_action_executor_input_v0, dict):
            if (
                str(navigation_governance_action_executor_input_v0.get("governance_action_executor_input_scope") or "")
                == "navigation_governance_action_executor_input_v0"
            ):
                kind = str(navigation_governance_action_executor_input_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""

    return GovernanceExecutorPlaceholderResult(
        ok=False,
        result_scope="navigation_governance_action_executor_input_v0",
        status="not_implemented",
        reason="governance_action_executor_skeleton:input_object:recognize_only",
        payload={
            "accepted": bool(accepted),
            "input_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def emit_governance_action_status() -> Dict[str, Any]:
    """
    状态回传接口占位（不产真实动作执行态）。

    当前行为（写死）：
    - 不报告 action_executing/action_completed/action_failed 等真实态
    - 只返回 idle/inactive/placeholder 级别对象
    - 正式 implemented 状态对象由主链 metadata 组装（见 navigation_governance_action_status_v0）
    """
    return {
        "governance_action_status_present": True,
        "governance_action_status_scope": GOVERNANCE_ACTION_STATUS_SCOPE_V0,
        "executor_identity": GOVERNANCE_ACTION_EXECUTOR_IDENTITY_V0,
        "action_execution_state": "idle_placeholder",
        "action_last_result": "not_implemented_placeholder",
        "consume_mode": "skeleton_placeholder",
    }


def accept_governance_action_status_object(*, navigation_governance_action_status_v0: Any) -> Dict[str, Any]:
    """
    正式状态对象识别接口（不执行治理动作，不迁移状态）。

    当前行为（写死）：
    - 只识别 implemented status object（object_kind == implemented_v0）
    - 返回 not_implemented / recognize-only 级别结果
    """
    accepted = False
    kind = ""
    try:
        if isinstance(navigation_governance_action_status_v0, dict):
            if str(navigation_governance_action_status_v0.get("governance_action_status_scope") or "") == GOVERNANCE_ACTION_STATUS_SCOPE_V0:
                kind = str(navigation_governance_action_status_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""

    return GovernanceExecutorPlaceholderResult(
        ok=False,
        result_scope=GOVERNANCE_ACTION_STATUS_SCOPE_V0,
        status="not_implemented",
        reason="governance_action_executor_skeleton:status_object:recognize_only",
        payload={
            "accepted": bool(accepted),
            "status_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_governance_action_approval_boundary(*, navigation_governance_action_approval_boundary_v0: Any) -> Dict[str, Any]:
    """
    已批准治理动作边界对象识别接口（不执行治理动作）。

    当前行为（写死）：
    - 校验 scope + approval attempted + approval_status 属于允许集合（recognize-only）
    """
    accepted = False
    st = ""
    try:
        allowed = {
            "approved_hold_executor_state",
            "approved_interrupt",
            "approved_release_control",
            "approved_rollback",
            "approval_blocked",
        }
        if isinstance(navigation_governance_action_approval_boundary_v0, dict):
            if str(navigation_governance_action_approval_boundary_v0.get("governance_action_approval_scope") or "") == GOVERNANCE_ACTION_APPROVAL_SCOPE_V0:
                if navigation_governance_action_approval_boundary_v0.get("governance_action_approval_attempted") is True:
                    st = str(navigation_governance_action_approval_boundary_v0.get("governance_action_approval_status") or "")
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return GovernanceExecutorPlaceholderResult(
        ok=False,
        result_scope=GOVERNANCE_ACTION_APPROVAL_SCOPE_V0,
        status="not_implemented",
        reason="governance_action_executor_skeleton:approval_boundary:recognize_only",
        payload={
            "accepted": bool(accepted),
            "approval_status": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def wire_governance_action_executor(*, navigation_governance_action_executor_wiring_v0: Any) -> Dict[str, Any]:
    """
    Wiring recognition interface (non-action).

    Current behavior (frozen):
    - Recognizes implemented wiring scope + safe wiring statuses only
    - Returns recognize-only / not_implemented; never executes governance actions
    """
    accepted = False
    st = ""
    try:
        allowed = {"wired_inactive", "wired_action_ready"}
        if isinstance(navigation_governance_action_executor_wiring_v0, dict):
            if (
                str(navigation_governance_action_executor_wiring_v0.get("governance_action_executor_wiring_scope") or "")
                == "navigation_governance_action_executor_wiring_v0"
            ):
                if navigation_governance_action_executor_wiring_v0.get("governance_action_executor_wiring_attempted") is True:
                    st = str(
                        navigation_governance_action_executor_wiring_v0.get("governance_action_executor_wiring_status") or ""
                    )
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return GovernanceExecutorPlaceholderResult(
        ok=False,
        result_scope="navigation_governance_action_executor_wiring_v0",
        status="not_implemented",
        reason="governance_action_executor_skeleton:wiring:recognize_only",
        payload={
            "accepted": bool(accepted),
            "wiring_status": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def raise_governance_action_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    异常上报接口占位（不吞语义，不做真实处理）。

    当前行为（写死）：
    - 不抛出异常以驱动主链
    - 返回标准化异常占位对象，表达“异常被看见，但本模块不处理”
    """
    ctx = dict(context or {})
    return {
        "governance_action_exception_present": True,
        "governance_action_exception_scope": GOVERNANCE_ACTION_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "governance_action_executor_skeleton:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "skeleton_placeholder",
    }

