# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Minimal Non-Effect Execution v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_skeleton_identity,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0,
    )

    wiring_ready = {
        "release_control_first_live_guarded_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0",
        "wiring_status": "first_live_guarded_wired_ready",
        "side_effects_released": False,
        "reason": "test_ready",
    }
    wiring_not_ready = {
        "release_control_first_live_guarded_implementation_wiring_attempted": True,
        "release_control_first_live_guarded_implementation_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0",
        "wiring_status": "first_live_guarded_wired_not_ready",
        "side_effects_released": False,
        "reason": "test_not_ready",
    }
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    # A: wiring ready + identity ok + state/result present => executed
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0=wiring_ready,
        release_control_first_live_guarded_implementation_skeleton_identity_v0=get_release_control_first_live_guarded_implementation_skeleton_identity(),
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("execution_status") == "first_live_guarded_non_effect_executed"
    assert payload.get("side_effects_released") is False
    tr = payload.get("execution_trace") or {}
    assert tr.get("execution_chain_order") == [
        "execution_state_placeholder_update",
        "result_placeholder_update",
        "failure_or_exit_placeholder_closure",
    ]

    # B: wiring not ready => not_ready
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0=wiring_not_ready,
        release_control_first_live_guarded_implementation_skeleton_identity_v0=get_release_control_first_live_guarded_implementation_skeleton_identity(),
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable2 is True
    assert isinstance(payload2, dict)
    assert payload2.get("execution_status") == "first_live_guarded_non_effect_not_ready"
    assert payload2.get("side_effects_released") is False

    # C: skeleton identity mismatch => blocked
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0=wiring_ready,
        release_control_first_live_guarded_implementation_skeleton_identity_v0={
            "is_skeleton": True,
            "can_open_side_effects_released": False,
            "can_execute_real_release_control": False,
            "release_control_first_live_guarded_implementation_skeleton_scope": "WRONG_SCOPE",
        },
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable3 is True
    assert isinstance(payload3, dict)
    assert payload3.get("execution_status") == "first_live_guarded_non_effect_blocked"
    assert payload3.get("side_effects_released") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

