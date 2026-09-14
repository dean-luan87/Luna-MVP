# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Shadow Evaluation Gate v0 (non-effect; non-action).

硬边界（写死）：
- 只做资格评估 gate：不真实启用、不真实写入、不打开 side_effects_released。
- relevant-only：无核心对象则不产出。
- 输出三态：go | no_go | blocked。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0"


def _result(
    *,
    status: str,
    reason: str,
    inputs_summary: Dict[str, Any],
    consistency: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "controlled_trial_shadow_eval_attempted": True,
        "controlled_trial_shadow_eval_scope": _SCOPE,
        "controlled_trial_shadow_eval_status": str(status),
        "side_effects_released": False,
        "reason": str(reason or ""),
        "inputs_summary": dict(inputs_summary),
        "consistency": dict(consistency),
        "consume_mode": "first_live_guarded_minimal_real_effect_controlled_trial_shadow_evaluation_gate_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_signal_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state controlled_trial_shadow_eval_status).
    """
    _ = context

    shadow = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0
    ct_go = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0
    )
    ct_adm = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0
    )
    sh_eval = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0
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
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_signal_v0
    )

    se_present = (side_effects_released is not None) and (side_effects_released is not False)
    any_core_present = any(
        isinstance(x, dict) for x in [shadow, ct_go, ct_adm, sh_eval, real_go, en_dry, ready, sig]
    ) or se_present
    if not any_core_present:
        return False, None

    inputs_summary: Dict[str, Any] = {
        "has_controlled_trial_shadow": isinstance(shadow, dict),
        "has_controlled_trial_go_no_go_gate": isinstance(ct_go, dict),
        "has_controlled_trial_admission_gate": isinstance(ct_adm, dict),
        "has_shadow_evaluation_gate": isinstance(sh_eval, dict),
        "has_real_write_go_no_go_gate": isinstance(real_go, dict),
        "has_controlled_trial_enablement_dry_run": isinstance(en_dry, dict),
        "has_controlled_trial_first_minimal_real_enablement": isinstance(ready, dict),
        "has_controlled_trial_shadow_evaluation_signal": isinstance(sig, dict),
    }

    if side_effects_released is not False:
        return True, _result(
            status="first_live_minimal_real_effect_controlled_trial_shadow_eval_blocked",
            reason="side_effects_released_must_be_false_for_controlled_trial_shadow_evaluation_gate",
            inputs_summary=inputs_summary,
            consistency={"side_effects_released_is_false": False},
        )

    ct_go_ok = isinstance(ct_go, dict) and str(ct_go.get("controlled_trial_go_no_go_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_go"
    )
    ct_adm_ok = isinstance(ct_adm, dict) and str(ct_adm.get("controlled_trial_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_admitted"
    )
    sh_eval_ok = isinstance(sh_eval, dict) and str(sh_eval.get("shadow_eval_status") or "") == (
        "first_live_minimal_real_effect_shadow_eval_go"
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

    shadow_status_ok = isinstance(shadow, dict) and str(shadow.get("shadow_trial_status") or "") == "shadow_trial_executed"
    shadow_enter_ok = bool(isinstance(shadow, dict) and shadow.get("would_have_entered_real_trial_enablement") is True)
    shadow_w_state = bool(isinstance(shadow, dict) and shadow.get("would_have_written_execution_state") is True)
    shadow_w_result = bool(isinstance(shadow, dict) and shadow.get("would_have_written_result_object") is True)
    shadow_se_false = bool(isinstance(shadow, dict) and shadow.get("side_effects_released") is False)
    shadow_quality_ok = all([shadow_status_ok, shadow_enter_ok, shadow_w_state, shadow_w_result, shadow_se_false])

    preconditions_ok = all([sig_ok, ct_go_ok, ct_adm_ok, sh_eval_ok, real_go_ok, en_dry_ok, ready_ok, shadow_quality_ok])

    consistency = {
        "controlled_trial_go_no_go_is_go": bool(ct_go_ok),
        "controlled_trial_admission_is_admitted": bool(ct_adm_ok),
        "shadow_eval_is_go": bool(sh_eval_ok),
        "real_write_go_no_go_is_go": bool(real_go_ok),
        "controlled_trial_enablement_dry_run_is_executed": bool(en_dry_ok),
        "controlled_trial_first_minimal_real_enablement_is_ready": bool(ready_ok),
        "shadow_status_is_executed": bool(shadow_status_ok),
        "shadow_would_have_entered_real_trial_enablement": bool(shadow_enter_ok),
        "shadow_would_have_written_execution_state": bool(shadow_w_state),
        "shadow_would_have_written_result_object": bool(shadow_w_result),
        "shadow_side_effects_released_is_false": bool(shadow_se_false),
        "shadow_quality_ok": bool(shadow_quality_ok),
        "preconditions_ok": bool(preconditions_ok),
    }

    if preconditions_ok:
        return True, _result(
            status="first_live_minimal_real_effect_controlled_trial_shadow_eval_go",
            reason="controlled_trial_shadow_results_consistent_for_next_stage_real_trial_preparation",
            inputs_summary=inputs_summary,
            consistency=consistency,
        )

    if not sig_ok:
        reason = "missing_controlled_trial_shadow_evaluation_signal_v0"
    elif not isinstance(shadow, dict):
        reason = "missing_controlled_trial_shadow_object_v0"
    elif not ct_go_ok:
        reason = "controlled_trial_go_no_go_gate_not_go_or_missing"
    elif not ct_adm_ok:
        reason = "controlled_trial_admission_gate_not_admitted_or_missing"
    elif not sh_eval_ok:
        reason = "shadow_evaluation_gate_not_go_or_missing"
    elif not real_go_ok:
        reason = "real_write_go_no_go_gate_not_go_or_missing"
    elif not en_dry_ok:
        reason = "controlled_trial_enablement_dry_run_not_executed_or_missing"
    elif not ready_ok:
        reason = "controlled_trial_first_minimal_real_enablement_not_ready_or_missing"
    elif not shadow_status_ok:
        reason = "shadow_trial_status_not_executed_or_missing"
    elif not shadow_enter_ok:
        reason = "shadow_would_have_entered_real_trial_enablement_not_true"
    elif not shadow_quality_ok:
        reason = "controlled_trial_shadow_quality_line_not_met"
    else:
        reason = "controlled_trial_shadow_evaluation_no_go"

    return True, _result(
        status="first_live_minimal_real_effect_controlled_trial_shadow_eval_no_go",
        reason=reason,
        inputs_summary=inputs_summary,
        consistency=consistency,
    )

