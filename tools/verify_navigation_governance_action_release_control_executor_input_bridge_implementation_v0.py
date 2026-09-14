# -*- coding: utf-8 -*-
"""
Self-test: Release Control Executor Input Bridge Minimal Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_executor_input_bridge_v0 import (
        evaluate_navigation_governance_action_release_control_executor_input_bridge_v0,
    )

    def rc_input() -> Dict[str, Any]:
        return {
            "release_control_input_present": True,
            "release_control_input_scope": "navigation_governance_action_release_control_input_v0",
            "object_kind": "implemented_v0",
            "action_type_confirmed": "release_control",
        }

    def rc_xs() -> Dict[str, Any]:
        return {
            "release_control_execution_state_present": True,
            "release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0",
            "object_kind": "implemented_v0",
            "action_type_class": {"action_type_confirmed": "release_control"},
            "execution_state_class": {"release_control_execution_state_fact": "not_started"},
        }

    def rc_rs() -> Dict[str, Any]:
        return {
            "release_control_result_present": True,
            "release_control_result_scope": "navigation_governance_action_release_control_result_v0",
            "object_kind": "implemented_v0",
            "action_type_class": {"action_type_confirmed": "release_control"},
            "result_state_class": {"release_control_result_state_fact": "not_executed"},
        }

    def rc_rg_ready() -> Dict[str, Any]:
        return {
            "release_control_readiness_attempted": True,
            "release_control_readiness_scope": "navigation_governance_action_release_control_readiness_gate_v0",
            "release_control_readiness_status": "ready_candidate",
        }

    def rc_rg_not_ready() -> Dict[str, Any]:
        x = rc_rg_ready()
        x["release_control_readiness_status"] = "not_ready"
        return x

    def rc_wiring_ok() -> Dict[str, Any]:
        return {
            "release_control_wiring_attempted": True,
            "release_control_wiring_scope": "navigation_governance_action_release_control_wiring_v0",
            "release_control_wiring_status": "wired_inactive",
        }

    def rc_wiring_bad() -> Dict[str, Any]:
        x = rc_wiring_ok()
        x["release_control_wiring_status"] = "blocked"
        return x

    def min_exec_ident_ok() -> Dict[str, Any]:
        return {
            "release_control_minimal_executor_identity": "navigation_governance_action_release_control_minimal_executor_v0",
            "release_control_minimal_executor_scope": "navigation_governance_action_release_control_minimal_executor_v0",
            "is_skeleton": True,
            "can_execute_real_release_control": False,
        }

    def min_exec_ident_bad() -> Dict[str, Any]:
        x = min_exec_ident_ok()
        x["release_control_minimal_executor_scope"] = "other"
        return x

    # A: all ready -> bridge ready but consumable_by_executor remains false
    app, payload = evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
        navigation_governance_action_release_control_input_v0=rc_input(),
        navigation_governance_action_release_control_execution_state_v0=rc_xs(),
        navigation_governance_action_release_control_result_v0=rc_rs(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg_ready(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring_ok(),
        release_control_minimal_executor_identity=min_exec_ident_ok(),
    )
    assert app is True
    assert payload["bridge_status"] == "executor_input_bridge_ready"
    assert payload["consumable_by_executor"] is False

    # B: missing core -> not_ready
    app2, payload2 = evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
        navigation_governance_action_release_control_input_v0=None,
        navigation_governance_action_release_control_execution_state_v0=rc_xs(),
        navigation_governance_action_release_control_result_v0=rc_rs(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg_ready(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring_ok(),
        release_control_minimal_executor_identity=min_exec_ident_ok(),
    )
    assert app2 is True
    assert payload2["bridge_status"] == "executor_input_bridge_not_ready"

    # C: readiness not ready -> not_ready
    app3, payload3 = evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
        navigation_governance_action_release_control_input_v0=rc_input(),
        navigation_governance_action_release_control_execution_state_v0=rc_xs(),
        navigation_governance_action_release_control_result_v0=rc_rs(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg_not_ready(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring_ok(),
        release_control_minimal_executor_identity=min_exec_ident_ok(),
    )
    assert app3 is True
    assert payload3["bridge_status"] == "executor_input_bridge_not_ready"

    # D: wiring bad -> blocked
    app4, payload4 = evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
        navigation_governance_action_release_control_input_v0=rc_input(),
        navigation_governance_action_release_control_execution_state_v0=rc_xs(),
        navigation_governance_action_release_control_result_v0=rc_rs(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg_ready(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring_bad(),
        release_control_minimal_executor_identity=min_exec_ident_ok(),
    )
    assert app4 is True
    assert payload4["bridge_status"] == "executor_input_bridge_blocked"

    # E: identity mismatch -> blocked
    app5, payload5 = evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
        navigation_governance_action_release_control_input_v0=rc_input(),
        navigation_governance_action_release_control_execution_state_v0=rc_xs(),
        navigation_governance_action_release_control_result_v0=rc_rs(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg_ready(),
        navigation_governance_action_release_control_wiring_v0=rc_wiring_ok(),
        release_control_minimal_executor_identity=min_exec_ident_bad(),
    )
    assert app5 is True
    assert payload5["bridge_status"] == "executor_input_bridge_blocked"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

