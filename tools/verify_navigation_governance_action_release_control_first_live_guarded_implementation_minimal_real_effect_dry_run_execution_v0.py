# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Minimal Real-Effect Dry-Run Execution v0.
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
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0,
    )

    wired_ready = {
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_minimal_real_effect_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0",
        "wiring_status": "first_live_minimal_real_effect_wired_ready",
        "side_effects_released": False,
        "reason": "test",
    }
    wired_not = dict(wired_ready)
    wired_not["wiring_status"] = "first_live_minimal_real_effect_wired_not_ready"

    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}
    stub_ok = get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()

    # A: wired_ready + stub + state/result => dry_run_executed
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=wired_ready,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=stub_ok,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("execution_status") == "first_live_minimal_real_effect_dry_run_executed"
    assert payload.get("side_effects_released") is False
    et = payload.get("execution_trace") or {}
    assert et.get("execution_chain_order") == [
        "execution_state_real_write_placeholder_call",
        "result_object_real_write_placeholder_call",
        "failure_or_exception_real_write_placeholder_closure",
    ]

    # B: wiring not ready => not_ready
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=wired_not,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=stub_ok,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable2 is True
    assert payload2.get("execution_status") == "first_live_minimal_real_effect_dry_run_not_ready"

    # C: stub scope mismatch => blocked
    bad_stub = dict(stub_ok)
    bad_stub["release_control_first_live_guarded_minimal_real_effect_stub_scope"] = "WRONG"
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=wired_ready,
        release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=bad_stub,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable3 is True
    assert payload3.get("execution_status") == "first_live_minimal_real_effect_dry_run_blocked"

    # relevant-only: no metadata core => not applicable
    applicable4, payload4 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=None,
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
