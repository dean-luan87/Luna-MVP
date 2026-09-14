# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation Admission Gate v0 (non-effect; non-action).

硬边界（写死）：
- 只做“是否允许进入真实 controlled trial 准备态”的准入判断；不真实准备、不真实启用。
- relevant-only：无核心对象则不产出。
- 输出三态：admitted | not_admitted | blocked。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0"


def _result(
    *,
    status: str,
    reason: str,
    inputs_summary: Dict[str, Any],
    consistency: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "controlled_trial_preparation_attempted": True,
        "controlled_trial_preparation_scope": _SCOPE,
        "controlled_trial_preparation_status": str(status),
        "side_effects_released": False,
        "reason": str(reason or ""),
        "inputs_summary": dict(inputs_summary),
        "consistency": dict(consistency),
        "consume_mode": "first_live_guarded_minimal_real_effect_controlled_trial_preparation_admission_gate_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_signal_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state controlled_trial_preparation_status).
    """
    _ = context

    sh_eval_gate = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0
    )
    shadow = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0
    )
    ct_go = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0
    )
    ct_adm = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0
    )
    real_go = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0
    )
    en_dry = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0
    )
    ready = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0
    )
    sig = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_signal_v0
    )

    se_present = (side_effects_released is not None) and (side_effects_released is not False)
    any_core_present = any(
        isinstance(x, dict) for x in [sh_eval_gate, shadow, ct_go, ct_adm, real_go, en_dry, ready, sig]
    ) or se_present
    if not any_core_present:
        return False, None

    inputs_summary: Dict[str, Any] = {
        "has_controlled_trial_shadow_eval_gate": isinstance(sh_eval_gate, dict),
        "has_controlled_trial_shadow": isinstance(shadow, dict),
        "has_controlled_trial_go_no_go_gate": isinstance(ct_go, dict),
        "has_controlled_trial_admission_gate": isinstance(ct_adm, dict),
        "has_real_write_go_no_go_gate": isinstance(real_go, dict),
        "has_controlled_trial_enablement_dry_run": isinstance(en_dry, dict),
        "has_controlled_trial_first_minimal_real_enablement": isinstance(ready, dict),
        "has_preparation_admission_signal": isinstance(sig, dict),
    }

    if side_effects_released is not False:
        return True, _result(
            status="first_live_minimal_real_effect_controlled_trial_preparation_blocked",
            reason="side_effects_released_must_be_false_for_controlled_trial_preparation_admission_gate",
            inputs_summary=inputs_summary,
            consistency={"side_effects_released_is_false": False},
        )

    sh_eval_ok = isinstance(sh_eval_gate, dict) and str(sh_eval_gate.get("controlled_trial_shadow_eval_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_shadow_eval_go"
    )
    shadow_ok = isinstance(shadow, dict) and str(shadow.get("shadow_trial_status") or "") == "shadow_trial_executed"
    shadow_enter_ok = bool(isinstance(shadow, dict) and shadow.get("would_have_entered_real_trial_enablement") is True)

    ct_go_ok = isinstance(ct_go, dict) and str(ct_go.get("controlled_trial_go_no_go_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_go"
    )
    ct_adm_ok = isinstance(ct_adm, dict) and str(ct_adm.get("controlled_trial_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_admitted"
    )
    real_go_ok = isinstance(real_go, dict) and str(real_go.get("real_write_status") or "") == (
        "first_live_minimal_real_effect_real_write_go"
    )
    en_dry_ok = isinstance(en_dry, dict) and str(en_dry.get("dry_run_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"
    )
    ready_ok = isinstance(ready, dict) and str(ready.get("real_enablement_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"
    )
    sig_ok = isinstance(sig, dict)

    preconditions_ok = all([sh_eval_ok, shadow_ok, shadow_enter_ok, ct_go_ok, ct_adm_ok, real_go_ok, en_dry_ok, ready_ok, sig_ok])

    consistency = {
        "controlled_trial_shadow_eval_is_go": bool(sh_eval_ok),
        "shadow_trial_status_is_executed": bool(shadow_ok),
        "shadow_would_have_entered_real_trial_enablement": bool(shadow_enter_ok),
        "controlled_trial_go_no_go_is_go": bool(ct_go_ok),
        "controlled_trial_admission_is_admitted": bool(ct_adm_ok),
        "real_write_go_no_go_is_go": bool(real_go_ok),
        "controlled_trial_enablement_dry_run_is_executed": bool(en_dry_ok),
        "controlled_trial_first_minimal_real_enablement_is_ready": bool(ready_ok),
        "preparation_admission_signal_present": bool(sig_ok),
        "preconditions_ok": bool(preconditions_ok),
    }

    if preconditions_ok:
        return True, _result(
            status="first_live_minimal_real_effect_controlled_trial_preparation_admitted",
            reason="controlled_trial_preparation_admitted_after_shadow_eval_go_with_explicit_preparation_signal",
            inputs_summary=inputs_summary,
            consistency=consistency,
        )

    if not sig_ok:
        reason = "missing_controlled_trial_preparation_admission_signal_v0"
    elif not sh_eval_ok:
        reason = "controlled_trial_shadow_evaluation_gate_not_go_or_missing"
    elif not shadow_ok:
        reason = "controlled_trial_shadow_trial_not_executed_or_missing"
    elif not shadow_enter_ok:
        reason = "shadow_would_have_entered_real_trial_enablement_not_true"
    elif not ct_go_ok:
        reason = "controlled_trial_go_no_go_gate_not_go_or_missing"
    elif not ct_adm_ok:
        reason = "controlled_trial_admission_gate_not_admitted_or_missing"
    elif not real_go_ok:
        reason = "real_write_go_no_go_gate_not_go_or_missing"
    elif not en_dry_ok:
        reason = "controlled_trial_enablement_dry_run_not_executed_or_missing"
    elif not ready_ok:
        reason = "controlled_trial_first_minimal_real_enablement_not_ready_or_missing"
    else:
        reason = "controlled_trial_preparation_not_admitted"

    return True, _result(
        status="first_live_minimal_real_effect_controlled_trial_preparation_not_admitted",
        reason=reason,
        inputs_summary=inputs_summary,
        consistency=consistency,
    )

