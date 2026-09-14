# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Enablement Dry-Run v0.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_trial_go() -> dict:
    return {"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"}


def _mk_trial_admitted() -> dict:
    return {"controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"}


def _mk_shadow_eval_go() -> dict:
    return {"shadow_eval_status": "first_live_minimal_real_effect_shadow_eval_go"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0,
    )

    # 1) relevant-only: no core objects
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0(
        controlled_trial_go_no_go_gate_v0=None,
        controlled_trial_admission_gate_v0=None,
        shadow_evaluation_gate_v0=None,
        real_write_go_no_go_gate_v0=None,
        live_code_path_dry_run_v0=None,
        live_implementation_wiring_v0=None,
        live_implementation_dry_run_execution_v0=None,
        rollout_plan_v0=None,
        first_real_code_activation_definition_v0=None,
        runtime_activation_stub_identity_v0=None,
        runtime_implementation_stub_identity_v0=None,
        chain_context_v0=None,
        controlled_trial_enablement_approval_or_signal_v0=None,
        controlled_trial_enablement_dry_run_signal_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    # 2) blocked: side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_admission_gate_v0=_mk_trial_admitted(),
        shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        real_write_go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        live_code_path_dry_run_v0={"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"},
        live_implementation_wiring_v0={"wiring_status": "first_live_minimal_real_effect_live_wired_ready"},
        live_implementation_dry_run_execution_v0={"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"},
        rollout_plan_v0={"plan": "frozen"},
        first_real_code_activation_definition_v0={"definition": "frozen"},
        runtime_activation_stub_identity_v0={"id": "stub"},
        runtime_implementation_stub_identity_v0={"id": "stub"},
        chain_context_v0={"chain": "ready"},
        controlled_trial_enablement_approval_or_signal_v0={"enable": True},
        controlled_trial_enablement_dry_run_signal_v0={"dry_run": True},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("dry_run_status") == "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_blocked"

    # 3) not_ready: missing dry-run signal
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_admission_gate_v0=_mk_trial_admitted(),
        shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        real_write_go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        live_code_path_dry_run_v0={"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"},
        live_implementation_wiring_v0={"wiring_status": "first_live_minimal_real_effect_live_wired_ready"},
        live_implementation_dry_run_execution_v0={"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"},
        rollout_plan_v0={"plan": "frozen"},
        first_real_code_activation_definition_v0={"definition": "frozen"},
        runtime_activation_stub_identity_v0={"id": "stub"},
        runtime_implementation_stub_identity_v0={"id": "stub"},
        chain_context_v0={"chain": "ready"},
        controlled_trial_enablement_approval_or_signal_v0={"enable": True},
        controlled_trial_enablement_dry_run_signal_v0=None,
        side_effects_released=False,
        context={"test": "missing_dry_run_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("dry_run_status") == "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_not_ready"
    assert payload.get("reason") == "missing_controlled_trial_enablement_dry_run_signal_v0"

    # 4) executed: accept ready + fixed chain runs
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_admission_gate_v0=_mk_trial_admitted(),
        shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        real_write_go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        live_code_path_dry_run_v0={"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"},
        live_implementation_wiring_v0={"wiring_status": "first_live_minimal_real_effect_live_wired_ready"},
        live_implementation_dry_run_execution_v0={"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"},
        rollout_plan_v0={"plan": "frozen"},
        first_real_code_activation_definition_v0={"definition": "frozen"},
        runtime_activation_stub_identity_v0={"id": "stub"},
        runtime_implementation_stub_identity_v0={"id": "stub"},
        chain_context_v0={"chain": "ready"},
        controlled_trial_enablement_approval_or_signal_v0={"enable": True, "reason": "unit_test"},
        controlled_trial_enablement_dry_run_signal_v0={"dry_run": True, "reason": "unit_test"},
        side_effects_released=False,
        context={"test": "executed"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("dry_run_status") == "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"
    trace = payload.get("dry_run_trace") or {}
    order = trace.get("order") if isinstance(trace, dict) else None
    assert isinstance(order, list) and len(order) == 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

