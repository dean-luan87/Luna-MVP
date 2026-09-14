# -*- coding: utf-8 -*-
"""
Local verification for navigation_rollback_and_interruption_governance_entry_v0 (minimal implementation; non-action).

Scenarios:
- A: eligible event present => governance_entry_open
- B: objects present but invalid => governance_entry_blocked
- C: objects present but no eligible event => governance_entry_not_applicable
- D: no standardized objects => relevant-only (False, None)
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

    from capabilities.mid_platform.runtime.navigation_rollback_and_interruption_governance_entry_v0 import (  # noqa: E402
        evaluate_navigation_rollback_and_interruption_governance_entry_v0,
    )

    def assert_true(v: bool, msg: str) -> None:
        if not v:
            raise AssertionError(msg)

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    base_executor_status = {
        "executor_status_scope": "navigation_real_executor_status_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
        "takeover_state": {"takeover_fact": "not_taken_over_yet"},
        "execution_state": {"execution_fact": "not_started"},
        "anomaly_state": {"anomaly_fact": "unknown_not_observed"},
    }
    base_monitoring_status = {
        "monitoring_status_scope": "navigation_execution_monitoring_status_v0",
        "object_kind": "implemented_v0",
        "consume_mode": "implemented_object",
        "execution_monitor": {"execution_monitor_fact": "not_started", "upstream_report_required": False},
        "anomaly_monitor": {"anomaly_monitor_fact": "unknown_not_observed", "upstream_report_required": False},
        "degradation_monitor": {"degradation_monitor_fact": "unknown_not_reported"},
    }

    # A) eligible event present => open
    st_a = dict(base_executor_status)
    st_a["execution_state"] = {"execution_fact": "failed"}
    applicable, payload = evaluate_navigation_rollback_and_interruption_governance_entry_v0(
        navigation_real_executor_status_v0=st_a,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
        navigation_executor_takeover_wiring_v0={"wiring_scope": "navigation_executor_takeover_wiring_v0", "wiring_status": "wired_ready_to_takeover"},
    )
    assert_true(applicable, "A applicable")
    assert_eq(payload.get("governance_entry_status"), "governance_entry_open", "A status")

    # B) objects present but invalid => blocked
    st_b = dict(base_executor_status)
    st_b["object_kind"] = "placeholder_v0"
    applicable, payload_b = evaluate_navigation_rollback_and_interruption_governance_entry_v0(
        navigation_real_executor_status_v0=st_b,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "B applicable")
    assert_eq(payload_b.get("governance_entry_status"), "governance_entry_blocked", "B status")

    # C) objects present but no eligible event => not_applicable
    applicable, payload_c = evaluate_navigation_rollback_and_interruption_governance_entry_v0(
        navigation_real_executor_status_v0=base_executor_status,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "C applicable")
    assert_eq(payload_c.get("governance_entry_status"), "governance_entry_not_applicable", "C status")

    # D) no objects => relevant-only (False, None)
    applicable, payload_d = evaluate_navigation_rollback_and_interruption_governance_entry_v0(
        navigation_real_executor_status_v0=None,
        navigation_execution_monitoring_status_v0=None,
        navigation_executor_takeover_wiring_v0=None,
    )
    assert_eq(applicable, False, "D applicable")
    assert_eq(payload_d, None, "D payload")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

