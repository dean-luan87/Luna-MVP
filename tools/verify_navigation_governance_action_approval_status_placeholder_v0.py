# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Approval Status Placeholder v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_approval_status_placeholder_v0 import (
        evaluate_navigation_governance_action_approval_status_placeholder_v0,
    )

    def approval(st: str) -> Dict[str, Any]:
        return {
            "governance_action_approval_attempted": True,
            "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
            "governance_action_approval_status": st,
            "reason": "test",
        }

    # A: minimal prerequisites satisfied => write
    app, payload = evaluate_navigation_governance_action_approval_status_placeholder_v0(
        navigation_governance_action_approval_boundary_v0=approval("approved_rollback"),
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("governance_action_approval_status_present") is True
    assert payload.get("governance_action_approval_status_scope") == "navigation_governance_action_approval_status_v0"
    assert payload.get("approval_state") == "approved_placeholder"
    assert payload.get("approved_action_type") == "rollback_request"
    assert payload.get("consume_mode") == "read_only"

    # B: missing approval boundary => relevant-only
    assert (
        evaluate_navigation_governance_action_approval_status_placeholder_v0(
            navigation_governance_action_approval_boundary_v0=None
        )
        == (False, None)
    )

    # C: blocked => placeholder blocked state
    _a2, p2 = evaluate_navigation_governance_action_approval_status_placeholder_v0(
        navigation_governance_action_approval_boundary_v0=approval("approval_blocked"),
    )
    assert _a2 is True
    assert p2.get("approval_state") == "approval_blocked_placeholder"
    assert p2.get("approved_action_type") == "hold"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

