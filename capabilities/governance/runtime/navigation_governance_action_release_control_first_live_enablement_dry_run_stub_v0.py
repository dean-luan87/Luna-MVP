# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Enablement Dry-Run Stub v0 (STUB; NOT executable).

定位：
- 这是 `first live enablement plan` 的代码演练承载位（Phase-Next-80）。
- 只演练：前提检查、灰度条件检查、回退顺序模拟；不放权、不改 side_effects_released。

硬边界（写死）：
- 不把 side_effects_released 从 false 改成 true。
- 不进入真实 live execution。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装启用成功事实；只返回 dry-run/blocked/not_implemented/placeholder-safe。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_ENABLEMENT_DRY_RUN_IDENTITY_V0 = (
    "navigation_governance_action_release_control_first_live_enablement_dry_run_stub_v0"
)
RELEASE_CONTROL_ENABLEMENT_DRY_RUN_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_enablement_dry_run_stub_v0"
)

RELEASE_CONTROL_ENABLEMENT_DRY_RUN_EXCEPTION_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_enablement_dry_run_exception_v0"
)


@dataclass(frozen=True)
class ReleaseControlFirstEnablementDryRunStubResult:
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


def get_release_control_first_live_enablement_dry_run_identity() -> Dict[str, Any]:
    """
    返回固定身份信息（不接线、不读取外部状态）。
    """
    return {
        "release_control_first_live_enablement_dry_run_identity": RELEASE_CONTROL_ENABLEMENT_DRY_RUN_IDENTITY_V0,
        "release_control_first_live_enablement_dry_run_scope": RELEASE_CONTROL_ENABLEMENT_DRY_RUN_SCOPE_V0,
        "is_stub": True,
        "can_open_side_effects_released": False,
        "can_execute_real_release_control": False,
        "consume_mode": "enablement_dry_run_stub_placeholder",
    }


def accept_enablement_dry_run_input(*, approval_signal: Any = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    enablement 输入接口占位（不真实消费、不改变任何开关）。
    """
    ctx = dict(context or {})
    return ReleaseControlFirstEnablementDryRunStubResult(
        ok=False,
        result_scope=RELEASE_CONTROL_ENABLEMENT_DRY_RUN_SCOPE_V0,
        status="not_implemented",
        reason="release_control_enablement_dry_run_stub:input_placeholder:no_enablement",
        payload={
            "approval_signal_present": approval_signal is not None,
            "side_effects_released": False,
            "enablement_attempted": False,
            "consume_mode": "enablement_dry_run_stub_placeholder",
            "context": ctx,
        },
    ).to_dict()


def evaluate_enablement_dry_run_preconditions(
    *,
    live_release_gate_v0: Any,
    side_effect_release_gate_v0: Any,
    guarded_live_stub_v0: Any,
    execution_state_v0: Any,
    result_v0: Any,
    approval_signal: Any = None,
) -> Dict[str, Any]:
    """
    前提检查接口占位（只回 dry-run 判定，不放权）。
    """
    # Conservative: if any required object missing => not_ready; identity/capability checks not performed in stub.
    required_present = all(
        isinstance(x, dict) for x in [live_release_gate_v0, side_effect_release_gate_v0, guarded_live_stub_v0, execution_state_v0, result_v0]
    )
    status = "enablement_dry_run_not_ready"
    reason = "missing_required_sources"
    if required_present:
        status = "enablement_dry_run_ready"
        reason = "dry_run_ready_but_side_effects_locked"

    return {
        "release_control_first_live_enablement_dry_run_attempted": True,
        "release_control_first_live_enablement_dry_run_scope": RELEASE_CONTROL_ENABLEMENT_DRY_RUN_SCOPE_V0,
        "dry_run_status": status,
        "side_effects_released": False,
        "approval_signal_present": approval_signal is not None,
        "reason": reason,
        "consume_mode": "enablement_dry_run_stub_placeholder",
        "hard_boundaries": {
            "side_effects_released_locked_false": True,
            "no_real_release_control": True,
            "no_route_change": True,
            "no_voice_or_memory_side_effects": True,
            "no_mid_platform_real_migration": True,
            "no_time_or_space_anchors": True,
        },
    }


def simulate_enablement_rollback_path(*, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    回退路径演练接口占位（不修改任何状态；只回“演练完成”占位）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_enablement_rollback_simulated": True,
        "release_control_first_live_enablement_dry_run_scope": RELEASE_CONTROL_ENABLEMENT_DRY_RUN_SCOPE_V0,
        "side_effects_released_restored": True,  # simulated
        "side_effects_released": False,
        "notes": "dry_run_stub_does_not_modify_runtime_flags",
        "context": ctx,
        "consume_mode": "enablement_dry_run_stub_placeholder",
    }


def raise_enablement_dry_run_exception(*, exc: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    异常/阻断接口占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_enablement_dry_run_exception_present": True,
        "release_control_first_live_enablement_dry_run_exception_scope": RELEASE_CONTROL_ENABLEMENT_DRY_RUN_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "release_control_enablement_dry_run_stub:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "context": ctx,
        "consume_mode": "enablement_dry_run_stub_placeholder",
    }


def accept_first_live_enablement_approval_gate(
    *,
    navigation_governance_action_release_control_first_live_enablement_approval_gate_v0: Any,
) -> Dict[str, Any]:
    """
    Recognize-only interface:
    - 接收 approval gate 对象（未来用于串联演练→批准→真实试运行线）。
    - 当前不触发任何动作；不改变 side_effects_released。
    """
    present = isinstance(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0,
        dict,
    )
    return {
        "release_control_first_live_enablement_dry_run_stub_accept_approval_gate_attempted": True,
        "release_control_first_live_enablement_dry_run_scope": RELEASE_CONTROL_ENABLEMENT_DRY_RUN_SCOPE_V0,
        "approval_gate_present": present,
        "side_effects_released": False,
        "reason": "recognize_only_no_side_effects",
        "consume_mode": "enablement_dry_run_stub_placeholder",
    }

