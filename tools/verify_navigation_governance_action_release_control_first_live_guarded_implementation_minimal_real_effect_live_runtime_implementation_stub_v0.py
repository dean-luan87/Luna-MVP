# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Minimal Runtime Implementation Stub v0
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_implementation_stub_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_runtime_implementation_input,
        enter_first_live_runtime_implementation_placeholder,
        exit_first_live_runtime_implementation_placeholder,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_implementation_stub_identity,
        perform_first_live_runtime_exception_or_failure_placeholder,
        perform_first_live_runtime_execution_state_placeholder,
        perform_first_live_runtime_result_placeholder,
        raise_first_live_minimal_real_effect_runtime_implementation_stub_exception,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_implementation_stub_identity()
    assert ident.get("is_stub") is True
    assert ident.get("is_live_runtime_implementation_stub") is True
    assert ident.get("side_effects_released") is False

    out = accept_first_live_minimal_real_effect_runtime_implementation_input(
        live_implementation_definition_v0={"definition": "frozen_placeholder"},
        live_implementation_skeleton_identity_v0={"identity": "present_placeholder"},
        live_implementation_stub_identity_v0={"identity": "present_placeholder"},
        minimal_code_skeleton_identity_v0={"identity": "present_placeholder"},
        admission_and_acceptance_v0={"frozen": True},
        minimal_implementation_plan_v0={"frozen": True},
        live_implementation_wiring_v0={"wiring_status": "first_live_minimal_real_effect_live_wired_ready"},
        live_implementation_dry_run_execution_v0={"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"},
        live_runtime_activation_stub_identity_v0={"is_live_runtime_activation_stub": True},
        rollout_plan_v0={"frozen": True},
        go_no_go_gate_v0={"real_write_status": "first_live_minimal_real_effect_real_write_go"},
        live_code_path_dry_run_v0={"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"},
        first_real_code_activation_definition_v0={"frozen": True},
        execution_state_v0={"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"},
        result_v0={"release_control_result_scope": "navigation_governance_action_release_control_result_v0"},
        exception_or_failure_path_v0={"path": "present_placeholder"},
        side_effects_released=False,
        context={"t": "x"},
    )
    assert isinstance(out, dict)
    assert out.get("status") == "live_runtime_implementation_stub_inactive"
    assert out.get("payload", {}).get("side_effects_released") is False
    assert out.get("payload", {}).get("entered_runtime") is False

    e = enter_first_live_runtime_implementation_placeholder(reason="test")
    assert e.get("side_effects_released") is False
    s1 = perform_first_live_runtime_execution_state_placeholder()
    assert s1.get("side_effects_released") is False
    r1 = perform_first_live_runtime_result_placeholder()
    assert r1.get("side_effects_released") is False
    ex1 = perform_first_live_runtime_exception_or_failure_placeholder(reason="x")
    assert ex1.get("side_effects_released") is False
    x = exit_first_live_runtime_implementation_placeholder(reason="test")
    assert x.get("side_effects_released") is False

    ex = raise_first_live_minimal_real_effect_runtime_implementation_stub_exception(exc=ValueError("x"))
    assert ex.get("exception_status") == "reported_placeholder"
    assert ex.get("side_effects_released") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

