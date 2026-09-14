# -*- coding: utf-8 -*-
"""
Self-test: Release Control Execution State Placeholder v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_execution_state_placeholder_v0 import (
        evaluate_navigation_governance_action_release_control_execution_state_placeholder_v0,
    )

    def rc_status() -> Dict[str, Any]:
        return {
            "release_control_status_present": True,
            "release_control_status_scope": "navigation_governance_action_release_control_status_v0",
            "object_kind": "implemented_v0",
            "action_type_class": {"action_type_confirmed": "release_control"},
        }

    def rc_wiring() -> Dict[str, Any]:
        return {
            "release_control_wiring_attempted": True,
            "release_control_wiring_scope": "navigation_governance_action_release_control_wiring_v0",
            "release_control_wiring_status": "wired_inactive",
        }

    # A: minimal prerequisites satisfied => placeholder execution state
    app, payload = evaluate_navigation_governance_action_release_control_execution_state_placeholder_v0(
        navigation_governance_action_release_control_status_v0=rc_status(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring(),
        navigation_governance_action_release_control_result_v0=None,
        navigation_governance_action_release_control_readiness_gate_v0=None,
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("release_control_execution_state_present") is True
    assert (
        payload.get("release_control_execution_state_scope")
        == "navigation_governance_action_release_control_execution_state_v0"
    )
    assert payload.get("consume_mode") == "read_only"
    assert str(payload.get("release_control_execution_state") or "").endswith("_placeholder")

    # B: missing status => relevant-only
    assert (
        evaluate_navigation_governance_action_release_control_execution_state_placeholder_v0(
            navigation_governance_action_release_control_status_v0=None,
            navigation_governance_action_release_control_wiring_v0=rc_wiring(),
        )
        == (False, None)
    )

    # C: placeholder-only; must not pretend executing/completed_candidate/failed facts.
    app2, payload2 = evaluate_navigation_governance_action_release_control_execution_state_placeholder_v0(
        navigation_governance_action_release_control_status_v0=rc_status(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring(),
    )
    assert app2 is True
    assert payload2.get("release_control_execution_state") == "not_started_placeholder"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

