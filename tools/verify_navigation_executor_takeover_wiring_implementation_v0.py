# -*- coding: utf-8 -*-
"""
Local verification for navigation_executor_takeover_wiring_v0 (minimal implementation; non-action).

Covers:
- A: 8 preconditions satisfied => wiring_status wired_ready_to_takeover and skeleton wired safely
- B: missing implemented monitoring status => not_applicable
- C: missing takeover ready_to_takeover => not_applicable
- D: skeleton wiring interface does not enter active/running/executing
- E: voice v1 minimal loop remains ALL_OK (run separately by caller)
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

    from capabilities.mid_platform.runtime.navigation_executor_takeover_wiring_v0 import (  # noqa: E402
        evaluate_navigation_executor_takeover_wiring_v0,
    )
    from capabilities.navigation.runtime.navigation_real_executor_v0 import wire_executor_takeover  # noqa: E402

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
    post_bound_stub = {
        "execution_stub_attempted": True,
        "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
        "execution_state": "execution_pending",
        "reason": "missing_formal_mid_platform_dispatch",
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
    inp_impl = {
        "executor_input_scope": "navigation_real_executor_input_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
    }
    st_impl = {
        "executor_status_scope": "navigation_real_executor_status_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
    }
    mon_impl = {
        "monitoring_status_scope": "navigation_execution_monitoring_status_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
    }

    # A) all satisfied => wired_ready_to_takeover
    applicable, payload = evaluate_navigation_executor_takeover_wiring_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_handoff_post_bound_execution_stub_v0=post_bound_stub,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_ready,
        navigation_real_executor_input_v0=inp_impl,
        navigation_real_executor_status_v0=st_impl,
        navigation_execution_monitoring_status_v0=mon_impl,
    )
    assert_true(applicable, "A applicable should be True")
    assert_true(isinstance(payload, dict), "A payload should be dict")
    assert_eq(payload.get("wiring_scope"), "navigation_executor_takeover_wiring_v0", "A scope")
    assert_eq(payload.get("wiring_status"), "wired_ready_to_takeover", "A wiring_status")

    # D) skeleton wiring interface stays in safe states only
    res_w = wire_executor_takeover(wiring_status=payload.get("wiring_status") or "", wiring_reason="x")
    assert_true(isinstance(res_w, dict), "D wire result dict")
    assert_true(res_w.get("status") in ("wired_inactive", "wired_ready_to_takeover"), "D safe status")
    assert_true(res_w.get("status") not in ("active", "running", "executing"), "D not active/running/executing")

    # B) missing monitoring => not_applicable
    applicable, payload_b = evaluate_navigation_executor_takeover_wiring_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_handoff_post_bound_execution_stub_v0=post_bound_stub,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_ready,
        navigation_real_executor_input_v0=inp_impl,
        navigation_real_executor_status_v0=st_impl,
        navigation_execution_monitoring_status_v0=None,
    )
    assert_true(applicable, "B applicable should be True")
    assert_eq(payload_b.get("wiring_status"), "not_applicable", "B status")

    # C) takeover not ready => not_applicable
    tk_not = dict(tk_ready)
    tk_not["takeover_status"] = "blocked"
    applicable, payload_c = evaluate_navigation_executor_takeover_wiring_v0(
        mid_platform_formal_decision_stub_v0=fd_allow,
        formal_decision_allow_progress_path_v0=ap_ok,
        navigation_handoff_post_bound_execution_stub_v0=post_bound_stub,
        navigation_real_execution_readiness_gate_stub_v0=rg_ready,
        navigation_executor_takeover_stub_v0=tk_not,
        navigation_real_executor_input_v0=inp_impl,
        navigation_real_executor_status_v0=st_impl,
        navigation_execution_monitoring_status_v0=mon_impl,
    )
    assert_true(applicable, "C applicable should be True")
    assert_eq(payload_c.get("wiring_status"), "not_applicable", "C status")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

