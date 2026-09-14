# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Dry-Effect Simulation v0.
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
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0,
    )

    executed = {
        "release_control_first_live_guarded_implementation_non_effect_execution_attempted": True,
        "release_control_first_live_guarded_implementation_non_effect_execution_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0",
        "execution_status": "first_live_guarded_non_effect_executed",
        "side_effects_released": False,
        "reason": "test_executed",
    }
    not_executed = {
        "release_control_first_live_guarded_implementation_non_effect_execution_attempted": True,
        "release_control_first_live_guarded_implementation_non_effect_execution_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0",
        "execution_status": "first_live_guarded_non_effect_not_ready",
        "side_effects_released": False,
        "reason": "test_not_ready",
    }
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    # A: executed + identity ok + state/result present => simulated, targets only allowed 3
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0=executed,
        release_control_first_live_guarded_implementation_skeleton_identity_v0=get_release_control_first_live_guarded_implementation_skeleton_identity(),
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("simulation_status") == "first_live_guarded_dry_effect_simulated"
    assert payload.get("side_effects_released") is False
    targets = payload.get("simulation_targets")
    assert targets == [
        "execution_state_update_target",
        "result_object_update_target",
        "failure_or_exception_path_target",
    ]

    # B: not executed => not_ready
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0=not_executed,
        release_control_first_live_guarded_implementation_skeleton_identity_v0=get_release_control_first_live_guarded_implementation_skeleton_identity(),
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable2 is True
    assert isinstance(payload2, dict)
    assert payload2.get("simulation_status") == "first_live_guarded_dry_effect_not_ready"
    assert payload2.get("side_effects_released") is False

    # C: skeleton identity mismatch => blocked
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0=executed,
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
    assert payload3.get("simulation_status") == "first_live_guarded_dry_effect_blocked"
    assert payload3.get("side_effects_released") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

