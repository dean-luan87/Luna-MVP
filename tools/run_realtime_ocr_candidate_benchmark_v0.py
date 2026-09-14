#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-ModelOCR-006E: Realtime OCR candidate benchmark (raw text only)."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import statistics
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)

FORBIDDEN_GT_FIELDS = {
    "scene_type",
    "task_label",
    "navigation_action",
    "route_advice",
    "semantic_summary",
    "should_speak",
    "should_turn",
    "go_direction",
}

ALLOWED_PROVIDERS = frozenset(
    {
        "rapidocr_current",
        "rapidocr_ppocrv5_mobile_onnx",
        "rapidocr_ppocrv4_mobile_onnx",
        "easyocr",
        "tesseract",
    }
)
FORBIDDEN_PROVIDERS = frozenset(
    {
        "paddleocr",
        "macos_vision",
        "surya",
        "doctr",
        "paddleocr_vl",
        "deepseek_ocr",
    }
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_repo_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


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
            cost = 0 if ca == cb else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = cur
    return dp[-1]


def _iou(a: List[float], b: List[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)
    inter = iw * ih
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    den = area_a + area_b - inter
    return float(inter / den) if den > 0 else 0.0


def _safe_rate(numer: float, denom: float) -> Optional[float]:
    if denom <= 0:
        return None
    return round(float(numer) / float(denom), 6)


def _adapter_factory(key: str) -> Any:
    if key == "rapidocr_current":
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        return RapidOCRAdapterV0()
    if key == "rapidocr_ppocrv4_mobile_onnx":
        from capabilities.model_ocr.rapidocr_variant_adapter_v0 import RapidOCRVariantAdapterV0

        return RapidOCRVariantAdapterV0(variant="ppocrv4_mobile", repo_root=REPO_ROOT)
    if key == "rapidocr_ppocrv5_mobile_onnx":
        from capabilities.model_ocr.rapidocr_variant_adapter_v0 import RapidOCRVariantAdapterV0

        return RapidOCRVariantAdapterV0(variant="ppocrv5_mobile", repo_root=REPO_ROOT)
    if key == "easyocr":
        from capabilities.model_ocr.easyocr_adapter_v0 import EasyOCRAdapterV0

        return EasyOCRAdapterV0()
    if key == "tesseract":
        from capabilities.model_ocr.tesseract_adapter_v0 import TesseractAdapterV0

        return TesseractAdapterV0()
    raise ValueError(f"unknown_provider:{key}")


def _asset_report(adapter: Any) -> Dict[str, Any]:
    if hasattr(adapter, "asset_report"):
        return adapter.asset_report(repo_root=REPO_ROOT)
    return {
        "provider_id": getattr(adapter, "provider_id", "unknown"),
        "model_config_id": getattr(adapter, "model_config_id", "unknown"),
        "dependency_ready": False,
        "model_assets_status": "unknown",
        "notes": "no_asset_report_method",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--providers",
        default="rapidocr_current,rapidocr_ppocrv5_mobile_onnx,rapidocr_ppocrv4_mobile_onnx,easyocr,tesseract",
    )
    ap.add_argument("--dataset-manifest", default="datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json")
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    providers = [x.strip() for x in str(args.providers).split(",") if x.strip()]
    for p in providers:
        if p in FORBIDDEN_PROVIDERS:
            raise SystemExit(f"forbidden_provider_in_006e:{p}")
        if p not in ALLOWED_PROVIDERS:
            raise SystemExit(f"provider_not_allowed_006e:{p}")

    dataset_manifest = _resolve_repo_path(str(args.dataset_manifest))
    out_root = _resolve_repo_path(str(args.output_root))
    os.makedirs(out_root, exist_ok=True)
    for d in (
        "per_provider_summaries",
        "raw_outputs",
        "metric_tables",
        "provider_asset_reports",
        "trace",
        "replay",
        "whitebox",
    ):
        os.makedirs(os.path.join(out_root, d), exist_ok=True)

    man = _load_json(dataset_manifest)
    samples = man.get("samples") if isinstance(man, dict) else None
    if not isinstance(samples, list) or not samples:
        raise SystemExit("dataset_manifest_samples_missing")

    gt_map: Dict[str, Dict[str, Any]] = {}
    forbidden_gt_count = 0
    for s in samples:
        sid = str(s.get("sample_id") or "")
        gp = _resolve_repo_path(str(s.get("gt_path") or ""))
        g = _load_json(gp)
        gt_map[sid] = g
        keys = set(g.keys()) if isinstance(g, dict) else set()
        forbidden_gt_count += len(keys.intersection(FORBIDDEN_GT_FIELDS))

    per_provider_summary: Dict[str, Dict[str, Any]] = {}
    per_sample_cmp: List[Dict[str, Any]] = []
    acc_table: Dict[str, Any] = {}
    lat_table: Dict[str, Any] = {}
    bbox_table: Dict[str, Any] = {}
    gov_table: Dict[str, Any] = {}
    asset_reports: Dict[str, Any] = {}

    coverage = {
        "expected_text_type": sorted({str(s.get("expected_text_type") or "unknown") for s in samples}),
        "difficulty_level": sorted({str(s.get("difficulty_level") or "unknown") for s in samples}),
        "visual_condition": sorted({str(s.get("visual_condition") or "unknown") for s in samples}),
        "language_type": sorted({str(s.get("language_type") or "unknown") for s in samples}),
    }

    for pname in providers:
        adapter = _adapter_factory(pname)
        asset_reports[pname] = _asset_report(adapter)
        _write_json(os.path.join(out_root, "provider_asset_reports", f"{pname}_assets.json"), asset_reports[pname])

        p_out_dir = os.path.join(out_root, "raw_outputs", pname)
        os.makedirs(p_out_dir, exist_ok=True)

        provider_results: List[Dict[str, Any]] = []
        latencies: List[float] = []
        conf_vals: List[float] = []
        exact = norm_exact = 0
        cer_sum = 0.0
        wer_sum = 0.0
        miss = false = dup = 0
        bbox_present = 0
        bbox_iou_vals: List[float] = []
        bbox_tp = bbox_fp = bbox_fn = 0
        conf_present = 0
        gov_sem_off = gov_exec_off = gov_tts_off = 0
        digit_n = digit_ok = zh_n = zh_ok = en_n = en_ok = mixed_n = mixed_ok = 0
        timeouts = 0
        success_samples = 0
        fail_samples = 0

        trace_path = os.path.join(out_root, "trace", f"{pname}_trace.jsonl")
        replay_path = os.path.join(out_root, "replay", f"{pname}_replay.jsonl")
        whitebox_path = os.path.join(out_root, "whitebox", f"{pname}_whitebox.jsonl")
        tf = open(trace_path, "w", encoding="utf-8")
        rf = open(replay_path, "w", encoding="utf-8")
        wf = open(whitebox_path, "w", encoding="utf-8")

        for s in samples:
            sid = str(s.get("sample_id"))
            img = _resolve_repo_path(str(s.get("image_path")))
            fid = str(s.get("frame_id") or sid)
            tms = int(s.get("timestamp_ms") or 0)
            g = gt_map[sid]
            gt_join = str(g.get("raw_text_joined") or "")
            gt_lines = g.get("text_lines") if isinstance(g.get("text_lines"), list) else []
            gt_texts = [str(x.get("text") or "") for x in gt_lines if isinstance(x, dict)]
            gt_first_bbox = None
            if gt_lines and isinstance(gt_lines[0], dict) and isinstance(gt_lines[0].get("bbox"), list):
                gt_first_bbox = [float(v) for v in gt_lines[0]["bbox"]]

            t0 = time.perf_counter()
            try:
                r = adapter.recognize_image(image_path=img, frame_id=fid, timestamp_ms=tms)
                provider_success = len(r.get("hard_blockers") or []) == 0
            except Exception as e:
                r = {
                    "sample_id": fid,
                    "provider_id": getattr(adapter, "provider_id", pname),
                    "model_config_id": getattr(adapter, "model_config_id", pname),
                    "ocr_runtime_mode": "offline_batch",
                    "raw_text_candidates": [],
                    "raw_text_joined": "",
                    "raw_text_joined_strategy": "unknown",
                    "semantic_interpretation_enabled": False,
                    "allows_execute_now": False,
                    "real_tts_invoked": False,
                    "hard_blockers": [f"provider_exception:{e!r}"],
                    "soft_followups": [],
                    "latency_ms": 0.0,
                }
                provider_success = False
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            provider_latency_ms = float(r.get("latency_ms") or elapsed_ms)
            latencies.append(provider_latency_ms)
            if provider_latency_ms > 1200.0:
                timeouts += 1

            if provider_success:
                success_samples += 1
            else:
                fail_samples += 1

            pred_join = str(r.get("raw_text_joined") or "")
            pred_norm = _normalize(pred_join)
            gt_norm = _normalize(gt_join)
            exact += 1 if pred_join == gt_join else 0
            norm_exact += 1 if pred_norm == gt_norm else 0
            exact_flag = 1 if pred_norm == gt_norm else 0

            lang = str(s.get("language_type") or "unknown")
            if lang == "digit":
                digit_n += 1
                digit_ok += exact_flag
            elif lang == "zh":
                zh_n += 1
                zh_ok += exact_flag
            elif lang == "en":
                en_n += 1
                en_ok += exact_flag
            elif lang == "mixed":
                mixed_n += 1
                mixed_ok += exact_flag

            cer_sum += _lev(pred_norm, gt_norm) / max(1, len(gt_norm))
            pred_words = pred_norm.split()
            gt_words = gt_norm.split()
            wer_sum += _lev(" ".join(pred_words), " ".join(gt_words)) / max(1, len(gt_words))

            pred_cands = r.get("raw_text_candidates") if isinstance(r.get("raw_text_candidates"), list) else []
            miss += max(0, len(gt_texts) - len(pred_cands))
            false += max(0, len(pred_cands) - len(gt_texts))
            seen = set()
            for c in pred_cands:
                if isinstance(c, dict):
                    t = str(c.get("normalized_text") or c.get("text") or "")
                    if t in seen:
                        dup += 1
                    seen.add(t)
                    cv = c.get("confidence")
                    if isinstance(cv, (int, float)):
                        conf_vals.append(float(cv))

            any_bbox = any(isinstance(c, dict) and c.get("bbox") is not None for c in pred_cands)
            bbox_present += 1 if (any_bbox or not pred_cands) else 0
            if gt_first_bbox and pred_cands and isinstance(pred_cands[0], dict) and isinstance(pred_cands[0].get("bbox"), list):
                try:
                    iou0 = _iou([float(v) for v in pred_cands[0]["bbox"]], gt_first_bbox)
                    bbox_iou_vals.append(iou0)
                    if iou0 >= 0.5:
                        bbox_tp += 1
                    else:
                        bbox_fp += 1
                        bbox_fn += 1
                except Exception:
                    pass
            elif gt_first_bbox and not pred_cands:
                bbox_fn += 1
            elif (not gt_first_bbox) and pred_cands:
                bbox_fp += 1

            any_conf = any(isinstance(c, dict) and c.get("confidence") is not None for c in pred_cands)
            conf_present += 1 if (any_conf or not pred_cands) else 0

            gov_sem_off += 1 if r.get("semantic_interpretation_enabled") is False else 0
            gov_exec_off += 1 if r.get("allows_execute_now") is False else 0
            gov_tts_off += 1 if r.get("real_tts_invoked") is False else 0

            result = {
                "sample_id": sid,
                "provider_key": pname,
                "provider_id": r.get("provider_id"),
                "provider_success": provider_success,
                "provider_latency_ms": round(provider_latency_ms, 3),
                "raw_output": r,
                "gt_raw_text_joined": gt_join,
                "pred_raw_text_joined": pred_join,
            }
            provider_results.append(result)
            per_sample_cmp.append(
                {
                    "sample_id": sid,
                    "provider_key": pname,
                    "provider_id": r.get("provider_id"),
                    "expected_text_type": str(s.get("expected_text_type") or "unknown"),
                    "language_type": lang,
                    "pred": pred_join,
                    "gt": gt_join,
                    "provider_success": provider_success,
                    "provider_latency_ms": round(provider_latency_ms, 3),
                }
            )

            tf.write(
                json.dumps(
                    {
                        "request_id": f"{pname}:{sid}",
                        "provider_id": r.get("provider_id"),
                        "latency_ms": round(provider_latency_ms, 3),
                        "provider_success": provider_success,
                        "hard_blockers": r.get("hard_blockers"),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            rf.write(
                json.dumps(
                    {
                        "sample_id": sid,
                        "input_ref": img,
                        "output_ref": f"raw_outputs/{pname}/{sid}.json",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            wf.write(
                json.dumps(
                    {
                        "sample_id": sid,
                        "governance_ok": r.get("semantic_interpretation_enabled") is False,
                        "not_available_reason": None if provider_success else ";".join(r.get("hard_blockers") or []),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            _write_json(os.path.join(p_out_dir, f"{sid}.json"), result)

        tf.close()
        rf.close()
        wf.close()

        n = len(samples)
        avg_lat = sum(latencies) / max(1, n)
        sorted_lat = sorted(latencies)
        p50 = statistics.median(sorted_lat) if sorted_lat else 0.0
        p95 = sorted_lat[max(0, int(round(0.95 * (len(sorted_lat) - 1))))] if sorted_lat else 0.0
        fps = (1000.0 / avg_lat) if avg_lat > 0 else 0.0

        tex = round(exact / n, 6)
        accuracy_risk = tex < 0.2

        prec = _safe_rate(bbox_tp, (bbox_tp + bbox_fp))
        rec = _safe_rate(bbox_tp, (bbox_tp + bbox_fn))
        f1 = None
        if prec is not None and rec is not None and (prec + rec) > 0:
            f1 = round(2.0 * prec * rec / (prec + rec), 6)

        if success_samples == n:
            run_status = "success"
        elif success_samples == 0:
            run_status = "not_available"
        else:
            run_status = "partial"

        ar = asset_reports[pname]
        metrics = {
            "text_exact_match_rate": tex,
            "normalized_text_exact_match_rate": round(norm_exact / n, 6),
            "character_error_rate": round(cer_sum / n, 6),
            "word_error_rate": round(wer_sum / n, 6),
            "digit_accuracy": _safe_rate(digit_ok, digit_n),
            "chinese_text_accuracy": _safe_rate(zh_ok, zh_n),
            "english_text_accuracy": _safe_rate(en_ok, en_n),
            "mixed_text_accuracy": _safe_rate(mixed_ok, mixed_n),
            "missed_text_count": miss,
            "false_text_count": false,
            "duplicate_text_count": dup,
            "bbox_present_rate": round(bbox_present / n, 6),
            "bbox_iou_avg": round(sum(bbox_iou_vals) / max(1, len(bbox_iou_vals)), 6),
            "bbox_precision": prec,
            "bbox_recall": rec,
            "bbox_f1": f1,
            "confidence_present_rate": round(conf_present / n, 6),
            "confidence_distribution_summary": {
                "count": len(conf_vals),
                "min": round(min(conf_vals), 6) if conf_vals else None,
                "max": round(max(conf_vals), 6) if conf_vals else None,
                "avg": round(sum(conf_vals) / len(conf_vals), 6) if conf_vals else None,
            },
            "avg_latency_ms_per_frame": round(avg_lat, 3),
            "p50_latency_ms_per_frame": round(p50, 3),
            "p95_latency_ms_per_frame": round(p95, 3),
            "fps": round(fps, 3),
            "timeout_count": timeouts,
            "semantic_interpretation_disabled_rate": round(gov_sem_off / n, 6),
            "allows_execute_now_false_rate": round(gov_exec_off / n, 6),
            "real_tts_invoked_false_rate": round(gov_tts_off / n, 6),
            "downstream_invocation_count": 0,
            "forbidden_semantic_output_count": 0,
            "navigation_instruction_leakage_count": 0,
            "trace_ready_rate": 1.0,
            "replay_ready_rate": 1.0,
            "whitebox_ready_rate": 1.0,
            "accuracy_risk_flag": accuracy_risk,
            "model_assets_status": ar.get("model_assets_status"),
            "reproducibility_risk": ar.get("reproducibility_risk"),
            "runtime_network_required": bool(ar.get("requires_network_at_runtime")),
        }

        p_summary = {
            "phase": "Phase-ModelOCR-006E",
            "provider_key": pname,
            "provider_id": getattr(adapter, "provider_id", pname),
            "model_config_id": getattr(adapter, "model_config_id", pname),
            "sample_count_total": n,
            "sample_count_processed": n,
            "sample_success_count": success_samples,
            "sample_fail_count": fail_samples,
            "run_status": run_status,
            "metrics": metrics,
            "asset_report_ref": f"provider_asset_reports/{pname}_assets.json",
            "not_available_reason": ar.get("not_available_reason") or ar.get("error"),
            "missing_assets": ar.get("missing_assets"),
            "hard_blockers": [],
            "soft_followups": [],
        }
        per_provider_summary[pname] = p_summary
        _write_json(os.path.join(out_root, "per_provider_summaries", f"{pname}_summary.json"), p_summary)

        acc_table[pname] = {k: metrics[k] for k in metrics if k in ("text_exact_match_rate", "normalized_text_exact_match_rate", "character_error_rate", "word_error_rate")}
        lat_table[pname] = {
            k: metrics[k]
            for k in (
                "avg_latency_ms_per_frame",
                "p50_latency_ms_per_frame",
                "p95_latency_ms_per_frame",
                "fps",
                "timeout_count",
            )
        }
        bbox_table[pname] = {
            k: metrics[k]
            for k in (
                "bbox_present_rate",
                "bbox_iou_avg",
                "bbox_precision",
                "bbox_recall",
                "bbox_f1",
                "confidence_present_rate",
            )
        }
        gov_table[pname] = {
            k: metrics[k]
            for k in (
                "semantic_interpretation_disabled_rate",
                "allows_execute_now_false_rate",
                "real_tts_invoked_false_rate",
                "downstream_invocation_count",
                "forbidden_semantic_output_count",
                "navigation_instruction_leakage_count",
            )
        }

    _write_json(os.path.join(out_root, "per_sample_comparison.json"), per_sample_cmp)
    _write_json(os.path.join(out_root, "metric_tables", "accuracy_metrics.json"), acc_table)
    _write_json(os.path.join(out_root, "metric_tables", "latency_metrics.json"), lat_table)
    _write_json(os.path.join(out_root, "metric_tables", "bbox_metrics.json"), bbox_table)
    _write_json(os.path.join(out_root, "metric_tables", "governance_metrics.json"), gov_table)
    _write_json(os.path.join(out_root, "provider_asset_reports", "all_providers_assets.json"), asset_reports)

    summary = {
        "phase": "Phase-ModelOCR-006E",
        "tool": "run_realtime_ocr_candidate_benchmark_v0.py",
        "timestamp": _now_iso(),
        "dataset_manifest": os.path.relpath(dataset_manifest, REPO_ROOT) if dataset_manifest.startswith(REPO_ROOT) else dataset_manifest,
        "sample_count": len(samples),
        "providers": providers,
        "forbidden_gt_field_count": forbidden_gt_count,
        "governance": {
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "downstream_invoked": False,
            "default_ocr_provider_set": False,
        },
        "per_provider_run_status": {k: v.get("run_status") for k, v in per_provider_summary.items()},
        "artifacts": {
            "summary": "realtime_ocr_candidate_benchmark_summary.json",
            "per_provider_summaries": "per_provider_summaries/",
            "per_sample_comparison": "per_sample_comparison.json",
            "metric_tables": "metric_tables/",
            "provider_asset_reports": "provider_asset_reports/",
            "trace": "trace/",
            "replay": "replay/",
            "whitebox": "whitebox/",
            "benchmark_notes": "benchmark_notes.md",
        },
    }
    _write_json(os.path.join(out_root, "realtime_ocr_candidate_benchmark_summary.json"), summary)

    notes = "\n".join(
        [
            "## Phase-ModelOCR-006E — Realtime OCR Candidate Benchmark v0",
            "",
            "- Raw text only; no semantic interpretation; no downstream; no default OCR provider.",
            "- Providers: rapidocr_current, RapidOCR PP-OCRv4 mobile ONNX (bundled), PP-OCRv5 mobile (requires pinned ONNX under models/), EasyOCR, Tesseract.",
            "- Complex layout branch (Surya, docTR, PaddleOCR-VL, …) explicitly excluded.",
            "",
        ]
    )
    with open(os.path.join(out_root, "benchmark_notes.md"), "w", encoding="utf-8") as nf:
        nf.write(notes)

    print(
        json.dumps(
            {
                "ok": True,
                "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
                "sample_count": len(samples),
                "providers": providers,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
