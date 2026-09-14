# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Boundary Minimal Implementation v0.

Hard boundary:
- This test only validates mapping + relevant-only behavior.
- It must not trigger any real governance actions.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional


def _mk_decision(status: str) -> Dict[str, Any]:
    return {
        "governance_decision_attempted": True,
        "governance_decision_scope": "navigation_rollback_and_interruption_governance_decision_v0",
        "governance_decision_status": str(status),
        "reason": "test",
    }


def _assert_payload(payload: Optional[Dict[str, Any]], expected: str) -> None:
    assert isinstance(payload, dict)
    assert payload.get("governance_action_boundary_attempted") is True
    assert payload.get("governance_action_boundary_scope") == "navigation_governance_action_boundary_v0"
    assert payload.get("governance_action_boundary_status") == expected
    r = str(payload.get("reason") or "")
    assert r


def main() -> int:
    # Allow running as a standalone script from repo root.
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.mid_platform.runtime.navigation_governance_action_boundary_v0 import (
        evaluate_navigation_governance_action_boundary_v0,
    )

    # A: recommend_rollback -> request_rollback
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=_mk_decision("recommend_rollback")
    )
    assert app is True
    _assert_payload(payload, "request_rollback")

    # B: recommend_release_control -> request_release_control
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=_mk_decision("recommend_release_control")
    )
    assert app is True
    _assert_payload(payload, "request_release_control")

    # C: recommend_interrupt -> request_interrupt
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=_mk_decision("recommend_interrupt")
    )
    assert app is True
    _assert_payload(payload, "request_interrupt")

    # D: hold_for_governance -> hold_executor_state
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=_mk_decision("hold_for_governance")
    )
    assert app is True
    _assert_payload(payload, "hold_executor_state")

    # E: governance_decision_blocked -> action_blocked
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=_mk_decision("governance_decision_blocked")
    )
    assert app is True
    _assert_payload(payload, "action_blocked")

    # F: missing decision => relevant-only (do not write)
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=None
    )
    assert app is False
    assert payload is None

    # F2: invalid decision scope => relevant-only
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0={
            "governance_decision_scope": "wrong_scope",
            "governance_decision_status": "recommend_rollback",
        }
    )
    assert app is False
    assert payload is None

    # Sanity: unknown decision status => action_blocked
    app, payload = evaluate_navigation_governance_action_boundary_v0(
        navigation_rollback_and_interruption_governance_decision_v0=_mk_decision("recommend_magic")
    )
    assert app is True
    _assert_payload(payload, "action_blocked")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

