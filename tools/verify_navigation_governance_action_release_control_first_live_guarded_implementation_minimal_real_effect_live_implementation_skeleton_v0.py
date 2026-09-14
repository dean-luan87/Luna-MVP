# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Skeleton v0

覆盖：
- 场景 A：模块可导入 + identity 固定
- 场景 B：输入接口返回 inactive/not_implemented 且 side_effects_released=false
- 场景 C：execution_state/result/failure_or_exception 接口 placeholder-safe 且 side_effects_released=false
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
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_live_implementation_input,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity,
        write_live_execution_state_real_effect_from_live_implementation,
        write_live_failure_or_exception_real_effect_from_live_implementation,
        write_live_result_object_real_effect_from_live_implementation,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity()
    _assert(isinstance(ident, dict), "identity must be a dict")
    _assert(ident.get("is_skeleton") is True, "identity.is_skeleton must be true")
    _assert(ident.get("is_live_implementation_skeleton") is True, "identity.is_live_implementation_skeleton must be true")
    _assert(ident.get("can_open_side_effects_released") is False, "identity must be conservative")

    out = accept_first_live_minimal_real_effect_live_implementation_input(
        admission_gate_v0={},
        guarded_launch_gate_v0={},
        pre_commit_dry_run_v0={},
        commit_gate_v0={},
        commit_dry_run_v0={},
        activation_gate_v0={},
        activation_dry_run_v0={},
        approval_gate_v0={},
        launch_dry_run_v0={},
        live_release_gate_v0={},
        side_effect_release_gate_v0={},
        dry_effect_simulation_v0={},
        implementation_dry_run_execution_v0={},
        execution_state_v0={},
        result_v0={},
        activation_or_live_execution_signal_v0={},
        context={"test": True},
    )
    _assert(isinstance(out, dict), "input interface must return dict")
    _assert(out.get("status") in ("live_implementation_skeleton_inactive",), "expected inactive status")
    _assert(out.get("payload", {}).get("side_effects_released") is False, "side_effects_released must be false")

    xs = write_live_execution_state_real_effect_from_live_implementation(context={"test": True})
    _assert(xs.get("side_effects_released") is False, "execution_state interface must keep side_effects_released false")

    rs = write_live_result_object_real_effect_from_live_implementation(context={"test": True})
    _assert(rs.get("side_effects_released") is False, "result interface must keep side_effects_released false")

    fe = write_live_failure_or_exception_real_effect_from_live_implementation(reason="x", context={"test": True})
    _assert(fe.get("side_effects_released") is False, "failure interface must keep side_effects_released false")

    print("ALL_OK")


if __name__ == "__main__":
    main()

