# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Code Path Dry-Run v0
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity,
    )

    lw = {"wiring_status": "first_live_minimal_real_effect_live_wired_ready"}
    ldr = {"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"}
    act_stub = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity()
    rp = {"rollout_plan_status": "frozen_placeholder"}
    gn_go = {"real_write_status": "first_live_minimal_real_effect_real_write_go"}
    gn_no = {"real_write_status": "first_live_minimal_real_effect_real_write_no_go"}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}
    ex_path = {"path": "present_placeholder"}

    # A: executed
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=ldr,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity_v0=act_stub,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0=rp,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=gn_go,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        exception_or_failure_path_v0=ex_path,
        side_effects_released=False,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("dry_run_status") == "first_live_minimal_real_effect_live_code_path_dry_run_executed"
    assert payload.get("side_effects_released") is False
    assert isinstance(payload.get("dry_run_trace"), dict)
    assert payload["dry_run_trace"]["code_path_order"][-1] == "perform_first_live_recover_side_effects_false_placeholder"

    # B: not_ready when gate not go
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=ldr,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity_v0=act_stub,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0=rp,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=gn_no,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        exception_or_failure_path_v0=ex_path,
        side_effects_released=False,
    )
    assert applicable2 is True
    assert isinstance(payload2, dict)
    assert payload2.get("dry_run_status") == "first_live_minimal_real_effect_live_code_path_dry_run_not_ready"

    # C: blocked when side_effects_released true
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=ldr,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity_v0=act_stub,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0=rp,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=gn_go,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        exception_or_failure_path_v0=ex_path,
        side_effects_released=True,
    )
    assert applicable3 is True
    assert isinstance(payload3, dict)
    assert payload3.get("dry_run_status") == "first_live_minimal_real_effect_live_code_path_dry_run_blocked"

    # relevant-only: none
    applicable4, payload4 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=None,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_first_real_write_rollout_plan_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=None,
        navigation_governance_action_release_control_execution_state_v0=None,
        navigation_governance_action_release_control_result_v0=None,
        exception_or_failure_path_v0=None,
        side_effects_released=None,
    )
    assert applicable4 is False
    assert payload4 is None

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

