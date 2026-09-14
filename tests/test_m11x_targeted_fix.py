# -*- coding: utf-8 -*-
"""M1.1.x-B 定点修复单测（R60/R61/R64）。"""

from __future__ import annotations

import json
from pathlib import Path

from decision_monitor.builder import DecisionMonitorBuilder


CTX_DIR = Path(__file__).resolve().parents[1] / "tests" / "real_scenarios" / "ctx"


def _build_case(name: str) -> dict:
    ctx = json.loads((CTX_DIR / name).read_text(encoding="utf-8"))
    return DecisionMonitorBuilder().build(ctx).to_dict()


def _assert_forced_repair(frame: dict) -> None:
    rp = frame.get("recheck_planner") or {}
    assert rp.get("recheck_action") == "ask_user_for_clarification"
    assert rp.get("recheck_applied") is True
    assert rp.get("recheck_blocked") is False
    assert "m11x_targeted_fix_forced_user_clarification" in str(rp.get("recheck_reason") or "")


def _assert_consistent_summary_entry(frame: dict) -> None:
    rsr = frame.get("run_summary_reference") or {}
    pse = frame.get("post_processing_summary_entry") or {}
    mss = frame.get("mainline_state_snapshot") or {}
    assert mss.get("mainline_phase") == "recheck_or_repair"
    assert "recheck_or_repair" in str(rsr.get("summary_brief") or "")
    assert "ask_user_for_clarification" in str(rsr.get("mainline_state_summary") or "")
    assert pse.get("process_observation_summary")
    assert "process_observation_hint" in str(pse.get("backfill_reason_summary") or "")


def test_r60_resume_chain_fragile_fixed():
    frame = _build_case("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")
    _assert_forced_repair(frame)
    _assert_consistent_summary_entry(frame)


def test_r61_memory_bias_accumulation_fixed():
    frame = _build_case("R61_memory_bias_accumulated_under_familiar_context_real_ctx.json")
    _assert_forced_repair(frame)
    _assert_consistent_summary_entry(frame)


def test_r64_phase_closure_misalignment_fixed():
    frame = _build_case("R64_phase_correct_but_closure_semantics_misaligned_real_ctx.json")
    _assert_forced_repair(frame)
    _assert_consistent_summary_entry(frame)
