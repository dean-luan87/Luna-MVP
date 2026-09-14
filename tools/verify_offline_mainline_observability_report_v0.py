#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-005
Verify unified observability report v0 integrity.

Hard boundaries:
- Read-only: does not rerun models or mainline pipeline.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Tuple


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _exists(p: str) -> bool:
    try:
        return os.path.exists(p)
    except Exception:
        return False


def _req(cond: bool, code: str, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"check": code, "pass": bool(cond), **details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="logs/offline_mainline_observability_ef005_<timestamp>")
    args = ap.parse_args()

    out_root = os.path.abspath(args.output_root)
    report_p = os.path.join(out_root, "observability_report.json")
    matrix_p = os.path.join(out_root, "sample_chain_matrix.json")
    index_p = os.path.join(out_root, "stage_artifact_index.json")
    cmp_p = os.path.join(out_root, "normal_vs_fallback_comparison.json")
    safety_p = os.path.join(out_root, "safety_boundary_summary.json")
    evidence_p = os.path.join(out_root, "evidence_boundary_summary.json")
    md_p = os.path.join(out_root, "observability_report.md")

    results: List[Dict[str, Any]] = []

    # Basic outputs exist
    results.append(_req(_exists(report_p), "C_main_report_json_exists", {"path": report_p}))
    results.append(_req(_exists(md_p), "C_main_report_md_exists", {"path": md_p}))
    results.append(_req(_exists(matrix_p), "D_sample_chain_matrix_exists", {"path": matrix_p}))
    results.append(_req(_exists(index_p), "E_stage_artifact_index_exists", {"path": index_p}))
    results.append(_req(_exists(cmp_p), "I_normal_vs_fallback_comparison_exists", {"path": cmp_p}))
    results.append(_req(_exists(safety_p), "J_safety_boundary_summary_exists", {"path": safety_p}))
    results.append(_req(_exists(evidence_p), "J_evidence_boundary_summary_exists", {"path": evidence_p}))

    report = _read_json(report_p) if _exists(report_p) else {}
    stage_index = _read_json(index_p) if _exists(index_p) else {}
    matrix = _read_json(matrix_p) if _exists(matrix_p) else {}

    normal_root = str(report.get("normal_root") or "")
    fallback_root = str(report.get("fallback_root") or "")

    # A/B roots readable
    results.append(_req(bool(normal_root and _exists(normal_root)), "A_normal_root_readable", {"normal_root": normal_root}))
    results.append(_req(bool(fallback_root and _exists(fallback_root)), "B_fallback_root_readable", {"fallback_root": fallback_root}))

    # mainline_summary and per_sample existence (from stage_artifact_index + report roots)
    n_summary = os.path.join(normal_root, "mainline_summary.json") if normal_root else ""
    f_summary = os.path.join(fallback_root, "mainline_summary.json") if fallback_root else ""
    n_per = os.path.join(normal_root, "per_sample_mainline_results.json") if normal_root else ""
    f_per = os.path.join(fallback_root, "per_sample_mainline_results.json") if fallback_root else ""
    results.append(_req(bool(n_summary and _exists(n_summary)), "C_normal_mainline_summary_readable", {"path": n_summary}))
    results.append(_req(bool(f_summary and _exists(f_summary)), "C_fallback_mainline_summary_readable", {"path": f_summary}))
    results.append(_req(bool(n_per and _exists(n_per)), "D_normal_per_sample_readable", {"path": n_per}))
    results.append(_req(bool(f_per and _exists(f_per)), "D_fallback_per_sample_readable", {"path": f_per}))

    # trace/replay/whitebox index readable
    n_trace = os.path.join(normal_root, "mainline_trace.jsonl") if normal_root else ""
    f_trace = os.path.join(fallback_root, "mainline_trace.jsonl") if fallback_root else ""
    n_replay = os.path.join(normal_root, "mainline_replay_index.json") if normal_root else ""
    f_replay = os.path.join(fallback_root, "mainline_replay_index.json") if fallback_root else ""
    n_white = os.path.join(normal_root, "mainline_whitebox_index.json") if normal_root else ""
    f_white = os.path.join(fallback_root, "mainline_whitebox_index.json") if fallback_root else ""
    results.append(_req(bool(n_trace and _exists(n_trace)), "E_normal_trace_readable", {"path": n_trace}))
    results.append(_req(bool(f_trace and _exists(f_trace)), "E_fallback_trace_readable", {"path": f_trace}))
    results.append(_req(bool(n_replay and _exists(n_replay)), "F_normal_replay_index_readable", {"path": n_replay}))
    results.append(_req(bool(f_replay and _exists(f_replay)), "F_fallback_replay_index_readable", {"path": f_replay}))
    results.append(_req(bool(n_white and _exists(n_white)), "G_normal_whitebox_index_readable", {"path": n_white}))
    results.append(_req(bool(f_white and _exists(f_white)), "G_fallback_whitebox_index_readable", {"path": f_white}))

    # H stage outputs refs exist: scan sample_chain_matrix stage_refs
    broken: List[Dict[str, Any]] = []
    samples = matrix.get("samples") if isinstance(matrix, dict) else None
    if not isinstance(samples, list):
        samples = []
    for row in samples:
        if not isinstance(row, dict):
            continue
        sid = row.get("sample_id")
        stage_refs = row.get("stage_refs") or {}
        for mode, root in [("normal", normal_root), ("fallback", fallback_root)]:
            refs = (stage_refs.get(mode) or {}) if isinstance(stage_refs, dict) else {}
            if not isinstance(refs, dict):
                continue
            for stage, rel in refs.items():
                if not isinstance(rel, str) or not rel:
                    broken.append({"sample_id": sid, "mode": mode, "stage": stage, "reason": "missing_ref"})
                    continue
                abs_p = os.path.join(root, rel) if root else ""
                if not abs_p or not _exists(abs_p):
                    broken.append({"sample_id": sid, "mode": mode, "stage": stage, "path": abs_p})
    results.append(_req(len(broken) == 0, "H_stage_output_refs_unbroken", {"broken_count": len(broken)}))

    # I comparison has required keys
    cmp_obj = _read_json(cmp_p) if _exists(cmp_p) else {}
    req_cmp = [
        "normal_source_distribution",
        "fallback_source_distribution",
        "normal_detection_count_total",
        "fallback_detection_count_total",
        "normal_chain_complete_rate",
        "fallback_chain_complete_rate",
        "normal_output_candidate_rate",
        "fallback_output_candidate_rate",
        "normal_safety_leakage_total",
        "fallback_safety_leakage_total",
        "normal_boundary_ok_rate",
        "fallback_boundary_ok_rate",
    ]
    missing_cmp = [k for k in req_cmp if k not in cmp_obj]
    results.append(_req(len(missing_cmp) == 0, "I_comparison_required_keys_present", {"missing": missing_cmp}))

    # J safety/evidence aggregation presence
    safety = _read_json(safety_p) if _exists(safety_p) else {}
    evidence = _read_json(evidence_p) if _exists(evidence_p) else {}
    req_safety = [
        "execute_leakage_count_total",
        "default_on_leakage_count_total",
        "release_retry_reopen_leakage_count_total",
        "side_effects_expansion_count_total",
        "forced_navigation_action_count_total",
        "forbidden_output_semantic_count_total",
        "allows_execute_now_false_rate",
        "real_tts_invoked_false_rate",
    ]
    req_evidence = [
        "evidence_type_preserved_rate",
        "controlled_live_stream_false_rate",
        "phone_local_capture_true_rate",
        "pending_real_sidewalk_run_true_rate",
        "evidence_type_mutation_count",
        "pending_closed_count",
    ]
    missing_safety = [k for k in req_safety if k not in safety]
    missing_evidence = [k for k in req_evidence if k not in evidence]
    results.append(_req(len(missing_safety) == 0, "J_safety_required_keys_present", {"missing": missing_safety}))
    results.append(_req(len(missing_evidence) == 0, "J_evidence_required_keys_present", {"missing": missing_evidence}))

    all_pass = all(bool(r.get("pass")) for r in results)
    verification = {
        "phase": "Phase-EngineeringFlow-005",
        "tool": "verify_offline_mainline_observability_report_v0.py",
        "output_root": out_root,
        "normal_root": normal_root,
        "fallback_root": fallback_root,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for r in results if r.get("pass"))),
        "all_pass": all_pass,
        "broken_stage_refs": broken[:200],
        "results": results,
    }

    out_p = os.path.join(out_root, "verification_result.json")
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)

    print(json.dumps({"verification_result": out_p, "all_pass": all_pass}, ensure_ascii=False, indent=2))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())

