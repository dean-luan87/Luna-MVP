# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Minimal Enablement v0 (implementation placeholder).

硬边界（写死）：
- 本模块是 future controlled trial enablement 的运行时承接位。
- 当前只做 placeholder-safe：不启用真实 trial、不进入默认路径。
- side_effects_released 必须保持为 False（否则 blocked）。
- 不触发真实写入 / 真实 release_control / rollback / interrupt / route / voice / memory / migration。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_v0"
_IDENTITY = _SCOPE


@dataclass(frozen=True)
class ControlledTrialEnablementResult:
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
            "side_effects_released": False,
        }
        if isinstance(self.payload, dict):
            out["payload"] = dict(self.payload)
        return out


def get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_identity() -> Dict[str, Any]:
    return {
        "controlled_trial_enablement_identity": _IDENTITY,
        "controlled_trial_enablement_scope": _SCOPE,
        "is_controlled_trial_enablement_runner": True,
        "default_enabled": False,
        "side_effects_released_default": False,
        "can_open_side_effects_released": False,
        "consume_mode": "first_live_guarded_minimal_real_effect_controlled_trial_enablement_v0_placeholder_safe",
    }


def accept_first_live_minimal_real_effect_controlled_trial_enablement_input(
    *,
    controlled_trial_go_no_go_gate_v0: Any,
    controlled_trial_admission_gate_v0: Any,
    shadow_evaluation_gate_v0: Any,
    real_write_go_no_go_gate_v0: Any,
    live_code_path_dry_run_v0: Any,
    live_implementation_wiring_v0: Any,
    live_implementation_dry_run_execution_v0: Any,
    rollout_plan_v0: Any,
    first_real_code_activation_definition_v0: Any,
    runtime_activation_stub_identity_v0: Any,
    runtime_implementation_stub_identity_v0: Any,
    chain_context_v0: Any,
    controlled_trial_enablement_approval_or_signal_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    最小入口接口：只做输入就绪性检查（不启用 trial，不写入）。
    """
    ctx = dict(context or {})

    if side_effects_released is not False:
        return ControlledTrialEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="blocked",
            reason="side_effects_released_must_be_false_for_controlled_trial_enablement_placeholder",
            payload={"context": ctx},
        ).to_dict()

    # Relevant-only: if none of core objects exist, do not claim readiness.
    any_core_present = any(
        isinstance(x, dict)
        for x in [
            controlled_trial_go_no_go_gate_v0,
            controlled_trial_admission_gate_v0,
            shadow_evaluation_gate_v0,
            real_write_go_no_go_gate_v0,
            live_code_path_dry_run_v0,
            live_implementation_wiring_v0,
            live_implementation_dry_run_execution_v0,
            rollout_plan_v0,
            first_real_code_activation_definition_v0,
            runtime_activation_stub_identity_v0,
            runtime_implementation_stub_identity_v0,
            chain_context_v0,
            controlled_trial_enablement_approval_or_signal_v0,
        ]
    )
    if not any_core_present:
        return ControlledTrialEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="relevant_only_no_core_objects_present",
            payload={"context": ctx},
        ).to_dict()

    # Preconditions (best-effort; still placeholder-safe).
    if not isinstance(controlled_trial_go_no_go_gate_v0, dict) or str(
        controlled_trial_go_no_go_gate_v0.get("controlled_trial_go_no_go_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_go":
        return ControlledTrialEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="controlled_trial_go_no_go_gate_not_go_or_missing",
            payload={"context": ctx},
        ).to_dict()

    if not isinstance(controlled_trial_admission_gate_v0, dict) or str(
        controlled_trial_admission_gate_v0.get("controlled_trial_status") or ""
    ) != "first_live_minimal_real_effect_controlled_trial_admitted":
        return ControlledTrialEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="controlled_trial_admission_gate_not_admitted_or_missing",
            payload={"context": ctx},
        ).to_dict()

    if not isinstance(shadow_evaluation_gate_v0, dict) or str(
        shadow_evaluation_gate_v0.get("shadow_eval_status") or ""
    ) != "first_live_minimal_real_effect_shadow_eval_go":
        return ControlledTrialEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="shadow_evaluation_gate_not_go_or_missing",
            payload={"context": ctx},
        ).to_dict()

    if not isinstance(controlled_trial_enablement_approval_or_signal_v0, dict):
        return ControlledTrialEnablementResult(
            ok=False,
            result_scope=_SCOPE,
            status="not_ready",
            reason="missing_controlled_trial_enablement_approval_or_signal_v0",
            payload={"context": ctx},
        ).to_dict()

    return ControlledTrialEnablementResult(
        ok=True,
        result_scope=_SCOPE,
        status="ready",
        reason="controlled_trial_enablement_placeholder_ready_but_not_enabled",
        payload={"context": ctx},
    ).to_dict()


def enter_first_live_controlled_trial_enablement_placeholder(
    *, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "enter_attempted": True,
        "enter_scope": _SCOPE,
        "enter_status": "inactive_placeholder",
        "side_effects_released": False,
        "reason": "controlled_trial_enablement_enter_placeholder_only",
        "context": dict(context or {}),
    }


def perform_first_live_controlled_trial_enablement_checks_placeholder(
    *, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "checks_attempted": True,
        "checks_scope": _SCOPE,
        "checks_status": "inactive_placeholder",
        "side_effects_released": False,
        "reason": "controlled_trial_enablement_checks_placeholder_only",
        "context": dict(context or {}),
    }


def exit_first_live_controlled_trial_enablement_placeholder(
    *, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "exit_attempted": True,
        "exit_scope": _SCOPE,
        "exit_status": "inactive_placeholder",
        "side_effects_released": False,
        "reason": "controlled_trial_enablement_exit_placeholder_only",
        "context": dict(context or {}),
    }


def raise_first_live_controlled_trial_enablement_exception(
    *, reason: str, context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "exception_attempted": True,
        "exception_scope": _SCOPE,
        "exception_status": "inactive_placeholder",
        "side_effects_released": False,
        "reason": str(reason or "unspecified"),
        "context": dict(context or {}),
    }

