# -*- coding: utf-8 -*-
"""
Verifier: Phase-Next-152 first minimal real enablement implementation obeys Phase-Next-151 definition.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_prep_go_gate() -> dict:
    return {"controlled_trial_preparation_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_preparation_go"}


def _mk_prep_shadow_eval_go() -> dict:
    return {"controlled_trial_preparation_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"}


def _mk_prep_admitted() -> dict:
    return {"controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"}


def _mk_enablement_dry_run_executed() -> dict:
    return {
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed"
    }


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_minimal_real_enablement_v0 import (  # noqa: E402
        accept_first_live_minimal_real_effect_controlled_trial_preparation_first_minimal_real_enablement_input,
        run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0,
    )

    # 1) readiness insufficient => no started, no release
    res = accept_first_live_minimal_real_effect_controlled_trial_preparation_first_minimal_real_enablement_input(
        preparation_go_no_go_gate_v0=None,
        preparation_shadow_eval_gate_v0=None,
        preparation_admission_gate_v0=None,
        preparation_enablement_dry_run_v0=None,
        preparation_enablement_intent_v0=None,
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        context={"test": "not_ready"},
    )
    assert res.get("ok") is False and res.get("status") == "not_ready"

    # 2) only preparation_go (missing others) => not_ready; must not started
    out = run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
        preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
        preparation_shadow_eval_gate_v0=None,
        preparation_admission_gate_v0=None,
        preparation_enablement_dry_run_v0=None,
        preparation_enablement_intent_v0={"intent": True},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=lambda p: {"ok": True},
        result_object_writer=lambda p: {"ok": True},
        exception_or_failure_writer=lambda p: {"ok": True},
        context={"test": "only_go"},
    )
    payload = out.get("payload") or {}
    state = payload.get("state") or {}
    assert out.get("ok") is False
    assert state.get("start_event_observed") is False
    assert state.get("real_enablement_started") is False
    assert state.get("side_effects_released") is False

    # 3) dry_run_executed but no real-start intent => not_ready
    out = run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
        preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
        preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
        preparation_admission_gate_v0=_mk_prep_admitted(),
        preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        preparation_enablement_intent_v0=None,
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=lambda p: {"ok": True},
        result_object_writer=lambda p: {"ok": True},
        exception_or_failure_writer=lambda p: {"ok": True},
        context={"test": "no_intent"},
    )
    payload = out.get("payload") or {}
    state = payload.get("state") or {}
    assert out.get("ok") is False
    assert state.get("real_enablement_started") is False
    assert state.get("side_effects_released") is False

    # 4) start gate satisfied => started + short window + closure => side_effects_released false finally
    calls = []

    def w_state(p: dict) -> dict:
        calls.append(("state", dict(p)))
        return {"ok": True}

    def w_result(p: dict) -> dict:
        calls.append(("result", dict(p)))
        return {"ok": True}

    def w_exc(p: dict) -> dict:
        calls.append(("exc", dict(p)))
        return {"ok": True}

    out = run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
        preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
        preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
        preparation_admission_gate_v0=_mk_prep_admitted(),
        preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        preparation_enablement_intent_v0={"intent": True, "reason": "unit_test"},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=w_state,
        result_object_writer=w_result,
        exception_or_failure_writer=w_exc,
        context={"test": "success"},
    )
    assert out.get("ok") is True and out.get("status") == "executed"
    payload = out.get("payload") or {}
    state = payload.get("state") or {}
    trace = payload.get("trace") or {}
    assert state.get("armed_not_started") is True
    assert state.get("start_event_observed") is True
    assert state.get("real_enablement_started") is True
    assert state.get("closed") is True
    assert state.get("side_effects_released") is False
    assert "start_event_observed" in (trace.get("order") or [])
    assert calls[0][0] == "state" and calls[1][0] == "result"

    # 5) failure path => must still close and se false; no illegal started without start_event
    calls.clear()

    def w_state_fail(p: dict) -> dict:
        calls.append(("state_fail", dict(p)))
        raise RuntimeError("boom_state")

    out = run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(
        preparation_go_no_go_gate_v0=_mk_prep_go_gate(),
        preparation_shadow_eval_gate_v0=_mk_prep_shadow_eval_go(),
        preparation_admission_gate_v0=_mk_prep_admitted(),
        preparation_enablement_dry_run_v0=_mk_enablement_dry_run_executed(),
        preparation_enablement_intent_v0={"intent": True, "reason": "unit_test"},
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=w_state_fail,
        result_object_writer=w_result,
        exception_or_failure_writer=w_exc,
        context={"test": "failure"},
    )
    assert out.get("ok") is False and out.get("status") == "failed"
    payload = out.get("payload") or {}
    state = payload.get("state") or {}
    trace = payload.get("trace") or {}
    assert state.get("start_event_observed") is True  # started only after event
    assert state.get("real_enablement_started") is True
    assert state.get("minimal_failure_reached") is True
    assert state.get("closed") is True
    assert state.get("side_effects_released") is False
    assert "closure_recover_side_effects_false_on_failure" in (trace.get("order") or [])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

