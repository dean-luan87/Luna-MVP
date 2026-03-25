# -*- coding: utf-8 -*-
"""M1.1：第八批 *_expected 标志 → recheck 可行动 fallback（最小定点）。"""

from decision_monitor.recheck_planner import build_recheck_planner


def _ctx(flag: str) -> dict:
    return {
        "frame_seq": 1,
        "trace_anchor_id": "t_m11",
        "focus_object_label": "bottle",
        flag: True,
    }


def test_m11_flags_force_clarification_and_unblock():
    flags = (
        "long_term_divergence_expected",
        "delayed_exposure_mismatch_expected",
        "task_subtask_fact_shift_expected",
        "success_condition_overwritten_expected",
        "false_multi_recovery_expected",
        "multi_feedback_source_conflict_expected",
    )
    for f in flags:
        r = build_recheck_planner(None, None, None, None, ctx=_ctx(f))
        assert r.recheck_applied is True
        assert r.recheck_blocked is False
        assert r.recheck_action == "ask_user_for_clarification"
        assert f in (r.recheck_reason or "")
        assert "m11_new_expected_forced_user_clarification" in (r.recheck_reason or "")
