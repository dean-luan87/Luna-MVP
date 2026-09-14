# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control v0 (SKELETON; NOT executable).

定位：
- 这是治理动作执行器未来可调用的“release_control 子动作壳子”（Phase-Next-50）。
- 只提供身份与最小接口占位：输入接口、状态回传接口、异常上报接口。

硬边界（写死）：
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 只返回 placeholder / inactive / not_implemented 级别结果，不伪装 completed/failed 等真实执行态。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_ACTION_IDENTITY_V0 = "navigation_governance_action_release_control_v0"
RELEASE_CONTROL_ACTION_SCOPE_V0 = "navigation_governance_action_release_control_v0"
RELEASE_CONTROL_STATUS_SCOPE_V0 = "navigation_governance_action_release_control_status_v0"
RELEASE_CONTROL_EXCEPTION_SCOPE_V0 = "navigation_governance_action_release_control_exception_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"
RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"


@dataclass(frozen=True)
class ReleaseControlSkeletonResult:
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


def get_release_control_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不接线、不读取外部状态）。
    """
    return {
        "release_control_action_identity": RELEASE_CONTROL_ACTION_IDENTITY_V0,
        "release_control_action_scope": RELEASE_CONTROL_ACTION_SCOPE_V0,
        "is_skeleton": True,
        "can_execute_real_release_control": False,
        "can_execute_real_actions": False,
        "consume_mode": "skeleton_placeholder",
    }


def accept_release_control_input(*, release_control_input: Any) -> Dict[str, Any]:
    """
    输入接口占位（不消费、不执行）。

    未来约束（不在本轮实现）：
    - 只允许接受“已批准 + readiness + wiring 已成立”的标准化输入面
    - 禁止直接消费 request_release_control / 散字段
    """
    accepted = False
    kind = ""
    try:
        if isinstance(release_control_input, dict):
            kind = str(release_control_input.get("object_kind") or "")
            accepted = False  # skeleton 不接受任何“可执行”输入
    except Exception:
        accepted = False
        kind = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope=RELEASE_CONTROL_ACTION_SCOPE_V0,
        status="not_implemented",
        reason="release_control_skeleton:input_placeholder:no_real_consumption",
        payload={
            "accepted": bool(accepted),
            "input_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_release_control_input_object(
    *, navigation_governance_action_release_control_input_v0: Any
) -> Dict[str, Any]:
    """
    正式输入对象识别接口（不执行 release_control）。

    当前行为（写死）：
    - 只识别 implemented input object（object_kind == implemented_v0）
    - 返回 not_implemented / recognize-only 级别结果
    """
    accepted = False
    kind = ""
    try:
        if isinstance(navigation_governance_action_release_control_input_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_input_v0.get(
                        "release_control_input_scope"
                    )
                    or ""
                )
                == "navigation_governance_action_release_control_input_v0"
            ):
                kind = str(navigation_governance_action_release_control_input_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope="navigation_governance_action_release_control_input_v0",
        status="not_implemented",
        reason="release_control_skeleton:input_object:recognize_only",
        payload={
            "accepted": bool(accepted),
            "input_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_release_control_readiness_gate(
    *, navigation_governance_action_release_control_readiness_gate_v0: Any
) -> Dict[str, Any]:
    """
    子动作 readiness gate 识别接口（不执行 release_control）。

    当前行为（写死）：
    - 只识别 scope + attempted + status 属于允许集合（recognize-only）
    - 返回 not_implemented
    """
    accepted = False
    st = ""
    try:
        allowed = {"ready_candidate", "not_ready", "blocked"}
        if isinstance(navigation_governance_action_release_control_readiness_gate_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_readiness_gate_v0.get(
                        "release_control_readiness_scope"
                    )
                    or ""
                )
                == "navigation_governance_action_release_control_readiness_gate_v0"
            ):
                if navigation_governance_action_release_control_readiness_gate_v0.get(
                    "release_control_readiness_attempted"
                ) is True:
                    st = str(
                        navigation_governance_action_release_control_readiness_gate_v0.get(
                            "release_control_readiness_status"
                        )
                        or ""
                    )
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope="navigation_governance_action_release_control_readiness_gate_v0",
        status="not_implemented",
        reason="release_control_skeleton:readiness_gate:recognize_only",
        payload={
            "accepted": bool(accepted),
            "readiness_status": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def wire_release_control(
    *, navigation_governance_action_release_control_wiring_v0: Any
) -> Dict[str, Any]:
    """
    子动作 wiring 识别接口（不执行 release_control）。

    当前行为（写死）：
    - 只识别 scope + attempted + wiring_status 属于允许集合（recognize-only）
    - 返回 not_implemented
    """
    accepted = False
    st = ""
    try:
        allowed = {"wired_inactive", "wired_action_ready"}
        if isinstance(navigation_governance_action_release_control_wiring_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_wiring_v0.get(
                        "release_control_wiring_scope"
                    )
                    or ""
                )
                == "navigation_governance_action_release_control_wiring_v0"
            ):
                if (
                    navigation_governance_action_release_control_wiring_v0.get(
                        "release_control_wiring_attempted"
                    )
                    is True
                ):
                    st = str(
                        navigation_governance_action_release_control_wiring_v0.get(
                            "release_control_wiring_status"
                        )
                        or ""
                    )
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope="navigation_governance_action_release_control_wiring_v0",
        status="not_implemented",
        reason="release_control_skeleton:wiring:recognize_only",
        payload={
            "accepted": bool(accepted),
            "wiring_status": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_release_control_result_object(
    *, navigation_governance_action_release_control_result_v0: Any
) -> Dict[str, Any]:
    """
    正式结果对象识别接口（recognize-only；不执行 release_control）。

    当前行为（写死）：
    - 只识别 implemented result object（object_kind == implemented_v0）
    - 返回 not_implemented / recognize-only 级别结果
    """
    accepted = False
    kind = ""
    st = ""
    try:
        if isinstance(navigation_governance_action_release_control_result_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_result_v0.get(
                        "release_control_result_scope"
                    )
                    or ""
                )
                == RELEASE_CONTROL_RESULT_SCOPE_V0
            ):
                kind = str(navigation_governance_action_release_control_result_v0.get("object_kind") or "")
                accepted = kind == "implemented_v0"
                st = str(
                    (
                        navigation_governance_action_release_control_result_v0.get("result_state_class") or {}
                    ).get("release_control_result_state_fact")
                    or ""
                )
    except Exception:
        accepted = False
        kind = ""
        st = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope=RELEASE_CONTROL_RESULT_SCOPE_V0,
        status="not_implemented",
        reason="release_control_skeleton:result_object:recognize_only",
        payload={
            "accepted": bool(accepted),
            "result_object_kind": str(kind),
            "result_state_fact": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def accept_release_control_execution_state_object(
    *, navigation_governance_action_release_control_execution_state_v0: Any
) -> Dict[str, Any]:
    """
    正式 execution state 对象识别接口（recognize-only；不执行 release_control）。

    当前行为（写死）：
    - 只识别 implemented execution state object（object_kind == implemented_v0）
    - 返回 not_implemented / recognize-only 级别结果
    """
    accepted = False
    kind = ""
    st = ""
    try:
        if isinstance(navigation_governance_action_release_control_execution_state_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_execution_state_v0.get(
                        "release_control_execution_state_scope"
                    )
                    or ""
                )
                == RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0
            ):
                kind = str(
                    navigation_governance_action_release_control_execution_state_v0.get("object_kind") or ""
                )
                accepted = kind == "implemented_v0"
                st = str(
                    (
                        navigation_governance_action_release_control_execution_state_v0.get(
                            "execution_state_class"
                        )
                        or {}
                    ).get("release_control_execution_state_fact")
                    or ""
                )
    except Exception:
        accepted = False
        kind = ""
        st = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope=RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        status="not_implemented",
        reason="release_control_skeleton:execution_state_object:recognize_only",
        payload={
            "accepted": bool(accepted),
            "execution_state_object_kind": str(kind),
            "execution_state_fact": str(st),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def emit_release_control_status() -> Dict[str, Any]:
    """
    状态回传接口占位（不产真实动作执行态）。
    """
    return {
        "release_control_status_present": True,
        "release_control_status_scope": RELEASE_CONTROL_STATUS_SCOPE_V0,
        "release_control_action_identity": RELEASE_CONTROL_ACTION_IDENTITY_V0,
        "release_control_execution_state": "inactive_placeholder",
        "release_control_last_result": "not_implemented_placeholder",
        "consume_mode": "skeleton_placeholder",
    }


def accept_release_control_status_object(
    *, navigation_governance_action_release_control_status_v0: Any
) -> Dict[str, Any]:
    """
    正式状态对象识别接口（不执行 release_control）。

    当前行为（写死）：
    - 只识别 implemented status object（object_kind == implemented_v0）
    - 返回 not_implemented / recognize-only 级别结果
    """
    accepted = False
    kind = ""
    try:
        if isinstance(navigation_governance_action_release_control_status_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_status_v0.get(
                        "release_control_status_scope"
                    )
                    or ""
                )
                == "navigation_governance_action_release_control_status_v0"
            ):
                kind = str(
                    navigation_governance_action_release_control_status_v0.get("object_kind") or ""
                )
                accepted = kind == "implemented_v0"
    except Exception:
        accepted = False
        kind = ""

    return ReleaseControlSkeletonResult(
        ok=False,
        result_scope="navigation_governance_action_release_control_status_v0",
        status="not_implemented",
        reason="release_control_skeleton:status_object:recognize_only",
        payload={
            "accepted": bool(accepted),
            "status_object_kind": str(kind),
            "execute_attempted": False,
            "consume_mode": "skeleton_placeholder",
        },
    ).to_dict()


def raise_release_control_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    异常上报接口占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_exception_present": True,
        "release_control_exception_scope": RELEASE_CONTROL_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "release_control_skeleton:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "skeleton_placeholder",
    }

