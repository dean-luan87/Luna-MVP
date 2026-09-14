# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Enablement Dry-Run v0 (non-effect; non-action).

硬边界（写死）：
- 只做 enablement runner 的 runtime 顺序演练：accept -> enter -> checks -> exit。
- 不启用真实 trial、不进入默认路径、不触发任何真实写入。
- side_effects_released 必须保持为 False（否则 blocked）。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0"


def _blocked(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "enablement_dry_run_attempted": True,
        "enablement_dry_run_scope": _SCOPE,
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_blocked",
        "side_effects_released": False,
        "reason": str(reason or "blocked"),
        "consume_mode": "first_live_guarded_minimal_real_effect_controlled_trial_enablement_dry_run_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["dry_run_trace"] = dict(trace)
    return out


def _not_ready(reason: str, *, trace: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "enablement_dry_run_attempted": True,
        "enablement_dry_run_scope": _SCOPE,
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_not_ready",
        "side_effects_released": False,
        "reason": str(reason or "not_ready"),
        "consume_mode": "first_live_guarded_minimal_real_effect_controlled_trial_enablement_dry_run_v0_non_effect",
    }
    if isinstance(trace, dict):
        out["dry_run_trace"] = dict(trace)
    return out


def _executed(reason: str, *, trace: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "enablement_dry_run_attempted": True,
        "enablement_dry_run_scope": _SCOPE,
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed",
        "side_effects_released": False,
        "dry_run_trace": dict(trace),
        "reason": str(reason or "executed"),
        "consume_mode": "first_live_guarded_minimal_real_effect_controlled_trial_enablement_dry_run_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0(
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
    controlled_trial_enablement_dry_run_signal_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state dry_run_status).
    """
    _ = context

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
            controlled_trial_enablement_dry_run_signal_v0,
        ]
    ) or ((side_effects_released is not None) and (side_effects_released is not False))

    if not any_core_present:
        return False, None

    trace: Dict[str, Any] = {"order": []}

    if side_effects_released is not False:
        return True, _blocked("side_effects_released_must_be_false_for_enablement_dry_run", trace=trace)

    if not isinstance(controlled_trial_enablement_dry_run_signal_v0, dict):
        return True, _not_ready("missing_controlled_trial_enablement_dry_run_signal_v0", trace=trace)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_controlled_trial_enablement_input,
        enter_first_live_controlled_trial_enablement_placeholder,
        exit_first_live_controlled_trial_enablement_placeholder,
        perform_first_live_controlled_trial_enablement_checks_placeholder,
    )

    trace["order"].append("accept_first_live_minimal_real_effect_controlled_trial_enablement_input")
    acc = accept_first_live_minimal_real_effect_controlled_trial_enablement_input(
        controlled_trial_go_no_go_gate_v0=controlled_trial_go_no_go_gate_v0,
        controlled_trial_admission_gate_v0=controlled_trial_admission_gate_v0,
        shadow_evaluation_gate_v0=shadow_evaluation_gate_v0,
        real_write_go_no_go_gate_v0=real_write_go_no_go_gate_v0,
        live_code_path_dry_run_v0=live_code_path_dry_run_v0,
        live_implementation_wiring_v0=live_implementation_wiring_v0,
        live_implementation_dry_run_execution_v0=live_implementation_dry_run_execution_v0,
        rollout_plan_v0=rollout_plan_v0,
        first_real_code_activation_definition_v0=first_real_code_activation_definition_v0,
        runtime_activation_stub_identity_v0=runtime_activation_stub_identity_v0,
        runtime_implementation_stub_identity_v0=runtime_implementation_stub_identity_v0,
        chain_context_v0=chain_context_v0,
        controlled_trial_enablement_approval_or_signal_v0=controlled_trial_enablement_approval_or_signal_v0,
        side_effects_released=False,
        context={"consume_mode": "enablement_dry_run_v0"},
    )
    trace["accept"] = dict(acc) if isinstance(acc, dict) else {"non_dict": True}

    if not (isinstance(acc, dict) and acc.get("status") == "ready" and acc.get("ok") is True):
        return True, _not_ready("enablement_accept_not_ready", trace=trace)

    trace["order"].append("enter_first_live_controlled_trial_enablement_placeholder")
    ent = enter_first_live_controlled_trial_enablement_placeholder(context={"consume_mode": "enablement_dry_run_v0"})
    trace["enter"] = dict(ent) if isinstance(ent, dict) else {"non_dict": True}

    trace["order"].append("perform_first_live_controlled_trial_enablement_checks_placeholder")
    chk = perform_first_live_controlled_trial_enablement_checks_placeholder(
        context={"consume_mode": "enablement_dry_run_v0"}
    )
    trace["checks"] = dict(chk) if isinstance(chk, dict) else {"non_dict": True}

    trace["order"].append("exit_first_live_controlled_trial_enablement_placeholder")
    exi = exit_first_live_controlled_trial_enablement_placeholder(context={"consume_mode": "enablement_dry_run_v0"})
    trace["exit"] = dict(exi) if isinstance(exi, dict) else {"non_dict": True}

    return True, _executed("enablement_runtime_chain_dry_run_executed_placeholder_only", trace=trace)

