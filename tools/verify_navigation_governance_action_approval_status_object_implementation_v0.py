# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Approval Status Object Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_approval_status_v0 import (
        evaluate_navigation_governance_action_approval_status_v0,
    )

    def approval(st: str) -> Dict[str, Any]:
        return {
            "governance_action_approval_attempted": True,
            "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
            "governance_action_approval_status": st,
            "reason": "test",
        }

    # A: minimal prerequisites satisfied => implemented object
    app, payload = evaluate_navigation_governance_action_approval_status_v0(
        navigation_governance_action_approval_boundary_v0=approval("approved_rollback"),
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("governance_action_approval_status_present") is True
    assert payload.get("governance_action_approval_status_scope") == "navigation_governance_action_approval_status_v0"
    assert payload.get("object_kind") == "implemented_v0"
    assert payload.get("consume_mode") == "implemented_object"
    asc = payload.get("approval_state_class") or {}
    assert asc.get("approval_state_fact") == "approved"
    aac = payload.get("approved_action_type_class") or {}
    assert aac.get("approved_action_type") == "rollback_request"

    # B: missing approval boundary => relevant-only
    assert (
        evaluate_navigation_governance_action_approval_status_v0(
            navigation_governance_action_approval_boundary_v0=None
        )
        == (False, None)
    )

    # C: blocked => still implemented object, but not \"approval chain executed\"
    app2, payload2 = evaluate_navigation_governance_action_approval_status_v0(
        navigation_governance_action_approval_boundary_v0=approval("approval_blocked"),
    )
    assert app2 is True
    asc2 = payload2.get("approval_state_class") or {}
    assert asc2.get("approval_state_fact") == "approval_blocked"
    bec2 = payload2.get("block_and_exception_class") or {}
    assert bec2.get("blocked") is True

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

