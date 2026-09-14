# -*- coding: utf-8 -*-
"""
Local verification for navigation_rollback_and_interruption_governance_decision_v0 (minimal implementation; non-action).

Scenarios:
- A: failure/unexecutable => recommend_rollback
- B: interrupted / takeover abnormal release => recommend_interrupt or recommend_release_control
- C: degraded/offroute/upstream intervention => hold_for_governance or recommend_interrupt
- D: entry open but objects incomplete => governance_decision_blocked
- E: no valid governance entry => relevant-only (False, None)
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

    from capabilities.mid_platform.runtime.navigation_rollback_and_interruption_governance_decision_v0 import (  # noqa: E402
        evaluate_navigation_rollback_and_interruption_governance_decision_v0,
    )

    def assert_true(v: bool, msg: str) -> None:
        if not v:
            raise AssertionError(msg)

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    entry_open = {
        "governance_entry_attempted": True,
        "governance_entry_scope": "navigation_rollback_and_interruption_governance_entry_v0",
        "governance_entry_status": "governance_entry_open",
        "reason": "x",
    }
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

    # A) failure => recommend_rollback
    st_a = dict(base_executor_status)
    st_a["execution_state"] = {"execution_fact": "failed"}
    applicable, payload = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
        navigation_rollback_and_interruption_governance_entry_v0=entry_open,
        navigation_real_executor_status_v0=st_a,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "A applicable")
    assert_eq(payload.get("governance_decision_status"), "recommend_rollback", "A decision")

    # B) interrupted => recommend_interrupt
    st_b = dict(base_executor_status)
    st_b["execution_state"] = {"execution_fact": "interrupted"}
    applicable, payload_b = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
        navigation_rollback_and_interruption_governance_entry_v0=entry_open,
        navigation_real_executor_status_v0=st_b,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "B applicable")
    assert_true(payload_b.get("governance_decision_status") in ("recommend_interrupt", "recommend_release_control"), "B decision")

    # B2) takeover abnormal release => recommend_release_control
    st_b2 = dict(base_executor_status)
    st_b2["takeover_state"] = {"takeover_fact": "takeover_abnormal_release"}
    applicable, payload_b2 = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
        navigation_rollback_and_interruption_governance_entry_v0=entry_open,
        navigation_real_executor_status_v0=st_b2,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "B2 applicable")
    assert_eq(payload_b2.get("governance_decision_status"), "recommend_release_control", "B2 decision")

    # C) degraded => hold_for_governance or recommend_interrupt
    st_c = dict(base_executor_status)
    st_c["execution_state"] = {"execution_fact": "degraded"}
    applicable, payload_c = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
        navigation_rollback_and_interruption_governance_entry_v0=entry_open,
        navigation_real_executor_status_v0=st_c,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "C applicable")
    assert_true(payload_c.get("governance_decision_status") in ("hold_for_governance", "recommend_interrupt"), "C decision")

    # D) entry open but missing objects => blocked
    applicable, payload_d = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
        navigation_rollback_and_interruption_governance_entry_v0=entry_open,
        navigation_real_executor_status_v0=None,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_true(applicable, "D applicable")
    assert_eq(payload_d.get("governance_decision_status"), "governance_decision_blocked", "D decision")

    # E) no valid entry => relevant-only
    applicable, payload_e = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
        navigation_rollback_and_interruption_governance_entry_v0=None,
        navigation_real_executor_status_v0=base_executor_status,
        navigation_execution_monitoring_status_v0=base_monitoring_status,
    )
    assert_eq(applicable, False, "E applicable")
    assert_eq(payload_e, None, "E payload")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

