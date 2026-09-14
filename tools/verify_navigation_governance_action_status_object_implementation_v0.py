# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Status Object Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_status_v0 import (
        evaluate_navigation_governance_action_status_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
        accept_governance_action_status_object,
    )

    def boundary(status: str) -> Dict[str, Any]:
        return {
            "governance_action_boundary_attempted": True,
            "governance_action_boundary_scope": "navigation_governance_action_boundary_v0",
            "governance_action_boundary_status": status,
            "reason": "test",
        }

    # A: implemented object
    app, payload = evaluate_navigation_governance_action_status_v0(
        navigation_governance_action_boundary_v0=boundary("request_rollback"),
    )
    assert app is True
    assert payload.get("object_kind") == "implemented_v0"
    assert payload.get("consume_mode") == "implemented_object"
    esc = payload.get("action_state_class") or {}
    assert esc.get("execution_fact") == "not_started"
    at = payload.get("action_type_class") or {}
    assert at.get("action_type_fact") == "rollback_request"

    # B: missing boundary
    assert evaluate_navigation_governance_action_status_v0(navigation_governance_action_boundary_v0=None) == (False, None)

    # C: mapping
    _a, p2 = evaluate_navigation_governance_action_status_v0(
        navigation_governance_action_boundary_v0=boundary("request_interrupt"),
    )
    assert (p2.get("action_type_class") or {}).get("action_type_fact") == "interrupt"
    assert (p2.get("action_state_class") or {}).get("execution_fact") == "not_started"

    # D: skeleton recognizes implemented object
    r = accept_governance_action_status_object(navigation_governance_action_status_v0=payload)
    assert r.get("status") == "not_implemented"
    assert (r.get("payload") or {}).get("accepted") is True
    assert (r.get("payload") or {}).get("execute_attempted") is False

    r2 = accept_governance_action_status_object(navigation_governance_action_status_v0={"object_kind": "placeholder"})
    assert (r2.get("payload") or {}).get("accepted") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
