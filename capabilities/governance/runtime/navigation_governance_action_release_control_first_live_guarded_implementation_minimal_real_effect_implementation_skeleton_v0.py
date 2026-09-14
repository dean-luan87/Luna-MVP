# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Implementation Skeleton v0

定位：
- Phase-Next-96：把 minimal real-effect implementation definition 对应的“未来真实写入实现壳子”先独立占出来。
- 本文件仅提供 skeleton 的身份与占位接口，不具备任何真实写入能力。

硬边界（写死）：
- 不把 side_effects_released 从 false 改成 true。
- 不执行真实 release_control。
- 不执行真实 rollback / interrupt。
- 不接地图、不引入坐标/时间锚点。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改 route/proposal。
- 不伪装真实写入已发生事实；只返回 implementation_skeleton_inactive / not_implemented / placeholder-safe。

参考（冻结标准）：
- implementation definition v0：
  docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_IDENTITY_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0"
)
RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0"
)

RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0 = "navigation_governance_action_release_control_execution_state_v0"
RELEASE_CONTROL_RESULT_SCOPE_V0 = "navigation_governance_action_release_control_result_v0"

RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_EXCEPTION_SCOPE_V0 = (
    "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_exception_v0"
)


@dataclass(frozen=True)
class ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult:
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


def get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity() -> Dict[str, Any]:
    """
    固定身份（不接线、不读取外部状态）。
    """
    return {
        "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_identity": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_IDENTITY_V0,
        "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        "is_skeleton": True,
        "is_real_effect_implementation_skeleton": True,
        "can_open_side_effects_released": False,
        "can_execute_real_release_control": False,
        "can_real_write_execution_state": False,
        "can_real_write_result_object": False,
        "can_real_write_failure_or_exception": False,
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
    }


def accept_first_live_minimal_real_effect_implementation_input(
    *,
    minimal_real_effect_implementation_definition_v0: Any,
    minimal_real_effect_plan_v0: Any,
    minimal_real_effect_wiring_v0: Any,
    minimal_real_effect_dry_run_execution_v0: Any,
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
    minimal real-effect implementation 输入接口占位（不真实消费、不触发写入；永远 side_effects_released=false）。

    未来约束（不在本轮实现）：
    - 仅接受 implementation definition 中写死的最小进入前提满足后的标准化输入面
    - 真实写入必须严格遵守：state -> result -> (failure/exception path) -> handoff
    """
    ctx = dict(context or {})
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=False,
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_inactive",
        reason="minimal_real_effect_implementation_skeleton_v0:inactive_placeholder:no_real_consumption",
        payload={
            "side_effects_released": False,
            "accepted": False,
            "entered_real_effect_write": False,
            "execute_attempted": False,
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_implementation_wiring(
    *,
    minimal_real_effect_implementation_wiring_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 implementation wiring 对象被接入，但不触发任何动作/写入。
    """
    ctx = dict(context or {})
    wiring_present = isinstance(minimal_real_effect_implementation_wiring_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(wiring_present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_wiring_recognized" if wiring_present else "implementation_skeleton_wiring_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:implementation_wiring_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(wiring_present),
            "wiring_scope": (
                str(minimal_real_effect_implementation_wiring_v0.get("release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_scope"))
                if wiring_present
                else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_implementation_dry_run_execution(
    *,
    minimal_real_effect_implementation_dry_run_execution_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 implementation dry-run execution 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_implementation_dry_run_execution_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_dry_run_execution_recognized" if present else "implementation_skeleton_dry_run_execution_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:implementation_dry_run_execution_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "execution_scope": (
                str(
                    minimal_real_effect_implementation_dry_run_execution_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_scope"
                    )
                )
                if present
                else ""
            ),
            "execution_status": (
                str(minimal_real_effect_implementation_dry_run_execution_v0.get("execution_status"))
                if present
                else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_admission_gate(
    *,
    minimal_real_effect_admission_gate_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 admission gate 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_admission_gate_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_admission_gate_recognized" if present else "implementation_skeleton_admission_gate_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:admission_gate_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "admission_scope": (
                str(
                    minimal_real_effect_admission_gate_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_scope"
                    )
                )
                if present
                else ""
            ),
            "admission_status": (
                str(minimal_real_effect_admission_gate_v0.get("admission_status")) if present else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_guarded_launch_dry_run(
    *,
    minimal_real_effect_guarded_launch_dry_run_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 guarded launch dry-run 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_guarded_launch_dry_run_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_guarded_launch_dry_run_recognized" if present else "implementation_skeleton_guarded_launch_dry_run_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:guarded_launch_dry_run_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "launch_scope": (
                str(
                    minimal_real_effect_guarded_launch_dry_run_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_scope"
                    )
                )
                if present
                else ""
            ),
            "launch_status": (
                str(minimal_real_effect_guarded_launch_dry_run_v0.get("launch_status")) if present else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_guarded_launch_gate(
    *,
    minimal_real_effect_guarded_launch_gate_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 guarded launch gate 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_guarded_launch_gate_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_guarded_launch_gate_recognized" if present else "implementation_skeleton_guarded_launch_gate_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:guarded_launch_gate_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "gate_scope": (
                str(
                    minimal_real_effect_guarded_launch_gate_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_scope"
                    )
                )
                if present
                else ""
            ),
            "launch_admission_status": (
                str(minimal_real_effect_guarded_launch_gate_v0.get("launch_admission_status"))
                if present
                else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_pre_commit_dry_run(
    *,
    minimal_real_effect_pre_commit_dry_run_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 pre-commit dry-run 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_pre_commit_dry_run_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_pre_commit_dry_run_recognized" if present else "implementation_skeleton_pre_commit_dry_run_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:pre_commit_dry_run_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "pre_commit_scope": (
                str(
                    minimal_real_effect_pre_commit_dry_run_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_scope"
                    )
                )
                if present
                else ""
            ),
            "pre_commit_status": (
                str(minimal_real_effect_pre_commit_dry_run_v0.get("pre_commit_status")) if present else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_commit_gate(
    *,
    minimal_real_effect_commit_gate_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 commit gate 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_commit_gate_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_commit_gate_recognized" if present else "implementation_skeleton_commit_gate_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:commit_gate_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "gate_scope": (
                str(
                    minimal_real_effect_commit_gate_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_scope"
                    )
                )
                if present
                else ""
            ),
            "commit_admission_status": (
                str(minimal_real_effect_commit_gate_v0.get("commit_admission_status")) if present else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_commit_dry_run(
    *,
    minimal_real_effect_commit_dry_run_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 commit dry-run 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_commit_dry_run_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_commit_dry_run_recognized"
        if present
        else "implementation_skeleton_commit_dry_run_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:commit_dry_run_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "dry_run_scope": (
                str(
                    minimal_real_effect_commit_dry_run_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_scope"
                    )
                )
                if present
                else ""
            ),
            "commit_dry_run_status": (
                str(minimal_real_effect_commit_dry_run_v0.get("commit_dry_run_status")) if present else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_activation_gate(
    *,
    minimal_real_effect_activation_gate_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 activation gate 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_activation_gate_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_activation_gate_recognized"
        if present
        else "implementation_skeleton_activation_gate_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:activation_gate_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "gate_scope": (
                str(
                    minimal_real_effect_activation_gate_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_scope"
                    )
                )
                if present
                else ""
            ),
            "activation_admission_status": (
                str(minimal_real_effect_activation_gate_v0.get("activation_admission_status"))
                if present
                else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def accept_first_live_minimal_real_effect_activation_dry_run(
    *,
    minimal_real_effect_activation_dry_run_v0: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    recognize-only：只承认 activation dry-run 对象被接入，不触发任何动作/写入。
    """
    ctx = dict(context or {})
    present = isinstance(minimal_real_effect_activation_dry_run_v0, dict)
    return ReleaseControlFirstLiveGuardedMinimalRealEffectImplementationSkeletonResult(
        ok=bool(present),
        result_scope=RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        status="implementation_skeleton_activation_dry_run_recognized"
        if present
        else "implementation_skeleton_activation_dry_run_missing",
        reason="minimal_real_effect_implementation_skeleton_v0:recognize_only:activation_dry_run_v0",
        payload={
            "side_effects_released": False,
            "recognized": bool(present),
            "dry_run_scope": (
                str(
                    minimal_real_effect_activation_dry_run_v0.get(
                        "release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_scope"
                    )
                )
                if present
                else ""
            ),
            "activation_dry_run_status": (
                str(minimal_real_effect_activation_dry_run_v0.get("activation_dry_run_status"))
                if present
                else ""
            ),
            "context": ctx,
            "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
        },
    ).to_dict()


def write_first_live_execution_state_real_effect_from_implementation(
    *, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    execution state real-write 接口占位（不写真实 state；placeholder-safe）。
    """
    ctx = dict(context or {})
    return {
        "release_control_execution_state_present": True,
        "release_control_execution_state_scope": RELEASE_CONTROL_EXECUTION_STATE_SCOPE_V0,
        "release_control_execution_state_fact": "minimal_real_effect_implementation_skeleton_no_real_write",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
    }


def write_first_live_result_object_real_effect_from_implementation(
    *, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    result object real-write 接口占位（不写真实 result；placeholder-safe）。
    """
    ctx = dict(context or {})
    return {
        "release_control_result_present": True,
        "release_control_result_scope": RELEASE_CONTROL_RESULT_SCOPE_V0,
        "release_control_result_state_fact": "minimal_real_effect_implementation_skeleton_no_real_write",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
    }


def write_first_live_failure_or_exception_real_effect_from_implementation(
    *, reason: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    failure/exception real-write 接口占位（不写真实 failure path；只回 stop-safe/reported-placeholder）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_failure_or_exception_attempted": True,
        "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_SCOPE_V0,
        "failure_or_exception_status": "stop_safe_reported_placeholder",
        "side_effects_released": False,
        "reason": str(reason or "unspecified"),
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
    }


def raise_first_live_minimal_real_effect_implementation_skeleton_exception(
    *, exc: Any, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    异常上报接口占位（不抛异常驱动主链、不做真实处理）。
    """
    ctx = dict(context or {})
    return {
        "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_exception_present": True,
        "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_exception_scope": RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_EXCEPTION_SCOPE_V0,
        "exception_status": "reported_placeholder",
        "exception_reason": "minimal_real_effect_implementation_skeleton_v0:exception_interface_placeholder:no_real_handling",
        "exception_type": type(exc).__name__,
        "exception_message": str(exc) if exc is not None else "",
        "side_effects_released": False,
        "context": ctx,
        "consume_mode": "first_live_guarded_minimal_real_effect_implementation_skeleton_inactive",
    }

