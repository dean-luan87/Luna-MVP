# -*- coding: utf-8 -*-
"""
只读：从 real_scenario_pack_m15.json 提取 critical_candidate 与对照样本的
tension + run_summary / TCS 摘要字段，输出结构化复盘 JSON。

不改 benchmark、不改规则、不重跑 pack（可选：重建 frame 以拉 run_summary_reference）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from tools.real_scenario_pack import (  # noqa: E402
    _load_ctx_json,
    _load_snapshot_json,
    default_real_cases,
)


def _s(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


def _case_ref_map() -> Dict[str, Tuple[Any, Dict[str, Any]]]:
    out: Dict[str, Tuple[Any, Dict[str, Any]]] = {}
    for case, ref in default_real_cases():
        out[case.case_id] = (case, ref)
    return out


def _build_frame(case_id: str) -> Optional[Dict[str, Any]]:
    m = _case_ref_map()
    if case_id not in m:
        return None
    case, ref = m[case_id]
    mode = ref.get("input_mode")
    p = Path(ref.get("input_ref") or "")
    if mode == "snapshot_json":
        return _load_snapshot_json(p)
    if mode == "ctx_json":
        ctx = _load_ctx_json(p)
        if not ctx:
            return None
        return DecisionMonitorBuilder().build(ctx).to_dict()
    return None


def _extract_run_summary_slice(frame: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(frame, dict):
        return {"error": "no_frame"}
    rsr = frame.get("run_summary_reference")
    if not isinstance(rsr, dict):
        rsr = {}
    tcs = frame.get("task_chain_state_snapshot")
    if not isinstance(tcs, dict):
        tcs = {}
    inputs = frame.get("inputs")
    if not isinstance(inputs, dict):
        inputs = {}
    tcp = _s(rsr.get("task_chain_progress_summary"))
    proc = _s(rsr.get("process_observation_summary"))
    return {
        "resume_chain_fragility_summary": _s(rsr.get("resume_chain_fragility_summary")) or "none",
        "resume_chain_stage_summary": _s(rsr.get("resume_chain_stage_summary"))[:220],
        "task_chain_progress_summary": tcp[:500],
        "mainline_state_summary": _s(rsr.get("mainline_state_summary"))[:400],
        "process_observation_summary": proc[:500],
        "closure_semantics_misalignment_summary": _s(rsr.get("closure_semantics_misalignment_summary")) or "none",
        "phase_closure_alignment_summary": _s(rsr.get("phase_closure_alignment_summary"))[:220],
        "mainline_narrative_brief": _s(rsr.get("mainline_narrative_brief"))[:300],
        "post_processing_narrative_readable": _s(
            (frame.get("post_processing_summary_entry") or {}).get("narrative_readable")
        )
        if isinstance(frame.get("post_processing_summary_entry"), dict)
        else "",
        "task_chain_resume_main_align": _s(tcs.get("resume_main_progress_alignment_summary"))[:400],
        "inputs_scenario_task_resume_target": _s(inputs.get("scenario_task_resume_target")),
        "inputs_recovery_declared_fragile_expected": inputs.get("recovery_declared_but_resume_chain_fragile_expected"),
        "inputs_main_task_resumed_not_progressed_expected": inputs.get("main_task_resumed_but_not_progressed_expected"),
    }


def _flags_from_strings(
    net: Dict[str, Any], rslice: Dict[str, Any]
) -> Dict[str, Any]:
    reasons = net.get("tension_reason_summaries") or {}
    if not isinstance(reasons, dict):
        reasons = {}
    lg_r = _s(reasons.get("local_global_progress"))
    pc_r = _s(reasons.get("phase_closure_outcome"))
    tcp = _s(rslice.get("task_chain_progress_summary"))
    proc = _s(rslice.get("process_observation_summary"))
    rf = _s(rslice.get("resume_chain_fragility_summary"))

    def has(pat: str, text: str) -> bool:
        return bool(re.search(pat, text, re.I))

    return {
        "tension_pc": _s(net.get("phase_closure_outcome_tension")),
        "tension_lg": _s(net.get("local_global_progress_tension")),
        "lg_reason": lg_r[:220],
        "pc_reason": pc_r[:220],
        "lg_reason_resume_fragility_family": has(
            r"resume_fragility|declared_main_not_progressed|main_not_progress", lg_r
        ),
        "lg_reason_global_stall_family": has(
            r"global|main_not_reached|not_terminal|stagnant|stalled", lg_r
        ),
        "pc_reason_closure_mismatch_family": has(
            r"closure|misalignment|phase_repair", pc_r
        ),
        "rsr_resume_fragility_not_none": rf not in ("", "none"),
        "rsr_resume_fragility_is_declared_main_not_progressed": rf
        == "resume_declared_but_main_not_progressed",
        "tcp_has_resume_main_align_token": has(r"resume_main_align=", tcp),
        "tcp_has_global_main_not_terminal": has(
            r"global_main_progress_not_terminal", tcp
        ),
        "tcp_has_local_only_risk": has(r"local_only_risk", tcp),
        "proc_has_m11x": has(r"m11x", proc),
        "proc_has_resume_frag": has(r"resume_frag", proc),
    }


def _result_by_id(pack: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in pack.get("results") or []:
        if isinstance(row, dict) and row.get("case_id"):
            out[str(row["case_id"])] = row
    return out


def analyze(
    pack_path: Path,
    extra_case_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    summary = pack.get("summary") or {}
    sev = summary.get("severity_audit") or {}
    critical_ids = list(sev.get("case_ids_critical_candidate") or [])
    results_idx = _result_by_id(pack)

    default_extras = [
        "R85_phase_closure_progress_pair_reappeared_real",
        "R87_complex_but_healthy_resume_and_global_progress_real",
        "R82_phase_closure_progress_pair_near_critical_candidate_real",
        "R10_partial_memory_vs_novel_real",
        "R3_general_search_real",
        "R1_container_real",
    ]
    control_ids = list(dict.fromkeys((extra_case_ids or []) + default_extras))

    all_ids = list(dict.fromkeys(critical_ids + control_ids))

    cases_detail: List[Dict[str, Any]] = []
    for cid in all_ids:
        row = results_idx.get(cid, {})
        sp = row.get("severity_profile") or {}
        overall = sp.get("overall_severity_profile")
        net = row.get("narrative_evidence_tension_review")
        if not isinstance(net, dict):
            net = {}

        frame = _build_frame(cid)
        rslice = _extract_run_summary_slice(frame)
        flags = _flags_from_strings(net, rslice)

        cases_detail.append(
            {
                "case_id": cid,
                "cohort": "critical_candidate"
                if cid in critical_ids
                else "control",
                "overall_severity_profile": overall,
                "tension_review_brief": net.get("tension_review_brief"),
                "flags": flags,
                "run_summary_slice": rslice,
            }
        )

    crit_flags = [c["flags"] for c in cases_detail if c["cohort"] == "critical_candidate"]

    def freq(key: str) -> Tuple[int, int]:
        ok = sum(1 for f in crit_flags if f.get(key) is True)
        return ok, len(crit_flags)

    aggregate = {
        "critical_sample_count": len(crit_flags),
        "freq_pc_raw_high": sum(
            1 for f in crit_flags if f.get("tension_pc") == "high"
        ),
        "freq_lg_raw_high": sum(
            1 for f in crit_flags if f.get("tension_lg") == "high"
        ),
        "freq_lg_reason_resume_fragility_family": freq("lg_reason_resume_fragility_family"),
        "freq_lg_reason_global_stall_family": freq("lg_reason_global_stall_family"),
        "freq_pc_reason_closure_mismatch_family": freq("pc_reason_closure_mismatch_family"),
        "freq_rsr_resume_fragility_not_none": freq("rsr_resume_fragility_not_none"),
        "freq_rsr_resume_declared_main_not_progressed_exact": freq(
            "rsr_resume_fragility_is_declared_main_not_progressed"
        ),
        "freq_tcp_resume_main_align_token": freq("tcp_has_resume_main_align_token"),
        "freq_tcp_global_main_not_terminal": freq("tcp_has_global_main_not_terminal"),
        "freq_tcp_local_only_risk": freq("tcp_has_local_only_risk"),
        "freq_proc_m11x": freq("proc_has_m11x"),
        "freq_proc_resume_frag": freq("proc_has_resume_frag"),
    }

    return {
        "source_pack": str(pack_path),
        "critical_candidate_case_ids": critical_ids,
        "control_case_ids_used": [c for c in control_ids if c not in critical_ids],
        "aggregate_across_critical_only": aggregate,
        "cases": cases_detail,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--pack",
        type=str,
        default=str(ROOT / "logs" / "real_scenario_pack_m15.json"),
    )
    ap.add_argument(
        "--out",
        type=str,
        default=str(ROOT / "logs" / "critical_candidate_pattern_m15.json"),
    )
    args = ap.parse_args()
    pack_path = Path(args.pack)
    out_path = Path(args.out)
    data = analyze(pack_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
