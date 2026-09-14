# -*- coding: utf-8 -*-
"""
Self-test: Controlled Trial Preparation Real v0 (minimal real writes; injected writers).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_prep_admitted() -> dict:
    return {"controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"}


def _mk_prep_dry_run_executed() -> dict:
    return {"dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed"}


def _mk_ct_go() -> dict:
    return {"controlled_trial_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_go"}


def _mk_ct_real_enablement_ready() -> dict:
    return {"real_enablement_status": "first_live_minimal_real_effect_controlled_trial_real_enablement_ready"}


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_real_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_controlled_trial_preparation_real_input,
        run_first_live_controlled_trial_first_minimal_real_preparation_v0,
    )

    calls = []

    def w_state(payload: dict) -> dict:
        calls.append(("state", dict(payload)))
        return {"ok": True}

    def w_result(payload: dict) -> dict:
        calls.append(("result", dict(payload)))
        return {"ok": True}

    def w_exc(payload: dict) -> dict:
        calls.append(("exc", dict(payload)))
        return {"ok": True}

    # 1) accept blocked when side_effects_released != False
    res = accept_first_live_minimal_real_effect_controlled_trial_preparation_real_input(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_real_approval_or_signal_v0={"approve": True},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=True,
        context={"test": "blocked"},
    )
    assert res.get("status") == "blocked"

    # 2) accept not_ready when missing approval/signal
    res = accept_first_live_minimal_real_effect_controlled_trial_preparation_real_input(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_real_approval_or_signal_v0=None,
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        context={"test": "missing_signal"},
    )
    assert res.get("status") == "not_ready"

    # 3) success path: executed + recover false in payload
    calls.clear()
    out = run_first_live_controlled_trial_first_minimal_real_preparation_v0(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_real_approval_or_signal_v0={"approve": True, "reason": "unit_test"},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=w_state,
        result_object_writer=w_result,
        exception_or_failure_writer=w_exc,
        context={"test": "success"},
    )
    assert out.get("status") == "executed"
    payload = out.get("payload") or {}
    assert payload.get("side_effects_released") is False
    trace = payload.get("trace") or {}
    assert trace.get("order")[:3] == [
        "enter_controlled_short_activation_semantic",
        "execution_state_real_write",
        "result_object_real_write",
    ]
    assert calls[0][0] == "state" and calls[1][0] == "result"

    # 4) failure path: state writer fails => failed + best-effort closure writes + exception writer called
    calls.clear()

    def w_state_fail(payload: dict) -> dict:
        calls.append(("state_fail", dict(payload)))
        raise RuntimeError("boom_state")

    out = run_first_live_controlled_trial_first_minimal_real_preparation_v0(
        controlled_trial_preparation_admission_gate_v0=_mk_prep_admitted(),
        controlled_trial_preparation_dry_run_v0=_mk_prep_dry_run_executed(),
        controlled_trial_go_no_go_gate_v0=_mk_ct_go(),
        controlled_trial_first_minimal_real_enablement_v0=_mk_ct_real_enablement_ready(),
        preparation_real_approval_or_signal_v0={"approve": True, "reason": "unit_test"},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=w_state_fail,
        result_object_writer=w_result,
        exception_or_failure_writer=w_exc,
        context={"test": "failure_state"},
    )
    assert out.get("status") == "failed"
    payload = out.get("payload") or {}
    assert payload.get("side_effects_released") is False
    trace = payload.get("trace") or {}
    assert "recover_side_effects_false_on_failure" in (trace.get("order") or [])
    assert any(c[0] == "exc" for c in calls) is True

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

