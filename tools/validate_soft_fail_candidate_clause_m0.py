# -*- coding: utf-8 -*-
"""
Soft-Fail Candidate Validation Pack M0：只读验证 SF-1′ 条款边界
（不接入 benchmark / 不改 hard-fail / 不改 triage）。

依据：docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from tools.real_scenario_pack import (  # noqa: E402
    _load_ctx_json,
    default_real_cases,
)

RSR_FRAG = "resume_declared_but_main_not_progressed"
TCP_GLOBAL = "global_main_progress_not_terminal_complete"

# 正样本（m15 critical_candidate）
POSITIVE = [
    "R53_main_task_resumed_but_not_progressed_real",
    "R59_multi_inserted_recovery_but_main_not_progressed_real",
    "R60_recovery_declared_but_resume_chain_fragile_real",
    "R83_resume_declared_main_still_not_progressed_real",
    "R84_recovery_chain_repeated_and_global_goal_not_advanced_real",
    "R86_resume_target_present_but_outcome_still_overclaimed_real",
    "R88_inserted_recovery_resolved_locally_but_main_goal_stagnant_real",
]
NEAR = [
    "R85_phase_closure_progress_pair_reappeared_real",
    "R82_phase_closure_progress_pair_near_critical_candidate_real",
    "R10_partial_memory_vs_novel_real",
]
HEALTHY = [
    "R87_complex_but_healthy_resume_and_global_progress_real",
    "R4_feedback_effective_real",
    "R1_container_real",
]
LOW_SIGNAL = [
    "R3_general_search_real",
]

EXTRA_CTX: List[Tuple[str, Path, str]] = [
    (
        "SFV01_just_below_threshold_pc_high_lg_medium_real",
        ROOT / "tests" / "real_scenarios" / "ctx" / "SFV01_just_below_threshold_pc_high_lg_medium_real_ctx.json",
        "mild_variant",
    ),
    (
        "SFV02_healthy_terminal_found_like_real",
        ROOT / "tests" / "real_scenarios" / "ctx" / "SFV02_healthy_terminal_found_like_real_ctx.json",
        "mild_variant",
    ),
]


def _case_ref_map() -> Dict[str, Tuple[Any, Dict[str, Any]]]:
    out: Dict[str, Tuple[Any, Dict[str, Any]]] = {}
    for case, ref in default_real_cases():
        out[case.case_id] = (case, ref)
    return out


def _net_dict(frame: Dict[str, Any]) -> Dict[str, Any]:
    net = frame.get("narrative_evidence_tension_review")
    if net is not None and hasattr(net, "to_dict"):
        net = net.to_dict()
    return net if isinstance(net, dict) else {}


def _rsr_dict(frame: Dict[str, Any]) -> Dict[str, Any]:
    r = frame.get("run_summary_reference")
    if r is not None and hasattr(r, "to_dict"):
        r = r.to_dict()
    return r if isinstance(r, dict) else {}


def _osi_dict(frame: Dict[str, Any]) -> Dict[str, Any]:
    o = frame.get("object_search_interaction")
    if o is not None and hasattr(o, "to_dict"):
        o = o.to_dict()
    return o if isinstance(o, dict) else {}


def _build_frame_from_pack(case_id: str) -> Optional[Dict[str, Any]]:
    m = _case_ref_map()
    if case_id not in m:
        return None
    case, ref = m[case_id]
    mode = ref.get("input_mode")
    p = Path(ref.get("input_ref") or "")
    if mode == "snapshot_json":
        from tools.real_scenario_pack import _load_snapshot_json

        return _load_snapshot_json(p)
    if mode == "ctx_json":
        ctx = _load_ctx_json(p)
        if not ctx:
            return None
        return DecisionMonitorBuilder().build(ctx).to_dict()
    return None


def _build_frame_from_ctx_path(path: Path) -> Optional[Dict[str, Any]]:
    ctx = _load_ctx_json(path)
    if not ctx:
        return None
    return DecisionMonitorBuilder().build(ctx).to_dict()


def evaluate_clause(frame: Dict[str, Any]) -> Dict[str, Any]:
    net = _net_dict(frame)
    pc = str(net.get("phase_closure_outcome_tension") or "").strip()
    lg = str(net.get("local_global_progress_tension") or "").strip()
    rsr = _rsr_dict(frame)
    tcp = str(rsr.get("task_chain_progress_summary") or "")
    rfrag = str(rsr.get("resume_chain_fragility_summary") or "").strip()
    osi = _osi_dict(frame)
    terminal = str(osi.get("search_terminal_status") or "").strip()

    sf1 = pc == "high" and lg == "high"
    rsr_ok = rfrag == RSR_FRAG
    tcp_ok = TCP_GLOBAL in tcp
    sf1_prime = sf1 and rsr_ok and tcp_ok

    # 草案 §五：健康对照（terminal 已达成 + tcp 无全局未收口 token → 不应标条款）
    exclude_healthy_terminal = (
        terminal == "found" and TCP_GLOBAL not in tcp and sf1
    )
    exclusions: List[str] = []
    if pc != "high":
        exclusions.append("pc_not_high")
    if lg != "high":
        exclusions.append("lg_not_high")
    if not rsr_ok:
        exclusions.append("rsr_not_resume_declared_main_not_progressed")
    if not tcp_ok:
        exclusions.append("tcp_missing_global_main_progress_not_terminal_complete")
    if exclude_healthy_terminal:
        exclusions.append("draft_exclusion_healthy_terminal_found_without_global_stall_token")

    human_candidate = sf1_prime and not exclude_healthy_terminal

    return {
        "phase_closure_outcome_tension": pc,
        "local_global_progress_tension": lg,
        "resume_chain_fragility_summary": rfrag or "none",
        "task_chain_progress_summary_has_global_token": tcp_ok,
        "sf1_match": sf1,
        "sf1_prime_match": sf1_prime,
        "exclusion_reasons": exclusions,
        "human_candidate_per_draft": human_candidate,
        "search_terminal_status": terminal or "none",
    }


def run_all() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    cohorts: Dict[str, List[str]] = {
        "positive": POSITIVE,
        "near_neighbor": NEAR,
        "healthy_or_low": HEALTHY + LOW_SIGNAL,
    }

    def add_row(case_id: str, cohort: str) -> None:
        frame = _build_frame_from_pack(case_id)
        if frame is None:
            rows.append(
                {
                    "case_id": case_id,
                    "cohort": cohort,
                    "error": "build_failed_or_unsupported_input_mode",
                }
            )
            return
        ev = evaluate_clause(frame)
        rows.append({"case_id": case_id, "cohort": cohort, **ev})

    for cid in POSITIVE:
        add_row(cid, "positive")
    for cid in NEAR:
        add_row(cid, "near_neighbor")
    for cid in HEALTHY:
        add_row(cid, "healthy_or_low")
    for cid in LOW_SIGNAL:
        add_row(cid, "healthy_or_low")

    for case_id, path, cohort in EXTRA_CTX:
        frame = _build_frame_from_ctx_path(path)
        if frame is None:
            rows.append(
                {
                    "case_id": case_id,
                    "cohort": cohort,
                    "error": "ctx_missing_or_build_failed",
                }
            )
            continue
        ev = evaluate_clause(frame)
        rows.append({"case_id": case_id, "cohort": cohort, **ev})

    # 汇总
    pos = [r for r in rows if r.get("cohort") == "positive" and "sf1_prime_match" in r]
    near = [r for r in rows if r.get("cohort") == "near_neighbor"]
    mild = [r for r in rows if r.get("cohort") == "mild_variant"]

    summary = {
        "positive": {
            "count": len(pos),
            "sf1_prime_hits": sum(1 for r in pos if r.get("sf1_prime_match")),
            "human_candidate_hits": sum(1 for r in pos if r.get("human_candidate_per_draft")),
        },
        "near_neighbor": {
            "sf1_prime_hits": sum(1 for r in near if r.get("sf1_prime_match")),
            "human_candidate_hits": sum(1 for r in near if r.get("human_candidate_per_draft")),
        },
        "mild_variant": {
            "sf1_prime_hits": sum(1 for r in mild if r.get("sf1_prime_match")),
            "human_candidate_hits": sum(1 for r in mild if r.get("human_candidate_per_draft")),
        },
    }

    return {
        "clause_ref": "docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md SF-1′",
        "rows": rows,
        "summary": summary,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=str,
        default=str(ROOT / "logs" / "soft_fail_candidate_validation_m0.json"),
    )
    args = ap.parse_args()
    data = run_all()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
