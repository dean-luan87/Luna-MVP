# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation Minimal Real-Effect Stub v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0 as m

    # A: import + identity fixed
    ident = m.get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()
    assert ident.get("is_stub") is True
    assert ident.get("is_real_effect_stub") is True
    assert ident.get("can_open_side_effects_released") is False
    assert ident.get("can_real_write_execution_state") is False

    # B: input interface never enables side effects
    out = m.accept_first_live_guarded_minimal_real_effect_input(
        minimal_real_effect_plan_v0={"scope": "plan_v0"},
        wiring_v0={"scope": "wiring_v0"},
        non_effect_execution_v0={"scope": "non_effect_execution_v0"},
        dry_effect_simulation_v0={"scope": "dry_effect_simulation_v0"},
        approval_gate_v0={"approval_status": "first_live_enablement_approved"},
        launch_dry_run_v0={"launch_status": "first_live_launch_dry_run_ready"},
        live_release_gate_v0={"live_release_status": "live_release_ready"},
        side_effect_release_gate_v0={"side_effect_release_status": "side_effect_release_ready"},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        context={"k": "v"},
    )
    assert out.get("status") in {"real_effect_stub_inactive", "not_implemented"}
    assert out.get("payload", {}).get("side_effects_released") is False

    # C: execution state real-write placeholder does not write real state
    xs = m.write_first_live_execution_state_real_effect(context={"k": "v"})
    assert xs.get("side_effects_released") is False
    assert xs.get("release_control_execution_state_fact") == "minimal_real_effect_stub_no_real_write"

    # D: result real-write placeholder does not write real result
    rs = m.write_first_live_result_object_real_effect(context={"k": "v"})
    assert rs.get("side_effects_released") is False
    assert rs.get("release_control_result_state_fact") == "minimal_real_effect_stub_no_real_write"

    # E: failure/exception placeholder is stop-safe/reported-placeholder
    st = m.write_first_live_failure_or_exception_real_effect(reason="test", context={"why": "t"})
    assert st.get("side_effects_released") is False
    assert st.get("failure_or_exception_status") == "stop_safe_reported_placeholder"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

