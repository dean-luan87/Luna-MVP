# -*- coding: utf-8 -*-
"""
Local verification for execution monitoring minimal loop implementation v0.

Covers:
- A: minimum evidence satisfied => returns implemented monitoring status object (NOT placeholder semantics)
- B: missing takeover stub => relevant-only (False, None)
- C: missing executor status object => relevant-only (False, None)
- D: executor skeleton can recognize monitoring object but remains not_implemented/no governance
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

    from capabilities.mid_platform.runtime.navigation_execution_monitoring_status_v0 import (  # noqa: E402
        evaluate_navigation_execution_monitoring_status_v0,
    )
    from capabilities.navigation.runtime.navigation_real_executor_v0 import (  # noqa: E402
        accept_execution_monitoring_status_object,
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
    st_impl = {
        "executor_status_scope": "navigation_real_executor_status_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
        "takeover_state": {"takeover_fact": "not_taken_over_yet"},
        "execution_state": {"execution_fact": "not_started"},
        "anomaly_state": {"anomaly_fact": "unknown_not_observed"},
    }
    inp_impl = {
        "executor_input_scope": "navigation_real_executor_input_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
    }

    # A) satisfied => implemented monitoring status object
    applicable, payload = evaluate_navigation_execution_monitoring_status_v0(
        navigation_real_executor_status_v0=st_impl,
        navigation_executor_takeover_stub_v0=tk,
        navigation_real_executor_input_v0=inp_impl,
    )
    assert_true(applicable, "A applicable should be True")
    assert_true(isinstance(payload, dict), "A payload should be dict")
    assert_eq(payload.get("monitoring_status_scope"), "navigation_execution_monitoring_status_v0", "A scope")
    assert_eq(payload.get("object_kind"), "implemented_v0", "A object_kind")
    assert_eq(payload.get("consume_mode"), "implemented_object", "A consume_mode")
    # Not placeholder semantics
    assert_true("monitoring_status_present" not in payload, "A must not use placeholder monitoring_status_present")
    assert_true(isinstance(payload.get("takeover_monitor"), dict), "A takeover_monitor must exist")
    assert_true(isinstance(payload.get("execution_monitor"), dict), "A execution_monitor must exist")
    assert_true(isinstance(payload.get("anomaly_monitor"), dict), "A anomaly_monitor must exist")
    assert_eq((payload.get("execution_monitor") or {}).get("execution_monitor_fact"), "not_started", "A execution_monitor_fact")

    # B) missing takeover => relevant-only
    applicable, payload_b = evaluate_navigation_execution_monitoring_status_v0(
        navigation_real_executor_status_v0=st_impl,
        navigation_executor_takeover_stub_v0=None,
    )
    assert_eq(applicable, False, "B applicable should be False")
    assert_eq(payload_b, None, "B payload should be None")

    # C) missing status => relevant-only
    applicable, payload_c = evaluate_navigation_execution_monitoring_status_v0(
        navigation_real_executor_status_v0=None,
        navigation_executor_takeover_stub_v0=tk,
    )
    assert_eq(applicable, False, "C applicable should be False")
    assert_eq(payload_c, None, "C payload should be None")

    # D) skeleton recognizes monitoring object but remains not_implemented and does not attempt governance
    res_d = accept_execution_monitoring_status_object(navigation_execution_monitoring_status_v0=payload)
    assert_true(isinstance(res_d, dict), "D result must be dict")
    assert_eq(res_d.get("status"), "not_implemented", "D skeleton status")
    assert_true(isinstance(res_d.get("payload"), dict), "D skeleton payload must be dict")
    assert_eq(res_d["payload"].get("accepted"), True, "D accepted")
    assert_eq(res_d["payload"].get("governance_attempted"), False, "D no governance")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

