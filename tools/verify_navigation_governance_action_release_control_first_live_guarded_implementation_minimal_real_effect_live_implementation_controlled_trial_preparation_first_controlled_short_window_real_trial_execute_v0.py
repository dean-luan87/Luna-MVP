# -*- coding: utf-8 -*-
"""
Verifier: Phase-Next-160 short-window REAL trial execute implementation obeys 151 + 155 + 158 + 159.

覆盖场景（至少）：
A no_execute_intent
B no_approval
C no_readiness_go
D armed_but_not_started
E legal_real_trial_execute_success
F legal_real_trial_execute_failure
G execute_window_timeout
H unauthorized_surface
I missing_audit_trace
J illegal_release_before_started
K execute_without_readiness_go (alias to C)
L default_path_probe (structural)
M closure_break_probe (synthetic illegal detection)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _readiness_go() -> dict:
    return {"overall_evaluation": "go"}


def _readiness_no_go() -> dict:
    return {"overall_evaluation": "no_go"}


def _guardrail_def() -> dict:
    return {"guardrail": "frozen_155"}


def _prep_go_gate() -> dict:
    return {"controlled_trial_preparation_go_no_go_status": "first_live_minimal_real_effect_controlled_trial_preparation_go"}


def _prep_shadow_eval_go() -> dict:
    return {"controlled_trial_preparation_shadow_eval_status": "first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go"}


def _prep_admitted() -> dict:
    return {"controlled_trial_preparation_status": "first_live_minimal_real_effect_controlled_trial_preparation_admitted"}


def _enablement_dry_run_executed() -> dict:
    return {
        "dry_run_status": "first_live_minimal_real_effect_controlled_trial_preparation_minimal_enablement_dry_run_executed"
    }


def _detect_illegal_states(observed: dict) -> list[str]:
    codes: list[str] = []
    start_event = bool(observed.get("start_event_observed"))
    started = bool(observed.get("controlled_short_window_real_trial_execute_started"))
    se = bool(observed.get("side_effects_released"))
    closed = bool(observed.get("closed"))

    if started and not start_event:
        codes.append("illegal_started_without_start_event")
    if se and not started:
        codes.append("illegal_release_without_started")
    if started and not closed:
        codes.append("illegal_started_without_closure")
    if closed and se:
        codes.append("illegal_release_not_recovered_after_closure")
    return codes


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_v0 import (  # noqa: E402
        run_first_controlled_short_window_real_trial_execute_v0,
    )

    def w_state(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_result(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_exc(p: dict) -> dict:
        return {"ok": True, "surface": p.get("surface")}

    def w_state_fail(_: dict) -> dict:
        raise RuntimeError("boom_state")

    base = dict(
        readiness_go_no_go_pack_v0=_readiness_go(),
        guardrail_definition_v0=_guardrail_def(),
        preparation_go_no_go_gate_v0=_prep_go_gate(),
        preparation_shadow_eval_gate_v0=_prep_shadow_eval_go(),
        preparation_admission_gate_v0=_prep_admitted(),
        preparation_enablement_dry_run_v0=_enablement_dry_run_executed(),
        execution_state_v0={"x": 1},
        result_v0={"x": 1},
        exception_or_failure_path_v0={"x": 1},
        side_effects_released=False,
        execution_state_writer=w_state,
        result_object_writer=w_result,
        exception_or_failure_writer=w_exc,
        execute_window_max_ms=1000,
        observed_elapsed_ms=10,
        execute_attempts_max=3,
        execute_attempts_observed=1,
        allowed_scopes_v0=["scope_a"],
        context={"test": "base"},
    )

    # A. no_execute_intent
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **base,
        explicit_short_window_real_trial_execute_intent_v0=None,
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("controlled_short_window_real_trial_execute_started") is False

    # B. no_approval
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **base,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0=None,
    )
    assert out.get("status") == "aborted"

    # C. no_readiness_go
    b_c = dict(base)
    b_c["readiness_go_no_go_pack_v0"] = _readiness_no_go()
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **b_c,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "execute_without_readiness_go"

    # D. armed_but_not_started
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **base,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": False},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "armed_not_started"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("armed_not_started") is True
    assert st.get("controlled_short_window_real_trial_execute_started") is False
    assert st.get("side_effects_released") is False

    # E. legal_real_trial_execute_success
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **base,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True, "requested_scope": "scope_a"},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "real_trial_execute_success"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("start_event_observed") is True
    assert st.get("controlled_short_window_real_trial_execute_started") is True
    assert st.get("closed") is True
    assert st.get("side_effects_released") is False

    # F. legal_real_trial_execute_failure (writer failure)
    b2 = dict(base)
    b2["execution_state_writer"] = w_state_fail
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **b2,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "real_trial_execute_failure_closed"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("closed") is True and st.get("side_effects_released") is False

    # G. execute_window_timeout
    b3 = dict(base)
    b3["observed_elapsed_ms"] = 2000
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **b3,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "execute_window_timeout"

    # H. unauthorized_surface
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **base,
        explicit_short_window_real_trial_execute_intent_v0={
            "intent": True,
            "allow_start_event_observed": True,
            "requested_surfaces": ["route"],
        },
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "unauthorized_side_effect_surface"

    # I. missing_audit_trace
    b4 = dict(base)
    b4["execute_window_max_ms"] = "x"
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **b4,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "audit_trace_missing_or_broken"

    # J. illegal_release_before_started (entry must reject se=true)
    b5 = dict(base)
    b5["side_effects_released"] = True
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **b5,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "no_started_but_release"

    # K. execute_without_readiness_go (alias)
    b_k = dict(base)
    b_k["readiness_go_no_go_pack_v0"] = _readiness_no_go()
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **b_k,
        explicit_short_window_real_trial_execute_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "execute_without_readiness_go"

    # L. default_path_probe: structural (explicit intent required)
    out = run_first_controlled_short_window_real_trial_execute_v0(
        **base,
        explicit_short_window_real_trial_execute_intent_v0=None,
        explicit_short_window_real_trial_execute_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"

    # M. closure_break_probe (synthetic illegal)
    synthetic = {
        "start_event_observed": True,
        "controlled_short_window_real_trial_execute_started": True,
        "side_effects_released": False,
        "closed": False,
    }
    codes = _detect_illegal_states(synthetic)
    assert "illegal_started_without_closure" in codes

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

