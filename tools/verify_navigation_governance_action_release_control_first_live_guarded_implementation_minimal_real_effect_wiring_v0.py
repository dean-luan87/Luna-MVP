# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Minimal Real-Effect Wiring v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity,
    )
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0,
    )

    ag_ok = {
        "approval_status": "first_live_enablement_approved",
    }
    ld_ok = {"launch_status": "first_live_launch_dry_run_ready"}
    lg_ok = {"live_release_status": "live_release_ready"}
    sg_ok = {"side_effect_release_status": "side_effect_release_ready"}
    ds_ok = {"simulation_status": "first_live_guarded_dry_effect_simulated"}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}
    stub_ok = get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()

    # A: all prerequisites + stub identity ok => wired_ready
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag_ok,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld_ok,
        navigation_governance_action_release_control_live_release_gate_v0=lg_ok,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=stub_ok,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("wiring_status") == "first_live_minimal_real_effect_wired_ready"
    assert payload.get("side_effects_released") is False

    # B: approval not approved => not_ready
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0={
            "approval_status": "first_live_enablement_not_approved",
        },
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld_ok,
        navigation_governance_action_release_control_live_release_gate_v0=lg_ok,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=stub_ok,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable2 is True
    assert payload2.get("wiring_status") == "first_live_minimal_real_effect_wired_not_ready"

    # C: stub identity scope mismatch => blocked
    bad_stub = dict(stub_ok)
    bad_stub["release_control_first_live_guarded_minimal_real_effect_stub_scope"] = "WRONG_SCOPE"
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag_ok,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld_ok,
        navigation_governance_action_release_control_live_release_gate_v0=lg_ok,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg_ok,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds_ok,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=bad_stub,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable3 is True
    assert payload3.get("wiring_status") == "first_live_minimal_real_effect_wired_blocked"

    # relevant-only: no core inputs and no stub => not applicable
    applicable4, payload4 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=None,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=None,
        navigation_governance_action_release_control_live_release_gate_v0=None,
        navigation_governance_action_release_control_side_effect_release_gate_v0=None,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=None,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=None,
        navigation_governance_action_release_control_execution_state_v0=None,
        navigation_governance_action_release_control_result_v0=None,
    )
    assert applicable4 is False
    assert payload4 is None

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
