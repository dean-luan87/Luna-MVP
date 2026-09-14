# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Preparation Shadow v0 (observe-only; no-op writers).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_prep_admitted() -> dict:
    return {"controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"}


def _mk_prep_dry_run_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed"}


def _mk_ct_go() -> dict:
    return {"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"}


def _mk_ct_real_enablement_ready() -> dict:
    return {"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0,
    )

    # 0) relevant-only
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0(
        controlled_trial_preparation_admission_gate_v0=None,
        controlled_trial_preparation_dry_run_v0=None,
        controlled_trial_go_no_go_gate_v0=None,
        controlled_trial_first_minimal_real_enablement_v0=None,
        preparation_shadow_enable_signal_v0=None,
        execution_state_v0=None,
        result_v0=None,
        exception_or_failure_path_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    # 1) blocked when side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_shadow_enable_signal_v0={"shadow": True},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("preparation_shadow_status") == "preparation_shadow_blocked"
    assert payload.get("side_effects_released") is False

    # 2) not_ready when missing shadow signal
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_shadow_enable_signal_v0=None,
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("preparation_shadow_status") == "preparation_shadow_not_ready"

    # 3) executed with would-have flags
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_shadow_enable_signal_v0={"shadow": True, "reason": "unit_test"},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        context={"test": "executed"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("preparation_shadow_status") == "preparation_shadow_executed"
    assert payload.get("would_have_entered_real_preparation_enablement") is True
    assert payload.get("would_have_written_execution_state") is True
    assert payload.get("would_have_written_result_object") is True

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

