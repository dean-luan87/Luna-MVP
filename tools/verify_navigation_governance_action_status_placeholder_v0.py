# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Status Placeholder v0.

Hard boundary:
- Validates read-only placeholder behavior only; must not imply real governance execution.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_status_placeholder_v0 import (
        evaluate_navigation_governance_action_status_placeholder_v0,
    )

    def boundary(status: str) -> Dict[str, Any]:
        return {
            "governance_action_boundary_attempted": True,
            "governance_action_boundary_scope": "navigation_governance_action_boundary_v0",
            "governance_action_boundary_status": status,
            "reason": "test",
        }

    # A: minimal prerequisites satisfied -> write-shaped payload
    app, payload = evaluate_navigation_governance_action_status_placeholder_v0(
        navigation_governance_action_boundary_v0=boundary("request_rollback"),
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("governance_action_status_present") is True
    assert payload.get("governance_action_status_scope") == "navigation_governance_action_status_v0"
    assert payload.get("action_type") == "rollback_request"
    assert payload.get("action_state") == "idle_placeholder"
    assert payload.get("consume_mode") == "read_only"

    # B: missing boundary -> relevant-only
    app2, payload2 = evaluate_navigation_governance_action_status_placeholder_v0(
        navigation_governance_action_boundary_v0=None,
    )
    assert app2 is False
    assert payload2 is None

    # B2: invalid boundary scope
    app3, payload3 = evaluate_navigation_governance_action_status_placeholder_v0(
        navigation_governance_action_boundary_v0={"governance_action_boundary_scope": "wrong"},
    )
    assert app3 is False
    assert payload3 is None

    # C: mapping + placeholder only (not executed)
    for st, want_type in (
        ("request_interrupt", "interrupt"),
        ("request_release_control", "release_control"),
        ("hold_executor_state", "hold"),
        ("action_blocked", "hold"),
    ):
        _a, p = evaluate_navigation_governance_action_status_placeholder_v0(
            navigation_governance_action_boundary_v0=boundary(st),
        )
        assert _a is True
        assert p.get("action_type") == want_type
        assert p.get("action_state") == "idle_placeholder"
        assert p.get("action_effect_state") == "unknown_not_applied"

    blocked = evaluate_navigation_governance_action_status_placeholder_v0(
        navigation_governance_action_boundary_v0=boundary("action_blocked"),
    )[1]
    assert blocked.get("action_block_state") == "blocked_placeholder"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
