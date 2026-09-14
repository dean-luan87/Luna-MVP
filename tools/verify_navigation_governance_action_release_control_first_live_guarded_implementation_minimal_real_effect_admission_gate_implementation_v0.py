# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Admission Gate v0 (Minimal Implementation)

覆盖：
- 场景 A：全部 ready + wiring wired_ready + impl dry-run executed + skeleton identity 正确 + state/result 在位 + admission signal 存在
  => admitted 且 side_effects_released=false
- 场景 B：approval 未通过或 launch 未 ready => not_admitted
- 场景 C：skeleton identity 不匹配或 side_effects_released != false => blocked
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
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0,
    )

    ag = {"approval_status": "first_live_enablement_approved"}
    ld = {"launch_status": "first_live_launch_dry_run_ready"}
    lg = {"live_release_status": "live_release_ready"}
    sg = {"side_effect_release_status": "side_effect_release_ready"}
    ds = {"simulation_status": "first_live_guarded_dry_effect_simulated"}
    mw = {"wiring_status": "first_live_minimal_real_effect_wired_ready"}
    idr = {"execution_status": "first_live_minimal_real_effect_implementation_dry_run_executed"}
    sk = {"is_skeleton": True, "is_real_effect_implementation_skeleton": True, "can_open_side_effects_released": False}
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}
    sig = {"admission_signal_present": True, "admission_signal_scope": "minimal_semantic_placeholder"}

    # A
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0=sig,
        side_effects_released=False,
    )
    _assert(applicable is True, "scenario A: expected applicable=True")
    _assert(payload.get("admission_status") == "first_live_minimal_real_effect_admitted", "scenario A: expected admitted")
    _assert(payload.get("side_effects_released") is False, "scenario A: side_effects_released must be false")

    # B1 approval not approved
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0={"approval_status": "first_live_enablement_not_approved"},
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0=sig,
        side_effects_released=False,
    )
    _assert(payload.get("admission_status") == "first_live_minimal_real_effect_not_admitted", "scenario B1: expected not_admitted")

    # B2 launch not ready
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0={"launch_status": "first_live_launch_dry_run_not_ready"},
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0=sig,
        side_effects_released=False,
    )
    _assert(payload.get("admission_status") == "first_live_minimal_real_effect_not_admitted", "scenario B2: expected not_admitted")

    # C1 skeleton mismatch
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0={"is_skeleton": False},
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0=sig,
        side_effects_released=False,
    )
    _assert(payload.get("admission_status") == "first_live_minimal_real_effect_blocked", "scenario C1: expected blocked")

    # C2 side_effects_released true
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
        navigation_governance_action_release_control_live_release_gate_v0=lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0=sig,
        side_effects_released=True,
    )
    _assert(payload.get("admission_status") == "first_live_minimal_real_effect_blocked", "scenario C2: expected blocked")

    print("ALL_OK")


if __name__ == "__main__":
    main()

