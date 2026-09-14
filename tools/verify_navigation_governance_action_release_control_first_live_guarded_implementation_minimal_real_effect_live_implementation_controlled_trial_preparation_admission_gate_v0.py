# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Preparation Admission Gate v0.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_shadow_eval_go() -> dict:
    return {"controlled_trial_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_shadow_eval_go"}


def _mk_shadow_trial_executed() -> dict:
    return {"shadow_trial_status": "shadow_trial_executed", "would_have_entered_real_trial_enablement": True}


def _mk_ct_go() -> dict:
    return {"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"}


def _mk_ct_adm() -> dict:
    return {"controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"}


def _mk_real_go() -> dict:
    return {"real_write_status": "first_live_minimal_real_effect_real_write_go"}


def _mk_en_dry_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"}


def _mk_ready() -> dict:
    return {"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"}


def main() -> int:
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0,
    )

    # 1) relevant-only: no core objects
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_signal_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    # 2) blocked: side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0=_mk_shadow_trial_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=_mk_ct_adm(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_real_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0=_mk_en_dry_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0=_mk_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_signal_v0={"prep": True},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_preparation_status") == "first_live_minimal_real_effect_controlled_trial_preparation_blocked"

    # 3) not_admitted: missing preparation signal
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0=_mk_shadow_trial_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=_mk_ct_adm(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_real_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0=_mk_en_dry_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0=_mk_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_signal_v0=None,
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_preparation_status") == "first_live_minimal_real_effect_controlled_trial_preparation_not_admitted"
    assert payload.get("reason") == "missing_controlled_trial_preparation_admission_signal_v0"

    # 4) admitted: all preconditions satisfied
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_evaluation_gate_v0=_mk_shadow_eval_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0=_mk_shadow_trial_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=_mk_ct_adm(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_real_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0=_mk_en_dry_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0=_mk_ready(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_signal_v0={"prep": True, "reason": "unit_test"},
        side_effects_released=False,
        context={"test": "admitted"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_preparation_status") == "first_live_minimal_real_effect_controlled_trial_preparation_admitted"
    assert payload.get("side_effects_released") is False

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

