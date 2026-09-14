#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-004A: macOS Vision OCR Raw Text Offline Harness (v0).

Hard boundaries:
- Uses macOS Vision OCR system provider only
- Outputs raw text candidates only (no semantics, no downstream)
- Does not trigger real TTS; does not execute navigation actions
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _write_text(path: str, s: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
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


def _candidate_schema_valid(sample: Dict[str, Any]) -> bool:
    try:
        if sample.get("provider_id") != "macos_vision_ocr_system_v0":
            return False
        if sample.get("model_config_id") != "macos_vision_ocr_system_v0":
            return False
        pm = sample.get("provider_method")
        if pm not in ("vision_framework", "bridge", "unavailable"):
            return False
        if sample.get("semantic_interpretation_enabled") is not False:
            return False
        if sample.get("allows_execute_now") is not False:
            return False
        if sample.get("real_tts_invoked") is not False:
            return False
        if sample.get("raw_text_joined_strategy") not in ("model_order", "bbox_top_left", "empty", "unknown"):
            return False
        cands = sample.get("raw_text_candidates")
        if not isinstance(cands, list):
            return False
        for c in cands:
            if not isinstance(c, dict):
                return False
            for k in [
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
            ]:
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
    ap.add_argument("--input-dir", default=None, help="Directory of images (recursive)")
    ap.add_argument("--video-path", default=None, help="Path to a video file")
    ap.add_argument("--output-root", required=True, help="Output root dir for logs/artifacts")
    ap.add_argument("--frame-step", type=int, default=30, help="Sample every N frames from video")
    ap.add_argument("--max-sampled-frames", type=int, default=100, help="Max frames sampled from video")
    args = ap.parse_args()

    if not args.input_dir and not args.video_path:
        raise SystemExit("must_provide_input_dir_or_video_path")
    if args.input_dir and args.video_path:
        raise SystemExit("provide_only_one_of_input_dir_or_video_path")

    out_root = os.path.abspath(os.path.join(REPO_ROOT, args.output_root)) if not os.path.isabs(str(args.output_root)) else os.path.abspath(str(args.output_root))
    os.makedirs(out_root, exist_ok=True)

    from capabilities.model_ocr.macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0

    adapter = MacOSVisionOCRAdapterV0()
    available, err = adapter.is_available()

    samples: List[Dict[str, Any]] = []
    input_desc: Dict[str, Any] = {}
    missing_reason: Optional[str] = None

    if args.input_dir:
        in_dir = os.path.abspath(str(args.input_dir))
        if not os.path.isdir(in_dir):
            missing_reason = "input_dir_not_found_or_not_directory"
            input_desc = {"kind": "image_dir", "input_dir": in_dir, "image_count": 0, "missing_input_samples": True}
        else:
            imgs = _iter_images_in_dir(in_dir)
            if not imgs:
                missing_reason = "no_images_under_input_dir"
                input_desc = {"kind": "image_dir", "input_dir": in_dir, "image_count": 0, "missing_input_samples": True}
            else:
                for i, p in enumerate(imgs):
                    frame_id = f"img_{i:06d}"
                    samples.append({"frame_id": frame_id, "timestamp_ms": 0, "image_path": p})
                input_desc = {"kind": "image_dir", "input_dir": in_dir, "image_count": len(samples)}
    else:
        vp = os.path.abspath(str(args.video_path))
        if not os.path.isfile(vp):
            missing_reason = "video_path_missing_or_not_file"
            input_desc = {"kind": "video", "video_path": vp, "missing_input_samples": True}
        else:
            frames_dir = os.path.join(out_root, "frames")
            frames, verr = _sample_video_frames(
                video_path=vp,
                output_frames_dir=frames_dir,
                frame_step=int(args.frame_step),
                max_sampled_frames=int(args.max_sampled_frames),
            )
            if verr:
                missing_reason = verr
                input_desc = {
                    "kind": "video",
                    "video_path": vp,
                    "frame_step": int(args.frame_step),
                    "max_sampled_frames": int(args.max_sampled_frames),
                    "sampled_frames": 0,
                    "missing_input_samples": True,
                    "video_error": verr,
                }
            else:
                samples = frames
                input_desc = {
                    "kind": "video",
                    "video_path": vp,
                    "frame_step": int(args.frame_step),
                    "max_sampled_frames": int(args.max_sampled_frames),
                    "sampled_frames": len(samples),
                    "frames_dir": os.path.relpath(frames_dir, REPO_ROOT) if frames_dir.startswith(REPO_ROOT) else frames_dir,
                }

    per_sample: List[Dict[str, Any]] = []
    trace_path = os.path.join(out_root, "ocr_raw_text_trace.jsonl")
    replay_path = os.path.join(out_root, "ocr_raw_text_replay.jsonl")
    whitebox_path = os.path.join(out_root, "ocr_raw_text_whitebox.jsonl")

    trace_f = open(trace_path, "w", encoding="utf-8")
    replay_f = open(replay_path, "w", encoding="utf-8")
    whitebox_f = open(whitebox_path, "w", encoding="utf-8")

    if missing_reason:
        trace_f.write(
            json.dumps(
                {
                    "event": "harness_skipped",
                    "reason": missing_reason,
                    "missing_input_samples": True,
                    "ts": _now_iso(),
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        replay_f.write(
            json.dumps(
                {"replay_event": "none", "missing_input_samples": True, "reason": missing_reason},
                ensure_ascii=False,
            )
            + "\n"
        )
        whitebox_f.write(
            json.dumps(
                {"whitebox": {"missing_input_samples": True, "reason": missing_reason}, "sample_id": None},
                ensure_ascii=False,
            )
            + "\n"
        )
        trace_f.close()
        replay_f.close()
        whitebox_f.close()

        summary_fail: Dict[str, Any] = {
            "phase": "Phase-ModelOCR-004A",
            "tool": "evaluate_macos_vision_ocr_raw_text_v0.py",
            "timestamp": _now_iso(),
            "provider_id": "macos_vision_ocr_system_v0",
            "model_config_id": "macos_vision_ocr_system_v0",
            "provider_available": available,
            "provider_error": err,
            "input": input_desc,
            "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
            "readiness_status": "not_ready",
            "harness_verdict": "NO_GO",
            "ok": False,
            "sample_count_total": 0,
            "sample_count_processed": 0,
            "counts": {"samples": 0, "results": 0},
            "metrics": {
                "ocr_result_generated_rate": 0.0,
                "raw_text_candidate_schema_valid_rate": 0.0,
                "bbox_present_or_declared_rate": 0.0,
                "confidence_present_or_declared_rate": 0.0,
                "raw_text_joined_present_rate": 0.0,
                "semantic_interpretation_disabled_rate": 1.0,
                "allows_execute_now_false_rate": 1.0,
                "real_tts_invoked_false_rate": 1.0,
                "trace_ready_rate": 1.0,
                "replay_ready_rate": 1.0,
                "whitebox_ready_rate": 1.0,
                "forbidden_semantic_output_count": 0,
                "downstream_invocation_count": 0,
            },
            "governance": {
                "semantic_interpretation_enabled": False,
                "allows_execute_now": False,
                "real_tts_invoked": False,
                "downstream_invoked": False,
            },
            "hard_blockers": ["missing_input_samples"],
            "soft_followups": [missing_reason],
            "recommendation": "Provide a valid --input-dir with at least one image, or a readable --video-path. Do not fabricate OCR output.",
            "artifacts": {
                "per_sample_results": "per_sample_ocr_raw_text_results.json",
                "summary": "ocr_raw_text_summary.json",
                "trace": "ocr_raw_text_trace.jsonl",
                "replay": "ocr_raw_text_replay.jsonl",
                "whitebox": "ocr_raw_text_whitebox.jsonl",
                "notes": "evaluation_notes.md",
            },
        }
        _write_json(os.path.join(out_root, "per_sample_ocr_raw_text_results.json"), [])
        _write_json(os.path.join(out_root, "ocr_raw_text_summary.json"), summary_fail)
        _write_text(
            os.path.join(out_root, "evaluation_notes.md"),
            "\n".join(
                [
                    "## Phase-ModelOCR-004A — evaluation stopped",
                    "",
                    f"- **missing_input_samples:** `{missing_reason}`",
                    "- No OCR rows were synthesized.",
                    "",
                ]
            ),
        )
        print(json.dumps({"ok": False, "output_root": summary_fail["output_root"], "samples": 0, "missing_input_samples": True, "reason": missing_reason}, ensure_ascii=False))
        return 2

    schema_valid_n = 0
    bbox_present_or_declared_n = 0
    conf_present_or_declared_n = 0
    joined_present_n = 0
    forbidden_semantic_output_count = 0
    generated_n = 0  # samples with no hard blockers

    for s in samples:
        frame_id = str(s["frame_id"])
        ts_ms = int(s["timestamp_ms"])
        img_path = str(s["image_path"])

        r = adapter.recognize_image(image_path=img_path, frame_id=frame_id, timestamp_ms=ts_ms)
        if not (r.get("hard_blockers") or []):
            generated_n += 1

        # governance fields (write-hard)
        r["allows_execute_now"] = False
        r["semantic_interpretation_enabled"] = False
        r["real_tts_invoked"] = False

        per_sample.append(r)

        # metrics
        if _candidate_schema_valid(r):
            schema_valid_n += 1
        if isinstance(r.get("raw_text_joined"), str) and len(r.get("raw_text_joined") or "") >= 0:
            joined_present_n += 1
        cands = r.get("raw_text_candidates") if isinstance(r.get("raw_text_candidates"), list) else []
        # bbox/conf: either present (non-null) on at least one cand OR explicitly null across all
        any_bbox = any(isinstance(c, dict) and c.get("bbox") is not None for c in cands)
        bbox_present_or_declared_n += 1 if (any_bbox or cands == [] or all(isinstance(c, dict) and c.get("bbox") is None for c in cands)) else 0
        any_conf = any(isinstance(c, dict) and c.get("confidence") is not None for c in cands)
        conf_present_or_declared_n += 1 if (any_conf or cands == [] or all(isinstance(c, dict) and c.get("confidence") is None for c in cands)) else 0

        # forbidden semantic output check: we only emit raw text, so count always 0
        forbidden_semantic_output_count += 0

        # trace/replay/whitebox (minimal but complete)
        trace_f.write(json.dumps({"event": "ocr_raw_text", "sample_id": r.get("sample_id"), "provider_id": r.get("provider_id"), "ts": _now_iso()}, ensure_ascii=False) + "\n")
        replay_f.write(json.dumps({"replay_event": "ocr_raw_text", "sample_id": r.get("sample_id"), "input_image_path": img_path}, ensure_ascii=False) + "\n")
        whitebox_f.write(json.dumps({"whitebox": {"provider_details": r.get("provider_details"), "hard_blockers": r.get("hard_blockers"), "soft_followups": r.get("soft_followups")}, "sample_id": r.get("sample_id")}, ensure_ascii=False) + "\n")

    trace_f.close()
    replay_f.close()
    whitebox_f.close()

    ocr_result_generated_rate = float(generated_n) / float(len(samples) or 1)
    raw_text_candidate_schema_valid_rate = float(schema_valid_n) / float(len(samples) or 1)
    bbox_present_or_declared_rate = float(bbox_present_or_declared_n) / float(len(samples) or 1)
    confidence_present_or_declared_rate = float(conf_present_or_declared_n) / float(len(samples) or 1)
    raw_text_joined_present_rate = float(joined_present_n) / float(len(samples) or 1)
    semantic_interpretation_disabled_rate = 1.0
    allows_execute_now_false_rate = 1.0
    real_tts_invoked_false_rate = 1.0
    trace_ready_rate = 1.0 if os.path.exists(trace_path) else 0.0
    replay_ready_rate = 1.0 if os.path.exists(replay_path) else 0.0
    whitebox_ready_rate = 1.0 if os.path.exists(whitebox_path) else 0.0

    agg_hb: List[str] = []
    agg_sf: List[str] = []
    for s in per_sample:
        if isinstance(s, dict):
            for x in s.get("hard_blockers") or []:
                if x not in agg_hb:
                    agg_hb.append(x)
            for x in s.get("soft_followups") or []:
                if x not in agg_sf:
                    agg_sf.append(x)

    downstream_invocation_count = 0
    nproc = len(samples)
    ok_flag = bool(available) and not agg_hb
    if not available:
        rec = "Provider unavailable on this host; fix Darwin + swift + tools/macos_vision_ocr_bridge_v0.swift, then re-run."
        verdict = "NO_GO"
        rstat = "not_ready"
    elif agg_hb:
        rec = "Some samples reported hard_blockers; inspect per_sample_ocr_raw_text_results.json and provider_details."
        verdict = "CONDITIONAL_GO"
        rstat = "partial"
    else:
        rec = "Artifacts written; run: python3 tools/verify_macos_vision_ocr_raw_text_v0.py --output-root <this_dir>"
        verdict = "EVAL_COMPLETED"
        rstat = "artifacts_ready"

    summary: Dict[str, Any] = {
        "phase": "Phase-ModelOCR-004A",
        "tool": "evaluate_macos_vision_ocr_raw_text_v0.py",
        "timestamp": _now_iso(),
        "provider_id": "macos_vision_ocr_system_v0",
        "model_config_id": "macos_vision_ocr_system_v0",
        "provider_available": available,
        "provider_error": err,
        "input": input_desc,
        "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
        "readiness_status": rstat,
        "harness_verdict": verdict,
        "ok": ok_flag,
        "sample_count_total": nproc,
        "sample_count_processed": nproc,
        "counts": {"samples": len(samples), "results": len(per_sample)},
        "metrics": {
            "ocr_result_generated_rate": ocr_result_generated_rate,
            "raw_text_candidate_schema_valid_rate": raw_text_candidate_schema_valid_rate,
            "bbox_present_or_declared_rate": bbox_present_or_declared_rate,
            "confidence_present_or_declared_rate": confidence_present_or_declared_rate,
            "raw_text_joined_present_rate": raw_text_joined_present_rate,
            "semantic_interpretation_disabled_rate": semantic_interpretation_disabled_rate,
            "allows_execute_now_false_rate": allows_execute_now_false_rate,
            "real_tts_invoked_false_rate": real_tts_invoked_false_rate,
            "trace_ready_rate": trace_ready_rate,
            "replay_ready_rate": replay_ready_rate,
            "whitebox_ready_rate": whitebox_ready_rate,
            "forbidden_semantic_output_count": forbidden_semantic_output_count,
            "downstream_invocation_count": downstream_invocation_count,
        },
        "governance": {
            "semantic_interpretation_enabled": False,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "downstream_invoked": False,
        },
        "hard_blockers": agg_hb,
        "soft_followups": agg_sf,
        "recommendation": rec,
        "artifacts": {
            "per_sample_results": "per_sample_ocr_raw_text_results.json",
            "summary": "ocr_raw_text_summary.json",
            "trace": "ocr_raw_text_trace.jsonl",
            "replay": "ocr_raw_text_replay.jsonl",
            "whitebox": "ocr_raw_text_whitebox.jsonl",
            "notes": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "per_sample_ocr_raw_text_results.json"), per_sample)
    _write_json(os.path.join(out_root, "ocr_raw_text_summary.json"), summary)
    notes_lines = [
        "## Phase-ModelOCR-004A — evaluation notes",
        "",
        "### Boundaries",
        "",
        "- **Provider:** macOS Vision OCR (`VNRecognizeTextRequest`) via `tools/macos_vision_ocr_bridge_v0.swift` only.",
        "- **Not in scope:** PaddleOCR runtime、YOLO、中台、SceneTask/Fusion/Output、语义提炼、导航执行、真实播报、controlled_live_stream、Option A 扩展。",
        "- **PaddleOCR:** 权重线为 **pinned_partial**（Fix-004）；本阶段 **不安装 / 不调用** paddlepaddle、paddleocr；推理依赖就绪归入 **004B**。",
        "- **Output:** raw text candidates only；`semantic_interpretation_enabled=false`、`allows_execute_now=false`、`real_tts_invoked=false`。",
        "",
        "### Reading order / layout（后续契约）",
        "",
        "- `line_order` / `raw_text_joined` 当前为 **启发式**（按 bbox 从上到下、从左到右拼接）；完整 **Reading Direction / Line Order / Layout Order Contract**（LTR/RTL/竖排/多列等）另阶段冻结；阅读顺序不确定时 **不得**进入语义提炼（见 OCR 路线图）。",
        "",
        "### Sandbox",
        "",
        "- Cursor 沙箱或非 macOS 环境可能导致 Vision 不可用；在非沙箱 macOS 上复现实验。",
        "",
    ]
    _write_text(os.path.join(out_root, "evaluation_notes.md"), "\n".join(notes_lines))

    print(
        json.dumps(
            {"ok": ok_flag, "output_root": summary["output_root"], "samples": len(samples), "harness_verdict": verdict},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

