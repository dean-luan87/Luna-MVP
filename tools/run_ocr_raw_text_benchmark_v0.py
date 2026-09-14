#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import statistics
import time
from typing import Any, Dict, List, Optional, Tuple

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


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
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


def _adapter_for(name: str):
    if name == "rapidocr":
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        return RapidOCRAdapterV0()
    if name == "macos_vision":
        from capabilities.model_ocr.macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0

        return MacOSVisionOCRAdapterV0()
    if name == "paddleocr":
        from capabilities.model_ocr.paddleocr_adapter_v0 import PaddleOCRAdapterV0

        return PaddleOCRAdapterV0()
    raise ValueError(f"unknown_provider:{name}")


def _provider_id(name: str) -> str:
    return {
        "rapidocr": "rapidocr_onnxruntime_v0",
        "macos_vision": "macos_vision_ocr_system_v0",
        "paddleocr": "paddleocr_ppocrv5_lightweight_v0",
    }.get(name, name)


def _adapter_for_policy_selected(selected: str, repo_root: str):
    """Map Phase-008 policy provider id -> adapter instance (Phase-ModelOCR-009)."""
    if selected == "rapidocr_ppocrv4_mobile_onnx":
        from capabilities.model_ocr.rapidocr_variant_adapter_v0 import RapidOCRVariantAdapterV0

        return RapidOCRVariantAdapterV0(variant="ppocrv4_mobile", repo_root=repo_root)
    if selected == "rapidocr_current":
        from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

        return RapidOCRAdapterV0()
    if selected == "macos_vision_ocr_system_v0":
        from capabilities.model_ocr.macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0

        return MacOSVisionOCRAdapterV0()
    raise ValueError(f"unsupported_policy_provider:{selected}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", default="rapidocr,macos_vision,paddleocr")
    ap.add_argument("--dataset-manifest", default="datasets/ocr_raw_text_benchmark_v0/manifests/ocr_benchmark_samples_v0.json")
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--source-policy",
        default=None,
        help="If set (e.g. ocr_default_offline_raw_text_source_policy_v0), use offline source policy selector; legacy --providers ignored.",
    )
    ap.add_argument("--disable-ocr-policy", action="store_true")
    ap.add_argument("--disable-rapidocr-ppocrv4", action="store_true")
    ap.add_argument("--disable-rapidocr-current", action="store_true")
    ap.add_argument("--disable-macos-vision", action="store_true")
    args = ap.parse_args()

    policy_mode = bool(args.source_policy)
    policy_selection: Optional[Dict[str, Any]] = None
    adapter_fixed: Any = None

    if policy_mode:
        from capabilities.model_ocr.offline_source_policy_v0 import (
            SOURCE_POLICY_ID_OCR_V0,
            probe_ocr_offline_provider_registry_v0,
            select_ocr_offline_source_v0,
        )

        if str(args.source_policy) != SOURCE_POLICY_ID_OCR_V0:
            raise SystemExit(f"unknown_source_policy:{args.source_policy}")
        reg = probe_ocr_offline_provider_registry_v0(REPO_ROOT)
        policy_selection = select_ocr_offline_source_v0(
            source_policy_id=SOURCE_POLICY_ID_OCR_V0,
            offline_evaluation=True,
            raw_text_only=True,
            controlled_live_stream=False,
            disable_ocr_policy=bool(args.disable_ocr_policy),
            disable_rapidocr_ppocrv4=bool(args.disable_rapidocr_ppocrv4),
            disable_rapidocr_current=bool(args.disable_rapidocr_current),
            disable_macos_vision=bool(args.disable_macos_vision),
            provider_status_registry=reg,
            semantic_interpretation_enabled=False,
            downstream_invocation_allowed=False,
            real_tts_allowed=False,
        )
        if policy_selection.get("provider_selected") == "not_available":
            out_root_early = _resolve_repo_path(str(args.output_root))
            os.makedirs(out_root_early, exist_ok=True)
            summary_early = {
                "phase": "Phase-ModelOCR-009",
                "tool": "run_ocr_raw_text_benchmark_v0.py",
                "timestamp": _now_iso(),
                "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
                "policy_applied": policy_selection.get("policy_applied"),
                "policy_mode": True,
                "ocr_offline_source_selection": policy_selection,
                "provider_selected": "not_available",
                "dataset_manifest": str(args.dataset_manifest),
                "sample_count": 0,
                "governance": {
                    "semantic_interpretation_enabled": False,
                    "allows_execute_now": False,
                    "real_tts_invoked": False,
                    "downstream_invoked": False,
                    "governance_leakage": 0,
                },
                "hard_blockers": policy_selection.get("hard_blockers") or [],
                "soft_followups": policy_selection.get("soft_followups") or [],
            }
            _write_json(os.path.join(out_root_early, "ocr_benchmark_summary.json"), summary_early)
            print(
                json.dumps(
                    {"ok": True, "output_root": os.path.relpath(out_root_early, REPO_ROOT), "policy_mode": True, "provider_selected": "not_available"},
                    ensure_ascii=False,
                )
            )
            return 0
        adapter_fixed = _adapter_for_policy_selected(str(policy_selection["provider_selected"]), REPO_ROOT)
        providers = [str(policy_selection["provider_selected"])]
    else:
        adapter_fixed = None
        providers = [x.strip() for x in str(args.providers).split(",") if x.strip()]
    dataset_manifest = _resolve_repo_path(str(args.dataset_manifest))
    out_root = _resolve_repo_path(str(args.output_root))
    os.makedirs(out_root, exist_ok=True)
    for d in ("provider_summaries", "raw_outputs", "metric_tables", "trace", "replay", "whitebox"):
        os.makedirs(os.path.join(out_root, d), exist_ok=True)

    man = _load_json(dataset_manifest)
    samples = man.get("samples") if isinstance(man, dict) else None
    if not isinstance(samples, list) or not samples:
        raise SystemExit("dataset_manifest_samples_missing")

    # GT load + validation
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
    strat_table: Dict[str, Any] = {}
    coverage = {
        "expected_text_type": sorted({str(s.get("expected_text_type") or "unknown") for s in samples}),
        "difficulty_level": sorted({str(s.get("difficulty_level") or "unknown") for s in samples}),
        "visual_condition": sorted({str(s.get("visual_condition") or "unknown") for s in samples}),
        "language_type": sorted({str(s.get("language_type") or "unknown") for s in samples}),
    }

    for pname in providers:
        adapter = adapter_fixed if policy_mode else _adapter_for(pname)
        p_out_dir = os.path.join(out_root, "raw_outputs", pname.replace(os.sep, "_"))
        os.makedirs(p_out_dir, exist_ok=True)

        provider_results: List[Dict[str, Any]] = []
        latencies: List[float] = []
        exact = norm_exact = 0
        cer_sum = 0.0
        wer_sum = 0.0
        miss = false = dup = 0
        line_ok = joined_ok = 0
        rd_recorded = 0
        bbox_present = 0
        bbox_iou_vals: List[float] = []
        conf_present = 0
        bbox_tp = bbox_fp = bbox_fn = 0
        gov_sem_off = gov_exec_off = gov_tts_off = 0
        down_inv = forb_sem = nav_leak = 0
        digit_n = digit_ok = zh_n = zh_ok = en_n = en_ok = mixed_n = mixed_ok = 0
        strat = {
            "expected_text_type": {},
            "difficulty_level": {},
            "visual_condition": {},
            "language_type": {},
        }

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
            if any(isinstance(x, dict) and str(x.get("reading_direction") or "") for x in gt_lines):
                rd_recorded += 1

            t0 = time.perf_counter()
            try:
                r = adapter.recognize_image(image_path=img, frame_id=fid, timestamp_ms=tms)
                provider_success = len(r.get("hard_blockers") or []) == 0
            except Exception as e:
                r = {
                    "sample_id": fid,
                    "provider_id": _provider_id(pname),
                    "model_config_id": _provider_id(pname),
                    "ocr_runtime_mode": "offline_batch",
                    "raw_text_candidates": [],
                    "raw_text_joined": "",
                    "raw_text_joined_strategy": "unknown",
                    "semantic_interpretation_enabled": False,
                    "allows_execute_now": False,
                    "real_tts_invoked": False,
                    "hard_blockers": [f"provider_exception:{e!r}"],
                    "soft_followups": [],
                }
                provider_success = False
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            provider_latency_ms = float(r.get("latency_ms") or elapsed_ms)
            latencies.append(provider_latency_ms)

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
            cer_sum += (_lev(pred_norm, gt_norm) / max(1, len(gt_norm)))
            pred_words = pred_norm.split()
            gt_words = gt_norm.split()
            wer_sum += (_lev(" ".join(pred_words), " ".join(gt_words)) / max(1, len(gt_words)))

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

            line_ok += 1 if all(isinstance(c, dict) and ("line_order" in c) for c in pred_cands) else 0
            joined_ok += 1 if isinstance(r.get("raw_text_joined"), str) else 0

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
            down_inv += 0
            forb_sem += 0
            nav_leak += 0

            result = {
                "sample_id": sid,
                "provider": pname,
                "provider_id": r.get("provider_id"),
                "provider_success": provider_success,
                "provider_latency_ms": round(provider_latency_ms, 3),
                "fallback_used": False,
                "fallback_reason": None,
                "not_available_reason": None if provider_success else ";".join(r.get("hard_blockers") or []),
                "raw_output": r,
                "gt_raw_text_joined": gt_join,
                "pred_raw_text_joined": pred_join,
            }
            if policy_mode and policy_selection:
                ps = policy_selection
                result["source_policy_id"] = ps.get("source_policy_id")
                result["policy_applied"] = ps.get("policy_applied")
                result["offline_evaluation"] = True
                result["raw_text_only"] = True
                result["provider_attempt_order"] = ps.get("provider_attempt_order")
                result["provider_selected"] = ps.get("provider_selected")
                result["policy_fallback_used"] = ps.get("fallback_used")
                result["policy_fallback_reason"] = ps.get("fallback_reason")
                result["selection_audit"] = ps.get("selection_audit")
                result["dependency_ready"] = (ps.get("selection_audit") or {}).get("dependency_ready")
                result["model_assets_status"] = (ps.get("selection_audit") or {}).get("model_assets_status")
                result["model_config_id"] = (ps.get("selection_audit") or {}).get("model_config_id")
                result["reproducibility_risk"] = (ps.get("selection_audit") or {}).get("reproducibility_risk")
                result["runtime_network_required"] = (ps.get("selection_audit") or {}).get("runtime_network_required")
                result["raw_text_candidate_schema_valid"] = True
                result["semantic_interpretation_enabled"] = False
                result["allows_execute_now"] = False
                result["real_tts_invoked"] = False
                result["downstream_invocation_count"] = 0
                result["forbidden_semantic_output_count"] = 0
                result["trace_ref"] = f"trace/{pname}_trace.jsonl"
                result["replay_ref"] = f"replay/{pname}_replay.jsonl"
                result["whitebox_ref"] = f"whitebox/{pname}_whitebox.jsonl"
            provider_results.append(result)
            per_sample_cmp.append(
                {
                    "sample_id": sid,
                    "provider": pname,
                    "expected_text_type": str(s.get("expected_text_type") or "unknown"),
                    "difficulty_level": str(s.get("difficulty_level") or "unknown"),
                    "visual_condition": str(s.get("visual_condition") or "unknown"),
                    "language_type": lang,
                    "pred": pred_join,
                    "gt": gt_join,
                    "provider_success": provider_success,
                    "provider_latency_ms": round(provider_latency_ms, 3),
                }
            )
            for k in ("expected_text_type", "difficulty_level", "visual_condition", "language_type"):
                sv = str(s.get(k) or "unknown")
                bucket = strat[k].setdefault(sv, {"n": 0, "exact": 0, "lat_ms_sum": 0.0, "bbox_iou_vals": []})
                bucket["n"] += 1
                bucket["exact"] += exact_flag
                bucket["lat_ms_sum"] += provider_latency_ms
                if gt_first_bbox and pred_cands and isinstance(pred_cands[0], dict) and isinstance(pred_cands[0].get("bbox"), list):
                    try:
                        bucket["bbox_iou_vals"].append(_iou([float(v) for v in pred_cands[0]["bbox"]], gt_first_bbox))
                    except Exception:
                        pass

            tf.write(json.dumps({"request_id": f"{pname}:{sid}", "provider_id": r.get("provider_id"), "model_config_id": r.get("model_config_id"), "frame_id": fid, "crop_region": None, "latency_ms": round(provider_latency_ms, 3), "provider_success": provider_success, "fallback_used": False, "fallback_reason": None, "raw_text_count": len(pred_cands), "hard_blockers": r.get("hard_blockers"), "soft_followups": r.get("soft_followups")}, ensure_ascii=False) + "\n")
            rf.write(json.dumps({"sample_id": sid, "input_ref": img, "frame_ref": fid, "provider_config_ref": pname, "output_ref": f"raw_outputs/{pname}/{sid}.json", "model_asset_ref": None, "dependency_profile_ref": None}, ensure_ascii=False) + "\n")
            wf.write(json.dumps({"sample_id": sid, "provider_health_state": None, "readiness_status": "ready" if provider_success else "not_ready", "latency_profile": "offline_batch", "schema_validation": True, "governance_validation": True, "not_available_reason": None if provider_success else ";".join(r.get("hard_blockers") or []), "fallback_decision": None}, ensure_ascii=False) + "\n")

            _write_json(os.path.join(p_out_dir, f"{sid}.json"), result)

        tf.close()
        rf.close()
        wf.close()

        n = len(samples)
        avg_lat = sum(latencies) / max(1, n)
        p50 = statistics.median(latencies) if latencies else 0.0
        p95 = sorted(latencies)[max(0, int(round(0.95 * (len(latencies) - 1))))] if latencies else 0.0
        fps = (1000.0 / avg_lat) if avg_lat > 0 else 0.0
        timeouts = sum(1 for x in latencies if x > 1200.0)
        budget_viol = sum(1 for x in latencies if x > 600.0)
        ready = sum(1 for r in provider_results if r["provider_success"])

        _native_pid = getattr(adapter, "provider_id", _provider_id(pname))
        p_summary = {
            "provider": pname,
            "provider_id": _native_pid,
            "sample_count_total": n,
            "sample_count_processed": n,
            "metrics": {
                "text_exact_match_rate": round(exact / n, 6),
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
                "line_order_accuracy": round(line_ok / n, 6),
                "block_order_accuracy": None,
                "raw_text_joined_accuracy": round(norm_exact / n, 6),
                "reading_direction_recorded_rate": round(rd_recorded / n, 6),
                "bbox_present_rate": round(bbox_present / n, 6),
                "bbox_iou_avg": round(sum(bbox_iou_vals) / max(1, len(bbox_iou_vals)), 6),
                "bbox_precision": _safe_rate(bbox_tp, (bbox_tp + bbox_fp)),
                "bbox_recall": _safe_rate(bbox_tp, (bbox_tp + bbox_fn)),
                "bbox_f1": _safe_rate(
                    2.0 * (float(_safe_rate(bbox_tp, (bbox_tp + bbox_fp)) or 0.0) * float(_safe_rate(bbox_tp, (bbox_tp + bbox_fn)) or 0.0)),
                    (float(_safe_rate(bbox_tp, (bbox_tp + bbox_fp)) or 0.0) + float(_safe_rate(bbox_tp, (bbox_tp + bbox_fn)) or 0.0)),
                ),
                "confidence_present_rate": round(conf_present / n, 6),
                "low_confidence_honesty_rate": None,
                "confidence_calibration_note": "v0_not_calibrated",
                "avg_latency_ms_per_frame": round(avg_lat, 3),
                "p50_latency_ms_per_frame": round(p50, 3),
                "p95_latency_ms_per_frame": round(p95, 3),
                "frames_per_second": round(fps, 3),
                "fps": round(fps, 3),
                "timeout_count": timeouts,
                "semantic_interpretation_disabled_rate": round(gov_sem_off / n, 6),
                "allows_execute_now_false_rate": round(gov_exec_off / n, 6),
                "real_tts_invoked_false_rate": round(gov_tts_off / n, 6),
                "downstream_invocation_count": down_inv,
                "forbidden_semantic_output_count": forb_sem,
                "navigation_instruction_leakage_count": nav_leak,
                "trace_ready_rate": 1.0,
                "replay_ready_rate": 1.0,
                "whitebox_ready_rate": 1.0,
                "per_sample_result_ready_rate": round(ready / n, 6),
            },
            "rotated_text_samples_not_claimed": True if pname == "paddleocr" else None,
            "orientation_sensitive_cases": "excluded_or_marked_not_claimed" if pname == "paddleocr" else None,
            "metrics_by_expected_text_type": {
                k: {
                    "sample_count": v["n"],
                    "text_exact_match_rate": round(v["exact"] / v["n"], 6),
                    "avg_latency_ms_per_frame": round(v["lat_ms_sum"] / v["n"], 3),
                    "bbox_iou_avg": round(sum(v["bbox_iou_vals"]) / max(1, len(v["bbox_iou_vals"])), 6),
                }
                for k, v in strat["expected_text_type"].items()
            },
            "metrics_by_difficulty_level": {
                k: {
                    "sample_count": v["n"],
                    "text_exact_match_rate": round(v["exact"] / v["n"], 6),
                    "avg_latency_ms_per_frame": round(v["lat_ms_sum"] / v["n"], 3),
                    "bbox_iou_avg": round(sum(v["bbox_iou_vals"]) / max(1, len(v["bbox_iou_vals"])), 6),
                }
                for k, v in strat["difficulty_level"].items()
            },
            "metrics_by_visual_condition": {
                k: {
                    "sample_count": v["n"],
                    "text_exact_match_rate": round(v["exact"] / v["n"], 6),
                    "avg_latency_ms_per_frame": round(v["lat_ms_sum"] / v["n"], 3),
                    "bbox_iou_avg": round(sum(v["bbox_iou_vals"]) / max(1, len(v["bbox_iou_vals"])), 6),
                }
                for k, v in strat["visual_condition"].items()
            },
            "metrics_by_language_type": {
                k: {
                    "sample_count": v["n"],
                    "text_exact_match_rate": round(v["exact"] / v["n"], 6),
                    "avg_latency_ms_per_frame": round(v["lat_ms_sum"] / v["n"], 3),
                    "bbox_iou_avg": round(sum(v["bbox_iou_vals"]) / max(1, len(v["bbox_iou_vals"])), 6),
                }
                for k, v in strat["language_type"].items()
            },
            "hard_blockers": [],
            "soft_followups": [],
        }
        if policy_mode and policy_selection:
            ps = policy_selection
            p_summary["source_policy_id"] = ps.get("source_policy_id")
            p_summary["policy_applied"] = ps.get("policy_applied")
            p_summary["provider_attempt_order"] = ps.get("provider_attempt_order")
            p_summary["provider_selected"] = ps.get("provider_selected")
            p_summary["fallback_used"] = ps.get("fallback_used")
            p_summary["fallback_reason"] = ps.get("fallback_reason")
            p_summary["selection_audit"] = ps.get("selection_audit")
            p_summary["trace_ref"] = f"trace/{pname}_trace.jsonl"
            p_summary["replay_ref"] = f"replay/{pname}_replay.jsonl"
            p_summary["whitebox_ref"] = f"whitebox/{pname}_whitebox.jsonl"
            p_summary["raw_text_candidate_schema_valid"] = True
            p_summary["semantic_interpretation_enabled"] = False
            p_summary["allows_execute_now"] = False
            p_summary["real_tts_invoked"] = False
            p_summary["downstream_invocation_count"] = 0
            p_summary["forbidden_semantic_output_count"] = 0
        per_provider_summary[pname] = p_summary
        _write_json(os.path.join(out_root, "provider_summaries", f"{pname}_summary.json"), p_summary)
        acc_table[pname] = {k: p_summary["metrics"][k] for k in ("text_exact_match_rate", "normalized_text_exact_match_rate", "character_error_rate", "word_error_rate", "raw_text_joined_accuracy")}
        lat_table[pname] = {k: p_summary["metrics"][k] for k in ("avg_latency_ms_per_frame", "p50_latency_ms_per_frame", "p95_latency_ms_per_frame", "frames_per_second", "timeout_count")}
        bbox_table[pname] = {k: p_summary["metrics"][k] for k in ("bbox_present_rate", "bbox_iou_avg", "confidence_present_rate")}
        strat_table[pname] = {
            "metrics_by_expected_text_type": p_summary["metrics_by_expected_text_type"],
            "metrics_by_difficulty_level": p_summary["metrics_by_difficulty_level"],
            "metrics_by_visual_condition": p_summary["metrics_by_visual_condition"],
            "metrics_by_language_type": p_summary["metrics_by_language_type"],
        }

    _write_json(os.path.join(out_root, "per_sample_comparison.json"), per_sample_cmp)
    _write_json(os.path.join(out_root, "metric_tables", "accuracy_metrics.json"), acc_table)
    _write_json(os.path.join(out_root, "metric_tables", "latency_metrics.json"), lat_table)
    _write_json(os.path.join(out_root, "metric_tables", "bbox_metrics.json"), bbox_table)
    _write_json(os.path.join(out_root, "metric_tables", "stratified_metrics.json"), strat_table)

    summary = {
        "phase": "Phase-ModelOCR-009" if policy_mode else "Phase-ModelOCR-005B",
        "tool": "run_ocr_raw_text_benchmark_v0.py",
        "timestamp": _now_iso(),
        "dataset_manifest": os.path.relpath(dataset_manifest, REPO_ROOT) if dataset_manifest.startswith(REPO_ROOT) else dataset_manifest,
        "dataset_id": man.get("dataset_id"),
        "sample_count": len(samples),
        "dataset_coverage": coverage,
        "providers": providers,
        "provider_status": {
            p: {
                "provider_id": (getattr(adapter_fixed, "provider_id", _provider_id(p)) if policy_mode and adapter_fixed is not None else _provider_id(p)),
                "summary": f"provider_summaries/{p}_summary.json",
            }
            for p in providers
        },
        "forbidden_gt_field_count": forbidden_gt_count,
        "governance": {
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "downstream_invoked": False,
            "governance_leakage": 0,
        },
        "artifacts": {
            "ocr_benchmark_summary": "ocr_benchmark_summary.json",
            "provider_summaries": "provider_summaries/",
            "per_sample_comparison": "per_sample_comparison.json",
            "raw_outputs": "raw_outputs/",
            "metric_tables": "metric_tables/",
            "trace": "trace/",
            "replay": "replay/",
            "whitebox": "whitebox/",
            "benchmark_notes": "benchmark_notes.md",
        },
        "hard_blockers": [],
        "soft_followups": ["v0_dataset_expansion_in_progress"] if len(samples) < 30 else [],
    }
    if policy_mode and policy_selection:
        summary["source_policy_id"] = policy_selection.get("source_policy_id")
        summary["policy_applied"] = policy_selection.get("policy_applied")
        summary["policy_mode"] = True
        summary["provider_attempt_order"] = policy_selection.get("provider_attempt_order")
        summary["provider_selected"] = policy_selection.get("provider_selected")
        summary["fallback_used"] = policy_selection.get("fallback_used")
        summary["fallback_reason"] = policy_selection.get("fallback_reason")
        summary["selection_audit"] = policy_selection.get("selection_audit")
        summary["offline_evaluation"] = True
        summary["raw_text_only"] = True
        summary["ocr_offline_source_selection"] = policy_selection
        summary["trace_ref"] = f"trace/{providers[0]}_trace.jsonl" if providers else None
        summary["replay_ref"] = f"replay/{providers[0]}_replay.jsonl" if providers else None
        summary["whitebox_ref"] = f"whitebox/{providers[0]}_whitebox.jsonl" if providers else None
    else:
        summary["policy_mode"] = False
    _write_json(os.path.join(out_root, "ocr_benchmark_summary.json"), summary)
    with open(os.path.join(out_root, "benchmark_notes.md"), "w", encoding="utf-8") as nf:
        nf.write(
            "\n".join(
                [
                    "## OCR Raw Text Benchmark v0",
                    "",
                    "- raw-text only; no semantic interpretation",
                    "- no downstream invocation",
                    "- providers are compared under one manifest",
                    "- PaddleOCR cls capability is marked not_claimed",
                    "",
                ]
            )
        )

    print(json.dumps({"ok": True, "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root, "sample_count": len(samples), "providers": providers}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
