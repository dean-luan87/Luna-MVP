# -*- coding: utf-8 -*-
"""
Self-test: Release Control Guarded Live Stub v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.governance.runtime.navigation_governance_action_release_control_guarded_live_stub_v0 as m

    # A: module import + identity fixed
    ident = m.get_release_control_guarded_live_identity()
    assert isinstance(ident, dict)
    assert ident.get("is_stub") is True
    assert ident.get("can_enter_real_live_execution") is False
    assert ident.get("can_execute_real_release_control") is False

    # B: input interface must not release side effects
    out = m.accept_guarded_live_input(
        executor_input_bridge_v0={
            "release_control_executor_input_bridge_scope": "navigation_governance_action_release_control_executor_input_bridge_v0",
            "bridge_status": "executor_input_bridge_ready",
            "consumable_by_executor": False,
        }
    )
    assert out.get("status") == "guarded_not_implemented"
    assert out.get("payload", {}).get("live_stub_entered") is True
    assert out.get("payload", {}).get("side_effects_released") is False
    assert out.get("payload", {}).get("entered_real_live_execution") is False

    # C: execution state safe update
    xs = m.emit_guarded_execution_state_update()
    assert xs.get("release_control_execution_state_present") is True
    assert xs.get("release_control_execution_state_fact") == "guarded_not_started_safe"

    # D: result safe update
    rs = m.emit_guarded_result_update()
    assert rs.get("release_control_result_present") is True
    assert rs.get("release_control_result_state_fact") == "guarded_not_executed_safe"

    # E: exception path preserves semantics
    rep = m.raise_guarded_live_exception(exc=RuntimeError("x"), context={"k": "v"})
    assert rep.get("exception_status") == "reported_placeholder"
    assert rep.get("exception_type") == "RuntimeError"
    assert rep.get("exception_message") == "x"
    assert rep.get("context", {}).get("k") == "v"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

