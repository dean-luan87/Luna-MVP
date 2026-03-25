# -*- coding: utf-8 -*-
"""Narrative / Evidence Tension Review M0 单测。"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from decision_monitor.builder import DecisionMonitorBuilder
from decision_monitor.narrative_evidence_tension_review import (
    build_narrative_evidence_tension_review,
)
from tools.reasoning_console_aggregator import aggregate_frame

ROOT = Path(__file__).resolve().parents[1]


def _ctx(name: str) -> dict:
    p = ROOT / "tests" / "real_scenarios" / "ctx" / name
    return json.loads(p.read_text(encoding="utf-8"))


def test_build_applied_and_five_keys():
    r = build_narrative_evidence_tension_review({})
    assert r.narrative_evidence_tension_review_applied is False

    frame = {
        "trace_anchor_id": "x",
        "run_summary_reference": {"summary_reference_applied": False},
    }
    r2 = build_narrative_evidence_tension_review(frame)
    assert r2.narrative_trace_support_tension == "unknown"


def test_three_dimensions_triggered_by_synthetic_frame():
    """至少三类张力可被启发式抬高：叙事↔事件、phase↔closure、backfill 契约。"""
    frame: dict = {
        "trace_anchor_id": "synthetic_tension",
        "object_search_interaction": {"search_terminal_status": "none"},
        "mainline_state_snapshot": {"mainline_phase": "closure"},
        "run_summary_reference": {
            "summary_reference_applied": True,
            "summary_id": "synthetic_tension",
            "structured_event_layer_snapshot": {"event_count": 0, "distinct_event_types": []},
            "mainline_narrative_brief": "主线叙事铺陈较长。" * 18,
            "closure_semantics_misalignment_summary": "phase_repair_visible_but_closure_still_none",
            "memory_bias_accumulation_summary": "none",
            "resume_chain_fragility_summary": "none",
            "resume_chain_progress_reached_main": True,
            "task_chain_progress_summary": "task_chain: idle",
            "process_observation_summary": "resume_frag=none",
        },
        "mainline_narrative_alignment": {
            "mainline_narrative_alignment_applied": True,
            "narrative_brief": "统一骨架下的可读叙事补充。" * 10,
        },
        "post_processing_summary_entry": {
            "post_processing_summary_entry_applied": True,
            "requires_trace_backfill": True,
            "requires_event_backfill": True,
            "requires_whitebox_backfill": True,
            "narrative_readable": "读起来已经较完整，但契约仍要求多层回溯。" * 8,
        },
    }
    out = build_narrative_evidence_tension_review(frame)
    assert out.narrative_evidence_tension_review_applied is True
    assert out.narrative_trace_support_tension in ("high", "medium")
    assert out.phase_closure_outcome_tension == "high"
    assert out.summary_backfill_tension == "high"
    assert "叙事—证据张力审计" in (out.tension_review_readable or "")
    assert out.suggested_backfill_direction_summary


def test_frame_dict_not_mutated():
    frame: dict = {
        "run_summary_reference": {
            "summary_reference_applied": True,
            "structured_event_layer_snapshot": {"event_count": 1},
            "mainline_narrative_brief": "short",
        }
    }
    snap = copy.deepcopy(frame)
    build_narrative_evidence_tension_review(frame)
    assert frame == snap


def test_review_in_builder_frame():
    b = DecisionMonitorBuilder().build(_ctx("R68_narrative_smooth_but_trace_support_weak_real_ctx.json"))
    d = b.to_dict()
    netr = d.get("narrative_evidence_tension_review")
    assert netr is not None
    if hasattr(netr, "to_dict"):
        nd = netr.to_dict()
    else:
        nd = netr
    assert nd.get("narrative_evidence_tension_review_applied") is True
    assert nd.get("tension_review_readable")


def test_aggregate_exposes_review():
    b = DecisionMonitorBuilder().build(_ctx("R68_narrative_smooth_but_trace_support_weak_real_ctx.json"))
    snap = aggregate_frame(b.to_dict())
    assert snap.narrative_evidence_tension_review is not None
    assert snap.tension_review_readable


def test_run_summary_unchanged_after_review():
    b = DecisionMonitorBuilder().build(_ctx("R57_summary_looks_ok_but_requires_backfill_real_ctx.json"))
    d = b.to_dict()
    rsr_before = copy.deepcopy(d.get("run_summary_reference"))
    build_narrative_evidence_tension_review(d)
    assert d.get("run_summary_reference") == rsr_before
