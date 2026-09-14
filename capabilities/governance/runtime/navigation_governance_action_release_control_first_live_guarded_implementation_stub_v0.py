# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation Stub v0 (STUB; NOT executable).

定位：
- 这是 `first live guarded implementation definition` 的代码承载位（Phase-Next-85）。
- 目标：占住“可进入、可观测、但仍不放权”的最后一层演练承载位。

硬边界（写死）：
- 不把 side_effects_released 从 false 改成 true。
- 不进入真实 live implementation。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装真实执行已开始/已完成事实；只返回 guarded_stub_* / blocked / not_implemented / placeholder-safe。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_IDENTITY_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_stub_v0"
)
RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_stub_v0"
)

RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"

RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_EXCEPTION_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_stub_exception_v0"
)


@dataclass(frozen=True)
class ReleaseControlFirstLiveGuardedImplementationStubResult:
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


def get_release_control_first_live_guarded_implementation_identity() -> Dict[str, Any]:
    """
    固定身份（不接线、不读取外部状态）。
    """
    return {
        "release_control_first_live_guarded_implementation_stub_identity": RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_IDENTITY_V0,
        "release_control_first_live_guarded_implementation_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0,
        "is_stub": True,
        "can_enter_real_guarded_implementation": False,
        "can_open_side_effects_released": False,
        "can_execute_real_release_control": False,
        "consume_mode": "first_live_guarded_implementation_stub_placeholder",
    }


def accept_first_live_guarded_implementation_input(
    *,
    approval_gate_v0: Any,
    launch_dry_run_v0: Any,
    live_release_gate_v0: Any,
    side_effect_release_gate_v0: Any,
    guarded_live_stub_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    guarded_live_identity_v0: Any,
    minimal_executor_identity_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    入口接口占位：
- 只做最小前提识别与三态输出；不放权、不触发真实执行。
    """
    ctx = dict(context or {})

    # Conservative: blocked if guarded stub claims side_effects already released
    side_effects_locked = False
    candidate_entered = False
    try:
        if isinstance(guarded_live_stub_v0, dict) and isinstance(guarded_live_stub_v0.get("payload"), dict):
            payload = guarded_live_stub_v0.get("payload") or {}
            candidate_entered = payload.get("live_stub_entered") is True
            side_effects_locked = payload.get("side_effects_released") is False
    except Exception:
        candidate_entered = False
        side_effects_locked = False

    if not candidate_entered or not side_effects_locked:
        return ReleaseControlFirstLiveGuardedImplementationStubResult(
            ok=False,
            result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0,
            status="guarded_stub_blocked",
            reason="guarded_candidate_missing_or_side_effects_not_locked",
            payload={
                "side_effects_released": False,
                "candidate_entered": bool(candidate_entered),
                "side_effects_locked": bool(side_effects_locked),
                "entered_real_guarded_implementation": False,
                "execute_attempted": False,
                "context": ctx,
                "consume_mode": "first_live_guarded_implementation_stub_placeholder",
            },
        ).to_dict()

    # Minimal not-ready checks: required objects must be present and in expected states
    if not (isinstance(approval_gate_v0, dict) and str(approval_gate_v0.get("approval_status") or "") == "first_live_enablement_approved"):
        return _not_ready("approval_not_approved_or_missing", ctx)
    if not (isinstance(launch_dry_run_v0, dict) and str(launch_dry_run_v0.get("launch_status") or "") == "first_live_launch_dry_run_ready"):
        return _not_ready("launch_dry_run_not_ready_or_missing", ctx)
    if not (isinstance(live_release_gate_v0, dict) and str(live_release_gate_v0.get("live_release_status") or "") == "live_release_ready"):
        return _not_ready("live_release_gate_not_ready_or_missing", ctx)
    if not (isinstance(side_effect_release_gate_v0, dict) and str(side_effect_release_gate_v0.get("side_effect_release_status") or "") == "side_effect_release_ready"):
        return _not_ready("side_effect_release_gate_not_ready_or_missing", ctx)
    if not (isinstance(execution_state_v0, dict) and isinstance(result_v0, dict)):
        return _not_ready("execution_state_or_result_missing", ctx)
    if not (isinstance(guarded_live_identity_v0, dict) and guarded_live_identity_v0.get("can_enter_real_live_execution") is False):
        return _blocked("guarded_identity_not_conservative", ctx)
    if not (isinstance(minimal_executor_identity_v0, dict) and minimal_executor_identity_v0.get("can_execute_real_release_control") is False):
        return _blocked("executor_identity_not_conservative", ctx)

    # Preconditions satisfied => ready (still stub; do NOT enter real implementation)
    return ReleaseControlFirstLiveGuardedImplementationStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0,
        status="guarded_stub_ready",
        reason="guarded_stub_ready_but_no_real_implementation_in_v0",
        payload={
            "side_effects_released": False,
            "entered_real_guarded_implementation": False,
            "execute_attempted": False,
            "allowed_real_side_effects": [
                "execution_state_update",
                "result_object_update",
                "exception_path",
            ],
            "still_forbidden": [
                "route_change",
                "voice_output",
                "memory_write",
                "mid_platform_real_migration",
                "rollback",
                "interrupt",
            ],
            "upstream_evidence": {
                "approval_status": "first_live_enablement_approved",
                "launch_status": "first_live_launch_dry_run_ready",
                "live_release_status": "live_release_ready",
                "side_effect_release_status": "side_effect_release_ready",
                "guarded_candidate_entered": True,
                "guarded_side_effects_locked": True,
                "execution_state_present": True,
                "result_present": True,
            },
            "context": ctx,
            "consume_mode": "first_live_guarded_implementation_stub_placeholder",
        },
    ).to_dict()


def emit_guarded_execution_state_update() -> Dict[str, Any]:
    """
    execution state safe update 占位（不推进真实执行状态）。
    """
    return {
        "release_control_execution_state_present": True,
        "release_control_execution_state_scope": RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        "release_control_execution_state_fact": "guarded_stub_safe_no_progress",
        "side_effects_released": False,
        "consume_mode": "first_live_guarded_implementation_stub_placeholder",
    }


def emit_guarded_result_update() -> Dict[str, Any]:
    """
    result safe update 占位（不产出真实执行结果）。
    """
    return {
        "release_control_result_present": True,
        "release_control_result_scope": RELEASE_CONTROL_RESULT_SCOPE_V0,
        "release_control_result_state_fact": "guarded_stub_safe_no_result",
        "side_effects_released": False,
        "consume_mode": "first_live_guarded_implementation_stub_placeholder",
    }


def perform_guarded_stop_or_exit(*, reason: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    止损/退出接口占位（不修改任何开关；只回 stop-safe/exit-safe）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_implementation_stop_attempted": True,
        "release_control_first_live_guarded_implementation_stub_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0,
        "stop_status": "stop_safe_exit_safe_placeholder",
        "side_effects_released": False,
        "reason": str(reason or "unspecified"),
        "context": ctx,
        "consume_mode": "first_live_guarded_implementation_stub_placeholder",
    }


def raise_guarded_implementation_stub_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    异常接口占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_implementation_stub_exception_present": True,
        "release_control_first_live_guarded_implementation_stub_exception_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "guarded_implementation_stub:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_implementation_stub_placeholder",
    }


def _not_ready(reason: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
    return ReleaseControlFirstLiveGuardedImplementationStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0,
        status="guarded_stub_not_ready",
        reason=str(reason),
        payload={
            "side_effects_released": False,
            "entered_real_guarded_implementation": False,
            "execute_attempted": False,
            "context": dict(ctx),
            "consume_mode": "first_live_guarded_implementation_stub_placeholder",
        },
    ).to_dict()


def _blocked(reason: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
    return ReleaseControlFirstLiveGuardedImplementationStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_SCOPE_V0,
        status="guarded_stub_blocked",
        reason=str(reason),
        payload={
            "side_effects_released": False,
            "entered_real_guarded_implementation": False,
            "execute_attempted": False,
            "context": dict(ctx),
            "consume_mode": "first_live_guarded_implementation_stub_placeholder",
        },
    ).to_dict()

