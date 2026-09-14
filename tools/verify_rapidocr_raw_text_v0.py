#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-ModelOCR-004C verifier for RapidOCR raw text harness (A–N)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

FORBIDDEN_KEYS = {
    "navigation",
    "scene_task",
    "fusion",
    "output_action",
    "execute_action",
    "semantic_summary",
}


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _schema_valid(sample: Dict[str, Any]) -> bool:
    try:
        if sample.get("provider_id") != "rapidocr_onnxruntime_v0":
            return False
        if sample.get("model_config_id") != "rapidocr_onnxruntime_v0":
            return False
        if sample.get("ocr_runtime_mode") != "local_onnxruntime_offline":
            return False
        if sample.get("semantic_interpretation_enabled") is not False:
            return False
        if sample.get("allows_execute_now") is not False:
            return False
        if sample.get("real_tts_invoked") is not False:
            return False
        if float(sample.get("latency_ms") or 0) < 0:
            return False
        if sample.get("raw_text_joined_strategy") not in ("model_order", "bbox_top_left", "empty", "unknown"):
            return False
        cands = sample.get("raw_text_candidates")
        if not isinstance(cands, list):
            return False
        for c in cands:
            if not isinstance(c, dict):
                return False
            for k in (
                "text_id",
                "text",
                "normalized_text",
                "bbox",
                "bbox_status",
                "confidence",
                "confidence_status",
                "frame_id",
                "timestamp_ms",
                "line_order",
                "allows_execute_now",
            ):
                if k not in c:
                    return False
        if "raw_text_joined" not in sample:
            return False
        return True
    except Exception:
        return False


def _forbidden_scan(obj: Any) -> int:
    cnt = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in FORBIDDEN_KEYS:
                cnt += 1
            cnt += _forbidden_scan(v)
    elif isinstance(obj, list):
        for x in obj:
            cnt += _forbidden_scan(x)
    return cnt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--macos-baseline-avg-ms",
        type=float,
        default=460.0,
        help="004A reference avg latency per frame (100 frames ~46s)",
    )
    args = ap.parse_args()

    out_root = (
        os.path.abspath(os.path.join(REPO_ROOT, str(args.output_root)))
        if not os.path.isabs(str(args.output_root))
        else os.path.abspath(str(args.output_root))
    )

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    # A
    try:
        import rapidocr_onnxruntime  # noqa: F401

        a_ok = True
        a_err = None
    except Exception as e:
        a_ok = False
        a_err = repr(e)

    checks: Dict[str, Any] = {}
    checks["A_rapidocr_import"] = {"ok": a_ok, "error": a_err}
    if not a_ok:
        hard_blockers.append("rapidocr_import_failed")

    summary_path = os.path.join(out_root, "ocr_raw_text_summary.json")
    per_path = os.path.join(out_root, "per_sample_ocr_raw_text_results.json")
    trace_path = os.path.join(out_root, "ocr_raw_text_trace.jsonl")
    replay_path = os.path.join(out_root, "ocr_raw_text_replay.jsonl")
    whitebox_path = os.path.join(out_root, "ocr_raw_text_whitebox.jsonl")

    if not os.path.exists(summary_path) or not os.path.exists(per_path):
        hard_blockers.append("missing_required_outputs")
        print(
            json.dumps(
                {
                    "phase": "Phase-ModelOCR-004C",
                    "verifier": "verify_rapidocr_raw_text_v0",
                    "checks": checks,
                    "verdict": "NO_GO",
                    "hard_blockers": hard_blockers,
                    "soft_followups": soft_followups,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    summary = _load_json(summary_path)
    per = _load_json(per_path)
    checks["B_outputs_present"] = {"ok": True}

    missing_input = bool((summary.get("input") or {}).get("missing_input_samples"))
    checks["B_input_valid"] = {"ok": not missing_input, "missing_input_samples": missing_input}
    if missing_input:
        hard_blockers.append("missing_input_samples")

    if not isinstance(per, list):
        hard_blockers.append("per_sample_not_list")
        per = []

    if len(per) == 0:
        hard_blockers.append("no_samples_in_output")

    schema_ok = sum(1 for s in per if isinstance(s, dict) and _schema_valid(s))
    checks["C_schema_valid_rate"] = {"ok": schema_ok == len(per), "valid": schema_ok, "total": len(per)}

    if schema_ok == 0 and len(per) > 0:
        hard_blockers.append("schema_invalid_all_samples")
    elif 0 < schema_ok < len(per):
        soft_followups.append(f"partial_schema_valid:{schema_ok}/{len(per)}")

    # D/E/F simplified rates
    def _bbox_ok(s: Dict[str, Any]) -> bool:
        cands = s.get("raw_text_candidates") if isinstance(s.get("raw_text_candidates"), list) else []
        if not cands:
            return True
        return any(isinstance(c, dict) and c.get("bbox") is not None for c in cands) or all(
            isinstance(c, dict) and c.get("bbox") is None for c in cands
        )

    def _conf_ok(s: Dict[str, Any]) -> bool:
        cands = s.get("raw_text_candidates") if isinstance(s.get("raw_text_candidates"), list) else []
        if not cands:
            return True
        return any(isinstance(c, dict) and c.get("confidence") is not None for c in cands) or all(
            isinstance(c, dict) and c.get("confidence") is None for c in cands
        )

    bbox_ok = sum(1 for s in per if isinstance(s, dict) and _bbox_ok(s))
    conf_ok = sum(1 for s in per if isinstance(s, dict) and _conf_ok(s))
    joined_ok = sum(1 for s in per if isinstance(s, dict) and isinstance(s.get("raw_text_joined"), str))
    n = len(per) or 1
    checks["D_bbox_rate"] = {"ok": bbox_ok == len(per), "ok_n": bbox_ok, "total": len(per)}
    checks["E_conf_rate"] = {"ok": conf_ok == len(per), "ok_n": conf_ok, "total": len(per)}
    checks["F_raw_text_joined_rate"] = {"ok": joined_ok == len(per), "ok_n": joined_ok, "total": len(per)}

    checks["G_allows_execute_now_false"] = {"ok": all(isinstance(s, dict) and s.get("allows_execute_now") is False for s in per)}
    checks["H_semantic_off"] = {"ok": all(isinstance(s, dict) and s.get("semantic_interpretation_enabled") is False for s in per)}
    checks["I_tts_off"] = {"ok": all(isinstance(s, dict) and s.get("real_tts_invoked") is False for s in per)}

    downstream_ok = bool((summary.get("governance") or {}).get("downstream_invoked") is False)
    mic = (summary.get("metrics") or {}).get("downstream_invocation_count")
    checks["J_downstream"] = {"ok": downstream_ok and mic in (None, 0)}

    def _non_empty(p: str) -> bool:
        return os.path.exists(p) and os.path.getsize(p) > 0

    checks["K_trace_files"] = {"ok": _non_empty(trace_path) and _non_empty(replay_path) and _non_empty(whitebox_path)}

    m = summary.get("metrics") or {}
    req_keys = (
        "total_runtime_seconds",
        "avg_latency_ms_per_frame",
        "p50_latency_ms_per_frame",
        "p95_latency_ms_per_frame",
    )
    checks["L_performance_metrics"] = {"ok": all(k in m for k in req_keys), "required": req_keys, "present": {k: k in m for k in req_keys}}
    if not checks["L_performance_metrics"]["ok"]:
        hard_blockers.append("performance_metrics_incomplete")

    mas = summary.get("model_asset_status")
    rr = summary.get("reproducibility_risk")
    checks["M_model_assets"] = {
        "ok": mas in ("pinned_local", "cache_detected", "auto_downloaded", "unknown"),
        "model_asset_status": mas,
        "reproducibility_risk": rr,
    }
    if mas == "auto_downloaded":
        soft_followups.append("model_auto_downloaded_reproducibility_risk")
    if mas == "unknown":
        soft_followups.append("model_asset_status_unknown")

    baseline = float(args.macos_baseline_avg_ms)
    avg_lat = float(m.get("avg_latency_ms_per_frame") or 0.0)
    if len(per) == 0:
        faster = False
        n_note = "skipped_no_samples"
    else:
        faster = avg_lat < baseline
        n_note = "004A macOS Vision ~460ms/frame @ 100 frames / ~46s wall"
    checks["N_vs_macos_vision_avg_latency"] = {
        "ok": faster if len(per) > 0 else False,
        "baseline_avg_ms_per_frame": baseline,
        "observed_avg_ms_per_frame": avg_lat,
        "note": n_note,
    }
    if len(per) > 0 and not faster:
        hard_blockers.append("not_faster_than_macos_vision_baseline")

    forbidden_cnt = _forbidden_scan(summary) + _forbidden_scan(per)
    checks["forbidden_key_scan"] = {"ok": forbidden_cnt == 0, "count": forbidden_cnt}
    if forbidden_cnt > 0:
        hard_blockers.append("forbidden_semantic_nav_fields")

    if not checks["G_allows_execute_now_false"]["ok"] or not checks["H_semantic_off"]["ok"] or not checks["I_tts_off"]["ok"]:
        hard_blockers.append("governance_invariant_failed")
    if not checks["J_downstream"]["ok"]:
        hard_blockers.append("downstream_invoked")
    if not checks["K_trace_files"]["ok"]:
        hard_blockers.append("trace_files_missing_or_empty")

    hard_blockers = list(dict.fromkeys(hard_blockers))

    if hard_blockers:
        verdict = "NO_GO"
    elif soft_followups:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    print(
        json.dumps(
            {
                "phase": "Phase-ModelOCR-004C",
                "verifier": "verify_rapidocr_raw_text_v0",
                "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
                "checks": checks,
                "verdict": verdict,
                "hard_blockers": hard_blockers,
                "soft_followups": soft_followups,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())
