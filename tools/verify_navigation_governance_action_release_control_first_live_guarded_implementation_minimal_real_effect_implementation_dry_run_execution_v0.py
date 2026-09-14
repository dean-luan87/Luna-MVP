# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Implementation Dry-Run Execution v0

覆盖：
- 场景 A：implementation wiring wired_ready + skeleton identity 正确 + state/result 在位 => dry_run_executed + 固定三步顺序
- 场景 B：wiring 未 ready => dry_run_not_ready
- 场景 C：skeleton identity 不匹配 => dry_run_blocked
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
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0 import (  # noqa: E402
        evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0,
    )

    good_wiring = {
        "wiring_status": "first_live_minimal_real_effect_implementation_wired_ready",
        "side_effects_released": False,
        "release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0",
    }
    good_sk = {
        "is_skeleton": True,
        "is_real_effect_implementation_skeleton": True,
        "can_open_side_effects_released": False,
    }
    xs = {"release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0"}
    rs = {"release_control_result_scope": "navigation_governance_action_release_control_result_v0"}

    # 场景 A
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0=good_wiring,
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=good_sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    _assert(applicable is True, "scenario A: expected applicable=True")
    _assert(isinstance(payload, dict), "scenario A: expected payload dict")
    _assert(
        payload.get("execution_status")
        == "first_live_minimal_real_effect_implementation_dry_run_executed",
        "scenario A: expected dry_run_executed",
    )
    _assert(payload.get("side_effects_released") is False, "scenario A: side_effects_released must be false")
    order = ((payload.get("execution_trace") or {}).get("execution_chain_order")) or []
    _assert(
        order
        == [
            "execution_state_real_write_placeholder_call_from_implementation",
            "result_object_real_write_placeholder_call_from_implementation",
            "failure_or_exception_real_write_placeholder_closure_from_implementation",
        ],
        f"scenario A: unexpected execution order: {order}",
    )

    # 场景 B：wiring 未 ready
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0={
            "wiring_status": "first_live_minimal_real_effect_implementation_wired_not_ready"
        },
        release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=good_sk,
        navigation_governance_action_release_control_execution_state_v0=xs,
        navigation_governance_action_release_control_result_v0=rs,
    )
    _assert(applicable is True, "scenario B: expected applicable=True")
    _assert(
        payload.get("execution_status")
        == "first_live_minimal_real_effect_implementation_dry_run_not_ready",
        "scenario B: expected dry_run_not_ready",
    )

    # 场景 C：skeleton identity 不匹配
    applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
        navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0=good_wiring,
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
        payload.get("execution_status")
        == "first_live_minimal_real_effect_implementation_dry_run_blocked",
        "scenario C: expected dry_run_blocked",
    )

    print("ALL_OK")


if __name__ == "__main__":
    main()

