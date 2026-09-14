# -*- coding: utf-8 -*-
"""
Self-test: Release Control Status Placeholder v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_status_placeholder_v0 import (
        evaluate_navigation_governance_action_release_control_status_placeholder_v0,
    )

    def rc_inp() -> Dict[str, Any]:
        return {
            "release_control_input_present": True,
            "release_control_input_scope": "navigation_governance_action_release_control_input_v0",
            "object_kind": "placeholder_v0",
            "action_type_confirmed": "release_control",
            "consume_mode": "read_only",
        }

    def wg() -> Dict[str, Any]:
        return {
            "governance_action_executor_wiring_attempted": True,
            "governance_action_executor_wiring_scope": "navigation_governance_action_executor_wiring_v0",
            "governance_action_executor_wiring_status": "wired_inactive",
        }

    # A: minimal prerequisites satisfied => placeholder object
    app, payload = evaluate_navigation_governance_action_release_control_status_placeholder_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_executor_wiring_v0=wg(),
        navigation_governance_action_status_v0=None,
        navigation_governance_action_executor_readiness_gate_v0=None,
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("release_control_status_present") is True
    assert payload.get("release_control_status_scope") == "navigation_governance_action_release_control_status_v0"
    assert payload.get("action_type_confirmed") == "release_control"
    assert payload.get("consume_mode") == "read_only"
    assert str(payload.get("release_control_state") or "").endswith("_placeholder")

    # B: missing release_control input => relevant-only
    assert (
        evaluate_navigation_governance_action_release_control_status_placeholder_v0(
            navigation_governance_action_release_control_input_v0=None,
            navigation_governance_action_executor_wiring_v0=wg(),
        )
        == (False, None)
    )

    # C: mapping remains placeholder (does not pretend execution facts)
    app2, payload2 = evaluate_navigation_governance_action_release_control_status_placeholder_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_executor_wiring_v0=wg(),
    )
    assert app2 is True
    assert payload2.get("release_control_state") == "inactive_placeholder"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

