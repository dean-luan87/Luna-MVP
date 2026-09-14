# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Shadow Trial v0 (observe-only).
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


def _mk_enablement_dry_run_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed"}


def _mk_real_enablement_ready() -> dict:
    return {"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"}


def _mk_xs() -> dict:
    return {"execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}


def _mk_rs() -> dict:
    return {"result_scope": "navigation_governance_action_release_control_result_v0"}


def _mk_ex() -> dict:
    return {"exception_or_failure_path_scope": "exception_or_failure_path_v0"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0,
    )

    # 1) relevant-only: no core objects
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
        controlled_trial_go_no_go_gate_v0=None,
        controlled_trial_enablement_dry_run_v0=None,
        controlled_trial_first_minimal_real_enablement_v0=None,
        shadow_trial_enable_signal_v0=None,
        execution_state_v0=None,
        result_v0=None,
        exception_or_failure_path_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    # 2) blocked: side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        shadow_trial_enable_signal_v0={"shadow": True},
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("shadow_trial_status") == "shadow_trial_blocked"

    # 3) not_ready: missing shadow trial signal (default-off)
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        shadow_trial_enable_signal_v0=None,
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("shadow_trial_status") == "shadow_trial_not_ready"
    assert payload.get("reason") == "missing_shadow_trial_enable_signal_v0"

    # 4) executed: all ready + no-op writers inside adapter
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
        controlled_trial_go_no_go_gate_v0=_mk_trial_go(),
        controlled_trial_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_real_enablement_ready(),
        shadow_trial_enable_signal_v0={"shadow": True, "reason": "unit_test"},
        execution_state_v0=_mk_xs(),
        result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        context={"test": "executed"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("shadow_trial_status") == "shadow_trial_executed"
    assert payload.get("would_have_written_execution_state") is True
    assert payload.get("would_have_written_result_object") is True
    assert payload.get("side_effects_released") is False

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

