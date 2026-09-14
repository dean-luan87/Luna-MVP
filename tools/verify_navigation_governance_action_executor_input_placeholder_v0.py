# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Executor Input Object Placeholder v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_executor_input_placeholder_v0 import (
        evaluate_navigation_governance_action_executor_input_placeholder_v0,
    )

    def approval(st: str) -> Dict[str, Any]:
        return {
            "governance_action_approval_attempted": True,
            "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
            "governance_action_approval_status": st,
            "reason": "test",
        }

    # A: prerequisites satisfied => write
    app, payload = evaluate_navigation_governance_action_executor_input_placeholder_v0(
        navigation_governance_action_approval_boundary_v0=approval("approved_rollback"),
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("governance_action_executor_input_present") is True
    assert payload.get("governance_action_executor_input_scope") == "navigation_governance_action_executor_input_v0"
    assert payload.get("approved_action_type") == "rollback_request"
    assert payload.get("execution_prerequisites_ready") is False
    assert payload.get("consume_mode") == "read_only"

    # B: missing approval => relevant-only
    assert (
        evaluate_navigation_governance_action_executor_input_placeholder_v0(
            navigation_governance_action_approval_boundary_v0=None
        )
        == (False, None)
    )

    # C: mapping correctness + not immediately executable
    mapping = (
        ("approved_interrupt", "interrupt"),
        ("approved_release_control", "release_control"),
        ("approved_hold_executor_state", "hold"),
        ("approval_blocked", "hold"),
    )
    for st, want in mapping:
        a2, p2 = evaluate_navigation_governance_action_executor_input_placeholder_v0(
            navigation_governance_action_approval_boundary_v0=approval(st),
        )
        assert a2 is True
        assert p2.get("approved_action_type") == want
        assert p2.get("execution_prerequisites_ready") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

