# -*- coding: utf-8 -*-
"""
Self-test: Release Control Minimal Runtime Stub v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.governance.runtime.navigation_governance_action_release_control_minimal_runtime_stub_v0 as m

    # A: module import + identity fixed
    ident = m.get_release_control_minimal_runtime_identity()
    assert isinstance(ident, dict)
    assert ident.get("is_stub") is True
    assert ident.get("can_enter_real_runtime") is False
    assert ident.get("can_execute_real_release_control") is False

    # B: runtime input interface must not enter runtime
    out = m.accept_release_control_runtime_input(
        executor_input_bridge_v0={
            "release_control_executor_input_bridge_scope": "navigation_governance_action_release_control_executor_input_bridge_v0",
            "bridge_status": "executor_input_bridge_ready",
            "consumable_by_executor": False,
        }
    )
    assert out.get("status") == "not_implemented"
    assert out.get("payload", {}).get("entered_runtime") is False
    assert out.get("payload", {}).get("execute_attempted") is False

    # C: execution state update interface returns safe placeholder
    xs = m.emit_runtime_execution_state_update()
    assert xs.get("release_control_execution_state_present") is True
    assert xs.get("release_control_execution_state_fact") == "not_started_safe"

    # D: result update interface returns safe placeholder
    rs = m.emit_runtime_result_update()
    assert rs.get("release_control_result_present") is True
    assert rs.get("release_control_result_state_fact") == "not_executed_safe"

    # E: exception interface preserves error semantics
    rep = m.raise_runtime_execution_exception(exc=RuntimeError("x"), context={"k": "v"})
    assert rep.get("exception_status") == "reported_placeholder"
    assert rep.get("exception_type") == "RuntimeError"
    assert rep.get("exception_message") == "x"
    assert rep.get("context", {}).get("k") == "v"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

