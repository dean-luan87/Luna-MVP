# -*- coding: utf-8 -*-
"""
Verifier: Phase-Next-164 post-execute decision implementation obeys Phase-Next-163.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def _mk_execute_result(
    *,
    closed: bool = True,
    se_false: bool = True,
    status: str = "real_trial_execute_success",
    reason: str = "ok",
    abort_trigger_id: str | None = None,
    stop_trigger_id: str | None = None,
    trace_ok: bool = True,
) -> dict:
    return {
        "ok": True,
        "status": status,
        "reason": reason,
        "payload": {
            "state": {
                "closed": bool(closed),
                "side_effects_released": False if se_false else True,
                "abort_trigger_id": abort_trigger_id,
                "stop_trigger_id": stop_trigger_id,
            },
            "trace": {"order": ["x"] if trace_ok else []},
        },
    }


def main() -> int:
    from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_post_execute_decision_v0 import (  # noqa: E402
        run_first_controlled_short_window_real_trial_post_execute_decision_v0,
    )

    base = dict(
        explicit_post_execute_decision_entry_v0={"intent": True},
        execute_result_v0=_mk_execute_result(),
        execute_go_no_go_pack_v0={"overall_evaluation": "go"},
        post_execute_decision_definition_v0={"frozen": "163"},
        context={"test": "base"},
    )

    # A. no_legal_final_close
    b_a = dict(base)
    b_a["execute_result_v0"] = _mk_execute_result(closed=False)
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_a)
    assert out.get("status") == "not_eligible"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("allowed_outcome_selected") == "remain_closed_safe"

    # B. se_not_false
    b_b = dict(base)
    b_b["execute_result_v0"] = _mk_execute_result(se_false=False)
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_b)
    assert out.get("status") == "not_eligible"

    # C. evidence_incomplete -> remain_closed_safe
    b_c = dict(base)
    b_c["execute_result_v0"] = _mk_execute_result(trace_ok=False)
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_c)
    assert out.get("status") == "decided"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("allowed_outcome_selected") == "remain_closed_safe"
    assert st.get("closed_safe_state_preserved") is True

    # D. clean_success_case -> retry_allowed_under_same_guardrails (but no auto retry)
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**base)
    assert out.get("status") == "decided"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("allowed_outcome_selected") in {"retry_allowed_under_same_guardrails", "remain_closed_safe"}
    assert st.get("allows_retry_now") is False
    assert st.get("closed_safe_state_preserved") is True

    # E. boundary_violation_case -> retry_not_allowed_until_new_definition
    b_e = dict(base)
    b_e["execute_result_v0"] = _mk_execute_result(abort_trigger_id="unauthorized_side_effect_surface")
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_e)
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("allowed_outcome_selected") == "retry_not_allowed_until_new_definition"
    assert st.get("requires_new_governance_definition") is True

    # F. widening_needed_case -> escalate_for_new_governance_definition
    b_f = dict(base)
    b_f["explicit_post_execute_decision_entry_v0"] = {"intent": True, "widening_needed": True}
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_f)
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("allowed_outcome_selected") == "escalate_for_new_governance_definition"

    # G. forbidden_reopen_probe -> blocked + remain_closed_safe
    b_g = dict(base)
    b_g["explicit_post_execute_decision_entry_v0"] = {"intent": True, "requested_forbidden_outcome_probe": "implicit_reopen"}
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_g)
    assert out.get("status") == "blocked"
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("forbidden_outcome_blocked") is True
    assert st.get("allowed_outcome_selected") == "remain_closed_safe"

    # H. forbidden_retry_probe
    b_h = dict(base)
    b_h["explicit_post_execute_decision_entry_v0"] = {"intent": True, "requested_forbidden_outcome_probe": "implicit_execute_retry"}
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_h)
    assert out.get("status") == "blocked"

    # I. forbidden_widen_probe
    b_i = dict(base)
    b_i["explicit_post_execute_decision_entry_v0"] = {"intent": True, "requested_forbidden_outcome_probe": "implicit_widening"}
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_i)
    assert out.get("status") == "blocked"

    # J. default_path_probe (no explicit entry)
    b_j = dict(base)
    b_j["explicit_post_execute_decision_entry_v0"] = None
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_j)
    assert out.get("status") == "blocked"

    # K. stop_block_case
    b_k = dict(base)
    b_k["explicit_post_execute_decision_entry_v0"] = {"intent": True, "structural_safety_issue": True}
    out = run_first_controlled_short_window_real_trial_post_execute_decision_v0(**b_k)
    st = (out.get("payload") or {}).get("state") or {}
    assert st.get("allowed_outcome_selected") == "stop_and_block_further_real_action"

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

