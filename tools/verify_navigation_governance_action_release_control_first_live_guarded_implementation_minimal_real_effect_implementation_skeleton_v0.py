#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-test for:
- capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0

Hard boundaries:
- MUST keep side_effects_released == False
- MUST NOT claim any real writes happened
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
    # 场景 A：模块可导入 + identity 固定
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (
        RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_IDENTITY_V0,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
        accept_first_live_minimal_real_effect_implementation_input,
        write_first_live_execution_state_real_effect_from_implementation,
        write_first_live_result_object_real_effect_from_implementation,
        write_first_live_failure_or_exception_real_effect_from_implementation,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
    _assert(isinstance(ident, dict), "identity must be dict")
    _assert(
        ident.get(
            "release_control_first_live_guarded_minimal_real_effect_implementation_skeleton_identity"
        )
        == RELEASE_CONTROL_FIRST_LIVE_GUARDED_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_IDENTITY_V0,
        "identity string must be fixed",
    )
    _assert(ident.get("can_open_side_effects_released") is False, "must not open side effects")
    _assert(ident.get("can_execute_real_release_control") is False, "must not execute real release_control")

    # 场景 B：调用输入接口（永远 inactive）
    out_in = accept_first_live_minimal_real_effect_implementation_input(
        minimal_real_effect_implementation_definition_v0={},
        minimal_real_effect_plan_v0={},
        minimal_real_effect_wiring_v0={},
        minimal_real_effect_dry_run_execution_v0={},
        non_effect_execution_v0={},
        dry_effect_simulation_v0={},
        approval_gate_v0={},
        launch_dry_run_v0={},
        live_release_gate_v0={},
        side_effect_release_gate_v0={},
        execution_state_v0={},
        result_v0={},
        context={"test": "input"},
    )
    _assert(isinstance(out_in, dict), "input accept must return dict")
    _assert(out_in.get("status") == "implementation_skeleton_inactive", "must be inactive placeholder")
    payload = out_in.get("payload") if isinstance(out_in.get("payload"), dict) else {}
    _assert(payload.get("side_effects_released") is False, "side_effects_released must be false")

    # 场景 C：execution state write placeholder
    out_x = write_first_live_execution_state_real_effect_from_implementation(context={"test": "xs"})
    _assert(isinstance(out_x, dict), "execution state placeholder must return dict")
    _assert(out_x.get("side_effects_released") is False, "side_effects_released must be false")
    _assert(
        out_x.get("release_control_execution_state_fact")
        == "minimal_real_effect_implementation_skeleton_no_real_write",
        "must not claim real write",
    )

    # 场景 D：result object write placeholder
    out_r = write_first_live_result_object_real_effect_from_implementation(context={"test": "rs"})
    _assert(isinstance(out_r, dict), "result object placeholder must return dict")
    _assert(out_r.get("side_effects_released") is False, "side_effects_released must be false")
    _assert(
        out_r.get("release_control_result_state_fact")
        == "minimal_real_effect_implementation_skeleton_no_real_write",
        "must not claim real write",
    )

    # 场景 E：failure/exception placeholder closure
    out_f = write_first_live_failure_or_exception_real_effect_from_implementation(reason="verify", context={"test": "f"})
    _assert(isinstance(out_f, dict), "failure placeholder must return dict")
    _assert(out_f.get("side_effects_released") is False, "side_effects_released must be false")
    _assert(out_f.get("failure_or_exception_status") == "stop_safe_reported_placeholder", "must be stop-safe")
    _assert(str(out_f.get("reason") or "") == "verify", "must preserve reason")

    print("ALL_OK")


if __name__ == "__main__":
    main()

