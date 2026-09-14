# -*- coding: utf-8 -*-
"""
Self-test: Release Control Input Contract Placeholder v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_input_placeholder_v0 import (
        evaluate_navigation_governance_action_release_control_input_placeholder_v0,
    )

    def inp(action_type: str) -> Dict[str, Any]:
        return {
            "governance_action_executor_input_present": True,
            "governance_action_executor_input_scope": "navigation_governance_action_executor_input_v0",
            "object_kind": "implemented_v0",
            "approved_action_type_class": {
                "approved_action_type": action_type,
                "approval_status": "approved_release_control",
            },
        }

    def rg() -> Dict[str, Any]:
        return {
            "governance_action_executor_readiness_attempted": True,
            "governance_action_executor_readiness_scope": "navigation_governance_action_executor_readiness_gate_v0",
            "governance_action_executor_readiness_status": "ready_candidate",
        }

    def wg() -> Dict[str, Any]:
        return {
            "governance_action_executor_wiring_attempted": True,
            "governance_action_executor_wiring_scope": "navigation_governance_action_executor_wiring_v0",
            "governance_action_executor_wiring_status": "wired_inactive",
        }

    # A: minimal prerequisites satisfied + action_type == release_control
    app, payload = evaluate_navigation_governance_action_release_control_input_placeholder_v0(
        navigation_governance_action_executor_input_v0=inp("release_control"),
        navigation_governance_action_executor_readiness_gate_v0=rg(),
        navigation_governance_action_executor_wiring_v0=wg(),
        navigation_governance_action_approval_status_v0=None,
        navigation_governance_action_status_v0=None,
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("release_control_input_present") is True
    assert payload.get("release_control_input_scope") == "navigation_governance_action_release_control_input_v0"
    assert payload.get("action_type_confirmed") == "release_control"
    assert payload.get("consume_mode") == "read_only"
    assert payload.get("execution_prerequisites_consistent") is False

    # B: action_type not release_control => relevant-only
    assert (
        evaluate_navigation_governance_action_release_control_input_placeholder_v0(
            navigation_governance_action_executor_input_v0=inp("rollback_request"),
            navigation_governance_action_executor_readiness_gate_v0=rg(),
            navigation_governance_action_executor_wiring_v0=wg(),
        )
        == (False, None)
    )

    # C: readiness/wiring only consistency; still conservative
    app2, payload2 = evaluate_navigation_governance_action_release_control_input_placeholder_v0(
        navigation_governance_action_executor_input_v0=inp("release_control"),
        navigation_governance_action_executor_readiness_gate_v0=rg(),
        navigation_governance_action_executor_wiring_v0=wg(),
    )
    assert app2 is True
    assert payload2.get("execution_prerequisites_consistent") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

