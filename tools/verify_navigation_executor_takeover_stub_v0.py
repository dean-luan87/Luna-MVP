# -*- coding: utf-8 -*-
"""
Local verification for navigation_executor_takeover_stub_v0 (read-only helper).

Covers:
- A: all preconditions satisfied => ready_to_takeover
- B: readiness gate blocked => blocked
- C: missing downstream interface match / consumption => not_applicable (or relevant-only by caller)
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

    from capabilities.mid_platform.runtime.navigation_executor_takeover_stub_v0 import (  # noqa: E402
        evaluate_navigation_executor_takeover_stub_v0,
    )

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    # Shared minimal upstream facts for the fallback "downstream consumption equivalent".
    destination_bound_v0 = {"destination_bound": True, "destination_text": "x"}
    consume_bound_v0 = {"bound_consumed": True, "consume_scope": "navigation_handoff_consume_bound_v0"}
    post_bound_stub_pending = {
        "execution_stub_attempted": True,
        "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
        "execution_state": "execution_pending",
        "reason": "missing_formal_mid_platform_dispatch",
    }

    # A) all satisfied => ready_to_takeover
    applicable, payload = evaluate_navigation_executor_takeover_stub_v0(
        mid_platform_formal_decision_stub_v0={
            "decision_scope": "mid_platform_formal_decision_stub_v0",
            "decision_result": "allow_progress",
        },
        formal_decision_allow_progress_path_v0={
            "allow_progress_path_present": True,
            "downstream_placeholder_interface": "navigation_handoff_post_bound_execution_stub_v0",
            "consume_mode": "read_only",
        },
        navigation_handoff_post_bound_execution_stub_v0=post_bound_stub_pending,
        navigation_real_execution_readiness_gate_stub_v0={
            "readiness_attempted": True,
            "readiness_scope": "navigation_real_execution_readiness_gate_stub_v0",
            "readiness_status": "ready_candidate",
            "reason": "all_minimum_readiness_preconditions_satisfied",
        },
        destination_bound_v0=destination_bound_v0,
        navigation_handoff_consume_bound_v0=consume_bound_v0,
    )
    assert_eq(applicable, True, "A applicable")
    assert_eq(payload["takeover_status"], "ready_to_takeover", "A takeover_status")

    # B) readiness gate blocked => blocked (even if other inputs look present)
    applicable, payload = evaluate_navigation_executor_takeover_stub_v0(
        mid_platform_formal_decision_stub_v0={
            "decision_scope": "mid_platform_formal_decision_stub_v0",
            "decision_result": "allow_progress",
        },
        formal_decision_allow_progress_path_v0={
            "allow_progress_path_present": True,
            "downstream_placeholder_interface": "navigation_handoff_post_bound_execution_stub_v0",
            "consume_mode": "read_only",
        },
        navigation_handoff_post_bound_execution_stub_v0=post_bound_stub_pending,
        navigation_real_execution_readiness_gate_stub_v0={
            "readiness_attempted": True,
            "readiness_scope": "navigation_real_execution_readiness_gate_stub_v0",
            "readiness_status": "blocked",
            "reason": "hard_blocked:executor_status:unavailable",
        },
        destination_bound_v0=destination_bound_v0,
        navigation_handoff_consume_bound_v0=consume_bound_v0,
    )
    assert_eq(applicable, True, "B applicable")
    assert_eq(payload["takeover_status"], "blocked", "B takeover_status")

    # C) missing downstream interface match or consumption => not_applicable
    applicable, payload = evaluate_navigation_executor_takeover_stub_v0(
        mid_platform_formal_decision_stub_v0={
            "decision_scope": "mid_platform_formal_decision_stub_v0",
            "decision_result": "allow_progress",
        },
        formal_decision_allow_progress_path_v0={
            "allow_progress_path_present": True,
            "downstream_placeholder_interface": "some_other_interface",
            "consume_mode": "read_only",
        },
        navigation_handoff_post_bound_execution_stub_v0=post_bound_stub_pending,
        navigation_real_execution_readiness_gate_stub_v0={
            "readiness_attempted": True,
            "readiness_scope": "navigation_real_execution_readiness_gate_stub_v0",
            "readiness_status": "ready_candidate",
            "reason": "all_minimum_readiness_preconditions_satisfied",
        },
        destination_bound_v0=destination_bound_v0,
        navigation_handoff_consume_bound_v0=consume_bound_v0,
    )
    assert_eq(applicable, True, "C applicable")
    assert_eq(payload["takeover_status"], "not_applicable", "C takeover_status")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

