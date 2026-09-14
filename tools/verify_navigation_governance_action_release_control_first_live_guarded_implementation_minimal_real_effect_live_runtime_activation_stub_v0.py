# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Minimal Runtime Activation Stub v0
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_runtime_activation_input,
        enter_live_runtime_activation_placeholder,
        exit_live_runtime_activation_placeholder,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity,
        raise_first_live_minimal_real_effect_runtime_activation_stub_exception,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity()
    assert ident.get("is_stub") is True
    assert ident.get("is_live_runtime_activation_stub") is True
    assert ident.get("side_effects_released") is False
    assert ident.get("can_open_side_effects_released") is False

    out = accept_first_live_minimal_real_effect_runtime_activation_input(
        live_implementation_wiring_v0={"wiring_status": "first_live_minimal_real_effect_live_wired_ready"},
        live_implementation_dry_run_execution_v0={"execution_status": "first_live_minimal_real_effect_live_dry_run_executed"},
        activation_contract_v0={"contract": "frozen_placeholder"},
        activation_gate_v0={"activation_admission_status": "first_live_minimal_real_effect_activation_admitted"},
        activation_dry_run_v0={"activation_dry_run_status": "first_live_minimal_real_effect_activation_ready"},
        execution_state_v0={"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"},
        result_v0={"release_control_result_scope": "navigation_governance_action_release_control_result_v0"},
        exception_or_failure_path_v0={"path": "present_placeholder"},
        side_effects_released=False,
        context={"t": "x"},
    )
    assert isinstance(out, dict)
    assert out.get("status") == "live_runtime_activation_stub_inactive"
    assert out.get("payload", {}).get("side_effects_released") is False
    assert out.get("payload", {}).get("entered_activation") is False

    e1 = enter_live_runtime_activation_placeholder(reason="test")
    assert e1.get("side_effects_released") is False
    x1 = exit_live_runtime_activation_placeholder(reason="test")
    assert x1.get("side_effects_released") is False

    ex = raise_first_live_minimal_real_effect_runtime_activation_stub_exception(exc=ValueError("x"))
    assert ex.get("exception_status") == "reported_placeholder"
    assert ex.get("side_effects_released") is False

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

