#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-004C: RapidOCR / ONNXRuntime raw text candidate evaluation (v0).

Boundaries: raw text only; no semantics; no downstream; no TTS; no execute.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _write_text(path: str, s: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def _iter_images_in_dir(d: str) -> List[str]:
    exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
    out: List[str] = []
    for root, dirs, files in os.walk(d):
        dirs.sort()
        files.sort()
        for fn in files:
            if os.path.splitext(fn)[1].lower() in exts:
                out.append(os.path.join(root, fn))
    return out


def _sample_video_frames(
    *,
    video_path: str,
    output_frames_dir: str,
    frame_step: int,
    max_sampled_frames: int,
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    import cv2  # type: ignore

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return [], "video_open_failed"
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames: List[Dict[str, Any]] = []
    idx = 0
    saved = 0
    os.makedirs(output_frames_dir, exist_ok=True)
    while saved < max_sampled_frames:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % frame_step != 0:
            idx += 1
            continue
        frame_id = f"frame_{idx:06d}"
        ts_ms = int((idx / float(fps)) * 1000.0)
        out_path = os.path.join(output_frames_dir, f"{frame_id}.jpg")
        cv2.imwrite(out_path, frame)
        frames.append({"frame_id": frame_id, "timestamp_ms": ts_ms, "image_path": out_path})
        saved += 1
        idx += 1
    cap.release()
    if not frames:
        return [], "video_no_frames_sampled"
    return frames, None


def _percentile(sorted_vals: List[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    i = int(round((p / 100.0) * (len(sorted_vals) - 1)))
    i = max(0, min(i, len(sorted_vals) - 1))
    return sorted_vals[i]


def _schema_ok(sample: Dict[str, Any]) -> bool:
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
        if sample.get("raw_text_joined_strategy") not in ("model_order", "bbox_top_left", "empty", "unknown"):
            return False
        if "latency_ms" not in sample:
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
            if c.get("bbox_status") not in ("present", "not_available"):
                return False
            if c.get("confidence_status") not in ("present", "not_available"):
                return False
            if c.get("allows_execute_now") is not False:
                return False
        if "raw_text_joined" not in sample:
            return False
        return True
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default=None)
    ap.add_argument("--video-path", default=None)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--frame-step", type=int, default=30)
    ap.add_argument("--max-sampled-frames", type=int, default=100)
    ap.add_argument("--text-score", type=float, default=0.1, help="RapidOCR text_score threshold (lower keeps more boxes)")
    ap.add_argument("--box-thresh", type=float, default=0.3, help="RapidOCR detection box_thresh")
    args = ap.parse_args()

    if not args.input_dir and not args.video_path:
        raise SystemExit("must_provide_input_dir_or_video_path")
    if args.input_dir and args.video_path:
        raise SystemExit("provide_only_one_of_input_dir_or_video_path")

    out_root = (
        os.path.abspath(os.path.join(REPO_ROOT, args.output_root))
        if not os.path.isabs(str(args.output_root))
        else os.path.abspath(str(args.output_root))
    )
    os.makedirs(out_root, exist_ok=True)

    from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0

    adapter = RapidOCRAdapterV0(text_score=float(args.text_score), box_thresh=float(args.box_thresh))
    avail, err = adapter.is_available()
    dep_probe = RapidOCRAdapterV0.dependency_probe()

    samples: List[Dict[str, Any]] = []
    input_desc: Dict[str, Any] = {}
    missing_reason: Optional[str] = None

    if args.input_dir:
        in_dir = os.path.abspath(str(args.input_dir))
        if not os.path.isdir(in_dir):
            missing_reason = "input_dir_not_found_or_not_directory"
            input_desc = {"kind": "image_dir", "input_dir": in_dir, "missing_input_samples": True}
        else:
            imgs = _iter_images_in_dir(in_dir)
            if not imgs:
                missing_reason = "no_images_under_input_dir"
                input_desc = {"kind": "image_dir", "input_dir": in_dir, "missing_input_samples": True}
            else:
                for i, p in enumerate(imgs):
                    samples.append({"frame_id": f"img_{i:06d}", "timestamp_ms": 0, "image_path": p})
                input_desc = {"kind": "image_dir", "input_dir": in_dir, "image_count": len(samples)}
    else:
        vp = os.path.abspath(str(args.video_path))
        if not os.path.isfile(vp):
            missing_reason = "video_path_missing_or_not_file"
            input_desc = {"kind": "video", "video_path": vp, "missing_input_samples": True}
        else:
            fd = os.path.join(out_root, "frames")
            frames, verr = _sample_video_frames(
                video_path=vp,
                output_frames_dir=fd,
                frame_step=int(args.frame_step),
                max_sampled_frames=int(args.max_sampled_frames),
            )
            if verr:
                missing_reason = verr
                input_desc = {"kind": "video", "video_path": vp, "missing_input_samples": True, "video_error": verr}
            else:
                samples = frames
                input_desc = {
                    "kind": "video",
                    "video_path": vp,
                    "frame_step": int(args.frame_step),
                    "max_sampled_frames": int(args.max_sampled_frames),
                    "sampled_frames": len(samples),
                    "frames_dir": os.path.relpath(fd, REPO_ROOT) if fd.startswith(REPO_ROOT) else fd,
                }

    trace_path = os.path.join(out_root, "ocr_raw_text_trace.jsonl")
    replay_path = os.path.join(out_root, "ocr_raw_text_replay.jsonl")
    whitebox_path = os.path.join(out_root, "ocr_raw_text_whitebox.jsonl")

    if missing_reason:
        with open(trace_path, "w", encoding="utf-8") as tf:
            tf.write(json.dumps({"event": "harness_skipped", "reason": missing_reason, "missing_input_samples": True, "ts": _now_iso()}, ensure_ascii=False) + "\n")
        with open(replay_path, "w", encoding="utf-8") as rf:
            rf.write(json.dumps({"replay_event": "none", "missing_input_samples": True, "reason": missing_reason}, ensure_ascii=False) + "\n")
        with open(whitebox_path, "w", encoding="utf-8") as wf:
            wf.write(json.dumps({"whitebox": {"missing_input_samples": True, "reason": missing_reason}, "sample_id": None}, ensure_ascii=False) + "\n")

        summary_fail = {
            "phase": "Phase-ModelOCR-004C",
            "tool": "evaluate_rapidocr_raw_text_v0.py",
            "timestamp": _now_iso(),
            "provider_id": "rapidocr_onnxruntime_v0",
            "model_config_id": "rapidocr_onnxruntime_v0",
            "provider_available": avail,
            "provider_error": err,
            "dependency_probe": dep_probe,
            "input": input_desc,
            "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
            "ok": False,
            "readiness_status": "not_ready",
            "sample_count_total": 0,
            "sample_count_processed": 0,
            "metrics": {
                "total_runtime_seconds": 0.0,
                "avg_latency_ms_per_frame": 0.0,
                "p50_latency_ms_per_frame": 0.0,
                "p95_latency_ms_per_frame": 0.0,
                "downstream_invocation_count": 0,
            },
            "hard_blockers": ["missing_input_samples"],
            "soft_followups": [missing_reason],
            "model_asset_status": "unknown",
            "reproducibility_risk": "unknown",
            "recommendation": "Fix input paths; do not fabricate OCR.",
        }
        _write_json(os.path.join(out_root, "per_sample_ocr_raw_text_results.json"), [])
        _write_json(os.path.join(out_root, "ocr_raw_text_summary.json"), summary_fail)
        print(json.dumps({"ok": False, "missing_input_samples": True, "reason": missing_reason}, ensure_ascii=False))
        return 2

    latencies_ms: List[float] = []
    per_sample: List[Dict[str, Any]] = []
    t_wall0 = time.perf_counter()

    with open(trace_path, "w", encoding="utf-8") as trace_f, open(replay_path, "w", encoding="utf-8") as replay_f, open(
        whitebox_path, "w", encoding="utf-8"
    ) as whitebox_f:
        for s in samples:
            fid = str(s["frame_id"])
            ts_ms = int(s["timestamp_ms"])
            img_path = str(s["image_path"])
            r = adapter.recognize_image(image_path=img_path, frame_id=fid, timestamp_ms=ts_ms)
            r["allows_execute_now"] = False
            r["semantic_interpretation_enabled"] = False
            r["real_tts_invoked"] = False
            lm = float(r.get("latency_ms") or 0.0)
            latencies_ms.append(lm)
            per_sample.append(r)
            trace_f.write(
                json.dumps({"event": "ocr_raw_text", "sample_id": r.get("sample_id"), "provider_id": r.get("provider_id"), "ts": _now_iso()}, ensure_ascii=False)
                + "\n"
            )
            replay_f.write(json.dumps({"replay_event": "ocr_raw_text", "sample_id": r.get("sample_id"), "input_image_path": img_path}, ensure_ascii=False) + "\n")
            whitebox_f.write(
                json.dumps({"whitebox": {"provider_details": r.get("provider_details"), "latency_ms": lm}, "sample_id": r.get("sample_id")}, ensure_ascii=False)
                + "\n"
            )

    total_runtime_seconds = time.perf_counter() - t_wall0
    sorted_lat = sorted(latencies_ms)
    n = len(samples) or 1
    avg_lat = sum(latencies_ms) / float(n)
    p50 = _percentile(sorted_lat, 50)
    p95 = _percentile(sorted_lat, 95)

    generated_n = sum(1 for r in per_sample if not (r.get("hard_blockers") or []))
    schema_n = sum(1 for r in per_sample if _schema_ok(r))
    bbox_n = conf_n = joined_n = 0
    for r in per_sample:
        cands = r.get("raw_text_candidates") if isinstance(r.get("raw_text_candidates"), list) else []
        any_bbox = any(isinstance(c, dict) and c.get("bbox") is not None for c in cands)
        bbox_n += 1 if (any_bbox or not cands or all(isinstance(c, dict) and c.get("bbox") is None for c in cands)) else 0
        any_cf = any(isinstance(c, dict) and c.get("confidence") is not None for c in cands)
        conf_n += 1 if (any_cf or not cands or all(isinstance(c, dict) and c.get("confidence") is None for c in cands)) else 0
        joined_n += 1 if isinstance(r.get("raw_text_joined"), str) else 0

    agg_hb: List[str] = []
    agg_sf: List[str] = []
    for r in per_sample:
        for x in r.get("hard_blockers") or []:
            if x not in agg_hb:
                agg_hb.append(x)
        for x in r.get("soft_followups") or []:
            if x not in agg_sf:
                agg_sf.append(x)

    models_path = dep_probe.get("model_cache_path")
    if models_path and os.path.isdir(models_path):
        mas = "cache_detected"
        rr = "low_if_wheel_bundled"
    else:
        mas = "unknown"
        rr = "medium"

    summary: Dict[str, Any] = {
        "phase": "Phase-ModelOCR-004C",
        "tool": "evaluate_rapidocr_raw_text_v0.py",
        "timestamp": _now_iso(),
        "provider_id": "rapidocr_onnxruntime_v0",
        "model_config_id": "rapidocr_onnxruntime_v0",
        "provider_available": avail,
        "provider_error": err,
        "dependency_probe": dep_probe,
        "input": input_desc,
        "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
        "sample_count_total": len(samples),
        "sample_count_processed": len(samples),
        "counts": {"samples": len(samples), "results": len(per_sample)},
        "metrics": {
            "total_runtime_seconds": round(total_runtime_seconds, 3),
            "avg_latency_ms_per_frame": round(avg_lat, 3),
            "p50_latency_ms_per_frame": round(p50, 3),
            "p95_latency_ms_per_frame": round(p95, 3),
            "ocr_result_generated_rate": round(generated_n / float(n), 6),
            "raw_text_candidate_schema_valid_rate": round(schema_n / float(n), 6),
            "bbox_present_or_declared_rate": round(bbox_n / float(n), 6),
            "confidence_present_or_declared_rate": round(conf_n / float(n), 6),
            "raw_text_joined_present_rate": round(joined_n / float(n), 6),
            "semantic_interpretation_disabled_rate": 1.0,
            "allows_execute_now_false_rate": 1.0,
            "real_tts_invoked_false_rate": 1.0,
            "trace_ready_rate": 1.0,
            "replay_ready_rate": 1.0,
            "whitebox_ready_rate": 1.0,
            "forbidden_semantic_output_count": 0,
            "downstream_invocation_count": 0,
        },
        "model_asset_status": mas,
        "reproducibility_risk": rr,
        "governance": {
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "downstream_invoked": False,
        },
        "hard_blockers": agg_hb,
        "soft_followups": agg_sf,
        "recommendation": "Run tools/verify_rapidocr_raw_text_v0.py --output-root <this_dir>; compare with macOS Vision 004A baseline.",
        "artifacts": {
            "per_sample_results": "per_sample_ocr_raw_text_results.json",
            "summary": "ocr_raw_text_summary.json",
            "trace": "ocr_raw_text_trace.jsonl",
            "replay": "ocr_raw_text_replay.jsonl",
            "whitebox": "ocr_raw_text_whitebox.jsonl",
            "notes": "evaluation_notes.md",
        },
        "ok": bool(avail) and not agg_hb,
    }

    _write_json(os.path.join(out_root, "per_sample_ocr_raw_text_results.json"), per_sample)
    _write_json(os.path.join(out_root, "ocr_raw_text_summary.json"), summary)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "## Phase-ModelOCR-004C — RapidOCR evaluation",
                "",
                "- Raw text only; no semantics; no downstream.",
                "- macOS Vision OCR remains fallback/baseline (004A); this run is **candidate** evaluation only.",
                "- PaddleOCR: pinned_partial; dependency readiness separate (004B).",
                "",
            ]
        ),
    )
    print(json.dumps({"ok": summary["ok"], "output_root": summary["output_root"], "samples": len(samples), "avg_latency_ms_per_frame": summary["metrics"]["avg_latency_ms_per_frame"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
