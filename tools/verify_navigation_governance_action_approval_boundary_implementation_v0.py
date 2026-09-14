# -*- coding: utf-8 -*-
"""Self-test: Navigation Governance Action Approval Boundary Minimal Implementation v0."""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.mid_platform.runtime.navigation_governance_action_approval_boundary_v0 import (
        evaluate_navigation_governance_action_approval_boundary_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
        accept_governance_action_approval_boundary,
    )

    def boundary(status: str) -> Dict[str, Any]:
        return {
            "governance_action_boundary_attempted": True,
            "governance_action_boundary_scope": "navigation_governance_action_boundary_v0",
            "governance_action_boundary_status": status,
            "reason": "test",
        }

    # A–E mapping
    cases = (
        ("request_rollback", "approved_rollback"),
        ("request_release_control", "approved_release_control"),
        ("request_interrupt", "approved_interrupt"),
        ("hold_executor_state", "approved_hold_executor_state"),
        ("action_blocked", "approval_blocked"),
    )
    for bs, want in cases:
        app, payload = evaluate_navigation_governance_action_approval_boundary_v0(
            navigation_governance_action_boundary_v0=boundary(bs),
        )
        assert app is True
        assert payload.get("governance_action_approval_scope") == "navigation_governance_action_approval_boundary_v0"
        assert payload.get("governance_action_approval_status") == want

    # F: no boundary
    assert evaluate_navigation_governance_action_approval_boundary_v0(
        navigation_governance_action_boundary_v0=None,
    ) == (False, None)

    # unknown status -> approval_blocked
    app_u, p_u = evaluate_navigation_governance_action_approval_boundary_v0(
        navigation_governance_action_boundary_v0=boundary("weird_unknown"),
    )
    assert app_u is True
    assert p_u.get("governance_action_approval_status") == "approval_blocked"

    # D: executor recognizes
    _, pl = evaluate_navigation_governance_action_approval_boundary_v0(
        navigation_governance_action_boundary_v0=boundary("request_rollback"),
    )
    r = accept_governance_action_approval_boundary(navigation_governance_action_approval_boundary_v0=pl)
    assert r.get("status") == "not_implemented"
    assert (r.get("payload") or {}).get("accepted") is True
    assert (r.get("payload") or {}).get("execute_attempted") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
