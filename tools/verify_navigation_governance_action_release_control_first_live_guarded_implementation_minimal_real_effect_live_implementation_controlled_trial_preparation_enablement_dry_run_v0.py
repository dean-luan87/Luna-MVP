# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Preparation Minimal Enablement Dry-Run v0 (non-effect; placeholder chain).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_prep_go() -> dict:
    return {"controlled_trial_preparation_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_preparation_go"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0,
    )

    # 0) relevant-only: none core objects and side_effects_released=False => (False, None)
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0(
        controlled_trial_preparation_go_no_go_gate_v0=None,
        controlled_trial_preparation_shadow_evaluation_gate_v0=None,
        controlled_trial_preparation_admission_gate_v0=None,
        controlled_trial_preparation_dry_run_v0=None,
        controlled_trial_go_no_go_gate_v0=None,
        controlled_trial_admission_gate_v0=None,
        real_write_go_no_go_gate_v0=None,
        controlled_trial_first_minimal_real_enablement_v0=None,
        runtime_activation_stub_identity_v0=None,
        runtime_implementation_stub_identity_v0=None,
        controlled_trial_preparation_enablement_approval_or_signal_v0=None,
        controlled_trial_preparation_enablement_dry_run_signal_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    base_kwargs = dict(
        controlled_trial_preparation_go_no_go_gate_v0=_mk_prep_go(),
        controlled_trial_preparation_shadow_evaluation_gate_v0={
            "controlled_trial_preparation_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"
        },
        controlled_trial_preparation_admission_gate_v0={
            "controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"
        },
        controlled_trial_preparation_dry_run_v0={
            "dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed"
        },
        controlled_trial_go_no_go_gate_v0={"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"},
        controlled_trial_admission_gate_v0={"controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"},
        real_write_go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        controlled_trial_first_minimal_real_enablement_v0={"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"},
        runtime_activation_stub_identity_v0={"id": "act_stub"},
        runtime_implementation_stub_identity_v0={"id": "impl_stub"},
        controlled_trial_preparation_enablement_approval_or_signal_v0={"sig": True},
    )

    # 1) blocked when side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0(
        **base_kwargs,
        controlled_trial_preparation_enablement_dry_run_signal_v0={"dry_run": True},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("dry_run_status") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_blocked"
    )
    assert payload.get("side_effects_released") is False

    # 2) not_ready when missing dry-run signal
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0(
        **base_kwargs,
        controlled_trial_preparation_enablement_dry_run_signal_v0=None,
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("dry_run_status") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_not_ready"
    )

    # 3) executed with fixed order
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_enablement_dry_run_v0(
        **base_kwargs,
        controlled_trial_preparation_enablement_dry_run_signal_v0={"dry_run": True, "reason": "unit_test"},
        side_effects_released=False,
        context={"test": "executed"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("dry_run_status") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed"
    )
    trace = payload.get("dry_run_trace") or {}
    assert trace.get("order") == [
        "accept_first_live_minimal_real_effect_controlled_trial_preparation_enablement_input",
        "enter_first_live_controlled_trial_preparation_enablement_placeholder",
        "perform_first_live_controlled_trial_preparation_enablement_checks_placeholder",
        "exit_first_live_controlled_trial_preparation_enablement_placeholder",
    ]

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

