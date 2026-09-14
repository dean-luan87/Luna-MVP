# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Skeleton v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 as m

    # A: import + identity fixed
    ident = m.get_release_control_first_live_guarded_implementation_skeleton_identity()
    assert ident.get("is_skeleton") is True
    assert ident.get("can_open_side_effects_released") is False
    assert ident.get("can_execute_real_release_control") is False

    # B: input interface never enables side effects
    out = m.accept_first_live_guarded_implementation_input(
        approval_gate_v0={"approval_status": "first_live_enablement_approved"},
        launch_dry_run_v0={"launch_status": "first_live_launch_dry_run_ready"},
        live_release_gate_v0={"live_release_status": "live_release_ready"},
        side_effect_release_gate_v0={"side_effect_release_status": "side_effect_release_ready"},
        guarded_live_stub_v0={"payload": {"live_stub_entered": True, "side_effects_released": False}},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        minimal_executor_identity_v0={"can_execute_real_release_control": False},
        context={"k": "v"},
    )
    assert out.get("status") in {"skeleton_inactive", "not_implemented"}
    assert out.get("payload", {}).get("side_effects_released") is False
    assert out.get("payload", {}).get("execute_attempted") is False

    # C: execution state placeholder-safe update
    xs = m.emit_first_live_execution_state_update(context={"k": "v"})
    assert xs.get("side_effects_released") is False
    assert xs.get("release_control_execution_state_fact") == "skeleton_inactive_no_progress"

    # D: result placeholder-safe update
    rs = m.emit_first_live_result_update(context={"k": "v"})
    assert rs.get("side_effects_released") is False
    assert rs.get("release_control_result_state_fact") == "skeleton_inactive_no_result"

    # E: failure/exit is placeholder-safe
    st = m.perform_first_live_failure_or_exit(reason="test", context={"why": "t"})
    assert st.get("side_effects_released") is False
    assert st.get("failure_or_exit_status") == "stop_safe_exit_safe_placeholder"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

