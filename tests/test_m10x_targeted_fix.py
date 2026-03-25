# -*- coding: utf-8 -*-
"""M1.0.x 定点修复单测（R53/R54/R55/R56 对应触发器）。"""

from __future__ import annotations

from decision_monitor.builder import DecisionMonitorBuilder


def _base(flag: str):
    return {
        "frame_seq": 100,
        "current_ts": 0.0,
        "trace_anchor_id": f"test_{flag}",
        "focus_object_label": "bottle",
        "search_subtask_state": "waiting_user_reply",
        "search_terminal_status": "none",
        "confirmation_input_type": "confirmed_no",
        "confirmation_input_raw_text": "not this one",
        flag: True,
    }


def _assert_forced_clarify(frame: dict):
    rp = frame.get("recheck_planner") or {}
    assert rp.get("recheck_action") == "ask_user_for_clarification"
    assert rp.get("recheck_applied") is True
    assert rp.get("recheck_blocked") is False


def test_r53_resume_without_progress_forced_clarify():
    frame = DecisionMonitorBuilder().build(_base("main_task_resumed_but_not_progressed_expected")).to_dict()
    _assert_forced_clarify(frame)


def test_r54_inserted_exit_ambiguous_forced_clarify():
    frame = DecisionMonitorBuilder().build(_base("inserted_task_exit_ambiguous_expected")).to_dict()
    _assert_forced_clarify(frame)


def test_r55_memory_observation_conflict_forced_clarify():
    ctx = _base("memory_supported_but_observation_conflicted_expected")
    ctx.update({"memory_hint_present": True, "novel_candidate_present": True})
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    _assert_forced_clarify(frame)


def test_r56_source_shift_reflected_in_mainline_phase():
    ctx = _base("dynamic_source_shift_but_mainline_static_expected")
    ctx.update({"memory_hint_present": True, "novel_candidate_present": True})
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    _assert_forced_clarify(frame)
    mss = frame.get("mainline_state_snapshot") or {}
    assert mss.get("mainline_phase") == "recheck_or_repair"
