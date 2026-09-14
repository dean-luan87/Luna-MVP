#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phase-ModelPerception-003

Compare baseline/mock PerceptionEval-001 outputs vs YOLO shadow outputs (ModelPerception-002B).

Hard boundaries:
- Comparison only; no runtime integration.
- Must not treat fallback as real YOLO capability.
- Must record blockers if baseline root missing.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


FORBIDDEN_TOKENS_V0: Tuple[str, ...] = (
    "execute_now",
    "walk_now",
    "turn_now",
    "cross_now",
    "force_action",
    "release_side_effects",
    "retry_now",
    "reopen_now",
    "enable_default_path",
    "override_governance",
    "final_navigation_instruction",
    "actual_tts",
)


def _ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def _write_json(path: str, obj: Any) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _token_scan(obj: Any) -> Dict[str, Any]:
    try:
        hay = json.dumps(obj, ensure_ascii=False, sort_keys=True).lower()
    except Exception:
        hay = repr(obj).lower()
    hits: List[str] = []
    for tok in FORBIDDEN_TOKENS_V0:
        pat = re.compile(rf"(^|[^a-z0-9_]){re.escape(tok)}([^a-z0-9_]|$)")
        if pat.search(hay) is not None:
            hits.append(tok)
    return {"count": len(hits), "hits": hits}


def _coverage_from_normalized_signals(signals: Any) -> Dict[str, Any]:
    keys = [
        "object_stability_signal",
        "spatial_passability_signal",
        "risk_field_signal",
        "ocr_navigation_signal",
        "dynamic_event_signal",
    ]
    has = {f"has_{k}": isinstance(signals, dict) and (k in signals) for k in keys}
    coverage_rate = sum(1 for v in has.values() if v) / float(len(keys))
    return {**has, "coverage_rate": coverage_rate}


def _find_baseline_file_for_sample(baseline_root: str, sample_id: str, max_files: int = 4000) -> Optional[str]:
    # Best-effort: scan json files and detect sample_id.
    seen = 0
    for dirpath, _, filenames in os.walk(baseline_root):
        for fn in filenames:
            if not fn.endswith(".json"):
                continue
            seen += 1
            if seen > max_files:
                return None
            p = os.path.join(dirpath, fn)
            try:
                obj = _read_json(p)
            except Exception:
                continue
            if isinstance(obj, dict) and obj.get("sample_id") == sample_id:
                return p
            # sometimes nested
            if isinstance(obj, dict) and isinstance(obj.get("normalized_perception_signals"), dict):
                if obj.get("sample_id") == sample_id:
                    return p
    return None


def _load_yolo_sample_result(yolo_root: str, sample_id: str) -> Optional[Dict[str, Any]]:
    p = os.path.join(yolo_root, sample_id, "per_sample_yolo_shadow_results.json")
    if not os.path.exists(p):
        return None
    try:
        return _read_json(p)
    except Exception:
        return None


def _yolo_detection_metrics_from_sample(yolo_obj: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(yolo_obj, dict):
        return {"detection_count": 0, "detected_class_distribution": {}}
    det_count = int(yolo_obj.get("detection_count", 0) or 0)
    dist: Dict[str, int] = {}
    try:
        sig = yolo_obj.get("normalized_perception_signals", {}).get("object_stability_signal", {})
        dist0 = sig.get("class_distribution")
        if isinstance(dist0, dict):
            for k, v in dist0.items():
                try:
                    dist[str(k)] = int(v)
                except Exception:
                    continue
    except Exception:
        dist = {}
    return {"detection_count": det_count, "detected_class_distribution": dist}


def _load_baseline_index_if_present(baseline_root: str) -> Dict[str, Dict[str, Any]]:
    """
    PerceptionEval-001 canonical output includes:
    - per_sample_results.json with {"samples":[{sample_id, signals, ...}, ...]}
    This helper builds an index for fast lookup.
    """
    p = os.path.join(baseline_root, "per_sample_results.json")
    if not os.path.exists(p):
        return {}
    try:
        obj = _read_json(p)
    except Exception:
        return {}
    out: Dict[str, Dict[str, Any]] = {}
    if isinstance(obj, dict) and isinstance(obj.get("samples"), list):
        for r in obj["samples"]:
            if isinstance(r, dict) and r.get("sample_id"):
                out[str(r["sample_id"])] = r
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fieldbatch-sample-matrix", required=True)
    ap.add_argument("--baseline-root", required=True)
    ap.add_argument("--yolo-shadow-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    output_root = os.path.abspath(args.output_root)
    _ensure_dir(output_root)

    fieldbatch = _read_json(args.fieldbatch_sample_matrix)
    samples = fieldbatch.get("samples", [])
    sample_ids = [str(s.get("sample_id")) for s in samples]

    baseline_root = os.path.abspath(args.baseline_root)
    yolo_root = os.path.abspath(args.yolo_shadow_root)

    blockers: List[str] = []
    if not os.path.isdir(baseline_root):
        blockers.append("baseline_root_not_found_or_not_dir")
    if not os.path.isdir(yolo_root):
        blockers.append("yolo_shadow_root_not_found_or_not_dir")

    per_sample: List[Dict[str, Any]] = []
    baseline_index = _load_baseline_index_if_present(baseline_root) if os.path.isdir(baseline_root) else {}

    for sid in sample_ids:
        rec: Dict[str, Any] = {
            "sample_id": sid,
            "baseline_root": baseline_root,
            "yolo_shadow_root": yolo_root,
            "baseline_found": False,
            "baseline_file_ref": None,
            "yolo_found": False,
            "yolo_file_ref": None,
            "notes": [],
        }

        # YOLO side (expected shape)
        yolo_obj = _load_yolo_sample_result(yolo_root, sid) if os.path.isdir(yolo_root) else None
        if yolo_obj is not None:
            rec["yolo_found"] = True
            rec["yolo_file_ref"] = os.path.join(yolo_root, sid, "per_sample_yolo_shadow_results.json")
            yolo_signals = yolo_obj.get("normalized_perception_signals")
            rec["yolo_signal_coverage"] = _coverage_from_normalized_signals(yolo_signals)
            rec["yolo_invoked"] = bool(yolo_obj.get("yolo_invoked", False))
            rec["yolo_disabled"] = bool(yolo_obj.get("yolo_disabled", False))
            rec["fallback_used"] = bool(yolo_obj.get("fallback_used", False))
            rec["fallback_reason"] = yolo_obj.get("fallback_reason")
            rec["yolo_object_detection_available"] = bool(rec["yolo_invoked"]) and int(yolo_obj.get("detection_count", 0) or 0) > 0
            detm = _yolo_detection_metrics_from_sample(yolo_obj)
            rec["detection_count"] = detm["detection_count"]
            rec["detected_class_distribution"] = detm["detected_class_distribution"]
            rec["yolo_allows_execute_now_false"] = (yolo_obj.get("allows_execute_now") is False)
            rec["evidence_type_preserved"] = bool(yolo_obj.get("evidence_type_preserved", False))
            rec["controlled_live_stream_false"] = bool(yolo_obj.get("controlled_live_stream_false", False))

            # Artifact integrity
            sample_dir = os.path.join(yolo_root, sid)
            rec["yolo_trace_ready"] = os.path.exists(os.path.join(sample_dir, "yolo_shadow_trace.jsonl"))
            rec["yolo_replay_ready"] = os.path.exists(os.path.join(sample_dir, "yolo_shadow_replay.jsonl"))
            rec["yolo_whitebox_ready"] = os.path.exists(os.path.join(sample_dir, "yolo_shadow_whitebox.jsonl"))

            leak = _token_scan(yolo_obj)
            rec["yolo_execute_leakage_count"] = leak["count"]
            rec["yolo_default_on_leakage_count"] = 1 if "enable_default_path" in leak["hits"] else 0
        else:
            rec["yolo_signal_coverage"] = _coverage_from_normalized_signals(None)
            rec["yolo_invoked"] = False
            rec["yolo_disabled"] = None
            rec["fallback_used"] = None
            rec["fallback_reason"] = "yolo_output_missing"
            rec["yolo_execute_leakage_count"] = 0
            rec["yolo_default_on_leakage_count"] = 0
            rec["yolo_trace_ready"] = False
            rec["yolo_replay_ready"] = False
            rec["yolo_whitebox_ready"] = False
            rec["detection_count"] = 0
            rec["detected_class_distribution"] = {}

        # Baseline side (best-effort; format may vary)
        baseline_obj: Optional[Dict[str, Any]] = None
        baseline_file: Optional[str] = None
        if sid in baseline_index:
            baseline_obj = baseline_index[sid]
            baseline_file = os.path.join(baseline_root, "per_sample_results.json")
        elif os.path.isdir(baseline_root):
            baseline_file = _find_baseline_file_for_sample(baseline_root, sid)
            if baseline_file:
                try:
                    baseline_obj = _read_json(baseline_file)
                except Exception:
                    baseline_obj = None

        if baseline_obj is not None and baseline_file is not None:
            rec["baseline_found"] = True
            rec["baseline_file_ref"] = baseline_file
            # try to locate signals object
            sig = None
            if isinstance(baseline_obj, dict):
                if isinstance(baseline_obj.get("normalized_perception_signals"), dict):
                    sig = baseline_obj.get("normalized_perception_signals")
                elif isinstance(baseline_obj.get("signals"), dict):
                    sig = baseline_obj.get("signals")
                elif any(k in baseline_obj for k in ["object_stability_signal", "risk_field_signal", "spatial_passability_signal"]):
                    sig = baseline_obj
            rec["baseline_signal_coverage"] = _coverage_from_normalized_signals(sig)
            leakb = _token_scan(baseline_obj)
            rec["baseline_execute_leakage_count"] = leakb["count"]
            rec["baseline_default_on_leakage_count"] = 1 if "enable_default_path" in leakb["hits"] else 0
        else:
            rec["baseline_signal_coverage"] = _coverage_from_normalized_signals(None)
            rec["baseline_execute_leakage_count"] = 0
            rec["baseline_default_on_leakage_count"] = 0
            rec["notes"].append("baseline_not_found_or_unreadable")

        # Explicit label: fallback-only
        if rec.get("yolo_found") and rec.get("fallback_used") is True and rec.get("yolo_invoked") is False:
            rec["notes"].append("yolo_fallback_only_no_invocation")

        per_sample.append(rec)

    n = max(1, len(per_sample))
    baseline_cov = sum(float(r["baseline_signal_coverage"]["coverage_rate"]) for r in per_sample) / n
    yolo_cov = sum(float(r["yolo_signal_coverage"]["coverage_rate"]) for r in per_sample) / n
    yolo_obj_avail = sum(1 for r in per_sample if r.get("yolo_object_detection_available")) / n

    yolo_invoked_count = sum(1 for r in per_sample if r.get("yolo_invoked") is True)
    yolo_fallback_count = sum(1 for r in per_sample if r.get("fallback_used") is True)
    yolo_disabled_count = sum(1 for r in per_sample if r.get("yolo_disabled") is True)
    detection_count_total = sum(int(r.get("detection_count", 0) or 0) for r in per_sample)
    detected_class_distribution: Dict[str, int] = {}
    for r in per_sample:
        d = r.get("detected_class_distribution") or {}
        if isinstance(d, dict):
            for k, v in d.items():
                try:
                    detected_class_distribution[str(k)] = detected_class_distribution.get(str(k), 0) + int(v)
                except Exception:
                    continue

    yolo_exec_leak = sum(int(r.get("yolo_execute_leakage_count", 0) or 0) for r in per_sample)
    base_exec_leak = sum(int(r.get("baseline_execute_leakage_count", 0) or 0) for r in per_sample)
    yolo_def_on = sum(int(r.get("yolo_default_on_leakage_count", 0) or 0) for r in per_sample)
    base_def_on = sum(int(r.get("baseline_default_on_leakage_count", 0) or 0) for r in per_sample)

    yolo_allows_false_rate = sum(1 for r in per_sample if r.get("yolo_allows_execute_now_false") is True) / n
    evidence_preserved_rate = sum(1 for r in per_sample if r.get("evidence_type_preserved") is True and r.get("controlled_live_stream_false") is True) / n

    trace_ready_rate = sum(1 for r in per_sample if r.get("yolo_trace_ready") is True) / n
    replay_ready_rate = sum(1 for r in per_sample if r.get("yolo_replay_ready") is True) / n
    whitebox_ready_rate = sum(1 for r in per_sample if r.get("yolo_whitebox_ready") is True) / n

    summary = {
        "phase": "Phase-ModelPerception-003",
        "tool": "compare_yolo_shadow_vs_baseline_perception_v0.py",
        "generated_at_s": time.time(),
        "inputs": {
            "fieldbatch_sample_matrix": args.fieldbatch_sample_matrix,
            "baseline_root": args.baseline_root,
            "yolo_shadow_root": args.yolo_shadow_root,
        },
        "blockers": blockers,
        "metrics": {
            # Coverage
            "baseline_signal_coverage_rate": baseline_cov,
            "yolo_signal_coverage_rate": yolo_cov,
            "yolo_object_detection_available_rate": yolo_obj_avail,
            # YOLO runtime status
            "yolo_invoked_count": yolo_invoked_count,
            "yolo_fallback_count": yolo_fallback_count,
            "yolo_disabled_count": yolo_disabled_count,
            "yolo_exception_count": 0,
            "yolo_dependency_unavailable_count": 0,
            "detection_count_total": detection_count_total,
            "detection_count_per_sample": {r["sample_id"]: int(r.get("detection_count", 0) or 0) for r in per_sample},
            "detected_class_distribution": detected_class_distribution,
            # Boundaries
            "baseline_execute_leakage_count": base_exec_leak,
            "yolo_execute_leakage_count": yolo_exec_leak,
            "baseline_default_on_leakage_count": base_def_on,
            "yolo_default_on_leakage_count": yolo_def_on,
            "yolo_allows_execute_now_false_rate": yolo_allows_false_rate,
            "evidence_type_preserved_rate": evidence_preserved_rate,
            # Artifact integrity
            "baseline_artifact_ready_rate": 0.0 if "baseline_root_not_found_or_not_dir" in blockers else 1.0,
            "yolo_replay_ready_rate": replay_ready_rate,
            "yolo_whitebox_ready_rate": whitebox_ready_rate,
            "yolo_trace_ready_rate": trace_ready_rate,
        },
        "notes": [
            "This report is comparison-only; it does not integrate YOLO into downstream evaluation chain.",
            "If baseline root is missing, baseline comparison is recorded as not_found and must be treated as a blocker.",
            "Fallback-only YOLO runs are explicitly labeled and must not be misrepresented as real model capability.",
        ],
    }

    _write_json(os.path.join(output_root, "yolo_shadow_vs_baseline_comparison_summary.json"), summary)
    _write_json(os.path.join(output_root, "yolo_shadow_vs_baseline_per_sample_comparison.json"), {"samples": per_sample})

    with open(os.path.join(output_root, "comparison_notes.md"), "w", encoding="utf-8") as f:
        f.write("# YOLO shadow vs baseline perception comparison (v0)\n\n")
        f.write(f"- baseline_root: `{args.baseline_root}`\n")
        f.write(f"- yolo_shadow_root: `{args.yolo_shadow_root}`\n")
        f.write(f"- blockers: `{blockers}`\n")
        f.write("\n")
        f.write("## Reminder\n")
        f.write("- This comparison does not imply integration.\n")
        f.write("- Fallback-only YOLO must not be treated as model capability.\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

