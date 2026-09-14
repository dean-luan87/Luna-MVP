# -*- coding: utf-8 -*-
"""
Local verification for navigation_real_executor_status_object_v0 (implemented object).

Covers:
- A: minimum evidence satisfied => returns implemented status object (NOT placeholder semantics)
- B: missing takeover stub => relevant-only (False, None)
- C: missing executor input object => relevant-only (False, None)
- D: executor skeleton can recognize implemented status object but remains not_implemented/placeholder-safe
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

    from capabilities.mid_platform.runtime.navigation_real_executor_status_object_v0 import (  # noqa: E402
        evaluate_navigation_real_executor_status_object_v0,
    )
    from capabilities.navigation.runtime.navigation_real_executor_v0 import (  # noqa: E402
        accept_executor_status_object,
    )

    def assert_true(v: bool, msg: str) -> None:
        if not v:
            raise AssertionError(msg)

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    tk = {
        "takeover_attempted": True,
        "takeover_scope": "navigation_executor_takeover_stub_v0",
        "takeover_status": "ready_to_takeover",
        "reason": "all_minimum_takeover_preconditions_satisfied",
    }
    inp_impl = {
        "executor_input_scope": "navigation_real_executor_input_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
        "takeover_authorization": {"authorized": True},
        "task_context": {"task_context_ready": True},
        "execution_constraints": {"constraints_ready": False},
    }

    # A) satisfied => implemented status object
    applicable, payload = evaluate_navigation_real_executor_status_object_v0(
        navigation_executor_takeover_stub_v0=tk,
        navigation_real_executor_input_v0=inp_impl,
        navigation_real_execution_readiness_gate_stub_v0=None,
    )
    assert_true(applicable, "A applicable should be True")
    assert_true(isinstance(payload, dict), "A payload should be dict")
    assert_eq(payload.get("executor_status_scope"), "navigation_real_executor_status_v0", "A scope")
    assert_eq(payload.get("object_kind"), "implemented_v0", "A object_kind")
    assert_eq(payload.get("consume_mode"), "implemented_object", "A consume_mode")
    # Not placeholder semantics
    assert_true("executor_status_present" not in payload, "A must not use placeholder executor_status_present")
    assert_true(isinstance(payload.get("takeover_state"), dict), "A takeover_state must exist")
    assert_true(isinstance(payload.get("execution_state"), dict), "A execution_state must exist")
    assert_true(isinstance(payload.get("anomaly_state"), dict), "A anomaly_state must exist")
    # Must not pretend running/completed/failed
    ex_fact = (payload.get("execution_state") or {}).get("execution_fact")
    assert_true(ex_fact == "not_started", "A execution_fact must be not_started")

    # B) missing takeover => relevant-only
    applicable, payload_b = evaluate_navigation_real_executor_status_object_v0(
        navigation_executor_takeover_stub_v0=None,
        navigation_real_executor_input_v0=inp_impl,
    )
    assert_eq(applicable, False, "B applicable should be False")
    assert_eq(payload_b, None, "B payload should be None")

    # C) missing input => relevant-only
    applicable, payload_c = evaluate_navigation_real_executor_status_object_v0(
        navigation_executor_takeover_stub_v0=tk,
        navigation_real_executor_input_v0=None,
    )
    assert_eq(applicable, False, "C applicable should be False")
    assert_eq(payload_c, None, "C payload should be None")

    # D) skeleton recognizes implemented status object but remains not_implemented
    res_d = accept_executor_status_object(navigation_real_executor_status_v0=payload)
    assert_true(isinstance(res_d, dict), "D result must be dict")
    assert_eq(res_d.get("status"), "not_implemented", "D skeleton status")
    assert_true(isinstance(res_d.get("payload"), dict), "D skeleton payload must be dict")
    assert_eq(res_d["payload"].get("accepted"), True, "D skeleton should mark accepted=True for implemented status object")
    assert_eq(res_d["payload"].get("execute_attempted"), False, "D skeleton must not execute")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

