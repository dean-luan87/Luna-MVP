# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Shadow Evaluation Gate v0 (non-effect; non-action).

硬边界（写死）：
- 只做资格评估 gate：不真实写入、不打开 side_effects_released。
- relevant-only：无核心对象则不产出。
- 输出三态：go | no_go | blocked。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0"


def _result(
    *,
    status: str,
    reason: str,
    inputs_summary: Dict[str, Any],
    consistency: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "shadow_eval_attempted": True,
        "shadow_eval_scope": _SCOPE,
        "shadow_eval_status": str(status),
        "side_effects_released": False,
        "reason": str(reason or ""),
        "inputs_summary": dict(inputs_summary),
        "consistency": dict(consistency),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_signal_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state shadow_eval_status).
    """
    _ = context

    shadow = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0
    go_no_go = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0
    )
    cpd = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0
    wiring = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0
    )
    live_dry = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0
    )
    sig = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_signal_v0
    )

    adm = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0
    lg = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0
    pc = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0
    cg = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0
    cdr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0
    ag = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0
    adr = navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0

    se_present = (side_effects_released is not None) and (side_effects_released is not False)
    any_core_present = any(
        isinstance(x, dict)
        for x in [shadow, go_no_go, cpd, wiring, live_dry, sig, adm, lg, pc, cg, cdr, ag, adr]
    ) or se_present
    if not any_core_present:
        return False, None

    inputs_summary: Dict[str, Any] = {
        "has_shadow": isinstance(shadow, dict),
        "has_go_no_go_gate": isinstance(go_no_go, dict),
        "has_live_code_path_dry_run": isinstance(cpd, dict),
        "has_live_implementation_wiring": isinstance(wiring, dict),
        "has_live_implementation_dry_run_execution": isinstance(live_dry, dict),
        "has_chain_admission_gate": isinstance(adm, dict),
        "has_chain_guarded_launch_gate": isinstance(lg, dict),
        "has_chain_pre_commit_dry_run": isinstance(pc, dict),
        "has_chain_commit_gate": isinstance(cg, dict),
        "has_chain_commit_dry_run": isinstance(cdr, dict),
        "has_chain_activation_gate": isinstance(ag, dict),
        "has_chain_activation_dry_run": isinstance(adr, dict),
        "has_shadow_evaluation_signal": isinstance(sig, dict),
    }

    if side_effects_released is not False:
        return True, _result(
            status="first_live_minimal_real_effect_shadow_eval_blocked",
            reason="side_effects_released_must_be_false_for_shadow_evaluation_gate",
            inputs_summary=inputs_summary,
            consistency={"side_effects_released_is_false": False},
        )

    # Preconditions (must all be satisfied for go).
    go_no_go_ok = isinstance(go_no_go, dict) and str(go_no_go.get("real_write_status") or "") == (
        "first_live_minimal_real_effect_real_write_go"
    )
    cpd_ok = isinstance(cpd, dict) and str(cpd.get("dry_run_status") or "") == (
        "first_live_minimal_real_effect_live_code_path_dry_run_executed"
    )
    wiring_ok = isinstance(wiring, dict) and str(wiring.get("wiring_status") or "") == (
        "first_live_minimal_real_effect_live_wired_ready"
    )
    live_dry_ok = isinstance(live_dry, dict) and str(live_dry.get("execution_status") or "") == (
        "first_live_minimal_real_effect_live_dry_run_executed"
    )

    # Chain readiness (minimal; strict).
    adm_ok = isinstance(adm, dict) and str(adm.get("admission_status") or "") == (
        "first_live_minimal_real_effect_admitted"
    )
    lg_ok = isinstance(lg, dict) and str(lg.get("launch_status") or "") == (
        "first_live_minimal_real_effect_launch_admitted"
    )
    pc_ok = isinstance(pc, dict) and str(pc.get("pre_commit_status") or "") == (
        "first_live_minimal_real_effect_pre_commit_ready"
    )
    cg_ok = isinstance(cg, dict) and str(cg.get("commit_status") or "") == (
        "first_live_minimal_real_effect_commit_admitted"
    )
    cdr_ok = isinstance(cdr, dict) and str(cdr.get("commit_dry_run_status") or "") == (
        "first_live_minimal_real_effect_commit_ready"
    )
    ag_ok = isinstance(ag, dict) and str(ag.get("activation_status") or "") == (
        "first_live_minimal_real_effect_activation_admitted"
    )
    adr_ok = isinstance(adr, dict) and str(adr.get("activation_dry_run_status") or "") == (
        "first_live_minimal_real_effect_activation_ready"
    )

    preconditions_ok = all(
        [
            isinstance(sig, dict),
            isinstance(shadow, dict),
            go_no_go_ok,
            cpd_ok,
            wiring_ok,
            live_dry_ok,
            adm_ok,
            lg_ok,
            pc_ok,
            cg_ok,
            cdr_ok,
            ag_ok,
            adr_ok,
        ]
    )

    # Shadow quality line.
    shadow_status_ok = isinstance(shadow, dict) and str(shadow.get("shadow_status") or "") == "shadow_executed"
    shadow_enter_ok = bool(isinstance(shadow, dict) and shadow.get("would_have_entered_real_write") is True)
    shadow_w_state = bool(isinstance(shadow, dict) and shadow.get("would_have_written_execution_state") is True)
    shadow_w_result = bool(isinstance(shadow, dict) and shadow.get("would_have_written_result_object") is True)
    shadow_se_false = bool(isinstance(shadow, dict) and shadow.get("side_effects_released") is False)
    shadow_quality_ok = all([shadow_status_ok, shadow_enter_ok, shadow_w_state, shadow_w_result, shadow_se_false])

    consistency = {
        "go_no_go_is_go": bool(go_no_go_ok),
        "live_code_path_dry_run_is_executed": bool(cpd_ok),
        "live_implementation_wiring_is_wired_ready": bool(wiring_ok),
        "live_implementation_dry_run_execution_is_executed": bool(live_dry_ok),
        "chain_admission_is_admitted": bool(adm_ok),
        "chain_launch_gate_is_admitted": bool(lg_ok),
        "chain_pre_commit_is_ready": bool(pc_ok),
        "chain_commit_gate_is_admitted": bool(cg_ok),
        "chain_commit_dry_run_is_ready": bool(cdr_ok),
        "chain_activation_gate_is_admitted": bool(ag_ok),
        "chain_activation_dry_run_is_ready": bool(adr_ok),
        "shadow_status_is_executed": bool(shadow_status_ok),
        "shadow_would_have_entered_real_write": bool(shadow_enter_ok),
        "shadow_would_have_written_execution_state": bool(shadow_w_state),
        "shadow_would_have_written_result_object": bool(shadow_w_result),
        "shadow_side_effects_released_is_false": bool(shadow_se_false),
        "shadow_quality_ok": bool(shadow_quality_ok),
        "preconditions_ok": bool(preconditions_ok),
    }

    if preconditions_ok and shadow_quality_ok:
        return True, _result(
            status="first_live_minimal_real_effect_shadow_eval_go",
            reason="shadow_observe_only_results_consistent_and_stable_for_next_stage_pretrial_evaluation",
            inputs_summary=inputs_summary,
            consistency=consistency,
        )

    # Default: no-go (still non-action).
    if not isinstance(sig, dict):
        reason = "missing_shadow_evaluation_signal_v0"
    elif not isinstance(shadow, dict):
        reason = "missing_shadow_object_v0"
    elif not go_no_go_ok:
        reason = "real_write_go_no_go_gate_not_go_or_missing"
    elif not cpd_ok:
        reason = "live_code_path_dry_run_not_executed_or_missing"
    elif not wiring_ok:
        reason = "live_implementation_wiring_not_wired_ready_or_missing"
    elif not live_dry_ok:
        reason = "live_implementation_dry_run_execution_not_executed_or_missing"
    elif not adm_ok:
        reason = "chain_admission_gate_not_admitted_or_missing"
    elif not lg_ok:
        reason = "chain_guarded_launch_gate_not_admitted_or_missing"
    elif not pc_ok:
        reason = "chain_pre_commit_not_ready_or_missing"
    elif not cg_ok:
        reason = "chain_commit_gate_not_admitted_or_missing"
    elif not cdr_ok:
        reason = "chain_commit_dry_run_not_ready_or_missing"
    elif not ag_ok:
        reason = "chain_activation_gate_not_admitted_or_missing"
    elif not adr_ok:
        reason = "chain_activation_dry_run_not_ready_or_missing"
    elif not shadow_status_ok:
        reason = "shadow_status_not_executed_or_missing"
    elif not shadow_enter_ok:
        reason = "shadow_would_have_entered_real_write_not_true"
    elif not shadow_quality_ok:
        reason = "shadow_quality_line_not_met"
    else:
        reason = "shadow_evaluation_no_go"

    return True, _result(
        status="first_live_minimal_real_effect_shadow_eval_no_go",
        reason=reason,
        inputs_summary=inputs_summary,
        consistency=consistency,
    )

