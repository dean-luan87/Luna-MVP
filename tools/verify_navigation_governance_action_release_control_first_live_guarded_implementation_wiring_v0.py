# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Wiring v0 (non-effect wiring).
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
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0,
    )

    # Common ready objects (minimal shapes matching existing gates)
    approval_gate = {"approval_status": "first_live_enablement_approved"}
    launch_dry_run = {"launch_status": "first_live_launch_dry_run_ready"}
    live_release_gate = {"live_release_status": "live_release_ready"}
    side_effect_release_gate = {"side_effect_release_status": "side_effect_release_ready"}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    # A: all ready => wired_ready written, but side_effects_released remains false
    md = {
        "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0": approval_gate,
        "navigation_governance_action_release_control_first_live_launch_dry_run_v0": launch_dry_run,
        "navigation_governance_action_release_control_live_release_gate_v0": live_release_gate,
        "navigation_governance_action_release_control_side_effect_release_gate_v0": side_effect_release_gate,
        "navigation_governance_action_release_control_execution_state_v0": xs,
        "navigation_governance_action_release_control_result_v0": rs,
    }
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=md.get(
            "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"
        ),
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=md.get(
            "navigation_governance_action_release_control_first_live_launch_dry_run_v0"
        ),
        navigation_governance_action_release_control_live_release_gate_v0=md.get(
            "navigation_governance_action_release_control_live_release_gate_v0"
        ),
        navigation_governance_action_release_control_side_effect_release_gate_v0=md.get(
            "navigation_governance_action_release_control_side_effect_release_gate_v0"
        ),
        release_control_first_live_guarded_implementation_skeleton_identity_v0=get_release_control_first_live_guarded_implementation_skeleton_identity(),
        navigation_governance_action_release_control_execution_state_v0=md.get(
            "navigation_governance_action_release_control_execution_state_v0"
        ),
        navigation_governance_action_release_control_result_v0=md.get(
            "navigation_governance_action_release_control_result_v0"
        ),
    )
    assert applicable is True
    assert isinstance(payload, dict)
    md["navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"] = payload
    w = md.get("navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0")
    assert isinstance(w, dict)
    assert w.get("wiring_status") == "first_live_guarded_wired_ready"
    assert w.get("side_effects_released") is False

    # B: approval missing => wired_not_ready
    md2 = {
        "navigation_governance_action_release_control_first_live_launch_dry_run_v0": launch_dry_run,
        "navigation_governance_action_release_control_live_release_gate_v0": live_release_gate,
        "navigation_governance_action_release_control_side_effect_release_gate_v0": side_effect_release_gate,
        "navigation_governance_action_release_control_execution_state_v0": xs,
        "navigation_governance_action_release_control_result_v0": rs,
    }
    applicable2, payload2 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=md2.get(
            "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"
        ),
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=md2.get(
            "navigation_governance_action_release_control_first_live_launch_dry_run_v0"
        ),
        navigation_governance_action_release_control_live_release_gate_v0=md2.get(
            "navigation_governance_action_release_control_live_release_gate_v0"
        ),
        navigation_governance_action_release_control_side_effect_release_gate_v0=md2.get(
            "navigation_governance_action_release_control_side_effect_release_gate_v0"
        ),
        release_control_first_live_guarded_implementation_skeleton_identity_v0=get_release_control_first_live_guarded_implementation_skeleton_identity(),
        navigation_governance_action_release_control_execution_state_v0=md2.get(
            "navigation_governance_action_release_control_execution_state_v0"
        ),
        navigation_governance_action_release_control_result_v0=md2.get(
            "navigation_governance_action_release_control_result_v0"
        ),
    )
    assert applicable2 is True
    assert isinstance(payload2, dict)
    md2["navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"] = payload2
    w2 = md2.get("navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0")
    assert isinstance(w2, dict)
    assert w2.get("wiring_status") == "first_live_guarded_wired_not_ready"
    assert w2.get("side_effects_released") is False

    # C: skeleton identity mismatch => wired_blocked
    applicable3, payload3 = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=approval_gate,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=launch_dry_run,
        navigation_governance_action_release_control_live_release_gate_v0=live_release_gate,
        navigation_governance_action_release_control_side_effect_release_gate_v0=side_effect_release_gate,
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
    assert payload3.get("wiring_status") == "first_live_guarded_wired_blocked"
    assert payload3.get("side_effects_released") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

