# -*- coding: utf-8 -*-
"""
只读：从真实 ctx 构建 frame，抽取 resume / closure / main progress 相关字段，
与 narrative_evidence_tension_review 的 pc/lg 对照。不改行为。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.narrative_evidence_tension_review import (  # noqa: E402
    build_narrative_evidence_tension_review,
)


def _d(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        d = obj.to_dict()
        return d if isinstance(d, dict) else {}
    return {}


def _ctx_resume_flags(ctx: Dict[str, Any]) -> Dict[str, Any]:
    keys = (
        "task_resume_target",
        "recovery_declared_but_resume_chain_fragile_expected",
        "phase_correct_but_closure_semantics_misaligned_expected",
        "memory_bias_accumulated_under_familiar_context_expected",
    )
    return {k: ctx.get(k) for k in keys if k in ctx}


def _inputs_flags(inputs: Dict[str, Any]) -> Dict[str, Any]:
    if not inputs:
        return {}
    keys = (
        "recovery_declared_but_resume_chain_fragile_expected",
        "phase_correct_but_closure_semantics_misaligned_expected",
        "memory_bias_accumulated_under_familiar_context_expected",
    )
    return {k: inputs.get(k) for k in keys if inputs.get(k) is not None}


def extract_case(ctx_path: Path) -> Dict[str, Any]:
    ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    rsr = _d(frame.get("run_summary_reference"))
    tcs = _d(frame.get("task_chain_state_snapshot"))
    mss = _d(frame.get("mainline_state_snapshot"))
    pse = _d(frame.get("post_processing_summary_entry"))
    mna = _d(frame.get("mainline_narrative_alignment"))
    inputs = _d(frame.get("inputs"))
    net = build_narrative_evidence_tension_review(frame)
    netd = net.to_dict() if hasattr(net, "to_dict") else _d(net)

    proc = rsr.get("process_observation_summary") or ""
    m11x = "m11x_ctx_observed" in proc

    return {
        "ctx_file": ctx_path.name,
        "trace_anchor_id": frame.get("trace_anchor_id"),
        "ctx_resume_related": _ctx_resume_flags(ctx),
        "inputs_expected_flags_present": _inputs_flags(inputs),
        "task_chain_state_snapshot": {
            "task_mode": tcs.get("task_mode"),
            "task_resume_target": tcs.get("task_resume_target"),
            "task_chain_stage": tcs.get("task_chain_stage"),
            "task_position_warning_summary": tcs.get("task_position_warning_summary"),
        },
        "mainline_state_snapshot": {
            "mainline_phase": mss.get("mainline_phase"),
        },
        "run_summary_reference": {
            "resume_chain_fragility_summary": rsr.get("resume_chain_fragility_summary"),
            "resume_chain_progress_reached_main": rsr.get("resume_chain_progress_reached_main"),
            "resume_chain_stage_summary": rsr.get("resume_chain_stage_summary"),
            "task_chain_progress_summary": rsr.get("task_chain_progress_summary"),
            "closure_semantics_misalignment_summary": rsr.get("closure_semantics_misalignment_summary"),
            "process_observation_summary": rsr.get("process_observation_summary"),
            "mainline_narrative_brief": (rsr.get("mainline_narrative_brief") or "")[:320],
            "summary_brief": (rsr.get("summary_brief") or "")[:320],
        },
        "mainline_narrative_alignment": {
            "narrative_brief": (mna.get("narrative_brief") or "")[:320],
        },
        "post_processing_summary_entry": {
            "narrative_readable": (pse.get("narrative_readable") or "")[:220],
            "requires_trace_backfill": pse.get("requires_trace_backfill"),
            "requires_event_backfill": pse.get("requires_event_backfill"),
            "requires_whitebox_backfill": pse.get("requires_whitebox_backfill"),
        },
        "narrative_evidence_tension_review": {
            "phase_closure_outcome_tension": netd.get("phase_closure_outcome_tension"),
            "local_global_progress_tension": netd.get("local_global_progress_tension"),
            "tension_review_brief": netd.get("tension_review_brief"),
        },
        "signals": {
            "process_observation_has_m11x_prefix": m11x,
            "resume_frag_non_none": (rsr.get("resume_chain_fragility_summary") or "none") != "none",
        },
    }


def aggregate_all(ctx_dir: Path) -> Dict[str, Any]:
    n_ctx_flag = 0
    n_tcs_resume = 0
    n_rf_strong = 0
    n_m11x = 0
    n_pc_high = 0
    n_lg_high = 0
    n_pc_lg_both_high = 0
    cases_ctx_not_tcs: List[str] = []

    for p in sorted(ctx_dir.glob("R*_real_ctx.json")):
        ctx = json.loads(p.read_text(encoding="utf-8"))
        frame = DecisionMonitorBuilder().build(ctx).to_dict()
        rsr = _d(frame.get("run_summary_reference"))
        if not rsr.get("summary_reference_applied"):
            continue
        tcs = _d(frame.get("task_chain_state_snapshot"))
        net = build_narrative_evidence_tension_review(frame)
        cid = str(frame.get("trace_anchor_id") or p.stem)

        if ctx.get("recovery_declared_but_resume_chain_fragile_expected") or ctx.get("task_resume_target"):
            n_ctx_flag += 1
        if tcs.get("task_resume_target"):
            n_tcs_resume += 1
        rf = rsr.get("resume_chain_fragility_summary") or ""
        if "resume_declared_but_main_not_progressed" in rf:
            n_rf_strong += 1
        proc = rsr.get("process_observation_summary") or ""
        if "m11x_ctx_observed" in proc:
            n_m11x += 1
        if net.phase_closure_outcome_tension == "high":
            n_pc_high += 1
        if net.local_global_progress_tension == "high":
            n_lg_high += 1
        if net.phase_closure_outcome_tension == "high" and net.local_global_progress_tension == "high":
            n_pc_lg_both_high += 1

        if ctx.get("recovery_declared_but_resume_chain_fragile_expected") and not tcs.get("task_resume_target"):
            cases_ctx_not_tcs.append(cid)

    return {
        "total_real_ctx_cases": len(list(ctx_dir.glob("R*_real_ctx.json"))),
        "cases_with_ctx_resume_or_fragility_flag": n_ctx_flag,
        "cases_with_task_chain_task_resume_target_set": n_tcs_resume,
        "cases_with_resume_chain_fragility_strong_string": n_rf_strong,
        "cases_with_process_observation_m11x_prefix": n_m11x,
        "cases_pc_high": n_pc_high,
        "cases_lg_high": n_lg_high,
        "cases_pc_high_and_lg_high": n_pc_lg_both_high,
        "case_ids_ctx_frag_flag_but_tcs_resume_target_none_sample": cases_ctx_not_tcs[:20],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--ctx-dir",
        default=str(ROOT / "tests" / "real_scenarios" / "ctx"),
    )
    ap.add_argument(
        "--focus",
        default="R82_phase_closure_progress_pair_near_critical_candidate_real_ctx.json,"
        "R60_recovery_declared_but_resume_chain_fragile_real_ctx.json,"
        "R53_main_task_resumed_but_not_progressed_real_ctx.json,"
        "R54_inserted_task_exit_ambiguous_real_ctx.json,"
        "R1_container_real_ctx.json,"
        "R57_summary_looks_ok_but_requires_backfill_real_ctx.json,"
        "R4_feedback_effective_real_ctx.json",
        help="comma-separated ctx filenames for detailed rows",
    )
    ap.add_argument("--out", default=str(ROOT / "logs" / "resume_closure_signal_alignment_m14.json"))
    args = ap.parse_args()
    ctx_dir = Path(args.ctx_dir)
    focus = [x.strip() for x in args.focus.split(",") if x.strip()]
    detail: List[Dict[str, Any]] = []
    for name in focus:
        p = ctx_dir / name
        if not p.is_file():
            print("missing", p, file=sys.stderr)
            return 1
        detail.append(extract_case(p))

    report = {
        "aggregate": aggregate_all(ctx_dir),
        "focus_cases": detail,
        "note": "只读聚合；resume_chain_fragility_summary 与 process_observation 来自 run_summary_builder._build_process_observation",
    }
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("wrote:", outp, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
