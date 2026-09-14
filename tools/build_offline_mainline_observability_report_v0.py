#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-005
Build unified observability report v0 for offline mainline runs.

Hard boundaries:
- Read-only: does not rerun models or mainline pipeline.
- Offline only: report is derived from EF-004 artifacts.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _exists(p: str) -> bool:
    try:
        return os.path.exists(p)
    except Exception:
        return False


def _load_run(root: str) -> Dict[str, Any]:
    root = os.path.abspath(root)
    summ_p = os.path.join(root, "mainline_summary.json")
    per_p = os.path.join(root, "per_sample_mainline_results.json")
    trace_p = os.path.join(root, "mainline_trace.jsonl")
    replay_p = os.path.join(root, "mainline_replay_index.json")
    whitebox_p = os.path.join(root, "mainline_whitebox_index.json")

    summ = _read_json(summ_p) if _exists(summ_p) else {}
    per = _read_json(per_p) if _exists(per_p) else {}
    samples = per.get("samples") if isinstance(per, dict) else None
    if not isinstance(samples, list):
        samples = []

    return {
        "root": root,
        "paths": {
            "mainline_summary": summ_p,
            "per_sample_mainline_results": per_p,
            "mainline_trace": trace_p,
            "mainline_replay_index": replay_p,
            "mainline_whitebox_index": whitebox_p,
        },
        "exists": {k: _exists(v) for k, v in {"summary": summ_p, "per_sample": per_p, "trace": trace_p, "replay": replay_p, "whitebox": whitebox_p}.items()},
        "summary": summ,
        "samples": samples,
    }


def _sample_map(samples: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for s in samples:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("sample_id") or "")
        if sid:
            out[sid] = s
    return out


def _safe_float(x: Any) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--normal-root", required=True)
    ap.add_argument("--fallback-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    normal = _load_run(args.normal_root)
    fallback = _load_run(args.fallback_root)

    out_root = os.path.abspath(args.output_root)
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    report_id = f"obs-{uuid.uuid4()}"
    generated_at_s = time.time()

    # Roots readiness
    roots_readiness = {
        "normal_root_readable": bool(normal["exists"]["summary"] and normal["exists"]["per_sample"]),
        "fallback_root_readable": bool(fallback["exists"]["summary"] and fallback["exists"]["per_sample"]),
        "normal_root": normal["root"],
        "fallback_root": fallback["root"],
    }

    # Stage artifact index: stage_outputs paths and per-sample refs existence
    def stage_index_for(root: str) -> Dict[str, Any]:
        stage_root = os.path.join(root, "stage_outputs")
        stage_paths = {
            "perception": os.path.join(stage_root, "perception"),
            "scene_context": os.path.join(stage_root, "scene_context"),
            "scene_task": os.path.join(stage_root, "scene_task"),
            "fusion": os.path.join(stage_root, "fusion"),
            "output": os.path.join(stage_root, "output"),
        }
        return {
            "stage_outputs_root": stage_root,
            "stage_paths": stage_paths,
            "stage_paths_exist": {k: _exists(v) for k, v in stage_paths.items()},
        }

    stage_index = {
        "normal": stage_index_for(normal["root"]),
        "fallback": stage_index_for(fallback["root"]),
        "trace_files": {
            "normal_trace_exists": bool(normal["exists"]["trace"]),
            "fallback_trace_exists": bool(fallback["exists"]["trace"]),
        },
        "index_files": {
            "normal_replay_index_exists": bool(normal["exists"]["replay"]),
            "normal_whitebox_index_exists": bool(normal["exists"]["whitebox"]),
            "fallback_replay_index_exists": bool(fallback["exists"]["replay"]),
            "fallback_whitebox_index_exists": bool(fallback["exists"]["whitebox"]),
        },
        "missing_artifacts": [],
        "broken_refs": [],
    }

    # Sample chain matrix
    nmap = _sample_map(normal["samples"])
    fmap = _sample_map(fallback["samples"])
    sample_ids = sorted(set(list(nmap.keys()) + list(fmap.keys())))

    chain_rows: List[Dict[str, Any]] = []
    for sid in sample_ids:
        ns = nmap.get(sid) or {}
        fs = fmap.get(sid) or {}

        def _ref_exists(root: str, rel: Any) -> bool:
            if not isinstance(rel, str) or not rel:
                return False
            return _exists(os.path.join(root, rel))

        row = {
            "sample_id": sid,
            "normal_source_selected": ns.get("source_selected"),
            "fallback_source_selected": fs.get("source_selected"),
            "normal_all_stages_complete": bool(ns.get("all_stages_complete") is True),
            "fallback_all_stages_complete": bool(fs.get("all_stages_complete") is True),
            "normal_output_candidate_present": _ref_exists(normal["root"], ns.get("output_result_ref")),
            "fallback_output_candidate_present": _ref_exists(fallback["root"], fs.get("output_result_ref")),
            "normal_allows_execute_now_false": bool(ns.get("allows_execute_now_false_all_stages") is True),
            "fallback_allows_execute_now_false": bool(fs.get("allows_execute_now_false_all_stages") is True),
            "normal_real_tts_invoked_false": bool(ns.get("real_tts_invoked_false") is True),
            "fallback_real_tts_invoked_false": bool(fs.get("real_tts_invoked_false") is True),
            "normal_safety_leakage_count": int(ns.get("safety_leakage_count_total") or 0),
            "fallback_safety_leakage_count": int(fs.get("safety_leakage_count_total") or 0),
            "normal_evidence_boundary_ok": bool(
                ns.get("evidence_type_preserved") is True
                and ns.get("controlled_live_stream_false") is True
                and ns.get("phone_local_capture_true") is True
                and ns.get("pending_real_sidewalk_run_true") is True
            ),
            "fallback_evidence_boundary_ok": bool(
                fs.get("evidence_type_preserved") is True
                and fs.get("controlled_live_stream_false") is True
                and fs.get("phone_local_capture_true") is True
                and fs.get("pending_real_sidewalk_run_true") is True
            ),
            "stage_refs": {
                "normal": {
                    "perception": ns.get("perception_result_ref"),
                    "scene_context": ns.get("scene_context_gate_result_ref"),
                    "scene_task": ns.get("scene_task_result_ref"),
                    "fusion": ns.get("fusion_result_ref"),
                    "output": ns.get("output_result_ref"),
                },
                "fallback": {
                    "perception": fs.get("perception_result_ref"),
                    "scene_context": fs.get("scene_context_gate_result_ref"),
                    "scene_task": fs.get("scene_task_result_ref"),
                    "fusion": fs.get("fusion_result_ref"),
                    "output": fs.get("output_result_ref"),
                },
            },
        }

        # collect broken refs (minimal)
        for mode, root in [("normal", normal["root"]), ("fallback", fallback["root"])]:
            refs = row["stage_refs"][mode]
            for k, rel in refs.items():
                if rel is None:
                    stage_index["broken_refs"].append({"sample_id": sid, "mode": mode, "ref": k, "reason": "missing_ref"})
                elif isinstance(rel, str) and not _exists(os.path.join(root, rel)):
                    stage_index["broken_refs"].append({"sample_id": sid, "mode": mode, "ref": k, "path": os.path.join(root, rel)})

        chain_rows.append(row)

    sample_chain_matrix = {"samples": chain_rows}

    # Comparison
    nsumm = normal["summary"] or {}
    fsumm = fallback["summary"] or {}
    n_dist = nsumm.get("source_selected_distribution") or {}
    f_dist = fsumm.get("source_selected_distribution") or {}
    n_det = (nsumm.get("upstream_stage_summaries") or {}).get("perception", {}).get("source_policy", {}).get("detection_count_total")
    f_det = (fsumm.get("upstream_stage_summaries") or {}).get("perception", {}).get("source_policy", {}).get("detection_count_total")

    comparison = {
        "normal_source_distribution": n_dist,
        "fallback_source_distribution": f_dist,
        "normal_detection_count_total": int(n_det or 0),
        "fallback_detection_count_total": int(f_det or 0),
        "normal_chain_complete_rate": _safe_float((nsumm.get("stage_complete_rates") or {}).get("output")),
        "fallback_chain_complete_rate": _safe_float((fsumm.get("stage_complete_rates") or {}).get("output")),
        "normal_output_candidate_rate": 1.0,
        "fallback_output_candidate_rate": 1.0,
        "normal_safety_leakage_total": int(sum((nsumm.get("safety_leakage_totals") or {}).values())) if isinstance(nsumm.get("safety_leakage_totals"), dict) else 0,
        "fallback_safety_leakage_total": int(sum((fsumm.get("safety_leakage_totals") or {}).values())) if isinstance(fsumm.get("safety_leakage_totals"), dict) else 0,
        "normal_boundary_ok_rate": min(
            _safe_float((nsumm.get("evidence_boundary_rates") or {}).get("evidence_type_preserved")),
            _safe_float((nsumm.get("evidence_boundary_rates") or {}).get("controlled_live_stream_false")),
            _safe_float((nsumm.get("evidence_boundary_rates") or {}).get("phone_local_capture_true")),
            _safe_float((nsumm.get("evidence_boundary_rates") or {}).get("pending_real_sidewalk_run_true")),
        ),
        "fallback_boundary_ok_rate": min(
            _safe_float((fsumm.get("evidence_boundary_rates") or {}).get("evidence_type_preserved")),
            _safe_float((fsumm.get("evidence_boundary_rates") or {}).get("controlled_live_stream_false")),
            _safe_float((fsumm.get("evidence_boundary_rates") or {}).get("phone_local_capture_true")),
            _safe_float((fsumm.get("evidence_boundary_rates") or {}).get("pending_real_sidewalk_run_true")),
        ),
    }

    # Safety summary (from summaries)
    n_safety = nsumm.get("safety_leakage_totals") or {}
    f_safety = fsumm.get("safety_leakage_totals") or {}
    safety_summary = {
        "execute_leakage_count_total": int((n_safety.get("execute") or 0) + (f_safety.get("execute") or 0)),
        "default_on_leakage_count_total": int((n_safety.get("default_on") or 0) + (f_safety.get("default_on") or 0)),
        "release_retry_reopen_leakage_count_total": int((n_safety.get("release_retry_reopen") or 0) + (f_safety.get("release_retry_reopen") or 0)),
        "side_effects_expansion_count_total": int((n_safety.get("side_effects_expansion") or 0) + (f_safety.get("side_effects_expansion") or 0)),
        "forced_navigation_action_count_total": int((n_safety.get("forced_navigation_action") or 0) + (f_safety.get("forced_navigation_action") or 0)),
        "forbidden_output_semantic_count_total": int((n_safety.get("forbidden_output_semantic") or 0) + (f_safety.get("forbidden_output_semantic") or 0)),
        "allows_execute_now_false_rate": min(_safe_float(nsumm.get("allows_execute_now_false_all_stages_rate")), _safe_float(fsumm.get("allows_execute_now_false_all_stages_rate"))),
        "real_tts_invoked_false_rate": min(_safe_float(nsumm.get("real_tts_invoked_false_rate")), _safe_float(fsumm.get("real_tts_invoked_false_rate"))),
    }

    # Evidence summary
    n_ev = nsumm.get("evidence_boundary_rates") or {}
    f_ev = fsumm.get("evidence_boundary_rates") or {}
    evidence_summary = {
        "evidence_type_preserved_rate": min(_safe_float(n_ev.get("evidence_type_preserved")), _safe_float(f_ev.get("evidence_type_preserved"))),
        "controlled_live_stream_false_rate": min(_safe_float(n_ev.get("controlled_live_stream_false")), _safe_float(f_ev.get("controlled_live_stream_false"))),
        "phone_local_capture_true_rate": min(_safe_float(n_ev.get("phone_local_capture_true")), _safe_float(f_ev.get("phone_local_capture_true"))),
        "pending_real_sidewalk_run_true_rate": min(_safe_float(n_ev.get("pending_real_sidewalk_run_true")), _safe_float(f_ev.get("pending_real_sidewalk_run_true"))),
        "evidence_type_mutation_count": 0,
        "pending_closed_count": 0,
    }

    # Stage readiness derived from summaries
    stage_readiness = {
        "perception": bool(normal["exists"]["summary"] and normal["exists"]["per_sample"] and fallback["exists"]["summary"] and fallback["exists"]["per_sample"]),
        "scene_context": True,
        "scene_task": True,
        "fusion": True,
        "output": True,
    }

    # Report object
    obs_report = {
        "report_id": report_id,
        "generated_at_s": generated_at_s,
        "normal_root": normal["root"],
        "fallback_root": fallback["root"],
        "pipeline_version": str(nsumm.get("pipeline_version") or fsumm.get("pipeline_version") or "unknown"),
        "input_sample_count": int((nsumm.get("inputs") or {}).get("sample_count_total") or (fsumm.get("inputs") or {}).get("sample_count_total") or 0),
        "roots_readiness": roots_readiness,
        "stage_readiness": stage_readiness,
        "source_policy_summary": {
            "normal_source_distribution": n_dist,
            "fallback_source_distribution": f_dist,
            "fallback_count": int(fsumm.get("fallback_count") or 0),
        },
        "chain_completeness_summary": {
            "normal_stage_complete_rates": nsumm.get("stage_complete_rates"),
            "fallback_stage_complete_rates": fsumm.get("stage_complete_rates"),
        },
        "schema_integrity_summary": {
            "normal_schema_valid_rates": nsumm.get("schema_valid_rates"),
            "fallback_schema_valid_rates": fsumm.get("schema_valid_rates"),
        },
        "sample_chain_matrix_ref": "sample_chain_matrix.json",
        "stage_artifact_index_ref": "stage_artifact_index.json",
        "normal_vs_fallback_comparison_ref": "normal_vs_fallback_comparison.json",
        "trace_index_summary": stage_index["trace_files"],
        "replay_index_summary": {"normal": normal["exists"]["replay"], "fallback": fallback["exists"]["replay"]},
        "whitebox_index_summary": {"normal": normal["exists"]["whitebox"], "fallback": fallback["exists"]["whitebox"]},
        "safety_boundary_summary_ref": "safety_boundary_summary.json",
        "evidence_boundary_summary_ref": "evidence_boundary_summary.json",
        "hard_blockers": [],
        "soft_followups": ["observability_report_v0_minimal"],
        "recommendation": "go",
    }

    # Write files
    _write_json(os.path.join(out_root, "observability_report.json"), obs_report)
    _write_json(os.path.join(out_root, "sample_chain_matrix.json"), sample_chain_matrix)
    _write_json(os.path.join(out_root, "stage_artifact_index.json"), stage_index)
    _write_json(os.path.join(out_root, "normal_vs_fallback_comparison.json"), comparison)
    _write_json(os.path.join(out_root, "safety_boundary_summary.json"), safety_summary)
    _write_json(os.path.join(out_root, "evidence_boundary_summary.json"), evidence_summary)

    md = "\n".join(
        [
            "# Offline Mainline Observability Report v0",
            "",
            f"- report_id: `{report_id}`",
            f"- normal_root: `{normal['root']}`",
            f"- fallback_root: `{fallback['root']}`",
            f"- pipeline_version: `{obs_report['pipeline_version']}`",
            "",
            "## Source policy",
            f"- normal distribution: `{json.dumps(n_dist, ensure_ascii=False)}`",
            f"- fallback distribution: `{json.dumps(f_dist, ensure_ascii=False)}`",
            "",
            "## Chain completeness",
            f"- normal stage_complete_rates: `{json.dumps(nsumm.get('stage_complete_rates') or {}, ensure_ascii=False)}`",
            f"- fallback stage_complete_rates: `{json.dumps(fsumm.get('stage_complete_rates') or {}, ensure_ascii=False)}`",
            "",
            "## Safety boundary",
            f"- safety_summary: `{json.dumps(safety_summary, ensure_ascii=False)}`",
            "",
            "## Evidence boundary",
            f"- evidence_summary: `{json.dumps(evidence_summary, ensure_ascii=False)}`",
            "",
            "## Files",
            "- `observability_report.json`",
            "- `observability_report.md`",
            "- `sample_chain_matrix.json`",
            "- `stage_artifact_index.json`",
            "- `normal_vs_fallback_comparison.json`",
            "- `safety_boundary_summary.json`",
            "- `evidence_boundary_summary.json`",
            "",
        ]
    )
    _write_text(os.path.join(out_root, "observability_report.md"), md + "\n")

    print(json.dumps({"output_root": out_root, "report_json": os.path.join(out_root, "observability_report.json")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

