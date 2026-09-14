# -*- coding: utf-8 -*-
"""
Self-test: Minimal Real-Effect Live Implementation Shadow Integration v0 (observe-only).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_go() -> dict:
    return {"real_write_status": "first_live_minimal_real_effect_real_write_go"}


def _mk_cpd_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"}


def _mk_xs() -> dict:
    return {"execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}


def _mk_rs() -> dict:
    return {"result_scope": "navigation_governance_action_release_control_result_v0"}


def _mk_ex() -> dict:
    return {"exception_or_failure_path_scope": "exception_or_failure_path_v0"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0,
    )

    # 1) relevant-only: no core objects -> not applicable
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0=None,
        navigation_governance_action_release_control_execution_state_v0=None,
        navigation_governance_action_release_control_result_v0=None,
        exception_or_failure_path_v0=None,
        side_effects_released=False,
        context={"test": "relevant_only"},
    )
    assert applicable is False and payload is None

    # 2) blocked: side_effects_released != False
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=_mk_cpd_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0={"shadow_enable": True},
        navigation_governance_action_release_control_execution_state_v0=_mk_xs(),
        navigation_governance_action_release_control_result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("shadow_status") == "shadow_blocked"

    # 3) not_ready: missing shadow signal (default-off)
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=_mk_cpd_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0=None,
        navigation_governance_action_release_control_execution_state_v0=_mk_xs(),
        navigation_governance_action_release_control_result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("shadow_status") == "shadow_not_ready"
    assert payload.get("reason") == "missing_shadow_enable_signal_v0"

    # 4) executed: all ready + no-op writers inside adapter
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=_mk_go(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=_mk_cpd_executed(),
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0={
            "shadow_enable": True,
            "reason": "unit_test",
        },
        navigation_governance_action_release_control_execution_state_v0=_mk_xs(),
        navigation_governance_action_release_control_result_v0=_mk_rs(),
        exception_or_failure_path_v0=_mk_ex(),
        side_effects_released=False,
        context={"test": "executed"},
    )
    assert applicable is True and isinstance(payload, dict)
    assert payload.get("shadow_status") == "shadow_executed"
    assert payload.get("would_have_written_execution_state") is True
    assert payload.get("would_have_written_result_object") is True
    assert payload.get("side_effects_released") is False

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

