# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Enablement Approval Gate v0 (minimal implementation; non-action).
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_enablement_approval_gate_v0 as g

    base_guarded_stub = {"payload": {"live_stub_entered": True, "side_effects_released": False}}
    base_guarded_ident = {"can_enter_real_live_execution": False}
    base_exec_ident = {"can_execute_real_release_control": False}
    base_live_gate = {"live_release_status": "live_release_ready"}
    base_side_gate = {"side_effect_release_status": "side_effect_release_ready"}
    base_xs = {"object_kind": "navigation_governance_action_release_control_execution_state_v0"}
    base_rs = {"object_kind": "navigation_governance_action_release_control_result_v0"}

    # A: all ready + approval granted => approved; still locked
    ok_app, ok_payload = g.evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_dry_run_v0={"dry_run_status": "enablement_dry_run_ready"},
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0=base_guarded_stub,
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
        release_control_first_live_enablement_approval_signal_v0={"approved": True},
    )
    assert ok_app is True and isinstance(ok_payload, dict)
    assert ok_payload.get("approval_status") == "first_live_enablement_approved"
    assert ok_payload.get("side_effects_released") is False

    # B: dry-run not ready => not_approved
    b_app, b_payload = g.evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_dry_run_v0={"dry_run_status": "enablement_dry_run_not_ready"},
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0=base_guarded_stub,
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
        release_control_first_live_enablement_approval_signal_v0={"approved": True},
    )
    assert b_app is True and isinstance(b_payload, dict)
    assert b_payload.get("approval_status") == "first_live_enablement_not_approved"

    # C: candidate not entered => blocked
    c_app, c_payload = g.evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_dry_run_v0={"dry_run_status": "enablement_dry_run_ready"},
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0={"payload": {"live_stub_entered": False, "side_effects_released": False}},
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
        release_control_first_live_enablement_approval_signal_v0={"approved": True},
    )
    assert c_app is True and isinstance(c_payload, dict)
    assert c_payload.get("approval_status") == "first_live_enablement_blocked"

    # D: approval signal missing => not_approved
    d_app, d_payload = g.evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_dry_run_v0={"dry_run_status": "enablement_dry_run_ready"},
        navigation_governance_action_release_control_live_release_gate_v0=base_live_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=base_side_gate,
        navigation_governance_action_release_control_guarded_live_stub_v0=base_guarded_stub,
        navigation_governance_action_release_control_execution_state_v0=base_xs,
        navigation_governance_action_release_control_result_v0=base_rs,
        navigation_governance_action_release_control_guarded_live_identity_v0=base_guarded_ident,
        navigation_governance_action_release_control_minimal_executor_identity_v0=base_exec_ident,
        release_control_first_live_enablement_approval_signal_v0=None,
    )
    assert d_app is True and isinstance(d_payload, dict)
    assert d_payload.get("approval_status") == "first_live_enablement_not_approved"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

