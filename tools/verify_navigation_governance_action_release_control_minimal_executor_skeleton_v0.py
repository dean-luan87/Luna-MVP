# -*- coding: utf-8 -*-
"""
Self-test: Release Control Minimal Executor Skeleton v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.governance.runtime.navigation_governance_action_release_control_minimal_executor_v0 as m

    # A: module import + identity fixed
    ident = m.get_release_control_minimal_executor_identity()
    assert isinstance(ident, dict)
    assert ident.get("is_skeleton") is True
    assert ident.get("can_execute_real_release_control") is False

    # B: input interface returns not_implemented and does not execute.
    out = m.accept_release_control_execution_input(
        navigation_governance_action_release_control_input_v0={"object_kind": "implemented_v0"},
        navigation_governance_action_release_control_readiness_gate_v0={"release_control_readiness_status": "ready_candidate"},
        navigation_governance_action_release_control_wiring_v0={"release_control_wiring_status": "wired_inactive"},
        navigation_governance_action_release_control_execution_state_v0={"object_kind": "implemented_v0"},
        navigation_governance_action_release_control_result_v0={"object_kind": "implemented_v0"},
    )
    assert isinstance(out, dict)
    assert out.get("status") == "not_implemented"
    assert out.get("payload", {}).get("execute_attempted") is False

    # C: execution state interface does not pretend real execution
    st = m.emit_release_control_execution_state()
    assert st.get("release_control_execution_state_present") is True
    assert st.get("release_control_execution_state") in {"inactive_placeholder"}

    # D: result object interface does not pretend real result
    rs = m.emit_release_control_result_object()
    assert rs.get("release_control_result_present") is True
    assert str(rs.get("release_control_result_state") or "").endswith("_placeholder")

    # E: exception interface reports placeholder and preserves error type/message
    exc = RuntimeError("x")
    rep = m.raise_release_control_execution_exception(exc=exc, context={"k": "v"})
    assert rep.get("release_control_execution_exception_present") is True
    assert rep.get("exception_status") == "reported_placeholder"
    assert rep.get("exception_type") == "RuntimeError"
    assert rep.get("exception_message") == "x"
    assert rep.get("context", {}).get("k") == "v"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

