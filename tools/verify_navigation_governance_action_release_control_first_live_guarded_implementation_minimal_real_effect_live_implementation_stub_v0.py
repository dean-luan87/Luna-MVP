# -*- coding: utf-8 -*-
"""
Self-test: Navigation Governance Action — Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation Stub v0

覆盖：
- 场景 A：模块可导入 + identity 固定
- 场景 B：runtime 输入接口返回 inactive 且 side_effects_released=false
- 场景 C：state/result/failure 占位接口 placeholder-safe 且 side_effects_released=false
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
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_live_implementation_runtime_input,
        emit_live_execution_state_real_effect_placeholder_from_stub,
        emit_live_failure_or_exception_real_effect_placeholder_from_stub,
        emit_live_result_object_real_effect_placeholder_from_stub,
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity()
    _assert(isinstance(ident, dict), "identity must be dict")
    _assert(ident.get("is_stub") is True, "identity.is_stub must be true")
    _assert(ident.get("side_effects_released") is False, "side_effects_released must be false")

    out = accept_first_live_minimal_real_effect_live_implementation_runtime_input(
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
    _assert(isinstance(out, dict), "runtime input must return dict")
    _assert(out.get("status") in ("live_implementation_stub_inactive",), "expected inactive status")
    _assert(out.get("payload", {}).get("side_effects_released") is False, "side_effects_released must be false")

    xs = emit_live_execution_state_real_effect_placeholder_from_stub(context={"test": True})
    _assert(xs.get("side_effects_released") is False, "xs side_effects_released must be false")

    rs = emit_live_result_object_real_effect_placeholder_from_stub(context={"test": True})
    _assert(rs.get("side_effects_released") is False, "rs side_effects_released must be false")

    fe = emit_live_failure_or_exception_real_effect_placeholder_from_stub(reason="x", context={"test": True})
    _assert(fe.get("side_effects_released") is False, "fe side_effects_released must be false")

    print("ALL_OK")


if __name__ == "__main__":
    main()

