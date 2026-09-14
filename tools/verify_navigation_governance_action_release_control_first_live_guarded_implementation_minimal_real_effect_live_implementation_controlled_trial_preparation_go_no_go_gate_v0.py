# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Preparation Go/No-Go Gate v0 (non-effect).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def main() -> int:
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0,
    )

    # 0) relevant-only
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_evaluation_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_activation_stub_identity_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_implementation_stub_identity_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_signal_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    base_kwargs = dict(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_evaluation_gate_v0={
            "controlled_trial_preparation_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_admission_gate_v0={
            "controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_dry_run_v0={
            "dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0={
            "controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_admission_gate_v0={
            "controlled_trial_status": "first_live_minimal_real_effect_controlled_trial_admitted"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0={
            "real_write_status": "first_live_minimal_real_effect_real_write_go"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0={
            "real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_activation_stub_identity_v0={
            "id": "act_stub"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_runtime_implementation_stub_identity_v0={
            "id": "impl_stub"
        },
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_signal_v0={
            "sig": True
        },
    )

    # 1) blocked when side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0(
        **base_kwargs,
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_preparation_go_no_go_status") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_blocked"
    )

    # 2) no_go when missing signal
    kwargs2 = dict(base_kwargs)
    kwargs2["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_signal_v0"] = None
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0(
        **kwargs2,
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_preparation_go_no_go_status") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_no_go"
    )

    # 3) go when all satisfied
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_go_no_go_gate_v0(
        **base_kwargs,
        side_effects_released=False,
        context={"test": "go"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("controlled_trial_preparation_go_no_go_status") == (
        "first_live_minimal_real_effect_controlled_trial_preparation_go"
    )
    assert payload.get("side_effects_released") is False

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

