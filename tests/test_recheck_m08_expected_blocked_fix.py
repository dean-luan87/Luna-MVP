# -*- coding: utf-8 -*-
"""M1.2：第九批 *_expected 标志 → recheck 可行动 fallback（最小定点）。"""

from decision_monitor.recheck_planner import build_recheck_planner


def _ctx(flag: str) -> dict:
    return {
        "frame_seq": 1,
        "trace_anchor_id": "t_m12",
        "focus_object_label": "bottle",
        flag: True,
    }


def test_m12_flags_force_clarification_and_unblock():
    flags = (
        "gradual_goal_drift_expected",
        "local_recovery_global_mismatch_expected",
        "multi_constraint_soft_shift_expected",
        "feedback_fact_consistent_but_wrong_expected",
        "task_semantic_crack_expected",
        "slow_poisoning_expected",
    )
    for f in flags:
        r = build_recheck_planner(None, None, None, None, ctx=_ctx(f))
        assert r.recheck_applied is True
        assert r.recheck_blocked is False
        assert r.recheck_action == "ask_user_for_clarification"
        assert f in (r.recheck_reason or "")
        assert "m12_new_expected_forced_user_clarification" in (r.recheck_reason or "")
