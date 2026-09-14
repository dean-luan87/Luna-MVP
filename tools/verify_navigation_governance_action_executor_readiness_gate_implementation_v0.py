# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Executor Readiness Gate Minimal Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.mid_platform.runtime.navigation_governance_action_executor_readiness_gate_v0 import (
        evaluate_navigation_governance_action_executor_readiness_gate_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
        get_governance_action_executor_identity,
    )

    def inp(approval_status: str, approved_action_type: str) -> Dict[str, Any]:
        return {
            "governance_action_executor_input_present": True,
            "governance_action_executor_input_scope": "navigation_governance_action_executor_input_v0",
            "object_kind": "implemented_v0",
            "approved_action_type_class": {
                "approved_action_type": approved_action_type,
                "approval_scope": "navigation_governance_action_approval_boundary_v0",
                "approval_status": approval_status,
            },
            "execution_constraints_class": {"constraint_profile": "minimal_safe_constraints_v0"},
        }

    def action_status() -> Dict[str, Any]:
        return {
            "governance_action_status_present": True,
            "governance_action_status_scope": "navigation_governance_action_status_v0",
            "object_kind": "implemented_v0",
        }

    def approval_status_obj(approval_status: str, approved_action_type: str) -> Dict[str, Any]:
        return {
            "governance_action_approval_status_present": True,
            "governance_action_approval_status_scope": "navigation_governance_action_approval_status_v0",
            "object_kind": "implemented_v0",
            "approved_action_type_class": {"approved_action_type": approved_action_type},
            "approval_state_class": {"approval_status": approval_status},
        }

    # Sanity: skeleton identity exists and matches expectation.
    ident = get_governance_action_executor_identity()
    assert isinstance(ident, dict)
    assert ident.get("governance_action_executor_identity") == "navigation_governance_action_executor_v0"
    assert ident.get("is_skeleton") is True

    # A: all objects present + consistent + identity OK => ready_candidate
    app, payload = evaluate_navigation_governance_action_executor_readiness_gate_v0(
        navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
        navigation_governance_action_status_v0=action_status(),
        navigation_governance_action_approval_status_v0=approval_status_obj("approved_rollback", "rollback_request"),
        navigation_governance_action_approval_boundary_v0={
            "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
            "governance_action_approval_attempted": True,
            "governance_action_approval_status": "approved_rollback",
        },
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("governance_action_executor_readiness_scope") == "navigation_governance_action_executor_readiness_gate_v0"
    assert payload.get("governance_action_executor_readiness_status") == "ready_candidate"

    # B: missing executor input object => relevant-only
    assert (
        evaluate_navigation_governance_action_executor_readiness_gate_v0(
            navigation_governance_action_executor_input_v0=None,
            navigation_governance_action_status_v0=action_status(),
            navigation_governance_action_approval_status_v0=approval_status_obj("approved_rollback", "rollback_request"),
        )
        == (False, None)
    )

    # C: skeleton identity mismatch => blocked (simulate by giving invalid identity via monkeypatch-like: not possible here)
    # We instead assert that if identity is unreadable, it blocks: call with scope mismatch input but keep applicable true.
    # For this minimal test, we check a hard-consistency block path (D) and surface-not-ready path (E) instead.

    # D: approval status vs input object mismatch => blocked
    app4, payload4 = evaluate_navigation_governance_action_executor_readiness_gate_v0(
        navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
        navigation_governance_action_status_v0=action_status(),
        navigation_governance_action_approval_status_v0=approval_status_obj("approved_interrupt", "interrupt"),
    )
    assert app4 is True
    assert payload4.get("governance_action_executor_readiness_status") == "blocked"

    # E: status return surface not ready => not_ready
    app5, payload5 = evaluate_navigation_governance_action_executor_readiness_gate_v0(
        navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
        navigation_governance_action_status_v0=None,
        navigation_governance_action_approval_status_v0=approval_status_obj("approved_rollback", "rollback_request"),
    )
    assert app5 is True
    assert payload5.get("governance_action_executor_readiness_status") == "not_ready"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

