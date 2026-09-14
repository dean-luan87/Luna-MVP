# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Preparation v0 (placeholder implementation).
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


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_controlled_trial_preparation_input,
        enter_first_live_controlled_trial_preparation_placeholder,
        exit_first_live_controlled_trial_preparation_placeholder,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_identity,
        perform_first_live_controlled_trial_preparation_checks_placeholder,
        raise_first_live_controlled_trial_preparation_exception,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_identity()
    assert isinstance(ident, dict)
    assert ident.get("side_effects_released_default") is False

    # 1) blocked when side_effects_released != False
    res = accept_first_live_minimal_real_effect_controlled_trial_preparation_input(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_shadow_evaluation_gate_v0={"eval": "go"},
        controlled_trial_shadow_v0={"shadow": "executed"},
        controlled_trial_go_no_go_gate_v0={"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"},
        controlled_trial_admission_gate_v0={"controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"},
        real_write_go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        controlled_trial_enablement_dry_run_v0={"dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"},
        controlled_trial_first_minimal_real_enablement_v0={"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"},
        runtime_activation_stub_identity_v0={"id": "stub"},
        runtime_implementation_stub_identity_v0={"id": "stub"},
        controlled_trial_preparation_approval_or_signal_v0={"prep": True},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert res.get("status") == "blocked"
    assert res.get("side_effects_released") is False

    # 2) not_ready when no core objects exist (relevant-only)
    res = accept_first_live_minimal_real_effect_controlled_trial_preparation_input(
        controlled_trial_preparation_admission_gate_v0=None,
        controlled_trial_shadow_evaluation_gate_v0=None,
        controlled_trial_shadow_v0=None,
        controlled_trial_go_no_go_gate_v0=None,
        controlled_trial_admission_gate_v0=None,
        real_write_go_no_go_gate_v0=None,
        controlled_trial_enablement_dry_run_v0=None,
        controlled_trial_first_minimal_real_enablement_v0=None,
        runtime_activation_stub_identity_v0=None,
        runtime_implementation_stub_identity_v0=None,
        controlled_trial_preparation_approval_or_signal_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert res.get("status") == "not_ready"

    # 3) ready (placeholder-ready but not enabled)
    res = accept_first_live_minimal_real_effect_controlled_trial_preparation_input(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_shadow_evaluation_gate_v0={"eval": "go"},
        controlled_trial_shadow_v0={"shadow": "executed"},
        controlled_trial_go_no_go_gate_v0={"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"},
        controlled_trial_admission_gate_v0={"controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"},
        real_write_go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        controlled_trial_enablement_dry_run_v0={"dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"},
        controlled_trial_first_minimal_real_enablement_v0={"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"},
        runtime_activation_stub_identity_v0={"id": "stub"},
        runtime_implementation_stub_identity_v0={"id": "stub"},
        controlled_trial_preparation_approval_or_signal_v0={"prep": True, "reason": "unit_test"},
        side_effects_released=False,
        context={"test": "ready"},
    )
    assert res.get("status") == "ready"
    assert res.get("side_effects_released") is False

    # 4) placeholder calls remain inactive
    assert enter_first_live_controlled_trial_preparation_placeholder(context={"x": 1}).get("enter_status") == "inactive_placeholder"
    assert perform_first_live_controlled_trial_preparation_checks_placeholder(context={"x": 1}).get("checks_status") == "inactive_placeholder"
    assert exit_first_live_controlled_trial_preparation_placeholder(context={"x": 1}).get("exit_status") == "inactive_placeholder"
    assert raise_first_live_controlled_trial_preparation_exception(reason="x", context={"x": 1}).get("exception_status") == "inactive_placeholder"

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

