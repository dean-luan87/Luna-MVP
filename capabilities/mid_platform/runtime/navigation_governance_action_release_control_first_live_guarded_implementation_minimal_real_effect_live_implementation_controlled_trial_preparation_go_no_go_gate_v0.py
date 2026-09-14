# -*- coding: utf-8 -*-
"""
Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Controlled Trial Preparation Go/No-Go Gate v0 (non-effect; non-action).

硬边界（写死）：
- 只做“本次是否真正启动第一阶段真实 preparation”的最终启动闸门；不真实写入、不启用默认路径。
- relevant-only：无核心对象则不产出。
- 输出三态：go | no_go | blocked。
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

_SCOPE = "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0"


def _result(*, status: str, reason: str, inputs_summary: Dict[str, Any], consistency: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "controlled_trial_preparation_go_no_go_attempted": True,
        "controlled_trial_preparation_go_no_go_scope": _SCOPE,
        "controlled_trial_preparation_go_no_go_status": str(status),
        "side_effects_released": False,
        "reason": str(reason or ""),
        "inputs_summary": dict(inputs_summary),
        "consistency": dict(consistency),
        "consume_mode": "first_live_guarded_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0_non_effect",
    }


def evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0(
    *,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_evaluation_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_dry_run_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_activation_stub_identity_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_implementation_stub_identity_v0: Any,
    navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_signal_v0: Any,
    side_effects_released: Any,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    relevant-only:
    - If none of the core objects exist, returns (False, None).
    - Otherwise returns (True, attempted object with 3-state controlled_trial_preparation_go_no_go_status).
    """
    _ = context

    prep_shadow_eval = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_evaluation_gate_v0
    )
    prep_adm = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0
    )
    prep_dry = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_dry_run_v0
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
    ready = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0
    )
    act_stub = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_activation_stub_identity_v0
    )
    impl_stub = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_implementation_stub_identity_v0
    )
    sig = (
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_signal_v0
    )

    se_present = (side_effects_released is not None) and (side_effects_released is not False)
    any_core_present = any(
        isinstance(x, dict)
        for x in [
            prep_shadow_eval,
            prep_adm,
            prep_dry,
            ct_go,
            ct_adm,
            real_go,
            ready,
            act_stub,
            impl_stub,
            sig,
        ]
    ) or se_present
    if not any_core_present:
        return False, None

    inputs_summary: Dict[str, Any] = {
        "has_preparation_shadow_evaluation_gate": isinstance(prep_shadow_eval, dict),
        "has_preparation_admission_gate": isinstance(prep_adm, dict),
        "has_preparation_dry_run": isinstance(prep_dry, dict),
        "has_controlled_trial_go_no_go_gate": isinstance(ct_go, dict),
        "has_controlled_trial_admission_gate": isinstance(ct_adm, dict),
        "has_real_write_go_no_go_gate": isinstance(real_go, dict),
        "has_controlled_trial_first_minimal_real_enablement": isinstance(ready, dict),
        "has_runtime_activation_stub_identity": isinstance(act_stub, dict),
        "has_runtime_implementation_stub_identity": isinstance(impl_stub, dict),
        "has_preparation_go_no_go_signal": isinstance(sig, dict),
    }

    if side_effects_released is not False:
        return True, _result(
            status="first_live_minimal_real_effect_controlled_trial_preparation_blocked",
            reason="side_effects_released_must_be_false_for_controlled_trial_preparation_go_no_go_gate",
            inputs_summary=inputs_summary,
            consistency={"side_effects_released_is_false": False},
        )

    sig_ok = isinstance(sig, dict)
    prep_shadow_eval_ok = isinstance(prep_shadow_eval, dict) and str(
        prep_shadow_eval.get("controlled_trial_preparation_shadow_eval_status") or ""
    ) == "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"

    prep_adm_ok = isinstance(prep_adm, dict) and str(prep_adm.get("controlled_trial_preparation_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_admitted"
    )
    prep_dry_ok = isinstance(prep_dry, dict) and str(prep_dry.get("dry_run_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed"
    )
    ct_go_ok = isinstance(ct_go, dict) and str(ct_go.get("controlled_trial_go_no_go_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_go"
    )
    ct_adm_ok = isinstance(ct_adm, dict) and str(ct_adm.get("controlled_trial_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_admitted"
    )
    real_go_ok = isinstance(real_go, dict) and str(real_go.get("real_write_status") or "") == (
        "first_live_minimal_real_effect_real_write_go"
    )
    ready_ok = isinstance(ready, dict) and str(ready.get("real_enablement_status") or "") == (
        "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"
    )
    stubs_ok = isinstance(act_stub, dict) and isinstance(impl_stub, dict)

    preconditions_ok = all(
        [sig_ok, prep_shadow_eval_ok, prep_adm_ok, prep_dry_ok, ct_go_ok, ct_adm_ok, real_go_ok, ready_ok, stubs_ok]
    )

    consistency = {
        "preparation_shadow_eval_is_go": bool(prep_shadow_eval_ok),
        "preparation_admission_is_admitted": bool(prep_adm_ok),
        "preparation_dry_run_is_executed": bool(prep_dry_ok),
        "controlled_trial_go_no_go_is_go": bool(ct_go_ok),
        "controlled_trial_admission_is_admitted": bool(ct_adm_ok),
        "real_write_go_no_go_is_go": bool(real_go_ok),
        "controlled_trial_first_minimal_real_enablement_is_ready": bool(ready_ok),
        "runtime_stubs_present": bool(stubs_ok),
        "preparation_go_no_go_signal_present": bool(sig_ok),
        "preconditions_ok": bool(preconditions_ok),
    }

    if preconditions_ok:
        return True, _result(
            status="first_live_minimal_real_effect_controlled_trial_preparation_go",
            reason="controlled_trial_preparation_go_after_shadow_eval_go_with_explicit_go_no_go_signal",
            inputs_summary=inputs_summary,
            consistency=consistency,
        )

    if not sig_ok:
        reason = "missing_controlled_trial_preparation_go_no_go_signal_v0"
    elif not prep_shadow_eval_ok:
        reason = "controlled_trial_preparation_shadow_evaluation_gate_not_go_or_missing"
    elif not prep_adm_ok:
        reason = "controlled_trial_preparation_admission_gate_not_admitted_or_missing"
    elif not prep_dry_ok:
        reason = "controlled_trial_preparation_dry_run_not_executed_or_missing"
    elif not ct_go_ok:
        reason = "controlled_trial_go_no_go_gate_not_go_or_missing"
    elif not ct_adm_ok:
        reason = "controlled_trial_admission_gate_not_admitted_or_missing"
    elif not real_go_ok:
        reason = "real_write_go_no_go_gate_not_go_or_missing"
    elif not ready_ok:
        reason = "controlled_trial_first_minimal_real_enablement_not_ready_or_missing"
    elif not stubs_ok:
        reason = "missing_runtime_activation_or_implementation_stub_identity_v0"
    else:
        reason = "controlled_trial_preparation_go_no_go_no_go"

    return True, _result(
        status="first_live_minimal_real_effect_controlled_trial_preparation_no_go",
        reason=reason,
        inputs_summary=inputs_summary,
        consistency=consistency,
    )

