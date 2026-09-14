# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action Executor Wiring Minimal Implementation v0.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict
from unittest.mock import patch


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.mid_platform.runtime.navigation_governance_action_executor_wiring_v0 import (
        evaluate_navigation_governance_action_executor_wiring_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (
        wire_governance_action_executor,
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

    def rg(status: str) -> Dict[str, Any]:
        return {
            "governance_action_executor_readiness_attempted": True,
            "governance_action_executor_readiness_scope": "navigation_governance_action_executor_readiness_gate_v0",
            "governance_action_executor_readiness_status": status,
            "reason": "test",
        }

    ap_b_ok = {
        "governance_action_approval_scope": "navigation_governance_action_approval_boundary_v0",
        "governance_action_approval_attempted": True,
        "governance_action_approval_status": "approved_rollback",
    }

    # A: full chain + ready_candidate + boundary consistent => wired_action_ready (narrow) or wired_inactive
    app, payload = evaluate_navigation_governance_action_executor_wiring_v0(
        navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
        navigation_governance_action_status_v0=action_status(),
        navigation_governance_action_approval_status_v0=approval_status_obj("approved_rollback", "rollback_request"),
        navigation_governance_action_executor_readiness_gate_v0=rg("ready_candidate"),
        navigation_governance_action_approval_boundary_v0=ap_b_ok,
    )
    assert app is True
    assert payload.get("governance_action_executor_wiring_scope") == "navigation_governance_action_executor_wiring_v0"
    assert payload.get("governance_action_executor_wiring_status") in ("wired_inactive", "wired_action_ready")
    wr = wire_governance_action_executor(navigation_governance_action_executor_wiring_v0=payload)
    assert wr.get("status") == "not_implemented"
    pld = wr.get("payload") or {}
    assert pld.get("execute_attempted") is False

    # B: no input, no readiness => relevant-only
    assert evaluate_navigation_governance_action_executor_wiring_v0(
        navigation_governance_action_executor_input_v0=None,
        navigation_governance_action_status_v0=None,
        navigation_governance_action_approval_status_v0=None,
        navigation_governance_action_executor_readiness_gate_v0=None,
    ) == (False, None)

    # C: identity mismatch => blocked
    with patch(
        "capabilities.mid_platform.runtime.navigation_governance_action_executor_wiring_v0._get_executor_identity",
        return_value={"governance_action_executor_identity": "wrong", "is_skeleton": True, "can_execute_real_actions": False},
    ):
        app_c, payload_c = evaluate_navigation_governance_action_executor_wiring_v0(
            navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
            navigation_governance_action_status_v0=action_status(),
            navigation_governance_action_approval_status_v0=approval_status_obj("approved_rollback", "rollback_request"),
            navigation_governance_action_executor_readiness_gate_v0=rg("ready_candidate"),
            navigation_governance_action_approval_boundary_v0=ap_b_ok,
        )
        assert app_c is True
        assert payload_c.get("governance_action_executor_wiring_status") == "blocked"

    # D: mismatch => blocked
    app_d, payload_d = evaluate_navigation_governance_action_executor_wiring_v0(
        navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
        navigation_governance_action_status_v0=action_status(),
        navigation_governance_action_approval_status_v0=approval_status_obj("approved_interrupt", "interrupt"),
        navigation_governance_action_executor_readiness_gate_v0=rg("ready_candidate"),
        navigation_governance_action_approval_boundary_v0=ap_b_ok,
    )
    assert app_d is True
    assert payload_d.get("governance_action_executor_wiring_status") == "blocked"

    # E: readiness not ready_candidate => not_applicable
    app_e, payload_e = evaluate_navigation_governance_action_executor_wiring_v0(
        navigation_governance_action_executor_input_v0=inp("approved_rollback", "rollback_request"),
        navigation_governance_action_status_v0=action_status(),
        navigation_governance_action_approval_status_v0=approval_status_obj("approved_rollback", "rollback_request"),
        navigation_governance_action_executor_readiness_gate_v0=rg("not_ready"),
        navigation_governance_action_approval_boundary_v0=ap_b_ok,
    )
    assert app_e is True
    assert payload_e.get("governance_action_executor_wiring_status") == "not_applicable"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
