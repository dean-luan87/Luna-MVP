# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Guarded Launch Dry-Run v0 (Minimal Implementation)

覆盖：
- 场景 A：admission admitted + gates ready + dry-effect simulated + impl dry-run executed + skeleton identity 正确 + state/result 在位
  => launch_ready 且 side_effects_released=false
- 场景 B：admission 未通过 => launch_not_ready
- 场景 C：implementation skeleton identity 不匹配 => launch_blocked
"""

from __future__ import annotations

import os
import sys


_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> None:
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0,
    )

    adm = {"admission_status": "first_live_minimal_real_effect_admitted"}
    ag = {"approval_status": "first_live_enablement_approved"}
    ld = {"launch_status": "first_live_launch_dry_run_ready"}
    lg = {"live_release_status": "live_release_ready"}
    sg = {"side_effect_release_status": "side_effect_release_ready"}
    ds = {"simulation_status": "first_live_guarded_dry_effect_simulated"}
    idr = {"execution_status": "first_live_minimal_real_effect_implementation_dry_run_executed"}
    sk = {"is_skeleton": True, "is_real_effect_implementation_skeleton": True, "can_open_side_effects_released": False}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    # A
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        side_effects_released=False,
    )
    _assert(applicable is True, "scenario A: expected applicable=True")
    _assert(payload.get("launch_status") == "first_live_minimal_real_effect_launch_ready", "scenario A: expected launch_ready")
    _assert(payload.get("side_effects_released") is False, "scenario A: side_effects_released must be false")

    # B admission not admitted
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0={"admission_status": "first_live_minimal_real_effect_not_admitted"},
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        side_effects_released=False,
    )
    _assert(payload.get("launch_status") == "first_live_minimal_real_effect_launch_not_ready", "scenario B: expected launch_not_ready")

    # C skeleton mismatch
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0={"is_skeleton": False},
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        side_effects_released=False,
    )
    _assert(payload.get("launch_status") == "first_live_minimal_real_effect_launch_blocked", "scenario C: expected launch_blocked")

    print("ALL_OK")


if __name__ == "__main__":
    main()

