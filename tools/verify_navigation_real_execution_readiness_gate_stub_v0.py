# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))


def _inputs_base() -> Dict[str, Any]:
    return {
        "readiness_gate_inputs_scope": "navigation_real_execution_readiness_gate_inputs_v0",
        "consume_mode": "read_only",
        "readiness_gate_inputs_present": True,
    }


def main() -> None:
    from capabilities.mid_platform.runtime.navigation_real_execution_readiness_gate_stub_v0 import (
        evaluate_navigation_real_execution_readiness_gate_stub_v0,
    )

    # 场景 D：无 gate inputs => relevant-only 不写
    app_d, out_d = evaluate_navigation_real_execution_readiness_gate_stub_v0(
        navigation_real_execution_readiness_gate_inputs_v0=None
    )
    assert app_d is False and out_d is None

    # 场景 C：gate 输入存在但不完整 => not_ready
    inp_c = {
        **_inputs_base(),
        "executor_gate_present": True,
        "executor_status": "available",
        "executor_takeover_allowed": True,
        # missing the other gate_present flags / statuses
    }
    app_c, out_c = evaluate_navigation_real_execution_readiness_gate_stub_v0(
        navigation_real_execution_readiness_gate_inputs_v0=inp_c
    )
    assert app_c is True and isinstance(out_c, dict)
    assert out_c.get("readiness_status") == "not_ready"

    # 场景 B：某 gate blocked / unavailable => blocked
    inp_b = {
        **_inputs_base(),
        "executor_gate_present": True,
        "executor_status": "unavailable",
        "executor_takeover_allowed": False,
    }
    app_b, out_b = evaluate_navigation_real_execution_readiness_gate_stub_v0(
        navigation_real_execution_readiness_gate_inputs_v0=inp_b
    )
    assert app_b is True and isinstance(out_b, dict)
    assert out_b.get("readiness_status") == "blocked"

    # 场景 A：5 类 gate 全部满足 => ready_candidate
    inp_a = {
        **_inputs_base(),
        "executor_gate_present": True,
        "executor_status": "available",
        "executor_takeover_allowed": True,
        "path_support_gate_present": True,
        "path_support_status": "partial",
        "execution_monitor_gate_present": True,
        "execution_monitor_status": "ready_candidate",
        "start_policy_gate_present": True,
        "start_policy_status": "ready_candidate",
        "fallback_gate_present": True,
        "fallback_status": "ready_candidate",
    }
    app_a, out_a = evaluate_navigation_real_execution_readiness_gate_stub_v0(
        navigation_real_execution_readiness_gate_inputs_v0=inp_a
    )
    assert app_a is True and isinstance(out_a, dict)
    assert out_a.get("readiness_status") == "ready_candidate"
    assert out_a.get("reason") == "all_minimum_readiness_preconditions_satisfied"

    print("VERIFY_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0: ALL_OK")


if __name__ == "__main__":
    main()

