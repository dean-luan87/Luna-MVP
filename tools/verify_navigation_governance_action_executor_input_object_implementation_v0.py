# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Executor Input Object Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_executor_input_v0 import (
        evaluate_navigation_governance_action_executor_input_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
        accept_governance_action_executor_input_object,
    )

    def approval(st: str) -> Dict[str, Any]:
        return {
            "governance_action_approval_attempted": True,
            "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
            "governance_action_approval_status": st,
            "reason": "test",
        }

    # A: minimal prerequisites satisfied => implemented object written
    app, payload = evaluate_navigation_governance_action_executor_input_v0(
        navigation_governance_action_approval_boundary_v0=approval("approved_rollback"),
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("governance_action_executor_input_scope") == "navigation_governance_action_executor_input_v0"
    assert payload.get("object_kind") == "implemented_v0"
    assert payload.get("consume_mode") == "implemented_object"
    assert (payload.get("approved_action_type_class") or {}).get("approved_action_type") == "rollback_request"
    assert (payload.get("execution_prerequisites_class") or {}).get("execution_prerequisites_ready") is False

    # B: missing approval boundary => relevant-only
    assert (
        evaluate_navigation_governance_action_executor_input_v0(
            navigation_governance_action_approval_boundary_v0=None
        )
        == (False, None)
    )

    # C: approval_blocked must NOT produce implemented input object
    assert (
        evaluate_navigation_governance_action_executor_input_v0(
            navigation_governance_action_approval_boundary_v0=approval("approval_blocked")
        )
        == (False, None)
    )

    # D: skeleton recognizes implemented input object
    r = accept_governance_action_executor_input_object(navigation_governance_action_executor_input_v0=payload)
    assert r.get("status") == "not_implemented"
    assert (r.get("payload") or {}).get("accepted") is True
    assert (r.get("payload") or {}).get("execute_attempted") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

