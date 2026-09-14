# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control Guarded Live Stub v0 (STUB; NOT executable).

定位：
- 这是 `minimal live execution definition` 之后、真实 live implementation 之前的“准 live 态”承载位（Phase-Next-74）。
- 允许识别并进入 live candidate，但默认 guardrail 仍压住所有真实 side effect。
- 只提供身份与最小接口占位：输入接口、execution state safe update、result safe update、blocked/failure path。

硬边界（写死）：
- 不进入真实 live execution。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装 execution_started/execution_completed/result_completed 等真实事实；只返回 guarded/blocked/not_implemented/placeholder-safe。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_GUARDED_LIVE_IDENTITY_V0 = "navigation_governance_action_release_control_guarded_live_stub_v0"
RELEASE_CONTROL_GUARDED_LIVE_SCOPE_V0 = "navigation_governance_action_release_control_guarded_live_stub_v0"

RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"
RELEASE_CONTROL_GUARDED_LIVE_EXCEPTION_SCOPE_V0 = "navigation_governance_action_release_control_guarded_live_exception_v0"
RELEASE_CONTROL_LIVE_RELEASE_GATE_SCOPE_V0 = "navigation_governance_action_release_control_live_release_gate_v0"
RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_SCOPE_V0 = (
    "navigation_governance_action_release_control_side_effect_release_gate_v0"
)


@dataclass(frozen=True)
class ReleaseControlGuardedLiveStubResult:
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


def get_release_control_guarded_live_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不接线、不读取外部状态）。
    """
    return {
        "release_control_guarded_live_identity": RELEASE_CONTROL_GUARDED_LIVE_IDENTITY_V0,
        "release_control_guarded_live_scope": RELEASE_CONTROL_GUARDED_LIVE_SCOPE_V0,
        "is_stub": True,
        "is_guarded_live_candidate": True,
        "can_enter_real_live_execution": False,
        "can_execute_real_release_control": False,
        "consume_mode": "guarded_live_stub_placeholder",
    }


def accept_guarded_live_input(*, executor_input_bridge_v0: Any) -> Dict[str, Any]:
    """
    live candidate 输入接口占位（不真实消费、不放行 side effect）。
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

    return ReleaseControlGuardedLiveStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_GUARDED_LIVE_SCOPE_V0,
        status="guarded_not_implemented",
        reason="release_control_guarded_live_stub:input_placeholder:guardrail_blocks_side_effects",
        payload={
            "live_stub_entered": True,
            "side_effects_released": False,
            "entered_real_live_execution": False,
            "execute_attempted": False,
            "consume_mode": "guarded_live_stub_placeholder",
            "observed_bridge": dict(observed),
        },
    ).to_dict()


def emit_guarded_execution_state_update() -> Dict[str, Any]:
    """
    execution state safe update 接口占位（不推进真实执行状态）。
    """
    return {
        "release_control_execution_state_present": True,
        "release_control_execution_state_scope": RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        "release_control_execution_state_fact": "guarded_not_started_safe",
        "consume_mode": "guarded_live_stub_placeholder",
    }


def emit_guarded_result_update() -> Dict[str, Any]:
    """
    result safe update 接口占位（不产出真实执行结果）。
    """
    return {
        "release_control_result_present": True,
        "release_control_result_scope": RELEASE_CONTROL_RESULT_SCOPE_V0,
        "release_control_result_state_fact": "guarded_not_executed_safe",
        "consume_mode": "guarded_live_stub_placeholder",
    }


def raise_guarded_live_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    blocked/failure path 占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_guarded_live_exception_present": True,
        "release_control_guarded_live_exception_scope": RELEASE_CONTROL_GUARDED_LIVE_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "release_control_guarded_live_stub:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "guarded_live_stub_placeholder",
    }


def accept_live_release_gate(
    *, navigation_governance_action_release_control_live_release_gate_v0: Any
) -> Dict[str, Any]:
    """
    live release gate 结果对象识别接口（recognize-only；不放行 side effect）。

    当前行为（写死）：
    - 只识别 scope + attempted + live_release_status 属于允许集合（recognize-only）
    - 返回 not_implemented
    """
    accepted = False
    st = ""
    try:
        allowed = {"live_release_ready", "live_release_not_ready", "live_release_blocked"}
        if isinstance(navigation_governance_action_release_control_live_release_gate_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_live_release_gate_v0.get(
                        "release_control_live_release_gate_scope"
                    )
                    or ""
                )
                == RELEASE_CONTROL_LIVE_RELEASE_GATE_SCOPE_V0
            ):
                if navigation_governance_action_release_control_live_release_gate_v0.get(
                    "release_control_live_release_gate_attempted"
                ) is True:
                    st = str(
                        navigation_governance_action_release_control_live_release_gate_v0.get(
                            "live_release_status"
                        )
                        or ""
                    )
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return ReleaseControlGuardedLiveStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_LIVE_RELEASE_GATE_SCOPE_V0,
        status="not_implemented",
        reason="release_control_guarded_live_stub:live_release_gate:recognize_only",
        payload={
            "accepted": bool(accepted),
            "live_release_status": str(st),
            "side_effects_released": False,
            "execute_attempted": False,
            "consume_mode": "guarded_live_stub_placeholder",
        },
    ).to_dict()


def accept_side_effect_release_gate(
    *, navigation_governance_action_release_control_side_effect_release_gate_v0: Any
) -> Dict[str, Any]:
    """
    side-effect release gate 结果对象识别接口（recognize-only；不放行 side effect）。

    当前行为（写死）：
    - 只识别 scope + attempted + side_effect_release_status 属于允许集合（recognize-only）
    - 返回 not_implemented
    """
    accepted = False
    st = ""
    try:
        allowed = {
            "side_effect_release_ready",
            "side_effect_release_not_ready",
            "side_effect_release_blocked",
        }
        if isinstance(navigation_governance_action_release_control_side_effect_release_gate_v0, dict):
            if (
                str(
                    navigation_governance_action_release_control_side_effect_release_gate_v0.get(
                        "release_control_side_effect_release_gate_scope"
                    )
                    or ""
                )
                == RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_SCOPE_V0
            ):
                if navigation_governance_action_release_control_side_effect_release_gate_v0.get(
                    "release_control_side_effect_release_gate_attempted"
                ) is True:
                    st = str(
                        navigation_governance_action_release_control_side_effect_release_gate_v0.get(
                            "side_effect_release_status"
                        )
                        or ""
                    )
                    accepted = st in allowed
    except Exception:
        accepted = False
        st = ""

    return ReleaseControlGuardedLiveStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_SCOPE_V0,
        status="not_implemented",
        reason="release_control_guarded_live_stub:side_effect_release_gate:recognize_only",
        payload={
            "accepted": bool(accepted),
            "side_effect_release_status": str(st),
            "side_effects_released": False,
            "execute_attempted": False,
            "consume_mode": "guarded_live_stub_placeholder",
        },
    ).to_dict()

