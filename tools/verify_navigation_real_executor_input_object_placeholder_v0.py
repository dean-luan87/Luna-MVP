# -*- coding: utf-8 -*-
"""
Local verification for navigation_real_executor_input_object_placeholder_v0 (read-only helper).

Covers:
- A: all evidence satisfied => writes placeholder payload
- B: missing takeover ready_to_takeover => not applicable (relevant-only)
- C: missing readiness ready_candidate => not applicable (relevant-only)
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

    from capabilities.mid_platform.runtime.navigation_real_executor_input_object_placeholder_v0 import (  # noqa: E402
        evaluate_navigation_real_executor_input_object_placeholder_v0,
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

    # A) all satisfied => applicable and payload present
    applicable, payload = evaluate_navigation_real_executor_input_object_placeholder_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_ready,
    )
    assert_true(applicable, "A applicable should be True")
    assert_true(isinstance(payload, dict), "A payload should be dict")
    assert_eq(payload.get("executor_input_scope"), "navigation_real_executor_input_v0", "A scope")
    assert_eq(payload.get("executor_input_present"), True, "A present")
    assert_eq(payload.get("consume_mode"), "read_only", "A consume_mode")

    # B) missing takeover ready => not applicable (relevant-only)
    tk_not = dict(tk_ready)
    tk_not["takeover_status"] = "not_applicable"
    applicable, payload = evaluate_navigation_real_executor_input_object_placeholder_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_not,
    )
    assert_eq(applicable, False, "B applicable should be False")
    assert_eq(payload, None, "B payload should be None")

    # C) missing readiness ready_candidate => not applicable (relevant-only)
    rg_not = dict(rg_ready)
    rg_not["readiness_status"] = "not_ready"
    applicable, payload = evaluate_navigation_real_executor_input_object_placeholder_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_real_execution_readiness_gate_stub_v0=rg_not,
        navigation_executor_takeover_stub_v0=tk_ready,
    )
    assert_eq(applicable, False, "C applicable should be False")
    assert_eq(payload, None, "C payload should be None")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

