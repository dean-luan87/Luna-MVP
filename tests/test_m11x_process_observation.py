# -*- coding: utf-8 -*-
"""M1.1.x-A 过程观察增强单测（R60/R61/R64）。"""

from __future__ import annotations

import json
from pathlib import Path

from decision_monitor.builder import DecisionMonitorBuilder


CTX_DIR = Path(__file__).resolve().parents[1] / "tests" / "real_scenarios" / "ctx"


def _build_ctx(name: str) -> dict:
    return json.loads((CTX_DIR / name).read_text(encoding="utf-8"))


def _timeline_types(frame: dict) -> list[str]:
    tv = frame.get("reasoning_timeline_view") or {}
    events = tv.get("events") or []
    return [str(e.get("event_type")) for e in events if isinstance(e, dict) and e.get("event_type")]


def test_r60_resume_chain_observation_visible():
    frame = DecisionMonitorBuilder().build(_build_ctx("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")).to_dict()
    rsr = frame.get("run_summary_reference") or {}
    assert rsr.get("process_observation_summary")
    assert rsr.get("resume_chain_stage_summary")
    assert rsr.get("resume_chain_fragility_summary")
    assert rsr.get("resume_chain_progress_reached_main") is False
    types = _timeline_types(frame)
    assert "resume_chain_declared" in types
    assert ("resume_chain_fragility_detected" in types) or ("resume_chain_not_progressing_main" in types)


def test_r61_memory_bias_observation_visible():
    frame = DecisionMonitorBuilder().build(_build_ctx("R61_memory_bias_accumulated_under_familiar_context_real_ctx.json")).to_dict()
    rsr = frame.get("run_summary_reference") or {}
    assert rsr.get("memory_bias_accumulation_summary")
    assert rsr.get("memory_bias_weight_shift_summary") is not None
    assert rsr.get("memory_bias_conflict_stage_summary")
    types = _timeline_types(frame)
    assert "memory_bias_accumulation_detected" in types


def test_r64_phase_closure_misalignment_observation_visible():
    frame = DecisionMonitorBuilder().build(_build_ctx("R64_phase_correct_but_closure_semantics_misaligned_real_ctx.json")).to_dict()
    rsr = frame.get("run_summary_reference") or {}
    assert rsr.get("phase_closure_alignment_summary")
    assert rsr.get("closure_semantics_misalignment_summary")
    types = _timeline_types(frame)
    assert "phase_identified_but_closure_misaligned" in types or "closure_semantics_repair_candidate" in types


def test_summary_entry_process_observation_consistent():
    frame = DecisionMonitorBuilder().build(_build_ctx("R61_memory_bias_accumulated_under_familiar_context_real_ctx.json")).to_dict()
    rsr = frame.get("run_summary_reference") or {}
    pse = frame.get("post_processing_summary_entry") or {}
    assert pse.get("process_observation_summary")
    assert "process_observation_hint" in str(pse.get("backfill_reason_summary") or "")
    assert str(pse.get("process_observation_summary")).startswith(str(rsr.get("process_observation_summary")).split(";")[0])
