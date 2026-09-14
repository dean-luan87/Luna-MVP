# -*- coding: utf-8 -*-
"""
Verifier: Phase-Next-156 short-window trial implementation obeys Phase-Next-151 + Phase-Next-155 guardrails.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _pack_go() -> dict:
    return {"recommended_go_no_go_pack_conclusion": "go"}


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


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_trial_v0 import (  # noqa: E402
        run_first_live_controlled_short_window_trial_v0,
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
        guardrail_pack_go_no_go_v0=_pack_go(),
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
        trial_window_max_ms=1000,
        observed_elapsed_ms=10,
        context={"test": "base"},
    )

    # A. no_explicit_intent => aborted
    out = run_first_live_controlled_short_window_trial_v0(
        **base,
        explicit_short_window_trial_intent_v0=None,
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("controlled_short_window_trial_started") is False

    # B. no_approval => aborted
    out = run_first_live_controlled_short_window_trial_v0(
        **base,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_trial_approval_v0=None,
    )
    assert out.get("status") == "aborted"

    # C. armed_but_not_started (intent forbids start_event)
    out = run_first_live_controlled_short_window_trial_v0(
        **base,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": False},
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "armed_not_started"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("armed_not_started") is True and st.get("controlled_short_window_trial_started") is False

    # D. legal_short_window_success
    out = run_first_live_controlled_short_window_trial_v0(
        **base,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "trial_executed_success"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("start_event_observed") is True
    assert st.get("controlled_short_window_trial_started") is True
    assert st.get("closed") is True
    assert st.get("side_effects_released") is False

    # E. legal_short_window_failure (writer failure)
    b2 = dict(base)
    b2["execution_state_writer"] = w_state_fail
    out = run_first_live_controlled_short_window_trial_v0(
        **b2,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "trial_executed_failure_closed"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("closed") is True and st.get("side_effects_released") is False

    # F. window_timeout => aborted with trial_window_timeout
    b3 = dict(base)
    b3["observed_elapsed_ms"] = 2000
    out = run_first_live_controlled_short_window_trial_v0(
        **b3,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "trial_window_timeout"

    # G. unauthorized_surface => aborted
    out = run_first_live_controlled_short_window_trial_v0(
        **base,
        explicit_short_window_trial_intent_v0={
            "intent": True,
            "allow_start_event_observed": True,
            "requested_surfaces": ["route"],
        },
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "unauthorized_side_effect_surface"

    # H. illegal_release_before_started (synthetic: entry must reject se=true)
    b4 = dict(base)
    b4["side_effects_released"] = True
    out = run_first_live_controlled_short_window_trial_v0(
        **b4,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "no_started_but_release"

    # I. missing_audit_trace (window params not int)
    b5 = dict(base)
    b5["trial_window_max_ms"] = "x"
    out = run_first_live_controlled_short_window_trial_v0(
        **b5,
        explicit_short_window_trial_intent_v0={"intent": True, "allow_start_event_observed": True},
        explicit_short_window_trial_approval_v0={"approve": True},
    )
    assert out.get("status") == "aborted"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("abort_trigger_id") == "audit_trace_missing_or_broken"

    # J. default_path_probe: there is no implicit entry; validate by absence of any exported default runner
    # (Verified structurally by requiring explicit_short_window_trial_intent_v0 and approval.)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

