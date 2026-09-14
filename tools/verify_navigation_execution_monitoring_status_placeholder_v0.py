from __future__ import annotations

import os
import sys
from pathlib import Path


def _boot_repo_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    sys.path.insert(0, str(root))
    return root


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> None:
    _boot_repo_root()

    from capabilities.mid_platform.runtime.navigation_execution_monitoring_status_placeholder_v0 import (
        evaluate_navigation_execution_monitoring_status_placeholder_v0,
    )

    # A) Missing all → relevant-only
    applicable, payload = evaluate_navigation_execution_monitoring_status_placeholder_v0(
        navigation_executor_takeover_stub_v0=None,
        navigation_real_executor_status_v0=None,
        navigation_real_executor_input_v0=None,
    )
    _assert(applicable is False, "A: should be relevant-only (not applicable)")
    _assert(payload is None, "A: payload must be None when not applicable")

    # B) Missing executor status → relevant-only
    applicable, payload = evaluate_navigation_execution_monitoring_status_placeholder_v0(
        navigation_executor_takeover_stub_v0={"takeover_scope": "navigation_executor_takeover_stub_v0", "takeover_status": "ready_to_takeover"},
        navigation_real_executor_status_v0=None,
        navigation_real_executor_input_v0=None,
    )
    _assert(applicable is False, "B: should be relevant-only (missing status)")
    _assert(payload is None, "B: payload must be None when not applicable")

    # C) Happy path minimal (tk + st)
    applicable, payload = evaluate_navigation_execution_monitoring_status_placeholder_v0(
        navigation_executor_takeover_stub_v0={"takeover_scope": "navigation_executor_takeover_stub_v0", "takeover_status": "ready_to_takeover"},
        navigation_real_executor_status_v0={
            "executor_status_present": True,
            "executor_status_scope": "navigation_real_executor_status_v0",
            "takeover_state": "placeholder_pre_execution",
            "execution_state": "not_started_placeholder",
            "consume_mode": "read_only",
        },
        navigation_real_executor_input_v0=None,
    )
    _assert(applicable is True, "C: should be applicable")
    _assert(isinstance(payload, dict), "C: payload must be dict")
    _assert(payload.get("monitoring_status_present") is True, "C: monitoring_status_present must be true")
    _assert(payload.get("monitoring_status_scope") == "navigation_execution_monitoring_status_v0", "C: scope mismatch")
    _assert(payload.get("takeover_monitor_state") == "pre_execution_placeholder", "C: takeover monitor must be placeholder")
    _assert(payload.get("execution_monitor_state") == "not_started_placeholder", "C: execution monitor must be placeholder")
    _assert(payload.get("consume_mode") == "read_only", "C: must be read_only")

    # D) With input object (must match scope + read_only)
    applicable, payload = evaluate_navigation_execution_monitoring_status_placeholder_v0(
        navigation_executor_takeover_stub_v0={"takeover_scope": "navigation_executor_takeover_stub_v0", "takeover_status": "ready_to_takeover"},
        navigation_real_executor_status_v0={"executor_status_scope": "navigation_real_executor_status_v0"},
        navigation_real_executor_input_v0={"executor_input_scope": "navigation_real_executor_input_v0", "consume_mode": "read_only"},
    )
    _assert(applicable is True, "D: should be applicable when optional input is valid")
    _assert(payload is not None, "D: payload should exist")

    # E) Reject mismatched scopes (avoid treating unrelated dicts as evidence)
    applicable, payload = evaluate_navigation_execution_monitoring_status_placeholder_v0(
        navigation_executor_takeover_stub_v0={"takeover_scope": "not_ours"},
        navigation_real_executor_status_v0={"executor_status_scope": "navigation_real_executor_status_v0"},
        navigation_real_executor_input_v0=None,
    )
    _assert(applicable is False, "E: should be relevant-only for mismatched takeover scope")
    _assert(payload is None, "E: payload must be None")

    print("OK: verify_navigation_execution_monitoring_status_placeholder_v0")


if __name__ == "__main__":
    main()

