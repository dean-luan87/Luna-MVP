# -*- coding: utf-8 -*-
"""Resume Progress Summary Alignment M0：场景 resume 线索进入 inputs/TCS/run_summary。"""

from __future__ import annotations

import json
from pathlib import Path

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.narrative_evidence_tension_review import build_narrative_evidence_tension_review
from decision_monitor.run_summary_builder import build_run_summary_reference
from decision_monitor.task_chain_state_snapshot import build_task_chain_progress_summary

ROOT = Path(__file__).resolve().parents[1]


def _ctx(name: str) -> dict:
    return json.loads((ROOT / "tests" / "real_scenarios" / "ctx" / name).read_text(encoding="utf-8"))


def test_scenario_resume_hint_merges_into_task_chain_snapshot():
    ctx = _ctx("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")
    d = DecisionMonitorBuilder().build(ctx).to_dict()
    inp = d.get("inputs")
    if hasattr(inp, "to_dict"):
        inp = inp.to_dict()
    assert inp.get("scenario_task_resume_target") == "resume_main_search_route"
    assert inp.get("recovery_declared_but_resume_chain_fragile_expected") is True
    tcs = d.get("task_chain_state_snapshot")
    if hasattr(tcs, "to_dict"):
        tcs = tcs.to_dict()
    assert tcs.get("task_resume_target") == "resume_main_search_route"
    assert "resume_main_progress_alignment_summary" in tcs
    assert "resume_chain_fragile_expected" in (tcs.get("resume_main_progress_alignment_summary") or "")


def test_task_chain_progress_summary_includes_resume_main_align():
    ctx = _ctx("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")
    d = DecisionMonitorBuilder().build(ctx).to_dict()
    tcs = d.get("task_chain_state_snapshot")
    if hasattr(tcs, "to_dict"):
        tcs = tcs.to_dict()
    line = build_task_chain_progress_summary(tcs)
    assert "resume_main_align=" in line
    assert "global_main_progress_not_terminal_complete" in line or "resume_target_traced" in line


def test_run_summary_resume_frag_and_m11x_when_fragile_expected():
    ctx = _ctx("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")
    d = DecisionMonitorBuilder().build(ctx).to_dict()
    rsr = build_run_summary_reference(d)
    if hasattr(rsr, "to_dict"):
        rsr = rsr.to_dict()
    assert rsr.get("resume_chain_fragility_summary") == "resume_declared_but_main_not_progressed"
    proc = rsr.get("process_observation_summary") or ""
    assert "m11x_ctx_observed" in proc
    assert "resume_frag=resume_declared_but_main_not_progressed" in proc


def test_pc_high_lg_high_same_frame_after_alignment():
    ctx = _ctx("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")
    d = DecisionMonitorBuilder().build(ctx).to_dict()
    r = build_narrative_evidence_tension_review(d)
    assert r.phase_closure_outcome_tension == "high"
    assert r.local_global_progress_tension == "high"


def test_r1_no_false_resume_injection():
    ctx = _ctx("R1_container_real_ctx.json")
    d = DecisionMonitorBuilder().build(ctx).to_dict()
    inp = d.get("inputs")
    if hasattr(inp, "to_dict"):
        inp = inp.to_dict()
    assert inp.get("recovery_declared_but_resume_chain_fragile_expected") is False
    assert inp.get("scenario_task_resume_target") is None
