# -*- coding: utf-8 -*-
"""
Local verification for navigation_real_executor_status_placeholder_v0 (read-only helper).

Covers:
- A: minimal evidence satisfied => writes placeholder payload
- B: missing takeover stub => not applicable (relevant-only)
- C: missing executor input object => not applicable (relevant-only)
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

    from capabilities.mid_platform.runtime.navigation_real_executor_status_placeholder_v0 import (  # noqa: E402
        evaluate_navigation_real_executor_status_placeholder_v0,
    )

    def assert_eq(a, b, msg: str) -> None:
        if a != b:
            raise AssertionError(f"{msg}: expected={b!r} got={a!r}")

    tk = {
        "takeover_attempted": True,
        "takeover_scope": "navigation_executor_takeover_stub_v0",
        "takeover_status": "ready_to_takeover",
        "reason": "all_minimum_takeover_preconditions_satisfied",
    }
    inp = {
        "executor_input_present": True,
        "executor_input_scope": "navigation_real_executor_input_v0",
        "takeover_authorized": True,
        "task_context_ready": True,
        "path_support_mode": "unknown_placeholder",
        "execution_constraints_ready": False,
        "monitor_binding_ready": False,
        "consume_mode": "read_only",
    }

    # A) satisfied => applicable True and payload present
    applicable, payload = evaluate_navigation_real_executor_status_placeholder_v0(
        navigation_executor_takeover_stub_v0=tk,
        navigation_real_executor_input_v0=inp,
        navigation_real_execution_readiness_gate_stub_v0=None,
    )
    assert_eq(applicable, True, "A applicable")
    assert_eq(payload.get("executor_status_scope"), "navigation_real_executor_status_v0", "A scope")
    assert_eq(payload.get("executor_status_present"), True, "A present")
    assert_eq(payload.get("consume_mode"), "read_only", "A consume_mode")
    assert_eq(payload.get("execution_state"), "not_started_placeholder", "A execution_state placeholder")

    # B) missing takeover stub => relevant-only
    applicable, payload = evaluate_navigation_real_executor_status_placeholder_v0(
        navigation_executor_takeover_stub_v0=None,
        navigation_real_executor_input_v0=inp,
    )
    assert_eq(applicable, False, "B applicable")
    assert_eq(payload, None, "B payload")

    # C) missing input object => relevant-only
    applicable, payload = evaluate_navigation_real_executor_status_placeholder_v0(
        navigation_executor_takeover_stub_v0=tk,
        navigation_real_executor_input_v0=None,
    )
    assert_eq(applicable, False, "C applicable")
    assert_eq(payload, None, "C payload")

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

