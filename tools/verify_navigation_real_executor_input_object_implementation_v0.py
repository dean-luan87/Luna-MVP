# -*- coding: utf-8 -*-
"""
Local verification for navigation_real_executor_input_object_v0 (implemented object).

Covers:
- A: all evidence satisfied => returns implemented object (NOT placeholder semantics)
- B: missing takeover ready_to_takeover => relevant-only (False, None)
- C: missing readiness ready_candidate => relevant-only (False, None)
- D: executor skeleton can recognize implemented object but remains not_implemented/no-op
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _bootstrap_repo_root() -> None:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    sys.path.insert(0, str(root))


def main() -> int:
    _bootstrap_repo_root()

    from capabilities.mid_platform.runtime.navigation_real_executor_input_object_v0 import (  # noqa: E402
        evaluate_navigation_real_executor_input_object_v0,
    )
    from capabilities.navigation.runtime.navigation_real_executor_v0 import (  # noqa: E402
        accept_executor_input,
    )

    def assert_true(v: bool, msg: str) -> None:
        if not v:
            raise AssertionError(msg)

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    fd_allow = {"decision_scope": "mid_platform_formal_decision_stub_v0", "decision_result": "allow_progress"}
    ap_ok = {
        "allow_progress_path_present": True,
        "downstream_placeholder_interface": "navigation_handoff_post_bound_execution_stub_v0",
        "consume_mode": "read_only",
    }
    rg_ready = {
        "readiness_attempted": True,
        "readiness_scope": "navigation_real_execution_readiness_gate_stub_v0",
        "readiness_status": "ready_candidate",
        "reason": "all_minimum_readiness_preconditions_satisfied",
    }
    tk_ready = {
        "takeover_attempted": True,
        "takeover_scope": "navigation_executor_takeover_stub_v0",
        "takeover_status": "ready_to_takeover",
        "reason": "all_minimum_takeover_preconditions_satisfied",
    }

    # A) all satisfied => implemented object
    applicable, payload = evaluate_navigation_real_executor_input_object_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_ready,
    )
    assert_true(applicable, "A applicable should be True")
    assert_true(isinstance(payload, dict), "A payload should be dict")
    assert_eq(payload.get("executor_input_scope"), "navigation_real_executor_input_v0", "A scope")
    assert_eq(payload.get("object_kind"), "implemented_v0", "A object_kind")
    # Not placeholder semantics
    assert_true("executor_input_present" not in payload, "A must not use placeholder executor_input_present")
    assert_true(payload.get("consume_mode") == "implemented_object", "A consume_mode should be implemented_object")
    assert_true(isinstance(payload.get("takeover_authorization"), dict), "A takeover_authorization must exist")
    assert_true(isinstance(payload.get("task_context"), dict), "A task_context must exist")
    assert_true(isinstance(payload.get("execution_constraints"), dict), "A execution_constraints must exist")

    # B) missing takeover ready => relevant-only
    tk_not = dict(tk_ready)
    tk_not["takeover_status"] = "not_applicable"
    applicable, payload_b = evaluate_navigation_real_executor_input_object_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_not,
    )
    assert_eq(applicable, False, "B applicable should be False")
    assert_eq(payload_b, None, "B payload should be None")

    # C) missing readiness ready_candidate => relevant-only
    rg_not = dict(rg_ready)
    rg_not["readiness_status"] = "not_ready"
    applicable, payload_c = evaluate_navigation_real_executor_input_object_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_real_execution_readiness_gate_stub_v0=rg_not,
        navigation_executor_takeover_stub_v0=tk_ready,
    )
    assert_eq(applicable, False, "C applicable should be False")
    assert_eq(payload_c, None, "C payload should be None")

    # D) executor skeleton recognizes implemented object but remains not_implemented/no-op
    res_d = accept_executor_input(navigation_real_executor_input_v0=payload)
    assert_true(isinstance(res_d, dict), "D result must be dict")
    assert_eq(res_d.get("status"), "not_implemented", "D skeleton status")
    assert_true(isinstance(res_d.get("payload"), dict), "D skeleton payload must be dict")
    assert_eq(res_d["payload"].get("accepted"), True, "D skeleton should mark accepted=True for implemented object")
    assert_eq(res_d["payload"].get("execute_attempted"), False, "D skeleton must not execute")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

