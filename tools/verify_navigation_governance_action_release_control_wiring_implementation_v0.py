# -*- coding: utf-8 -*-
"""
Self-test: Release Control Wiring Minimal Implementation v0.
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

    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_wiring_v0 import (
        evaluate_navigation_governance_action_release_control_wiring_v0,
    )
    from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (
        wire_release_control,
    )

    def rc_inp() -> Dict[str, Any]:
        return {
            "release_control_input_present": True,
            "release_control_input_scope": "navigation_governance_action_release_control_input_v0",
            "object_kind": "implemented_v0",
            "action_type_confirm_class": {"action_type_confirmed": "release_control"},
        }

    def rc_status() -> Dict[str, Any]:
        return {
            "release_control_status_present": True,
            "release_control_status_scope": "navigation_governance_action_release_control_status_v0",
            "object_kind": "implemented_v0",
            "action_type_class": {"action_type_confirmed": "release_control"},
        }

    def rc_rg(status: str = "ready_candidate") -> Dict[str, Any]:
        return {
            "release_control_readiness_attempted": True,
            "release_control_readiness_scope": "navigation_governance_action_release_control_readiness_gate_v0",
            "release_control_readiness_status": status,
        }

    # A: core objects present + ready_candidate + identity OK => wired_inactive or wired_action_ready
    app, payload = evaluate_navigation_governance_action_release_control_wiring_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_release_control_status_v0=rc_status(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg("ready_candidate"),
        navigation_governance_action_executor_wiring_v0=None,
        navigation_governance_action_approval_status_v0=None,
    )
    assert app is True
    assert payload.get("release_control_wiring_scope") == "navigation_governance_action_release_control_wiring_v0"
    assert payload.get("release_control_wiring_status") in ("wired_inactive", "wired_action_ready")

    # Skeleton recognize-only
    r = wire_release_control(navigation_governance_action_release_control_wiring_v0=payload)
    assert isinstance(r, dict)
    assert r.get("status") == "not_implemented"
    rp = r.get("payload") or {}
    assert rp.get("execute_attempted") is False

    # B: missing input + missing readiness => relevant-only
    assert (
        evaluate_navigation_governance_action_release_control_wiring_v0(
            navigation_governance_action_release_control_input_v0=None,
            navigation_governance_action_release_control_status_v0=None,
            navigation_governance_action_release_control_readiness_gate_v0=None,
        )
        == (False, None)
    )

    # C: identity mismatch => blocked
    with patch(
        "capabilities.mid_platform.runtime.navigation_governance_action_release_control_wiring_v0._get_release_control_identity",
        return_value={
            "release_control_action_identity": "wrong",
            "is_skeleton": True,
            "can_execute_real_release_control": False,
        },
    ):
        appc, payloadc = evaluate_navigation_governance_action_release_control_wiring_v0(
            navigation_governance_action_release_control_input_v0=rc_inp(),
            navigation_governance_action_release_control_status_v0=rc_status(),
            navigation_governance_action_release_control_readiness_gate_v0=rc_rg("ready_candidate"),
        )
        assert appc is True
        assert payloadc.get("release_control_wiring_status") == "blocked"

    # D: input/status mismatch => blocked
    bad_status = dict(rc_status())
    bad_status["action_type_class"] = {"action_type_confirmed": "interrupt"}
    appd, payloadd = evaluate_navigation_governance_action_release_control_wiring_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_release_control_status_v0=bad_status,
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg("ready_candidate"),
    )
    assert appd is True
    assert payloadd.get("release_control_wiring_status") == "blocked"

    # E: readiness not ready_candidate => not_applicable
    appe, payloade = evaluate_navigation_governance_action_release_control_wiring_v0(
        navigation_governance_action_release_control_input_v0=rc_inp(),
        navigation_governance_action_release_control_status_v0=rc_status(),
        navigation_governance_action_release_control_readiness_gate_v0=rc_rg("not_ready"),
    )
    assert appe is True
    assert payloade.get("release_control_wiring_status") == "not_applicable"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

