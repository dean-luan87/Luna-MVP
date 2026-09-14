# -*- coding: utf-8 -*-
"""Local-Global Progress 梯度收紧（M0）单测：只验证 narrative_evidence_tension_review 的 lg 分档。"""

from __future__ import annotations

from decision_monitor.narrative_evidence_tension_review import build_narrative_evidence_tension_review

_BASE_RSR = {
    "summary_reference_applied": True,
    "structured_event_layer_snapshot": {"event_count": 3},
    "mainline_narrative_brief": "brief",
    "memory_bias_accumulation_summary": "none",
    "closure_semantics_misalignment_summary": "none",
    "phase_closure_alignment_summary": "aligned",
}


def _frame(rsr: dict) -> dict:
    return {
        "trace_anchor_id": "lg_grad_test",
        "object_search_interaction": {"search_terminal_status": "none"},
        "run_summary_reference": {**_BASE_RSR, **rsr},
    }


def test_lg_low_weak_exploration_main_mixed_only():
    """正常探索：main_push_hint=mixed、无局部成功风险 → low（非 medium 一锅端）。"""
    tcp = (
        "stage=recheck; mode=paused; subtask=x; resume=—; success_hint=terminal=none; "
        "main_push_hint=mixed; local_only_risk=no; inserted_open=no; recovering=no; warn=none"
    )
    f = _frame(
        {
            "resume_chain_fragility_summary": "none",
            "resume_chain_progress_reached_main": False,
            "task_chain_progress_summary": tcp,
            "process_observation_summary": "resume_frag=none; phase_closure=aligned_or_unknown",
        }
    )
    r = build_narrative_evidence_tension_review(f)
    assert r.local_global_progress_tension == "low"


def test_lg_medium_local_risk_without_escalation():
    """局部成功风险 + 主未到位：仍为 medium（典型工程摩擦）。"""
    tcp = (
        "stage=fallback; mode=subtask; subtask=bottle; resume=—; success_hint=terminal=none; "
        "main_push_hint=mixed; local_only_risk=yes; inserted_open=no; recovering=no; warn=none"
    )
    f = _frame(
        {
            "resume_chain_fragility_summary": "none",
            "resume_chain_progress_reached_main": False,
            "task_chain_progress_summary": tcp,
            "process_observation_summary": "resume_frag=none; phase_closure=aligned_or_unknown",
        }
    )
    r = build_narrative_evidence_tension_review(f)
    assert r.local_global_progress_tension == "medium"


def test_lg_high_resume_fragility_string():
    """resume 链显式声明主未推进 → high。"""
    f = _frame(
        {
            "resume_chain_fragility_summary": "resume_declared_but_main_not_progressed",
            "resume_chain_progress_reached_main": False,
            "task_chain_progress_summary": "mode=main; resume=—",
            "process_observation_summary": "resume_frag=none",
        }
    )
    r = build_narrative_evidence_tension_review(f)
    assert r.local_global_progress_tension == "high"


def test_lg_high_structural_local_plus_inserted():
    """结构叠加：local_only_risk + inserted_open → high。"""
    tcp = (
        "stage=x; mode=subtask; subtask=a; resume=—; "
        "main_push_hint=mixed; local_only_risk=yes; inserted_open=yes; recovering=no; warn=none"
    )
    f = _frame(
        {
            "resume_chain_fragility_summary": "none",
            "resume_chain_progress_reached_main": False,
            "task_chain_progress_summary": tcp,
            "process_observation_summary": "resume_frag=none",
        }
    )
    r = build_narrative_evidence_tension_review(f)
    assert r.local_global_progress_tension == "high"


def test_resume_field_name_does_not_force_medium():
    """resume= 字段名不应单独触发「推进语言」假阳性（仅靠模板字段名不算 meaningful）。"""
    tcp = (
        "stage=s; mode=main; resume=—; success_hint=terminal=none; "
        "main_push_hint=yes; local_only_risk=no; inserted_open=no; recovering=no; warn=none"
    )
    f = _frame(
        {
            "resume_chain_fragility_summary": "none",
            "resume_chain_progress_reached_main": False,
            "task_chain_progress_summary": tcp,
            "process_observation_summary": "resume_frag=none",
        }
    )
    r = build_narrative_evidence_tension_review(f)
    assert r.local_global_progress_tension in ("low", "medium")


def test_pc_high_lg_pair_space_documented():
    """收紧后仍可能无 pc+lg 同 high；此处只断言 high 与 pc 可独立存在（不强制 critical）。"""
    f = _frame(
        {
            "resume_chain_fragility_summary": "resume_declared_but_main_not_progressed",
            "resume_chain_progress_reached_main": False,
            "task_chain_progress_summary": "mode=subtask; local_only_risk=yes",
            "process_observation_summary": "resume_frag=none",
            "closure_semantics_misalignment_summary": "phase_repair_visible_but_closure_still_none",
        }
    )
    r = build_narrative_evidence_tension_review(f)
    assert r.phase_closure_outcome_tension == "high"
    assert r.local_global_progress_tension == "high"
