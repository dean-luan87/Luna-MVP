# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Launch Dry-Run v0 (minimal implementation; non-action).
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_launch_dry_run_v0 as m

    base_guarded_stub = {"payload": {"live_stub_entered": True, "side_effects_released": False}}
    base_guarded_ident = {"can_enter_real_live_execution": False}
    base_exec_ident = {"can_execute_real_release_control": False}
    base_live_gate = {"live_release_status": "live_release_ready"}
    base_side_gate = {"side_effect_release_status": "side_effect_release_ready"}
    base_ag = {"approval_status": "first_live_enablement_approved"}
    base_xs = {"object_kind": "navigation_governance_action_release_control_execution_state_v0"}
    base_rs = {"object_kind": "navigation_governance_action_release_control_result_v0"}

    # A: all ready => launch ready; still locked
    app, payload = m.evaluate_navigation_governance_action_release_control_first_live_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=base_ag,
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0=base_guarded_stub,
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
    )
    assert app is True and isinstance(payload, dict)
    assert payload.get("launch_status") == "first_live_launch_dry_run_ready"
    assert payload.get("side_effects_released") is False

    # B: approval not approved => not_ready
    app2, payload2 = m.evaluate_navigation_governance_action_release_control_first_live_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0={"approval_status": "first_live_enablement_not_approved"},
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0=base_guarded_stub,
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
    )
    assert app2 is True and isinstance(payload2, dict)
    assert payload2.get("launch_status") == "first_live_launch_dry_run_not_ready"

    # C: candidate not entered => blocked
    app3, payload3 = m.evaluate_navigation_governance_action_release_control_first_live_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=base_ag,
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0={"payload": {"live_stub_entered": False, "side_effects_released": False}},
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
    )
    assert app3 is True and isinstance(payload3, dict)
    assert payload3.get("launch_status") == "first_live_launch_dry_run_blocked"

    # D: identity not conservative => blocked
    app4, payload4 = m.evaluate_navigation_governance_action_release_control_first_live_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=base_ag,
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0=base_guarded_stub,
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0={"can_enter_real_live_execution": True},
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
    )
    assert app4 is True and isinstance(payload4, dict)
    assert payload4.get("launch_status") == "first_live_launch_dry_run_blocked"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

