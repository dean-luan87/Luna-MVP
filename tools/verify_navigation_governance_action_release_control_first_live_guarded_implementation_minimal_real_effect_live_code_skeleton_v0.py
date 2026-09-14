# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Minimal Code Skeleton v0
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_skeleton_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_live_code_input,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_skeleton_identity,
        perform_first_live_exception_or_failure_real_write_placeholder,
        perform_first_live_execution_state_real_write_placeholder,
        perform_first_live_recover_side_effects_false_placeholder,
        perform_first_live_result_object_real_write_placeholder,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_skeleton_identity()
    assert ident.get("is_skeleton") is True
    assert ident.get("is_live_code_skeleton") is True
    assert ident.get("side_effects_released") is False
    assert ident.get("can_open_side_effects_released") is False

    out = accept_first_live_minimal_real_effect_live_code_input(
        real_write_go_no_go_gate_v0={"gate": "frozen_placeholder"},
        rollout_plan_v0={"plan": "frozen_placeholder"},
        live_implementation_wiring_v0={"wiring_status": "first_live_minimal_real_effect_live_wired_ready"},
        live_implementation_dry_run_execution_v0={"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"},
        live_runtime_activation_stub_identity_v0={"is_live_runtime_activation_stub": True},
        execution_state_v0={"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"},
        result_v0={"release_control_result_scope": "navigation_governance_action_release_control_result_v0"},
        exception_or_failure_path_v0={"path": "present_placeholder"},
        side_effects_released=False,
        context={"t": "x"},
    )
    assert isinstance(out, dict)
    assert out.get("status") == "live_code_skeleton_inactive"
    assert out.get("payload", {}).get("side_effects_released") is False
    assert out.get("payload", {}).get("entered_real_write") is False

    s1 = perform_first_live_execution_state_real_write_placeholder()
    assert s1.get("side_effects_released") is False
    r1 = perform_first_live_result_object_real_write_placeholder()
    assert r1.get("side_effects_released") is False
    e1 = perform_first_live_exception_or_failure_real_write_placeholder(reason="x")
    assert e1.get("side_effects_released") is False
    rec = perform_first_live_recover_side_effects_false_placeholder(reason="x")
    assert rec.get("side_effects_released") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

