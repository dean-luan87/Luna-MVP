# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Dry-Run Execution v0

Covers:
- Scenario A: wiring wired_ready + identities ok + state/result present => dry_run_executed
- Scenario B: wiring not ready => dry_run_not_ready
- Scenario C: missing stub identity => dry_run_blocked
- relevant-only: no core inputs => not applicable
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0,
    )

    lw_ready = {"wiring_status": "first_live_minimal_real_effect_live_wired_ready"}
    lw_not_ready = {"wiring_status": "first_live_minimal_real_effect_live_wired_not_ready"}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    sk = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity()
    stub = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity()

    # A
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw_ready,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=stub,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable is True
    assert isinstance(payload, dict)
    assert payload.get("execution_status") == "first_live_minimal_real_effect_live_dry_run_executed"
    assert payload.get("side_effects_released") is False
    assert isinstance(payload.get("execution_trace"), dict)

    # B
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw_not_ready,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=stub,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable2 is True
    assert isinstance(payload2, dict)
    assert payload2.get("execution_status") == "first_live_minimal_real_effect_live_dry_run_not_ready"

    # C
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw_ready,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=None,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    assert applicable3 is True
    assert isinstance(payload3, dict)
    assert payload3.get("execution_status") == "first_live_minimal_real_effect_live_dry_run_blocked"

    # relevant-only
    applicable4, payload4 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=None,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=None,
        release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=None,
        navigation_governance_action_release_control_execution_state_v0=None,
        navigation_governance_action_release_control_result_v0=None,
    )
    assert applicable4 is False
    assert payload4 is None

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

