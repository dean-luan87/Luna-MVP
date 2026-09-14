# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Minimal Enablement v0 (placeholder implementation).
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
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_controlled_trial_enablement_input,
        enter_first_live_controlled_trial_enablement_placeholder,
        exit_first_live_controlled_trial_enablement_placeholder,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_identity,
        perform_first_live_controlled_trial_enablement_checks_placeholder,
        raise_first_live_controlled_trial_enablement_exception,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_identity()
    assert isinstance(ident, dict)
    assert ident.get("side_effects_released_default") is False

    # 1) blocked when side_effects_released != False
    res = accept_first_live_minimal_real_effect_controlled_trial_enablement_input(
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
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert res.get("status") == "blocked"
    assert res.get("side_effects_released") is False

    # 2) not_ready when no core objects exist (relevant-only)
    res = accept_first_live_minimal_real_effect_controlled_trial_enablement_input(
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
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert res.get("status") == "not_ready"

    # 3) ready (placeholder-ready but not enabled)
    res = accept_first_live_minimal_real_effect_controlled_trial_enablement_input(
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
        side_effects_released=False,
        context={"test": "ready"},
    )
    assert res.get("status") == "ready"
    assert res.get("side_effects_released") is False

    # 4) placeholder calls remain inactive
    assert enter_first_live_controlled_trial_enablement_placeholder(context={"x": 1}).get("enter_status") == "inactive_placeholder"
    assert perform_first_live_controlled_trial_enablement_checks_placeholder(context={"x": 1}).get("checks_status") == "inactive_placeholder"
    assert exit_first_live_controlled_trial_enablement_placeholder(context={"x": 1}).get("exit_status") == "inactive_placeholder"
    assert raise_first_live_controlled_trial_enablement_exception(reason="x", context={"x": 1}).get("exception_status") == "inactive_placeholder"

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

