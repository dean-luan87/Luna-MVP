# -*- coding: utf-8 -*-
"""
Self-test: Minimal Real-Effect Live Implementation Controlled Trial Go/No-Go Gate v0.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_trial_admitted() -> dict:
    return {"controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"}


def _mk_shadow_eval_go() -> dict:
    return {"shadow_eval_status": "first_live_minimal_real_effect_shadow_eval_go"}


def _mk_go_no_go_go() -> dict:
    return {"real_write_status": "first_live_minimal_real_effect_real_write_go"}


def _mk_cpd_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"}


def _mk_wired_ready() -> dict:
    return {"wiring_status": "first_live_minimal_real_effect_live_wired_ready"}


def _mk_live_dry_executed() -> dict:
    return {"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"}


def _mk_adm_admitted() -> dict:
    return {"admission_status": "first_live_minimal_real_effect_admitted"}


def _mk_launch_admitted() -> dict:
    return {"launch_status": "first_live_minimal_real_effect_launch_admitted"}


def _mk_pre_commit_ready() -> dict:
    return {"pre_commit_status": "first_live_minimal_real_effect_pre_commit_ready"}


def _mk_commit_admitted() -> dict:
    return {"commit_status": "first_live_minimal_real_effect_commit_admitted"}


def _mk_commit_ready() -> dict:
    return {"commit_dry_run_status": "first_live_minimal_real_effect_commit_ready"}


def _mk_activation_admitted() -> dict:
    return {"activation_status": "first_live_minimal_real_effect_activation_admitted"}


def _mk_activation_ready() -> dict:
    return {"activation_dry_run_status": "first_live_minimal_real_effect_activation_ready"}


def main() -> int:
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0,
    )

    # 1) relevant-only: no core objects
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_signal_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    # 2) blocked: side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=_mk_trial_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_go_no_go_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=_mk_cpd_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=_mk_wired_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=_mk_live_dry_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=_mk_adm_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=_mk_launch_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=_mk_pre_commit_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=_mk_commit_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=_mk_commit_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=_mk_activation_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=_mk_activation_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0={"plan": "frozen"},
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_signal_v0={"trial_go": True},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_go_no_go_status") == "first_live_minimal_real_effect_controlled_trial_blocked"

    # 3) no_go: missing go/no-go signal
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=_mk_trial_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_go_no_go_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=_mk_cpd_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=_mk_wired_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=_mk_live_dry_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=_mk_adm_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=_mk_launch_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=_mk_pre_commit_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=_mk_commit_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=_mk_commit_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=_mk_activation_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=_mk_activation_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0={"plan": "frozen"},
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_signal_v0=None,
        side_effects_released=False,
        context={"test": "no_go_missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_go_no_go_status") == "first_live_minimal_real_effect_controlled_trial_no_go"
    assert payload.get("reason") == "missing_controlled_trial_go_no_go_signal_v0"

    # 4) go: all preconditions satisfied
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=_mk_trial_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_go_no_go_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=_mk_cpd_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=_mk_wired_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=_mk_live_dry_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=_mk_adm_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=_mk_launch_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=_mk_pre_commit_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=_mk_commit_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=_mk_commit_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=_mk_activation_admitted(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=_mk_activation_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0={"plan": "frozen"},
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_signal_v0={"trial_go": True, "reason": "unit_test"},
        side_effects_released=False,
        context={"test": "go"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_go_no_go_status") == "first_live_minimal_real_effect_controlled_trial_go"
    assert payload.get("side_effects_released") is False

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

