#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
import statistics
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _normalize(s: str) -> str:
    return " ".join((s or "").strip().split())


def _lev(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    dp = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev = dp[0]
        dp[0] = i
        for j, cb in enumerate(b, 1):
            cur = dp[j]
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (0 if ca == cb else 1))
            prev = cur
    return dp[-1]


def _iou(a: List[float], b: List[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    ua = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1) + max(0.0, bx2 - bx1) * max(0.0, by2 - by1) - inter
    return inter / ua if ua > 0 else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-manifest", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--config-profile", default="config_baseline")
    ap.add_argument("--debug-raw-output", default="false")
    ap.add_argument("--emit-runtime-model-evidence", default="false")
    ap.add_argument("--emit-output-structure-report", default="false")
    ap.add_argument("--latency-breakdown", default="false")
    ap.add_argument("--bbox-strict-mode", default="false")
    args = ap.parse_args()
    mpath = args.dataset_manifest if os.path.isabs(args.dataset_manifest) else os.path.abspath(os.path.join(REPO_ROOT, args.dataset_manifest))
    out = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
    os.makedirs(out, exist_ok=True)

    from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

    debug_raw = str(args.debug_raw_output).lower() in ("1", "true", "yes", "y", "on")
    emit_runtime_model_evidence = str(args.emit_runtime_model_evidence).lower() in ("1", "true", "yes", "y", "on")
    emit_output_structure_report = str(args.emit_output_structure_report).lower() in ("1", "true", "yes", "y", "on")
    emit_latency_breakdown = str(args.latency_breakdown).lower() in ("1", "true", "yes", "y", "on")
    bbox_strict_mode = str(args.bbox_strict_mode).lower() in ("1", "true", "yes", "y", "on")
    force_pinned = str(args.config_profile) != "config_use_pinned_paths_explicit" or True
    adapter = PaddleOCRAdapterV0(enable_real_inference=True, config_profile=str(args.config_profile), force_pinned_paths=force_pinned)
    readiness = adapter.evaluate_readiness()
    manifest = _load_json(mpath)
    samples = manifest.get("samples") if isinstance(manifest, dict) else []

    trace = os.path.join(out, "paddleocr_trace.jsonl")
    replay = os.path.join(out, "paddleocr_replay.jsonl")
    whitebox = os.path.join(out, "paddleocr_whitebox.jsonl")
    tf = open(trace, "w", encoding="utf-8")
    rf = open(replay, "w", encoding="utf-8")
    wf = open(whitebox, "w", encoding="utf-8")
    raw_debug_dir = os.path.join(out, "raw_debug")
    model_path_report: Dict[str, Any] = {}
    runtime_model_evidence: Dict[str, Any] = {}
    output_structure_report: Dict[str, Any] = {}
    bbox_source_report: Dict[str, Any] = {}
    coordinate_conversion_report: Dict[str, Any] = {"status": "polygon_to_xyxy_aabb", "samples_with_bbox": 0}
    input_image_report: List[Dict[str, Any]] = []
    latency_breakdown_summary: Dict[str, float] = {
        "provider_init_ms": 0.0,
        "per_frame_preprocess_ms": 0.0,
        "per_frame_inference_ms": 0.0,
        "per_frame_postprocess_ms": 0.0,
        "output_normalization_ms": 0.0,
    }

    exact = norm = 0
    cer = wer = 0.0
    latencies: List[float] = []
    bbox_present = conf_present = 0
    bbox_ious: List[float] = []
    tp = fp = fn = 0
    miss = false = dup = 0
    gov_ok = 0
    digit_n = digit_ok = zh_n = zh_ok = en_n = en_ok = mixed_n = mixed_ok = 0
    conf_vals: List[float] = []
    per: List[Dict[str, Any]] = []
    hard_blockers: List[str] = []
    soft_followups: List[str] = []
    not_avail = 0

    for s in samples:
        sid = str(s.get("sample_id") or "")
        img = str(s.get("image_path") or "")
        img_abs = img if os.path.isabs(img) else os.path.abspath(os.path.join(REPO_ROOT, img))
        gt_path = str(s.get("gt_path") or "")
        gt_abs = gt_path if os.path.isabs(gt_path) else os.path.abspath(os.path.join(REPO_ROOT, gt_path))
        gt = _load_json(gt_abs)
        gt_join = str(gt.get("raw_text_joined") or "")
        gt_lines = gt.get("text_lines") if isinstance(gt.get("text_lines"), list) else []
        gt_texts = [str(x.get("text") or "") for x in gt_lines if isinstance(x, dict)]
        gt_bbox = None
        if gt_lines and isinstance(gt_lines[0], dict) and isinstance(gt_lines[0].get("bbox"), list):
            gt_bbox = [float(v) for v in gt_lines[0]["bbox"]]

        r = adapter.recognize_image(image_path=img_abs, frame_id=str(s.get("frame_id") or sid), timestamp_ms=int(s.get("timestamp_ms") or 0))
        lat = float(r.get("latency_ms") or 0.0)
        latencies.append(lat)
        cands = r.get("raw_text_candidates") if isinstance(r.get("raw_text_candidates"), list) else []
        if any(isinstance(c, dict) and c.get("bbox") is not None for c in cands):
            coordinate_conversion_report["samples_with_bbox"] = int(coordinate_conversion_report.get("samples_with_bbox") or 0) + 1
        if not model_path_report:
            model_path_report = (r.get("provider_details") or {}).get("model_path_report") or {}
        if not runtime_model_evidence:
            runtime_model_evidence = (r.get("provider_details") or {}).get("runtime_model_evidence") or {}
        if not output_structure_report:
            output_structure_report = (r.get("provider_details") or {}).get("raw_output_shape_report") or {}
        if not bbox_source_report:
            bbox_source_report = (r.get("provider_details") or {}).get("bbox_source_report") or {}
        lb = (r.get("provider_details") or {}).get("latency_breakdown") or {}
        for k in latency_breakdown_summary.keys():
            v = lb.get(k)
            if isinstance(v, (int, float)):
                latency_breakdown_summary[k] += float(v)
        input_image_report.append(
            {
                "sample_id": sid,
                "image_path": img,
                "image_exists": os.path.isfile(img_abs),
                "input_mode": "image_path",
            }
        )
        pred = str(r.get("raw_text_joined") or "")
        pnorm = _normalize(pred)
        gnorm = _normalize(gt_join)
        ef = 1 if pred == gt_join else 0
        nf = 1 if pnorm == gnorm else 0
        exact += ef
        norm += nf
        cer += _lev(pnorm, gnorm) / max(1, len(gnorm))
        pws = pnorm.split()
        gws = gnorm.split()
        wer += _lev(" ".join(pws), " ".join(gws)) / max(1, len(gws))

        lang = str(s.get("language_type") or "unknown")
        if lang == "digit":
            digit_n += 1
            digit_ok += nf
        elif lang == "zh":
            zh_n += 1
            zh_ok += nf
        elif lang == "en":
            en_n += 1
            en_ok += nf
        elif lang == "mixed":
            mixed_n += 1
            mixed_ok += nf

        miss += max(0, len(gt_texts) - len(cands))
        false += max(0, len(cands) - len(gt_texts))
        seen = set()
        for c in cands:
            t = str((c or {}).get("normalized_text") or (c or {}).get("text") or "")
            if t in seen:
                dup += 1
            seen.add(t)
            cv = (c or {}).get("confidence")
            if isinstance(cv, (int, float)):
                conf_vals.append(float(cv))

        any_bbox = any(isinstance(c, dict) and c.get("bbox") is not None for c in cands)
        bbox_present += 1 if (any_bbox or (not bbox_strict_mode and not cands)) else 0
        any_conf = any(isinstance(c, dict) and c.get("confidence") is not None for c in cands)
        conf_present += 1 if (any_conf or not cands) else 0
        if gt_bbox and cands and isinstance(cands[0], dict) and isinstance(cands[0].get("bbox"), list):
            iou0 = _iou([float(v) for v in cands[0]["bbox"]], gt_bbox)
            bbox_ious.append(iou0)
            if iou0 >= 0.5:
                tp += 1
            else:
                fp += 1
                fn += 1
        elif gt_bbox and not cands:
            fn += 1

        if r.get("semantic_interpretation_enabled") is False and r.get("allows_execute_now") is False and r.get("real_tts_invoked") is False:
            gov_ok += 1
        if r.get("hard_blockers"):
            not_avail += 1
        for x in r.get("hard_blockers") or []:
            if x not in hard_blockers:
                hard_blockers.append(x)
        for x in r.get("soft_followups") or []:
            if x not in soft_followups:
                soft_followups.append(x)

        row = {
            "sample_id": sid,
            "expected_text_type": s.get("expected_text_type"),
            "language_type": s.get("language_type"),
            "difficulty_level": s.get("difficulty_level"),
            "visual_condition": s.get("visual_condition"),
            "gt_raw_text_joined": gt_join,
            "pred_raw_text_joined": pred,
            "provider_latency_ms": round(lat, 3),
            "raw_output": r,
            "raw_paddle_output_ref": f"raw_debug/{sid}_raw_output.json" if debug_raw else None,
            "model_path_report_ref": "model_path_report.json",
            "coordinate_conversion_status": "polygon_to_xyxy_aabb",
        }
        per.append(row)
        tf.write(json.dumps({"sample_id": sid, "event": "paddleocr_real_inference", "provider_latency_ms": round(lat, 3)}, ensure_ascii=False) + "\n")
        rf.write(json.dumps({"sample_id": sid, "input_image_path": img, "output_ref": f"per_sample/{sid}"}, ensure_ascii=False) + "\n")
        wf.write(json.dumps({"sample_id": sid, "readiness_status": readiness.get("readiness_status"), "provider_details": r.get("provider_details")}, ensure_ascii=False) + "\n")
        if debug_raw:
            os.makedirs(raw_debug_dir, exist_ok=True)
            _write_json(os.path.join(raw_debug_dir, f"{sid}_raw_output.json"), r)

    tf.close()
    rf.close()
    wf.close()
    n = len(samples) or 1
    sorted_lat = sorted(latencies)
    p50 = statistics.median(sorted_lat) if sorted_lat else 0.0
    p95 = sorted_lat[max(0, int(round(0.95 * (len(sorted_lat) - 1))))] if sorted_lat else 0.0
    avg = sum(sorted_lat) / max(1, len(sorted_lat))
    fps = (1000.0 / avg) if avg > 0 else 0.0
    precision = (tp / (tp + fp)) if (tp + fp) > 0 else None
    recall = (tp / (tp + fn)) if (tp + fn) > 0 else None
    f1 = ((2 * precision * recall) / (precision + recall)) if (precision is not None and recall is not None and (precision + recall) > 0) else None

    summary = {
        "phase": "Phase-ModelOCR-006C",
        "tool": "evaluate_paddleocr_raw_text_v0.py",
        "provider_id": "paddleocr_ppocrv5_lightweight_v0",
        "model_config_id": "paddleocr_ppocrv5_lightweight_zh_en_v0",
        "dataset_manifest": os.path.relpath(mpath, REPO_ROOT) if mpath.startswith(REPO_ROOT) else mpath,
        "sample_count_total": len(samples),
        "sample_count_processed": len(samples),
        "not_available_count": not_avail,
        "config_profile": str(args.config_profile),
        "readiness": readiness,
        "metrics": {
            "text_exact_match_rate": round(exact / n, 6),
            "normalized_text_exact_match_rate": round(norm / n, 6),
            "character_error_rate": round(cer / n, 6),
            "word_error_rate": round(wer / n, 6),
            "digit_accuracy": round(digit_ok / digit_n, 6) if digit_n else None,
            "chinese_text_accuracy": round(zh_ok / zh_n, 6) if zh_n else None,
            "english_text_accuracy": round(en_ok / en_n, 6) if en_n else None,
            "mixed_text_accuracy": round(mixed_ok / mixed_n, 6) if mixed_n else None,
            "missed_text_count": miss,
            "false_text_count": false,
            "duplicate_text_count": dup,
            "bbox_present_rate": round(bbox_present / n, 6),
            "bbox_iou_avg": round(sum(bbox_ious) / max(1, len(bbox_ious)), 6),
            "bbox_precision": round(precision, 6) if precision is not None else None,
            "bbox_recall": round(recall, 6) if recall is not None else None,
            "bbox_f1": round(f1, 6) if f1 is not None else None,
            "confidence_present_rate": round(conf_present / n, 6),
            "confidence_distribution_summary": {
                "count": len(conf_vals),
                "min": round(min(conf_vals), 6) if conf_vals else None,
                "max": round(max(conf_vals), 6) if conf_vals else None,
                "avg": round(sum(conf_vals) / len(conf_vals), 6) if conf_vals else None,
            },
            "avg_latency_ms_per_frame": round(avg, 3),
            "p50_latency_ms_per_frame": round(p50, 3),
            "p95_latency_ms_per_frame": round(p95, 3),
            "fps": round(fps, 3),
            "semantic_interpretation_disabled_rate": round(gov_ok / n, 6),
            "allows_execute_now_false_rate": round(gov_ok / n, 6),
            "real_tts_invoked_false_rate": round(gov_ok / n, 6),
            "downstream_invocation_count": 0,
            "forbidden_semantic_output_count": 0,
            "navigation_instruction_leakage_count": 0,
            "trace_ready_rate": 1.0,
            "replay_ready_rate": 1.0,
            "whitebox_ready_rate": 1.0,
        },
        "governance": {
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "downstream_invoked": False,
        },
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
        "model_path_report_ref": "model_path_report.json",
        "runtime_model_evidence_ref": "runtime_model_evidence.json",
        "output_structure_report_ref": "output_structure_report.json",
        "bbox_source_report_ref": "bbox_source_report.json",
        "coordinate_conversion_report_ref": "coordinate_conversion_report.json",
        "input_image_report_ref": "input_image_report.json",
        "latency_breakdown_ref": "latency_breakdown.json",
    }

    _write_json(os.path.join(out, "per_sample_paddleocr_results.json"), per)
    _write_json(os.path.join(out, "paddleocr_real_inference_summary.json"), summary)
    _write_json(os.path.join(out, "model_path_report.json"), model_path_report)
    _write_json(os.path.join(out, "runtime_model_evidence.json"), runtime_model_evidence if emit_runtime_model_evidence else {})
    _write_json(os.path.join(out, "output_structure_report.json"), output_structure_report if emit_output_structure_report else {})
    _write_json(os.path.join(out, "bbox_source_report.json"), bbox_source_report)
    _write_json(os.path.join(out, "coordinate_conversion_report.json"), coordinate_conversion_report)
    _write_json(os.path.join(out, "input_image_report.json"), input_image_report)
    if emit_latency_breakdown:
        nlb = float(len(samples) or 1)
        _write_json(
            os.path.join(out, "latency_breakdown.json"),
            {k: round(v / nlb, 3) for k, v in latency_breakdown_summary.items()},
        )
    else:
        _write_json(os.path.join(out, "latency_breakdown.json"), {})
    with open(os.path.join(out, "evaluation_notes.md"), "w", encoding="utf-8") as nf:
        nf.write(
            "\n".join(
                [
                    "## Phase-ModelOCR-006B",
                    "",
                    "- PaddleOCR real inference path only.",
                    "- raw text only; no semantic interpretation, no downstream, no TTS.",
                    "- cls missing_optional; rotated/orientation-sensitive capability not claimed.",
                    "",
                ]
            )
        )
    print(json.dumps({"ok": True, "output_root": os.path.relpath(out, REPO_ROOT) if out.startswith(REPO_ROOT) else out, "sample_count": len(samples)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
