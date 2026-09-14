# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Implementation Non-Effect Wiring v0

覆盖：
- 场景 A：全部 ready + skeleton identity 正确 + state/result 在位 => wired_ready 且 side_effects_released=false
- 场景 B：approval 未通过 或 launch 未 ready => wired_not_ready
- 场景 C：implementation skeleton identity 不匹配 => wired_blocked
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
    from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0,
    )

    good_ag = {"approval_status": "first_live_enablement_approved"}
    good_ld = {"launch_status": "first_live_launch_dry_run_ready"}
    good_lg = {"live_release_status": "live_release_ready"}
    good_sg = {"side_effect_release_status": "side_effect_release_ready"}
    good_ds = {"simulation_status": "first_live_guarded_dry_effect_simulated"}
    good_dr = {"execution_status": "first_live_minimal_real_effect_dry_run_executed"}
    good_sk = {
        "is_skeleton": True,
        "is_real_effect_implementation_skeleton": True,
        "can_open_side_effects_released": False,
    }
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    # 场景 A
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=good_ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=good_ld,
        navigation_governance_action_release_control_live_release_gate_v0=good_lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=good_sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=good_ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0=good_dr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=good_sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    _assert(applicable is True, "scenario A: expected applicable=True")
    _assert(isinstance(payload, dict), "scenario A: expected payload dict")
    _assert(
        payload.get("wiring_status") == "first_live_minimal_real_effect_implementation_wired_ready",
        "scenario A: expected wired_ready",
    )
    _assert(payload.get("side_effects_released") is False, "scenario A: side_effects_released must be false")

    # 场景 B1：approval 未通过
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0={"approval_status": "first_live_enablement_not_approved"},
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=good_ld,
        navigation_governance_action_release_control_live_release_gate_v0=good_lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=good_sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=good_ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0=good_dr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=good_sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    _assert(applicable is True, "scenario B1: expected applicable=True")
    _assert(
        payload.get("wiring_status") == "first_live_minimal_real_effect_implementation_wired_not_ready",
        "scenario B1: expected wired_not_ready",
    )

    # 场景 B2：launch 未 ready
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=good_ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0={"launch_status": "first_live_launch_dry_run_not_ready"},
        navigation_governance_action_release_control_live_release_gate_v0=good_lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=good_sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=good_ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0=good_dr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=good_sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    _assert(applicable is True, "scenario B2: expected applicable=True")
    _assert(
        payload.get("wiring_status") == "first_live_minimal_real_effect_implementation_wired_not_ready",
        "scenario B2: expected wired_not_ready",
    )

    # 场景 C：skeleton identity 不匹配
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
        navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=good_ag,
        navigation_governance_action_release_control_first_live_launch_dry_run_v0=good_ld,
        navigation_governance_action_release_control_live_release_gate_v0=good_lg,
        navigation_governance_action_release_control_side_effect_release_gate_v0=good_sg,
        navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=good_ds,
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0=good_dr,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0={
            "is_skeleton": False,
            "is_real_effect_implementation_skeleton": False,
            "can_open_side_effects_released": False,
        },
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    _assert(applicable is True, "scenario C: expected applicable=True")
    _assert(
        payload.get("wiring_status") == "first_live_minimal_real_effect_implementation_wired_blocked",
        "scenario C: expected wired_blocked",
    )

    print("ALL_OK")


if __name__ == "__main__":
    main()

