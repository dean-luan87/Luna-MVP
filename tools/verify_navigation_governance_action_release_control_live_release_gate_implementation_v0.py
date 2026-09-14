# -*- coding: utf-8 -*-
"""
Self-test: Release Control Live Release Gate Minimal Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_live_release_gate_v0 import (
        evaluate_navigation_governance_action_release_control_live_release_gate_v0,
    )

    def bridge_ready() -> Dict[str, Any]:
        return {
            "release_control_executor_input_bridge_attempted": True,
            "release_control_executor_input_bridge_scope": "navigation_governance_action_release_control_executor_input_bridge_v0",
            "bridge_status": "executor_input_bridge_ready",
            "consumable_by_executor": False,
        }

    def bridge_not_ready() -> Dict[str, Any]:
        x = bridge_ready()
        x["bridge_status"] = "executor_input_bridge_not_ready"
        return x

    def guarded_stub_entered_locked() -> Dict[str, Any]:
        return {
            "ok": False,
            "result_scope": "navigation_governance_action_release_control_guarded_live_stub_v0",
            "status": "guarded_not_implemented",
            "reason": "x",
            "payload": {
                "live_stub_entered": True,
                "side_effects_released": False,
            },
        }

    def guarded_stub_not_entered() -> Dict[str, Any]:
        x = guarded_stub_entered_locked()
        x["payload"]["live_stub_entered"] = False
        return x

    def xs_present() -> Dict[str, Any]:
        return {"release_control_execution_state_present": True}

    def rs_present() -> Dict[str, Any]:
        return {"release_control_result_present": True}

    def guarded_ident_ok() -> Dict[str, Any]:
        return {"can_enter_real_live_execution": False}

    def exec_ident_ok() -> Dict[str, Any]:
        return {"can_execute_real_release_control": False}

    # A: all prereqs => ready but side_effects_released false
    app, payload = evaluate_navigation_governance_action_release_control_live_release_gate_v0(
        navigation_governance_action_release_control_executor_input_bridge_v0=bridge_ready(),
        navigation_governance_action_release_control_guarded_live_stub_v0=guarded_stub_entered_locked(),
        navigation_governance_action_release_control_execution_state_v0=xs_present(),
        navigation_governance_action_release_control_result_v0=rs_present(),
        navigation_governance_action_release_control_guarded_live_identity_v0=guarded_ident_ok(),
        navigation_governance_action_release_control_minimal_executor_identity_v0=exec_ident_ok(),
    )
    assert app is True
    assert payload["live_release_status"] == "live_release_ready"
    assert payload["side_effects_released"] is False

    # B: bridge not ready => not_ready
    _, p2 = evaluate_navigation_governance_action_release_control_live_release_gate_v0(
        navigation_governance_action_release_control_executor_input_bridge_v0=bridge_not_ready(),
        navigation_governance_action_release_control_guarded_live_stub_v0=guarded_stub_entered_locked(),
        navigation_governance_action_release_control_execution_state_v0=xs_present(),
        navigation_governance_action_release_control_result_v0=rs_present(),
        navigation_governance_action_release_control_guarded_live_identity_v0=guarded_ident_ok(),
        navigation_governance_action_release_control_minimal_executor_identity_v0=exec_ident_ok(),
    )
    assert p2["live_release_status"] == "live_release_not_ready"

    # C: guarded candidate not entered => blocked
    _, p3 = evaluate_navigation_governance_action_release_control_live_release_gate_v0(
        navigation_governance_action_release_control_executor_input_bridge_v0=bridge_ready(),
        navigation_governance_action_release_control_guarded_live_stub_v0=guarded_stub_not_entered(),
        navigation_governance_action_release_control_execution_state_v0=xs_present(),
        navigation_governance_action_release_control_result_v0=rs_present(),
        navigation_governance_action_release_control_guarded_live_identity_v0=guarded_ident_ok(),
        navigation_governance_action_release_control_minimal_executor_identity_v0=exec_ident_ok(),
    )
    assert p3["live_release_status"] == "live_release_blocked"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

