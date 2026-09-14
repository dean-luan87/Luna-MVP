# -*- coding: utf-8 -*-

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.information_source_scheduler import build_scheduled_source_state
from decision_monitor.run_summary_builder import build_run_summary_reference
from decision_monitor.task_chain_state_snapshot import build_task_chain_state_snapshot


def _ctx():
    return {
        "frame_seq": 3,
        "current_ts": 1.0,
        "trace_anchor_id": "t_tcs_m0",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [1, 2, 3, 4]}],
    }


def test_build_minimal_task_chain_state_snapshot():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    snap = frame.get("task_chain_state_snapshot")
    assert isinstance(snap, dict)
    assert snap.get("task_chain_state_snapshot_applied") is True
    assert snap.get("task_chain_id")
    assert snap.get("task_mode") in ("main", "subtask", "inserted", "recovering", "paused", "unknown")


def test_snapshot_on_frame():
    f = DecisionMonitorBuilder().build(_ctx())
    assert f.task_chain_state_snapshot is not None
    assert f.task_chain_state_snapshot.task_chain_state_snapshot_applied is True


def test_scheduled_source_includes_task_state():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    sched = build_scheduled_source_state(frame).to_dict()
    assert "task_state" in (sched.get("participating_sources") or [])
    assert sched.get("task_state_presence_summary")


def test_whitebox_tree_summary_has_task():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree

    tree = build_reasoning_structure_tree(frame).to_dict()
    ts = tree.get("tree_summary") or ""
    assert "task_pos=" in ts


def test_run_summary_has_task_chain_progress():
    frame = DecisionMonitorBuilder().build(_ctx()).to_dict()
    rsr = build_run_summary_reference(frame).to_dict()
    assert rsr.get("task_chain_progress_summary")
    assert "stage=" in (rsr.get("task_chain_progress_summary") or "")
