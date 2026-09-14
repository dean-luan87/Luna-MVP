# -*- coding: utf-8 -*-
"""
Self-test: Release Control Status Object Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_status_v0 import (
        evaluate_navigation_governance_action_release_control_status_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (
        accept_release_control_status_object,
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

    # A: minimal prerequisites satisfied => implemented object
    app, payload = evaluate_navigation_governance_action_release_control_status_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_executor_wiring_v0=wg(),
        navigation_governance_action_status_v0=None,
        navigation_governance_action_executor_readiness_gate_v0=None,
    )
    assert app is True
    assert isinstance(payload, dict)
    assert payload.get("release_control_status_present") is True
    assert payload.get("release_control_status_scope") == "navigation_governance_action_release_control_status_v0"
    assert payload.get("object_kind") == "implemented_v0"
    assert payload.get("consume_mode") == "implemented_object"
    atc = payload.get("action_type_class") or {}
    assert atc.get("action_type_confirmed") == "release_control"
    sac = payload.get("sub_action_state_class") or {}
    assert sac.get("release_control_state_fact") == "not_started"

    # Skeleton recognize-only can accept implemented object (still non-action)
    r = accept_release_control_status_object(navigation_governance_action_release_control_status_v0=payload)
    assert isinstance(r, dict)
    assert r.get("status") == "not_implemented"
    rp = r.get("payload") or {}
    assert rp.get("accepted") is True
    assert rp.get("execute_attempted") is False

    # B: missing release_control input => relevant-only
    assert (
        evaluate_navigation_governance_action_release_control_status_v0(
            navigation_governance_action_release_control_input_v0=None,
            navigation_governance_action_executor_wiring_v0=wg(),
        )
        == (False, None)
    )

    # C: action type confirmed
    app2, payload2 = evaluate_navigation_governance_action_release_control_status_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_executor_wiring_v0=wg(),
    )
    assert app2 is True
    assert (payload2.get("action_type_class") or {}).get("action_type_confirmed") == "release_control"
    # Must not pretend action executed
    assert (payload2.get("sub_action_state_class") or {}).get("release_control_state_fact") == "not_started"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

