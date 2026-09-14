# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Enablement Dry-Run Stub v0.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import capabilities.governance.runtime.navigation_governance_action_release_control_first_live_enablement_dry_run_stub_v0 as m

    # A: import + identity fixed
    ident = m.get_release_control_first_live_enablement_dry_run_identity()
    assert ident.get("is_stub") is True
    assert ident.get("can_open_side_effects_released") is False

    # B: input interface does not enable
    out = m.accept_enablement_dry_run_input(approval_signal={"approved": True}, context={"k": "v"})
    assert out.get("status") == "not_implemented"
    assert out.get("payload", {}).get("side_effects_released") is False

    # C: precondition evaluation returns dry-run result and keeps lock false
    pre = m.evaluate_enablement_dry_run_preconditions(
        live_release_gate_v0={"x": 1},
        side_effect_release_gate_v0={"x": 1},
        guarded_live_stub_v0={"x": 1},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        approval_signal={"approved": True},
    )
    assert pre.get("release_control_first_live_enablement_dry_run_attempted") is True
    assert pre.get("side_effects_released") is False
    assert pre.get("dry_run_status") in {"enablement_dry_run_ready", "enablement_dry_run_not_ready", "enablement_dry_run_blocked"}

    # D: rollback simulation does not modify state; returns safe payload
    rb = m.simulate_enablement_rollback_path(context={"why": "test"})
    assert rb.get("side_effects_released") is False
    assert rb.get("side_effects_released_restored") is True

    # E: exception preserves semantics
    rep = m.raise_enablement_dry_run_exception(exc=RuntimeError("x"), context={"k": "v"})
    assert rep.get("exception_status") == "reported_placeholder"
    assert rep.get("exception_type") == "RuntimeError"
    assert rep.get("exception_message") == "x"
    assert rep.get("context", {}).get("k") == "v"

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

