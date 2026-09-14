# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Release Control Skeleton v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime import navigation_governance_action_release_control_v0 as mod

    # A: import + identity fixed
    ident = mod.get_release_control_identity()
    assert isinstance(ident, dict)
    assert ident.get("release_control_action_identity") == "navigation_governance_action_release_control_v0"
    assert ident.get("is_skeleton") is True
    assert ident.get("can_execute_real_release_control") is False

    # B: input interface does not execute
    r = mod.accept_release_control_input(release_control_input={"object_kind": "implemented_v0"})
    assert isinstance(r, dict)
    assert r.get("result_scope") == "navigation_governance_action_release_control_v0"
    assert r.get("status") == "not_implemented"
    payload = r.get("payload") or {}
    assert payload.get("execute_attempted") is False

    # C: status interface does not pretend runtime state
    st = mod.emit_release_control_status()
    assert isinstance(st, dict)
    assert st.get("release_control_status_present") is True
    assert st.get("release_control_status_scope") == "navigation_governance_action_release_control_status_v0"
    assert st.get("release_control_execution_state") in ("inactive_placeholder", "idle_placeholder")

    # D: exception interface returns standardized placeholder result
    ex = mod.raise_release_control_exception(exc=ValueError("boom"), context={"k": "v"})
    assert isinstance(ex, dict)
    assert ex.get("release_control_exception_present") is True
    assert ex.get("release_control_exception_scope") == "navigation_governance_action_release_control_exception_v0"
    assert ex.get("exception_status") == "reported_placeholder"
    assert ex.get("exception_type") == "ValueError"
    assert ex.get("context") == {"k": "v"}

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

