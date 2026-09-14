# -*- coding: utf-8 -*-
"""
Self-test: Release Control First Live Guarded Implementation
Minimal Real-Effect Live Implementation v0 (First Minimal Real Write Code)

This test uses in-memory writers only (no external side effects).
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0 import (  # noqa: E402
        get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_identity,
        run_first_live_minimal_real_write_v0,
    )

    ident = get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_identity()
    assert ident.get("default_enabled") is False
    assert "execution_state_real_write" in (ident.get("allowed_real_write_surfaces") or [])

    events: list[tuple[str, dict]] = []

    def mk_writer(tag: str, *, fail: bool = False):
        def _w(payload: dict) -> dict:
            events.append((tag, dict(payload)))
            if fail:
                raise RuntimeError(f"{tag}_failed")
            return {"ok": True, "tag": tag, "side_effects_released": False}

        return _w

    go = {"real_write_status": "first_live_minimal_real_effect_real_write_go"}
    cp = {"dry_run_status": "first_live_minimal_real_effect_live_code_path_dry_run_executed"}
    sig = {"signal": "explicit_real_write"}
    xs = {"present": True}
    rs = {"present": True}
    ex = {"present": True}

    # A: normal success
    events.clear()
    out = run_first_live_minimal_real_write_v0(
        real_write_go_no_go_gate_v0=go,
        live_code_path_dry_run_v0=cp,
        real_write_approval_or_signal_v0=sig,
        execution_state_v0=xs,
        result_v0=rs,
        exception_or_failure_path_v0=ex,
        side_effects_released=False,
        execution_state_writer=mk_writer("state"),
        result_object_writer=mk_writer("result"),
        exception_or_failure_writer=mk_writer("exception"),
        context={"test": "A"},
    )
    assert out.get("ok") is True
    assert out.get("payload", {}).get("side_effects_released") is False
    assert [t for (t, _) in events] == ["state", "result"]

    # B: missing signal => not_ready, no writes
    events.clear()
    out2 = run_first_live_minimal_real_write_v0(
        real_write_go_no_go_gate_v0=go,
        live_code_path_dry_run_v0=cp,
        real_write_approval_or_signal_v0=None,
        execution_state_v0=xs,
        result_v0=rs,
        exception_or_failure_path_v0=ex,
        side_effects_released=False,
        execution_state_writer=mk_writer("state"),
        result_object_writer=mk_writer("result"),
        exception_or_failure_writer=mk_writer("exception"),
        context={"test": "B"},
    )
    assert out2.get("ok") is False
    assert out2.get("status") in ("not_ready", "blocked")
    assert events == []

    # C: side_effects_released != false => blocked, no writes
    events.clear()
    out3 = run_first_live_minimal_real_write_v0(
        real_write_go_no_go_gate_v0=go,
        live_code_path_dry_run_v0=cp,
        real_write_approval_or_signal_v0=sig,
        execution_state_v0=xs,
        result_v0=rs,
        exception_or_failure_path_v0=ex,
        side_effects_released=True,
        execution_state_writer=mk_writer("state"),
        result_object_writer=mk_writer("result"),
        exception_or_failure_writer=mk_writer("exception"),
        context={"test": "C"},
    )
    assert out3.get("ok") is False
    assert out3.get("status") == "blocked"
    assert events == []

    # D: state write fails => failure path attempts failure writes then exception write
    events.clear()
    out4 = run_first_live_minimal_real_write_v0(
        real_write_go_no_go_gate_v0=go,
        live_code_path_dry_run_v0=cp,
        real_write_approval_or_signal_v0=sig,
        execution_state_v0=xs,
        result_v0=rs,
        exception_or_failure_path_v0=ex,
        side_effects_released=False,
        execution_state_writer=mk_writer("state", fail=True),
        result_object_writer=mk_writer("result"),
        exception_or_failure_writer=mk_writer("exception"),
        context={"test": "D"},
    )
    assert out4.get("ok") is False
    assert out4.get("payload", {}).get("side_effects_released") is False
    tags = [t for (t, _) in events]
    assert "exception" in tags

    print("ALL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

