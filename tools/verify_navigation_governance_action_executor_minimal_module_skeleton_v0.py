# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Executor Minimal Module Skeleton v0.

Hard boundary:
- This test only validates skeleton identity + placeholder behavior.
- It must not trigger any real governance actions.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    # Allow running as a standalone script from repo root.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime import navigation_governance_action_executor_v0 as mod

    # A: module import + identity fixed
    ident = mod.get_governance_action_executor_identity()
    assert isinstance(ident, dict)
    assert ident.get("governance_action_executor_identity") == "navigation_governance_action_executor_v0"
    assert ident.get("is_skeleton") is True
    assert ident.get("can_execute_real_actions") is False
    assert ident.get("can_self_authorize_action") is False

    # B: accept input interface does not execute real actions
    boundary_obj: Dict[str, Any] = {
        "governance_action_boundary_attempted": True,
        "governance_action_boundary_scope": "navigation_governance_action_boundary_v0",
        "governance_action_boundary_status": "request_rollback",
        "reason": "test",
    }
    r = mod.accept_governance_action_boundary(approved_action_boundary_v0=boundary_obj)
    assert isinstance(r, dict)
    assert r.get("result_scope") == "navigation_governance_action_boundary_v0"
    assert r.get("status") == "not_implemented"
    payload = r.get("payload")
    assert isinstance(payload, dict)
    assert payload.get("execute_attempted") is False
    assert payload.get("accepted") is True

    # C: status interface does not pretend to be real runtime state
    st = mod.emit_governance_action_status()
    assert isinstance(st, dict)
    assert st.get("governance_action_status_present") is True
    assert st.get("governance_action_status_scope") == "navigation_governance_action_status_v0"
    assert st.get("action_execution_state") in ("idle_placeholder", "inactive_placeholder")

    # D: exception interface returns standardized placeholder result
    ex = mod.raise_governance_action_exception(exc=ValueError("boom"), context={"k": "v"})
    assert isinstance(ex, dict)
    assert ex.get("governance_action_exception_present") is True
    assert ex.get("governance_action_exception_scope") == "navigation_governance_action_exception_v0"
    assert ex.get("exception_status") == "reported_placeholder"
    assert ex.get("exception_type") == "ValueError"
    assert ex.get("context") == {"k": "v"}

    # E: wiring recognition (non-action)
    w = mod.wire_governance_action_executor(
        navigation_governance_action_executor_wiring_v0={
            "governance_action_executor_wiring_attempted": True,
            "governance_action_executor_wiring_scope": "navigation_governance_action_executor_wiring_v0",
            "governance_action_executor_wiring_status": "wired_inactive",
            "reason": "test",
        }
    )
    assert isinstance(w, dict)
    assert w.get("result_scope") == "navigation_governance_action_executor_wiring_v0"
    assert w.get("status") == "not_implemented"
    wp = w.get("payload")
    assert isinstance(wp, dict)
    assert wp.get("execute_attempted") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

