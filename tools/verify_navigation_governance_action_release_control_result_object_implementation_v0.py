# -*- coding: utf-8 -*-
"""
Self-test: Release Control Result Object Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_result_v0 import (
        evaluate_navigation_governance_action_release_control_result_v0,
    )

    def rc_status_impl() -> Dict[str, Any]:
        return {
            "release_control_status_present": True,
            "release_control_status_scope": "navigation_governance_action_release_control_status_v0",
            "object_kind": "implemented_v0",
            "action_type_class": {"action_type_confirmed": "release_control"},
        }

    def rc_status_placeholder() -> Dict[str, Any]:
        return {
            "release_control_status_present": True,
            "release_control_status_scope": "navigation_governance_action_release_control_status_v0",
            "object_kind": "placeholder_v0",
            "action_type_class": {"action_type_confirmed": "release_control"},
        }

    def rc_wiring() -> Dict[str, Any]:
        return {
            "release_control_wiring_attempted": True,
            "release_control_wiring_scope": "navigation_governance_action_release_control_wiring_v0",
            "release_control_wiring_status": "wired_inactive",
        }

    # A: minimal prerequisites satisfied => implemented result object
    app, payload = evaluate_navigation_governance_action_release_control_result_v0(
        navigation_governance_action_release_control_status_v0=rc_status_impl(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring(),
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("release_control_result_present") is True
    assert payload.get("release_control_result_scope") == "navigation_governance_action_release_control_result_v0"
    assert payload.get("object_kind") == "implemented_v0"
    assert payload.get("consume_mode") == "implemented_object"
    assert payload.get("action_type_class", {}).get("action_type_confirmed") == "release_control"
    assert payload.get("result_state_class", {}).get("release_control_result_state_fact") == "not_executed"

    # Must NOT look like placeholder or completed/failed facts.
    assert "placeholder" not in str(payload.get("result_state_class", {}).get("release_control_result_state_fact") or "")
    assert payload.get("result_state_class", {}).get("release_control_result_state_fact") not in {
        "completed",
        "failed",
        "blocked",
    }

    # B: missing status => relevant-only
    assert (
        evaluate_navigation_governance_action_release_control_result_v0(
            navigation_governance_action_release_control_status_v0=None,
            navigation_governance_action_release_control_wiring_v0=rc_wiring(),
        )
        == (False, None)
    )

    # C: status not implemented => relevant-only (do not promote from placeholder)
    assert (
        evaluate_navigation_governance_action_release_control_result_v0(
            navigation_governance_action_release_control_status_v0=rc_status_placeholder(),
            navigation_governance_action_release_control_wiring_v0=rc_wiring(),
        )
        == (False, None)
    )

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

